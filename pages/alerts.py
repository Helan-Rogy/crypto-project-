import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Market Alerts", layout="wide")

# --- Consistent Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; background-color: #0E1117; color: #FFFFFF; }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_risk_data():
    if os.path.exists("data/risk_analysis.csv"):
        return pd.read_csv("data/risk_analysis.csv")
    return None

df = load_risk_data()

if df is not None:
    st.title("Market Alerts")
    st.markdown("<p style='color: #8B949E;'>Automated notifications based on market risk thresholds and growth targets.</p>", unsafe_allow_html=True)

    # Filter critical data
    high_risk = df[df["risk"] == "High"]
    high_return = df[df["predicted_return"] > 5]

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Capital Risk Alerts")
        # Show only top 5 for clarity as requested
        for i, (_, row) in enumerate(high_risk.head(5).iterrows()):
            with st.container():
                st.markdown(f"""
                <div style="background-color: #3D1D1D; color: #F85149; border-left: 5px solid #F85149; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                    <h4 style="margin: 0;">{row['name']}</h4>
                    <p style="margin: 5px 0 0;">Potential for massive 24h volatility. Handle with caution.</p>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.subheader("High Return Opportunities")
        for i, (_, row) in enumerate(high_return.head(5).iterrows()):
            with st.container():
                st.markdown(f"""
                <div style="background-color: #1E2F23; color: #3FB950; border-left: 5px solid #3FB950; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                    <h4 style="margin: 0;">{row['name']}</h4>
                    <p style="margin: 5px 0 0;">Opportunity identified with projected return of <b>{row['predicted_return']:.2f}%</b>.</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Alerts are triggered based on CoinGecko market values.")

else:
    st.error("Alerts rely on risk data. Please generate your risk levels first.")
