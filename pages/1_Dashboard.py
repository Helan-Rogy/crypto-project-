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
    div[data-testid="stMetricDelta"]  { font-size: 14px; font-weight: 500; }
    h1, h2, h3 { color: #0F172A !important; }

    .section-label {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #94A3B8;
        margin-bottom: 8px;
    }
    .alert-card {
        background: #FFF7ED;
        border-left: 4px solid #F97316;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .alert-card-red {
        background: #FEF2F2;
        border-left: 4px solid #EF4444;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .alert-name  { font-weight: 700; color: #0F172A; font-size: 15px; }
    .alert-meta  { font-size: 13px; color: #64748B; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    inv_path  = "data/investment_mix.csv"
    risk_path = "data/risk_analysis.csv"
    if os.path.exists(inv_path) and os.path.exists(risk_path):
        return pd.read_csv(inv_path), pd.read_csv(risk_path)
    return None, None


invest_df, risk_df = load_data()

# ---------- Header ----------
user = st.session_state.get("user_email", "Investor")
st.markdown(f"<h1 style='margin-bottom:2px;'>Crypto Intelligence Hub</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#64748B; font-size:15px; margin-bottom:28px;'>Welcome back, <b>{user}</b> · Market overview & portfolio summary</p>", unsafe_allow_html=True)

if invest_df is None or invest_df.empty:
    st.info("No data available. Run the analysis pipeline first.")
    st.stop()

# =========================================================
# ROW 1 – KPI Cards
# =========================================================
total_coins    = len(risk_df)
avg_return     = risk_df["predicted_return"].mean()
high_risk_cnt  = len(risk_df[risk_df["risk"] == "High"])
low_risk_cnt   = len(risk_df[risk_df["risk"] == "Low"])

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Coins Tracked", f"{total_coins}", delta="Live data")
with c2:
    st.metric("Avg Predicted Return", f"+{avg_return:.2f}%", delta="vs. baseline")
with c3:
    st.metric("High Risk Count", f"{high_risk_cnt}", delta="Action Needed", delta_color="inverse")
with c4:
    st.metric("Low Risk Assets", f"{low_risk_cnt}", delta="Safe zone", delta_color="normal")

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# ROW 2 – Charts
# =========================================================
col_pie, col_bar = st.columns([1, 1], gap="large")

with col_pie:
    st.markdown("<div class='section-label'>Portfolio Allocation</div>", unsafe_allow_html=True)
    sorted_inv = invest_df[invest_df["allocation"] > 0].sort_values("allocation", ascending=False)

    # Take top 6 by allocation, group rest as "Others"
    if len(sorted_inv) > 6:
        top6       = sorted_inv.head(6).copy()
        others_val = sorted_inv.iloc[6:]["allocation"].sum()
        others_row = pd.DataFrame({"name": ["Others"], "allocation": [others_val]})
        pie_data   = pd.concat([top6, others_row])
    else:
        pie_data = sorted_inv

    # Cohesive blue-gradient + accent palette
    palette = ["#0072FF", "#338BFF", "#66A4FF", "#99BDFF", "#CCd6FF", "#E2EBFF", "#CBD5E1"]

    fig_pie = px.pie(
        pie_data, values="allocation", names="name", hole=0.62,
        color_discrete_sequence=palette
    )
    fig_pie.update_traces(
        textinfo="none",          # Hide all slice labels — keep it clean
        hovertemplate="<b>%{label}</b><br>Allocation: %{value:.2f}%<extra></extra>",
        marker=dict(line=dict(color="#F8FAFC", width=3))
    )
    fig_pie.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle", y=0.5,
            xanchor="left", x=1.02,
            font=dict(size=12, color="#475569"),
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(t=10, b=10, l=0, r=120),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(
            text="<b>Portfolio</b>",
            x=0.5, y=0.5,
            font_size=14,
            font_color="#0F172A",
            showarrow=False
        )]
    )
    st.plotly_chart(fig_pie, width="stretch")

with col_bar:
    st.markdown("<div class='section-label'>Top Predicted Returns</div>", unsafe_allow_html=True)
    top10 = risk_df.sort_values("predicted_return", ascending=False).head(10)
    fig_bar = px.bar(
        top10, x="predicted_return", y="name", orientation="h",
        color="predicted_return", color_continuous_scale=["#00C6FF","#0072FF"]
    )
    fig_bar.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Predicted Return (%)", yaxis_title="",
        margin=dict(t=10, b=0, l=0, r=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False
    )
    fig_bar.update_traces(marker_line_width=0)
    st.plotly_chart(fig_bar, width="stretch")

# =========================================================
# ROW 3 – Alerts Preview (Top 5 High Risk)
# =========================================================
st.markdown("---")
st.markdown("<div class='section-label'>High Risk Alerts Preview</div>", unsafe_allow_html=True)

high_risk_df = risk_df[risk_df["risk"] == "High"].sort_values("change", key=abs, ascending=False).head(5)

if high_risk_df.empty:
    st.success("No high-risk assets detected. Portfolio looks stable.")
else:
    alert_cols = st.columns(min(len(high_risk_df), 5))
    for i, (_, row) in enumerate(high_risk_df.iterrows()):
        change = row.get("change", 0)
        color  = "#EF4444" if change < 0 else "#F97316"
        sign   = "▼" if change < 0 else "▲"
        with alert_cols[i]:
            st.markdown(f"""
            <div class='alert-card-red'>
                <div class='alert-name'>{row['name']}</div>
                <div class='alert-meta'>24h: <b style='color:{color}'>{sign} {abs(change):.2f}%</b></div>
                <div class='alert-meta'>Risk: <b>High</b></div>
            </div>
            """, unsafe_allow_html=True)
