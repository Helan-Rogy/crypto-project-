import streamlit as st
import time

st.set_page_config(page_title="Logout", layout="centered")

# --- LIGHT THEME STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #0F172A !important; }
</style>
""", unsafe_allow_html=True)

if not st.session_state.get("logged_in"):
    st.warning("You are already logged out.")
    st.markdown("<p style='text-align: center;'><a href='/' target='_self'>Return to Login</a></p>", unsafe_allow_html=True)
    st.stop()

st.markdown("<h2 style='text-align: center; color: #0072FF; margin-top: 20vh;'>Logging Out securely...</h2>", unsafe_allow_html=True)

with st.spinner("Clearing session data..."):
    time.sleep(1.5)
    st.session_state["logged_in"] = False
    st.session_state["splash_done"] = False
    st.session_state["user_email"] = None
    st.switch_page("app.py")
