import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Portfolio Strategy", layout="wide")

# --- Page Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; background-color: #0E1117; color: #FFFFFF; }
    div[data-testid="stMetric"] { background-color: #161B22 !important; border: 1px solid #30363D; border-radius: 12px; padding: 20px !important; }
</style>
""", unsafe_allow_html=True)

# --- Data Engine ---
@st.cache_data
def load_invest_data():
    if os.path.exists("data/investment_mix.csv"):
        return pd.read_csv("data/investment_mix.csv")
    return None

df = load_invest_data()

if df is not None:
    st.title("Investment Portfolio")
    st.markdown("<p style='color: #8B949E;'>Strategic allocation based on reward-to-risk calculations.</p>", unsafe_allow_html=True)

    # Top Asset Highlights
    top3 = df.head(3)
    c1, c2, c3 = st.columns(3)
    c1.metric("Primary Asset", top3.iloc[0]['name'], f"{top3.iloc[0]['allocation']:.2f}%")
    c2.metric("Secondary Asset", top3.iloc[1]['name'], f"{top3.iloc[1]['allocation']:.2f}%")
    c3.metric("Tertiary Asset", top3.iloc[2]['name'], f"{top3.iloc[2]['allocation']:.2f}%")

    st.divider()

    # Visual Layout
    col_chart, col_table = st.columns([1.3, 0.7])

    with col_chart:
        st.subheader("📊 Allocation Distribution")
        # Horizontal Bars are much cleaner for long crypto names
        top15 = df.head(15).sort_values(by="allocation", ascending=True)
        st.bar_chart(top15.set_index("name")["allocation"], color="#00C6FF", horizontal=True)

    with col_table:
        st.subheader("Target Weights")
        st.dataframe(df[["name", "allocation"]].head(20), width="stretch")

else:
    st.error("Portfolio data missing.")
