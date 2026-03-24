import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import random

# Auth Guard
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

# --- STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #0F172A !important; }

    .section-label {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #94A3B8;
        margin: 20px 0 10px;
    }

    /* ── Notification Card ── */
    .notif-card {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        background: #FFFFFF;
        border: 1px solid #F1F5F9;
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s;
    }
    .notif-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); }

    /* Avatar circle */
    .notif-avatar {
        width: 46px; height: 46px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
    }
    .avatar-red    { background: #FEF2F2; }
    .avatar-green  { background: #F0FDF4; }
    .avatar-orange { background: #FFF7ED; }

    /* Text block */
    .notif-body { flex: 1; }
    .notif-title {
        font-size: 15px; font-weight: 700; color: #0F172A; margin: 0 0 3px;
    }
    .notif-sub {
        font-size: 13px; color: #64748B; margin: 0;
    }
    .notif-time {
        font-size: 12px; color: #CBD5E1; white-space: nowrap; padding-top: 4px;
    }

    /* Badges */
    .badge {
        display: inline-block;
        border-radius: 20px;
        padding: 3px 10px;
        font-size: 12px;
        font-weight: 700;
        margin-left: 6px;
    }
    .badge-red    { background: #FEE2E2; color: #DC2626; }
    .badge-green  { background: #DCFCE7; color: #16A34A; }
    .badge-orange { background: #FFEDD5; color: #EA580C; }

    /* Summary row */
    .summary-row {
        background: #F8FAFC; border-radius: 12px;
        padding: 14px 20px; margin-bottom: 20px;
        display: flex; gap: 32px;
    }
    .sum-item { text-align: center; }
    .sum-val  { font-size: 28px; font-weight: 700; color: #0F172A; }
    .sum-lbl  { font-size: 12px; color: #94A3B8; font-weight: 600; }

    /* Divider label */
    .divider-lbl {
        font-size: 13px; font-weight: 700; color: #94A3B8;
        text-align: center; margin: 8px 0 16px;
        display: flex; align-items: center; gap: 10px;
    }
    .divider-lbl::before, .divider-lbl::after {
        content: ""; flex: 1; height: 1px; background: #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    risk_path = "data/risk_analysis.csv"
    if os.path.exists(risk_path):
        return pd.read_csv(risk_path)
    return None


df = load_data()


# Helper: fake "time ago" for realism
def time_ago(minutes_back):
    if minutes_back < 60:
        return f"{minutes_back}m ago"
    return f"{minutes_back // 60}h ago"


# ── Header ──────────────────────────────────────────────
col_hdr, col_refresh = st.columns([5, 1])
with col_hdr:
    st.markdown("<h1 style='margin-bottom:4px;'>Alerts</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-size:15px; margin-bottom:16px;'>Real-time market signals, high-risk warnings, and high-return opportunities.</p>", unsafe_allow_html=True)
with col_refresh:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↻ Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

if df is None or df.empty:
    st.warning("Alert data not available. Run the analysis pipeline first.")
    st.stop()

# ── Split data ───────────────────────────────────────────
high_risk    = df[df["risk"] == "High"].sort_values("change",            key=abs, ascending=False).head(7)
high_return  = df.sort_values("predicted_return", ascending=False).head(7)
total_alerts = len(high_risk) + len(high_return)

# ── Summary Strip ─────────────────────────────────────────
st.markdown(f"""
<div class='summary-row'>
    <div class='sum-item'><div class='sum-val'>{total_alerts}</div><div class='sum-lbl'>TOTAL ALERTS</div></div>
    <div class='sum-item'><div class='sum-val' style='color:#EF4444'>{len(high_risk)}</div><div class='sum-lbl'>HIGH RISK</div></div>
    <div class='sum-item'><div class='sum-val' style='color:#22C55E'>{len(high_return)}</div><div class='sum-lbl'>OPPORTUNITIES</div></div>
    <div class='sum-item'><div class='sum-val' style='color:#0072FF'>{datetime.now().strftime('%H:%M')}</div><div class='sum-lbl'>LAST CHECKED</div></div>
</div>
""", unsafe_allow_html=True)

# ── Feed Layout ───────────────────────────────────────────
feed_col, _ = st.columns([1, 0.001])   # single wide column for feed

with feed_col:
    # ─── HIGH RISK SECTION ───────────────────────────────
    st.markdown("<div class='divider-lbl'>🚨 High Risk Warnings</div>", unsafe_allow_html=True)

    random.seed(42)
    for i, (_, row) in enumerate(high_risk.iterrows()):
        change  = row.get("change", 0)
        minutes = random.randint(2, 55)
        direction = "dropped" if change < 0 else "surged"
        sign      = "▼" if change < 0 else "▲"
        clr       = "#EF4444" if change < 0 else "#F97316"

        st.markdown(f"""
        <div class='notif-card'>
            <div class='notif-avatar avatar-red'>⚠️</div>
            <div class='notif-body'>
                <p class='notif-title'>
                    {row['name']}
                    <span class='badge badge-red'>HIGH RISK</span>
                </p>
                <p class='notif-sub'>
                    Price {direction} <b style='color:{clr}'>{sign} {abs(change):.2f}%</b> in 24h · 
                    Predicted return: <b>{row.get('predicted_return', 0):.2f}%</b>
                </p>
            </div>
            <div class='notif-time'>{time_ago(minutes)}</div>
        </div>
        """, unsafe_allow_html=True)

    # ─── HIGH RETURN SECTION ─────────────────────────────
    st.markdown("<div class='divider-lbl'>📈 High Return Opportunities</div>", unsafe_allow_html=True)

    random.seed(99)
    for i, (_, row) in enumerate(high_return.iterrows()):
        ret     = row.get("predicted_return", 0)
        risk    = row.get("risk", "Medium")
        minutes = random.randint(3, 58)
        badge_cls = "badge-red" if risk == "High" else ("badge-orange" if risk == "Medium" else "badge-green")

        st.markdown(f"""
        <div class='notif-card'>
            <div class='notif-avatar avatar-green'>📈</div>
            <div class='notif-body'>
                <p class='notif-title'>
                    {row['name']}
                    <span class='badge {badge_cls}'>{risk} Risk</span>
                </p>
                <p class='notif-sub'>
                    Strong opportunity detected · Predicted return: 
                    <b style='color:#16A34A'>+{ret:.2f}%</b>
                </p>
            </div>
            <div class='notif-time'>{time_ago(minutes)}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#CBD5E1; font-size:13px; margin-top:20px;'>All alerts are generated from the latest CoinGecko market analysis.</p>", unsafe_allow_html=True)
