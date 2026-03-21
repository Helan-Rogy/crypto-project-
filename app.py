import streamlit as st
import pandas as pd
import os

# --- Page Config ---
st.set_page_config(
    page_title="Crypto Intelligence Hub",
    layout="wide",
)

# --- Global Style: Montserrat + Neutral Professional ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 24px !important;
    }

    div[data-testid="stMetricValue"] > div { color: #00C6FF !important; font-weight: 700 !important; }
    div[data-testid="stMetricLabel"] > div { color: #8B949E !important; font-size: 13px; text-transform: uppercase; }

    [data-testid="stSidebar"] {
        background-color: #0A0D12 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Engine ---
@st.cache_data
def get_dashboard_data():
    try:
        r = pd.read_csv("data/risk_analysis.csv")
        i = pd.read_csv("data/investment_mix.csv")
        return r, i
    except:
        return None, None

risk_df, invest_df = get_dashboard_data()

if risk_df is None:
    st.error("Data missing. Please run collectors first.")
    st.stop()

# --- HEADER SECTION ---
st.title("Intelligence Dashboard")
st.markdown("<p style='color: #8B949E;'>Market risk and allocation strategy summary.</p>", unsafe_allow_html=True)

# --- KPI ROW ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Assets Analyzed", f"{len(risk_df)}")
k2.metric("Average Yield", f"{risk_df['predicted_return'].mean():.2f}%")
k3.metric("Capital Status", "Stable")
k4.metric("Market Sentiment", "Positive")

st.markdown("---")

# --- MAIN CHARTS ---
col_left, col_right = st.columns([1.2, 0.8])

with col_left:
    st.subheader("Top Allocation Targets")
    top10_alloc = invest_df.head(10).sort_values(by="allocation", ascending=True)
    st.bar_chart(top10_alloc.set_index("name")["allocation"], color="#00C6FF", horizontal=True)

with col_right:
    st.subheader("Predicted Returns")
    top10_returns = risk_df.sort_values(by="predicted_return", ascending=False).head(10)
    st.bar_chart(top10_returns.set_index("name")["predicted_return"], color="#0072FF")

st.markdown("---")

# --- DATA SUMMARY ---
st.subheader("Asset Breakdown")
st.dataframe(invest_df[["name", "risk", "predicted_return", "allocation"]].head(15), width="stretch")

st.sidebar.markdown(f"<h1 style='color: #00C6FF; font-family: Montserrat'>CryptoPro</h1>", unsafe_allow_html=True)
st.sidebar.caption("Automated Market Edge")
st.sidebar.divider()
st.sidebar.markdown("Use the navigation menu to explore Risk, Alerts, and Detailed Reports.")