import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Final Reports", layout="wide")

# --- Page Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; background-color: #0E1117; color: #FFFFFF; }
</style>
""", unsafe_allow_html=True)

# --- Data Engine ---
@st.cache_data
def load_report_data():
    if os.path.exists("data/final_report.csv"):
        return pd.read_csv("data/final_report.csv")
    return None

df = load_report_data()

if df is not None:
    st.title("Final Reports")
    st.markdown("<p style='color: #8B949E;'>Consolidated portfolio report including risk profiles and investment allocation.</p>", unsafe_allow_html=True)
    
    # Timestamp logic
    mod_time = os.path.getmtime("data/final_report.csv")
    last_update = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')

    st.markdown(f"**Last System Update:** {last_update}")
    
    # Desktop-class download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Master Report (CSV)",
        data=csv,
        file_name='crypto_final_report.csv',
        mime='text/csv',
    )
    
    st.markdown("---")
    st.subheader("Master Table View")
    st.dataframe(df, width="stretch")

else:
    st.error("Report database not found.")
