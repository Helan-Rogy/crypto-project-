import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Risk Analysis", layout="wide")

# --- Page Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; background-color: #0E1117; color: #FFFFFF; }
</style>
""", unsafe_allow_html=True)

# --- Data Engine ---
@st.cache_data
def load_risk_data():
    if os.path.exists("data/risk_analysis.csv"):
        return pd.read_csv("data/risk_analysis.csv")
    return None

df = load_risk_data()

# --- Risk Styling Logic: Updated for 2026 Standards ---
def color_risk_level(val):
    if val == 'High':
        return 'background-color: #3D1D1D; color: #F85149; font-weight: 700;'
    elif val == 'Medium':
        return 'background-color: #3A2E1C; color: #D29922; font-weight: 700;'
    return 'background-color: #1E2F23; color: #3FB950; font-weight: 700;'

if df is not None:
    st.title("Risk Profiling")
    st.markdown("<p style='color: #8B949E;'>Market volatility score based on 24h absolute price change.</p>", unsafe_allow_html=True)
    
    # Quick Interaction
    c_f1, c_f2 = st.columns([1, 1])
    with c_f1:
        s_coin = st.selectbox("Market Asset", options=["Show All"] + list(df["name"].values))
    with c_f2:
        r_filter = st.multiselect("Risk Threshold", options=df["risk"].unique(), default=df["risk"].unique())
        
    f_df = df[df["risk"].isin(r_filter)]
    if s_coin != "Show All":
        f_df = f_df[f_df["name"] == s_coin]
        
    st.markdown("---")
    
    # Styled Table
    st.subheader("Asset Risk Index")
    # ✅ Fixed: Changed .applymap() to .map() for Pandas 2.x compatibility
    # ✅ Fixed: Changed use_container_width=True to width="stretch"
    st.dataframe(f_df.style.map(color_risk_level, subset=['risk']), width="stretch")

else:
    st.error("No risk data available.")
