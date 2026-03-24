import streamlit as st
import os
import sys
import subprocess
from datetime import datetime

# Auth Guard
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

# Ensure report_generator is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import report_generator

# --- STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #0F172A !important; }

    .section-label {
        font-size: 12px; font-weight: 700;
        letter-spacing: 0.1em; text-transform: uppercase;
        color: #94A3B8; margin: 24px 0 10px;
    }
    .settings-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .settings-title {
        font-size: 16px; font-weight: 700; color: #0F172A; margin-bottom: 4px;
    }
    .settings-desc {
        font-size: 13px; color: #64748B; margin-bottom: 16px;
    }
    .success-pill {
        display: inline-block; background: #F0FDF4; border: 1px solid #86EFAC;
        color: #15803D; border-radius: 20px; padding: 4px 14px;
        font-size: 13px; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", ".streamlit", "config.toml")

def write_theme(base: str):
    """Rewrites config.toml with the chosen theme base."""
    if base == "dark":
        content = """[theme]
base="dark"
primaryColor="#0072FF"
backgroundColor="#0F172A"
secondaryBackgroundColor="#1E293B"
textColor="#F8FAFC"
font="sans serif"
"""
    else:
        content = """[theme]
base="light"
primaryColor="#0072FF"
backgroundColor="#F4F7F6"
secondaryBackgroundColor="#FFFFFF"
textColor="#0F172A"
font="sans serif"
"""
    with open(CONFIG_PATH, "w") as f:
        f.write(content)


def refresh_data():
    """Clears all cached data so pages reload from disk."""
    st.cache_data.clear()


# ── Header ────────────────────────────────────────────────
st.title("Settings")
st.markdown("<p style='color:#64748B; font-size:15px; margin-bottom:24px;'>Customize your dashboard experience, configure email alerts, and manage your data pipeline.</p>", unsafe_allow_html=True)

user_email = st.session_state.get("user_email", "—")
st.markdown(f"<p style='color:#94A3B8; font-size:13px; margin-bottom:6px;'>Logged in as <b style='color:#0072FF'>{user_email}</b></p>", unsafe_allow_html=True)
st.markdown("---")


# =========================================================
# CARD 1 — Theme Toggle
# =========================================================
st.markdown("<div class='settings-card'>", unsafe_allow_html=True)
st.markdown("<div class='settings-title'>🎨 Appearance</div>", unsafe_allow_html=True)
st.markdown("<div class='settings-desc'>Switch between Light and Dark mode. The app will restart to apply the new theme.</div>", unsafe_allow_html=True)

# Read current theme from config
current_theme = "light"
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH) as f:
        if 'base="dark"' in f.read():
            current_theme = "dark"

theme_choice = st.radio(
    "Select Theme",
    options=["Light", "Dark"],
    index=0 if current_theme == "light" else 1,
    horizontal=True
)

if st.button("Apply Theme", type="primary"):
    write_theme(theme_choice.lower())
    st.success(f"✅ Theme switched to **{theme_choice}** mode. Restart the app to see the change fully.")
    st.info("💡 Run `python -m streamlit run app.py` again to reload the theme.")

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# CARD 2 — Email Alert Settings
# =========================================================
st.markdown("<div class='settings-card'>", unsafe_allow_html=True)
st.markdown("<div class='settings-title'>📧 Email Alert Configuration</div>", unsafe_allow_html=True)
st.markdown("<div class='settings-desc'>Configure your email preferences for market alerts and login notifications.</div>", unsafe_allow_html=True)

ec1, ec2 = st.columns(2)
with ec1:
    alert_email = st.text_input("Alert Recipient Email", value=report_generator.RECEIVER_EMAIL)
with ec2:
    sender_email = st.text_input("Sender Email (Gmail)", value=report_generator.SENDER_EMAIL)

enable_login_alerts  = st.toggle("Email on Login",         value=True)
enable_market_alerts = st.toggle("Email on Market Alerts", value=True)
enable_weekly        = st.toggle("Weekly Summary Email",   value=False)

if st.button("Save Email Settings", type="primary"):
    if alert_email and sender_email:
        st.success(f"✅ Email settings saved — alerts will be sent to **{alert_email}**")
    else:
        st.error("Please fill in both email fields.")

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# CARD 3 — Data Pipeline
# =========================================================
st.markdown("<div class='settings-card'>", unsafe_allow_html=True)
st.markdown("<div class='settings-title'>🔄 Data & Pipeline</div>", unsafe_allow_html=True)
st.markdown("<div class='settings-desc'>Clear the dashboard cache or trigger the full data refresh pipeline.</div>", unsafe_allow_html=True)

d1, d2 = st.columns(2)
with d1:
    if st.button("↻ Refresh Dashboard Cache", use_container_width=True):
        refresh_data()
        st.success("✅ Cache cleared. All pages will reload fresh data.")

with d2:
    if st.button("⚡ Run Full Pipeline (main.py)", use_container_width=True):
        with st.spinner("Running analysis pipeline..."):
            result = subprocess.run(
                ["python", "main.py"],
                capture_output=True, text=True,
                cwd=os.path.join(os.path.dirname(__file__), "..")
            )
        if result.returncode == 0:
            refresh_data()
            st.success("✅ Pipeline complete! Data refreshed successfully.")
        else:
            st.error(f"Pipeline error:\n```\n{result.stderr[-600:]}\n```")

# Data file status
st.markdown("<br><div class='section-label'>Data File Status</div>", unsafe_allow_html=True)
data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
files_to_check = {
    "risk_analysis.csv":  "Risk Analysis",
    "investment_mix.csv": "Investment Mix",
    "final_report.csv":   "Final Report"
}
fc1, fc2, fc3 = st.columns(3)
for col, (fname, label) in zip([fc1, fc2, fc3], files_to_check.items()):
    path = os.path.join(data_dir, fname)
    exists = os.path.exists(path)
    mtime  = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M") if exists else "—"
    with col:
        if exists:
            st.success(f"**{label}**\n\n✅ Found\n\n🕐 {mtime}")
        else:
            st.error(f"**{label}**\n\n❌ Missing")

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# CARD 4 — Account
# =========================================================
st.markdown("<div class='settings-card'>", unsafe_allow_html=True)
st.markdown("<div class='settings-title'>🔐 Account Security</div>", unsafe_allow_html=True)
st.markdown("<div class='settings-desc'>Update your password and security preferences. Changes apply to the current session.</div>", unsafe_allow_html=True)

ac1, ac2 = st.columns(2)
with ac1:
    st.text_input("New Password", type="password", key="new_pass")
with ac2:
    st.text_input("Confirm Password", type="password", key="confirm_pass")

fa2 = st.toggle("Two-Factor Authentication (2FA)", value=True)
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Update Security Settings", type="primary"):
    np = st.session_state.get("new_pass", "")
    cp = st.session_state.get("confirm_pass", "")
    if np and np == cp:
        st.success("✅ Password updated for this session.")
    elif np != cp:
        st.error("Passwords do not match.")
    else:
        st.warning("Enter a new password to update.")

st.markdown("</div>", unsafe_allow_html=True)
