import streamlit as st
import pandas as pd
import os
import plotly.express as px

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
    div[data-testid="stMetricValue"] { color: #0F172A; font-weight: 700; font-size: 28px; }
    h1, h2, h3 { color: #0F172A !important; }

    .section-label {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #94A3B8;
        margin-bottom: 8px;
    }
    .risk-high   { color: #EF4444; font-weight: 700; }
    .risk-medium { color: #F97316; font-weight: 700; }
    .risk-low    { color: #22C55E; font-weight: 700; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_risk():
    path = "data/risk_analysis.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


df = load_risk()

st.title("Risk Analysis")
st.markdown("<p style='color:#64748B; font-size:15px; margin-bottom:24px;'>Deep-dive into market volatility, predicted returns, and risk classification for each tracked asset.</p>", unsafe_allow_html=True)

if df is None or df.empty:
    st.warning("Risk data not available. Run the analysis pipeline first.")
    st.stop()

# =========================================================
# ROW 1 — KPI Summary Cards
# =========================================================
total   = len(df)
high_c  = len(df[df["risk"] == "High"])
med_c   = len(df[df["risk"] == "Medium"])
low_c   = len(df[df["risk"] == "Low"])
avg_ret = df["predicted_return"].mean()

c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.metric("Total Assets",      f"{total}")
with c2: st.metric("High Risk",         f"{high_c}",  delta="Caution", delta_color="inverse")
with c3: st.metric("Medium Risk",       f"{med_c}",   delta="Monitor", delta_color="off")
with c4: st.metric("Low Risk",          f"{low_c}",   delta="Safe",    delta_color="normal")
with c5: st.metric("Avg Return (pred)", f"+{avg_ret:.2f}%")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# =========================================================
# ROW 2 — Filters
# =========================================================
st.markdown("<div class='section-label'>Filters & Sorting</div>", unsafe_allow_html=True)

f1, f2, f3 = st.columns([2, 1, 1])
with f1:
    coins_list = ["All Coins"] + sorted(df["name"].tolist())
    selected_coin = st.selectbox("Select Coin", coins_list)
with f2:
    risk_filter = st.selectbox("Risk Level", ["All", "High", "Medium", "Low"])
with f3:
    sort_by = st.selectbox("Sort By", ["predicted_return (High→Low)", "predicted_return (Low→High)", "name (A→Z)", "change (High→Low)"])

# =========================================================
# Apply Filters
# =========================================================
filtered = df.copy()
if selected_coin != "All Coins":
    filtered = filtered[filtered["name"] == selected_coin]
if risk_filter != "All":
    filtered = filtered[filtered["risk"] == risk_filter]

sort_map = {
    "predicted_return (High→Low)": ("predicted_return", False),
    "predicted_return (Low→High)": ("predicted_return", True),
    "name (A→Z)":                  ("name",             True),
    "change (High→Low)":           ("change",           False),
}
sort_col, sort_asc = sort_map[sort_by]
filtered = filtered.sort_values(sort_col, ascending=sort_asc).reset_index(drop=True)

st.markdown(f"<p style='color:#64748B; font-size:13px; margin-top:6px;'>Showing <b>{len(filtered)}</b> of <b>{total}</b> assets</p>", unsafe_allow_html=True)
st.markdown("---")

# =========================================================
# ROW 3 — Risk Table + Bar Chart
# =========================================================
col_table, col_chart = st.columns([1, 1], gap="large")

with col_table:
    st.markdown("<div class='section-label'>Asset Risk Index</div>", unsafe_allow_html=True)

    # Style the risk column with colour coding
    def risk_color(val):
        if val == "High":
            return "color: #EF4444; font-weight: 700"
        elif val == "Medium":
            return "color: #F97316; font-weight: 700"
        return "color: #22C55E; font-weight: 700"

    # Columns to show
    show_cols = [c for c in ["name", "risk", "predicted_return", "change"] if c in filtered.columns]
    rename_map = {"name":"Coin", "risk":"Risk Level", "predicted_return":"Pred. Return (%)", "change":"24h Change (%)"}

    display_df = filtered[show_cols].rename(columns=rename_map)
    styled     = display_df.style.map(risk_color, subset=["Risk Level"])

    st.dataframe(styled, width="stretch", height=420)

with col_chart:
    st.markdown("<div class='section-label'>Return Distribution by Risk</div>", unsafe_allow_html=True)
    
    if not filtered.empty:
        color_map = {"High": "#EF4444", "Medium": "#F97316", "Low": "#22C55E"}
        top_vis = filtered.head(20)

        fig = px.bar(
            top_vis,
            x="name",
            y="predicted_return",
            color="risk",
            color_discrete_map=color_map,
            labels={"name": "", "predicted_return": "Predicted Return (%)", "risk": "Risk"},
            barmode="group"
        )
        fig.update_layout(
            xaxis_tickangle=-40,
            margin=dict(t=10, b=80, l=0, r=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(title="Risk Level", font_size=12),
            yaxis=dict(gridcolor="#F1F5F9")
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("No data to visualise with current filters.")
