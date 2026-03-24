import streamlit as st
import pandas as pd
import os
import time
import sys
import plotly.express as px

# Ensure report_generator is accessible
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import report_generator

# --- Page Config ---
st.set_page_config(page_title="Crypto Investment Manager", layout="wide", initial_sidebar_state="expanded")

# Initialize Session State Variables
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "splash_done" not in st.session_state:
    st.session_state["splash_done"] = False

# --- LIGHT THEME STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Clean Metric Cards */
    div[data-testid="stMetric"] { 
        background: #FFFFFF; 
        border: 1px solid #E2E8F0; 
        border-radius: 12px; 
        padding: 20px 24px; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    div[data-testid="stMetricValue"] { color: #0F172A; font-weight: 700; font-size: 28px; }
    div[data-testid="stMetricDelta"] { font-size: 14px; font-weight: 500; }
    h1, h2, h3 { color: #0F172A !important; }
    
    /* Specific Login styling */
    .login-container { max-width: 400px; margin: 0 auto; padding-top: 50px; }
    .splash-container { text-align: center; margin-top: 15vh; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. SPLASH SCREEN FLOW
# ==========================================
if not st.session_state["splash_done"]:
    st.markdown("<div class='splash-container'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 48px; color: #0072FF;'>Crypto Investment Manager</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 20px; color: #64748B;'>Smart Crypto Insights & Portfolio Optimization</p>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    with st.spinner("Initializing System Modules..."):
        time.sleep(2) # Simulate loading for UX
        st.session_state["splash_done"] = True
        st.rerun()

import re

def validate_password(password):
    if len(password) < 8:
        return False, "Must be at least 8 characters."
    if not re.search(r"[A-Z]", password):
        return False, "Must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Must contain at least one special character."
    return True, "Valid"

# ==========================================
# 2. AUTHENTICATION FLOW
# ==========================================
if "auth_mode" not in st.session_state:
    st.session_state["auth_mode"] = "Login"

if not st.session_state["logged_in"]:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    
    # CSS for cleaner, centered form
    st.markdown("""
    <style>
        .login-box {
            background-color: #FFFFFF;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; margin-bottom: 20px;'>{st.session_state['auth_mode']}</h2>", unsafe_allow_html=True)
    
    if st.session_state["auth_mode"] == "Login":
        email_in = st.text_input("Email Address", key="login_email")
        pass_in = st.text_input("Password", type="password", key="login_pass")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign In", type="primary", width="stretch"):
            if email_in and pass_in:
                with st.spinner("Authenticating..."):
                    time.sleep(1)
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = email_in
                    report_generator.send_login_alert(email_in)
                    st.success("Login Successful!")
                    time.sleep(0.5)
                    st.rerun()
            else:
                st.error("Please enter both email and password.")
                
        st.markdown("<p style='text-align:center; font-size:14px; margin-top:15px;'><a style='color:#0072FF; cursor:pointer;'>Forgot Password?</a></p>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<p style='text-align:center; font-size:14px;'>Don't have an account?</p>", unsafe_allow_html=True)
        if st.button("Create Account", width="stretch"):
            st.session_state["auth_mode"] = "Sign Up"
            st.rerun()
            
    else:
        # Sign Up
        st.markdown("<h4 style='text-align: center; color: #64748B; margin-top: -10px; margin-bottom: 20px;'>Create your secure portfolio</h4>", unsafe_allow_html=True)
        
        c_left, c_right = st.columns(2)
        with c_left:
            signup_fname = st.text_input("First Name")
        with c_right:
            signup_lname = st.text_input("Last Name")
            
        signup_email = st.text_input("Email Address")
        
        c_geo1, c_geo2 = st.columns(2)
        with c_geo1:
            signup_country = st.selectbox("Country of Residence", ["United States", "United Kingdom", "Canada", "Australia", "India", "Germany", "Other"])
        with c_geo2:
            signup_currency = st.selectbox("Base Default Currency", ["USD ($)", "EUR (€)", "GBP (£)", "INR (₹)"])
            
        signup_pass = st.text_input("Create Password", type="password")
        signup_confirm = st.text_input("Confirm Password", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        agree_tos = st.checkbox("I agree to the Terms of Service & Privacy Policy")
        agree_2fa = st.checkbox("Enable 2-Factor Authentication (Recommended)", value=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Complete Sign Up", type="primary", width="stretch"):
            if not signup_fname or not signup_email or not signup_pass or not signup_confirm:
                st.error("Please fill in all required fields.")
            elif signup_pass != signup_confirm:
                st.error("Passwords do not match.")
            elif not agree_tos:
                st.error("You must agree to the Terms of Service to create an account.")
            else:
                is_valid, msg = validate_password(signup_pass)
                if not is_valid:
                    st.error(f"Weak Password: {msg}")
                    st.info("Password Requirements:\n- At least 8 chars\n- Uppercase & Lowercase letter\n- Minimum 1 number\n- Minimum 1 special character")
                else:
                    st.success(f"Welcome {signup_fname}! Your account has been securely created. Redirecting to login...")
                    time.sleep(1.5)
                    st.session_state["auth_mode"] = "Login"
                    st.rerun()
                    
        st.markdown("---")
        st.markdown("<p style='text-align:center; font-size:14px;'>Already have an account?</p>", unsafe_allow_html=True)
        if st.button("Back to Login", width="stretch"):
            st.session_state["auth_mode"] = "Login"
            st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    
    st.markdown("<style> [data-testid='stSidebarNav'] { display: none; } </style>", unsafe_allow_html=True)
    st.stop()



# ==========================================
# 3. SECURE ROUTING & NAVIGATION
# ==========================================
# Streamlit 1.36+ Native Router - cleanly renames 'App' tab and sets exact page order
pg = st.navigation([
    st.Page("pages/1_Dashboard.py", title="Dashboard", icon=":material/home:"),
    st.Page("pages/2_Risk_Analysis.py", title="Risk Analysis", icon=":material/monitoring:"),
    st.Page("pages/3_Portfolio.py", title="Portfolio", icon=":material/pie_chart:"),
    st.Page("pages/4_Reports.py", title="Reports", icon=":material/description:"),
    st.Page("pages/5_Alerts.py", title="Alerts", icon=":material/notifications:"),
    st.Page("pages/6_Settings.py", title="Settings", icon=":material/settings:"),
    st.Page("pages/7_Logout.py", title="Logout", icon=":material/logout:")
])
pg.run()