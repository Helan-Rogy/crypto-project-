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
    .top-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }
    .top-card-rank { font-size: 12px; color: #94A3B8; font-weight: 600; }
    .top-card-name { font-size: 17px; font-weight: 700; color: #0F172A; margin: 4px 0; }
    .top-card-alloc { font-size: 22px; font-weight: 700; color: #0072FF; }
    .top-card-risk-High   { color: #EF4444; font-size: 13px; font-weight: 600; }
    .top-card-risk-Medium { color: #F97316; font-size: 13px; font-weight: 600; }
    .top-card-risk-Low    { color: #22C55E; font-size: 13px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_portfolio():
    inv_path  = "data/investment_mix.csv"
    risk_path = "data/risk_analysis.csv"
    if os.path.exists(inv_path) and os.path.exists(risk_path):
        inv_df  = pd.read_csv(inv_path)
        risk_df = pd.read_csv(risk_path)
        merged  = pd.merge(inv_df, risk_df[["name", "risk", "predicted_return"]], on="name", how="left")
        merged  = merged.sort_values("allocation", ascending=False).reset_index(drop=True)
        return merged
    return None


df = load_portfolio()

st.title("Investment Portfolio")
st.markdown("<p style='color:#64748B; font-size:15px; margin-bottom:24px;'>Strategic allocation breakdown, top assets, and portfolio composition for smart decision-making.</p>", unsafe_allow_html=True)

if df is None or df.empty:
    st.warning("Portfolio data not available. Run the investment analysis pipeline first.")
    st.stop()

# =========================================================
# ROW 1 — KPI Cards
# =========================================================
total_assets    = len(df[df["allocation"] > 0])
top_coin        = df.iloc[0]["name"]
top_alloc       = df.iloc[0]["allocation"]
avg_alloc       = df[df["allocation"] > 0]["allocation"].mean()
total_allocated = df["allocation"].sum()

c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Active Positions",    f"{total_assets}")
with c2: st.metric("Top Holding",         f"{top_coin}",         delta=f"{top_alloc:.2f}% allocated")
with c3: st.metric("Avg Allocation",      f"{avg_alloc:.2f}%")
with c4: st.metric("Total Allocated",     f"{total_allocated:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# =========================================================
# ROW 2 — Top 5 Asset Highlight Cards + Pie Chart
# =========================================================
st.markdown("<div class='section-label'>Top 5 Assets by Allocation</div>", unsafe_allow_html=True)

top5 = df[df["allocation"] > 0].head(5)
card_cols = st.columns(5)
for i, (_, row) in enumerate(top5.iterrows()):
    risk_val = row.get("risk", "—")
    risk_cls = f"top-card-risk-{risk_val}" if risk_val in ["High","Medium","Low"] else "top-card-risk-Low"
    with card_cols[i]:
        st.markdown(f"""
        <div class='top-card'>
            <div class='top-card-rank'>#{i+1} TOP HOLD</div>
            <div class='top-card-name'>{row['name']}</div>
            <div class='top-card-alloc'>{row['allocation']:.2f}%</div>
            <div class='{risk_cls}'>● {risk_val} Risk</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# =========================================================
# ROW 3 — Pie Chart + Full Allocation Table
# =========================================================
col_pie, col_table = st.columns([1, 1], gap="large")

with col_pie:
    st.markdown("<div class='section-label'>Portfolio Composition</div>", unsafe_allow_html=True)

    active = df[df["allocation"] > 0].sort_values("allocation", ascending=False)
    if len(active) > 7:
        top7       = active.head(7).copy()
        others_val = active.iloc[7:]["allocation"].sum()
        others_row = pd.DataFrame({"name": ["Others"], "allocation": [others_val]})
        pie_data   = pd.concat([top7, others_row])
    else:
        pie_data = active

    palette = ["#0072FF","#338BFF","#66A4FF","#4ADE80","#FBBF24","#F97316","#94A3B8","#CBD5E1"]
    fig_pie = px.pie(
        pie_data, values="allocation", names="name", hole=0.60,
        color_discrete_sequence=palette
    )
    fig_pie.update_traces(
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>Allocation: %{value:.2f}%<extra></extra>",
        marker=dict(line=dict(color="#F8FAFC", width=3))
    )
    fig_pie.update_layout(
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5,
                    xanchor="left", x=1.02, font=dict(size=12, color="#475569"),
                    bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=10, b=10, l=0, r=130),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(text="<b>Allocation</b>", x=0.5, y=0.5,
                          font_size=13, font_color="#0F172A", showarrow=False)]
    )
    st.plotly_chart(fig_pie, width="stretch")

with col_table:
    st.markdown("<div class='section-label'>Full Allocation Table</div>", unsafe_allow_html=True)

    def style_risk(val):
        if val == "High":   return "color: #EF4444; font-weight: 700"
        if val == "Medium": return "color: #F97316; font-weight: 700"
        return "color: #22C55E; font-weight: 700"

    show_cols   = [c for c in ["name","allocation","risk","predicted_return"] if c in df.columns]
    rename_map  = {"name":"Coin","allocation":"Allocation (%)","risk":"Risk","predicted_return":"Pred. Return (%)"}
    display_df  = df[df["allocation"] > 0][show_cols].rename(columns=rename_map).reset_index(drop=True)

    col_risk = "Risk" if "Risk" in display_df.columns else None
    if col_risk:
        styled = display_df.style.map(style_risk, subset=[col_risk])
    else:
        styled = display_df.style

    st.dataframe(styled, width="stretch", height=420)
