import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Auth Guard
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

# --- STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricValue"] { color: #0F172A; font-weight: 700; font-size: 26px; }
    h1, h2, h3 { color: #0F172A !important; }

    .section-label {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #94A3B8;
        margin-bottom: 8px;
    }
    .info-banner {
        background: #EFF6FF;
        border-left: 4px solid #0072FF;
        border-radius: 8px;
        padding: 14px 18px;
        font-size: 14px;
        color: #1E3A5F;
        margin-bottom: 20px;
    }
    .updated-badge {
        display: inline-block;
        background: #F0FDF4;
        border: 1px solid #86EFAC;
        color: #15803D;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

REPORT_FILE = "data/final_report.csv"
RISK_FILE   = "data/risk_analysis.csv"
INV_FILE    = "data/investment_mix.csv"


import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    from database import create_connection, fetch_latest_report
except ImportError:
    pass

@st.cache_data
def load_report():
    """Load final report if available, otherwise build it on-the-fly from source files."""
    df, last_updated, src = None, None, None
    
    # 1. Try to load from database first (for scalability)
    try:
        conn = create_connection()
        db_df = fetch_latest_report(conn)
        conn.close()
        if not db_df.empty:
            df = db_df
            src = "SQLite Database (reports table)"
            # Use most recent entry date
            last_updated = df.iloc[0]["generated_at"]
            # Rename database columns to match CSV used in rest of app context if needed
            if "change_24h" in df.columns:
                df = df.rename(columns={"change_24h": "change"})
            return df, last_updated, src
    except Exception as e:
        print(f"DB Load error: {e}")

    # 2. Fallback to CSV files
    if os.path.exists(REPORT_FILE):
        df = pd.read_csv(REPORT_FILE)
        src = REPORT_FILE
    elif os.path.exists(RISK_FILE) and os.path.exists(INV_FILE):
        risk_df = pd.read_csv(RISK_FILE)
        inv_df  = pd.read_csv(INV_FILE)
        df = pd.merge(risk_df, inv_df, on="name", suffixes=("", "_dup"))
        df = df.loc[:, ~df.columns.str.endswith("_dup")]
        df = df.sort_values("allocation", ascending=False).reset_index(drop=True)
        src = "Generated from risk & investment data"
    else:
        return None, None, None

    mtime = os.path.getmtime(REPORT_FILE) if os.path.exists(REPORT_FILE) else os.path.getmtime(RISK_FILE)
    last_updated = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    return df, last_updated, src


df, last_updated, source = load_report()

# ---------- Header ----------
st.title("Reports & Data Export")
st.markdown("<p style='color:#64748B; font-size:15px; margin-bottom:20px;'>View the final consolidated report, inspect asset-level data, and export a clean CSV for offline analysis.</p>", unsafe_allow_html=True)

if df is None:
    st.warning("Report data not found. Please run the full analysis pipeline first (`main.py`).")
    st.stop()

# =========================================================
# Last Updated Banner
# =========================================================
st.markdown(f"<div class='updated-badge'>✅ Last Updated: {last_updated}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='info-banner'>📂 Data Source: <b>{source}</b> &nbsp;|&nbsp; Total records: <b>{len(df)}</b></div>", unsafe_allow_html=True)

# =========================================================
# ROW 1 — KPI Cards
# =========================================================
cols_present = df.columns.tolist()
total_records = len(df)
high_risk     = len(df[df["risk"] == "High"]) if "risk" in cols_present else "—"
avg_return    = round(df["predicted_return"].mean(), 2) if "predicted_return" in cols_present else "—"
top_asset     = df.iloc[0]["name"] if "name" in cols_present else "—"

c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Total Records",      f"{total_records}")
with c2: st.metric("Avg Predicted Return", f"+{avg_return}%")
with c3: st.metric("High Risk Assets",   f"{high_risk}", delta="Review", delta_color="inverse")
with c4: st.metric("Top Asset",          f"{top_asset}")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# =========================================================
# ROW 2 — Search / Filter Bar + Download
# =========================================================
st.markdown("<div class='section-label'>Filter & Export</div>", unsafe_allow_html=True)
f1, f2, f3 = st.columns([2, 1, 1])

with f1:
    search = st.text_input("Search Coin", placeholder="Type coin name to filter...")
with f2:
    risk_filter = st.selectbox("Risk Level", ["All", "High", "Medium", "Low"]) if "risk" in cols_present else st.selectbox("Risk Level", ["All"])
with f3:
    st.markdown("<br>", unsafe_allow_html=True)
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Download Full CSV",
        data=csv_bytes,
        file_name=f"crypto_report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# Apply filters
filtered = df.copy()
if search:
    filtered = filtered[filtered["name"].str.contains(search, case=False, na=False)]
if risk_filter != "All" and "risk" in cols_present:
    filtered = filtered[filtered["risk"] == risk_filter]

st.markdown(f"<p style='color:#64748B; font-size:13px; margin-top:4px;'>Showing <b>{len(filtered)}</b> of <b>{total_records}</b> records</p>", unsafe_allow_html=True)
st.markdown("---")

# =========================================================
# ROW 3 — Styled Full Report Table
# =========================================================
st.markdown("<div class='section-label'>Final Report Data</div>", unsafe_allow_html=True)

def style_risk(val):
    if val == "High":   return "color: #EF4444; font-weight: 700"
    if val == "Medium": return "color: #F97316; font-weight: 700"
    return "color: #22C55E; font-weight: 700"

# Round numeric columns
for col in ["predicted_return", "allocation", "change"]:
    if col in filtered.columns:
        filtered[col] = filtered[col].round(2)

styled = filtered.style
if "risk" in filtered.columns:
    styled = styled.map(style_risk, subset=["risk"])

# Rename headers for display
rename_map = {
    "name": "Coin", "risk": "Risk Level", "predicted_return": "Pred. Return (%)",
    "allocation": "Allocation (%)", "change": "24h Change (%)"
}
display_df = filtered.rename(columns=rename_map)
styled_display = display_df.style
if "Risk Level" in display_df.columns:
    styled_display = styled_display.map(style_risk, subset=["Risk Level"])

st.dataframe(styled_display, width="stretch", height=480)
