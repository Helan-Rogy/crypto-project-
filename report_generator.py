import pandas as pd
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Constants ---
RISK_FILE = "data/risk_analysis.csv"
INVEST_FILE = "data/investment_mix.csv"
FINAL_REPORT = "data/final_report.csv"

# --- Email Credentials ---
SENDER_EMAIL = "helanrogyle@gmail.com"
RECEIVER_EMAIL = "nvnnil06@gmail.com"
APP_PASSWORD = "edpmhcvhxxzvqyqs"

def send_email_alert(html_content):
    """Sends a professionally formatted HTML email alert."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🚨 Crypto Portfolio Market Alert [{datetime.now().strftime('%Y-%m-%d')}]"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    # Attach HTML version
    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("📧 Professional HTML Email alert sent successfully!")
    except Exception as e:
        print(f"❌ Error sending professional email: {e}")

def send_login_alert(user_email):
    """Sends a login security alert email to the user's own login email."""
    if not user_email:
        return
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🔐 Login Alert: Crypto Investment Manager"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL   # ✅ Always alert the account owner

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6; margin: 0; padding: 0;">
        <div style="max-width: 600px; margin: 30px auto; border: 1px solid #E2E8F0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">

            <!-- Header -->
            <div style="background: linear-gradient(135deg, #0072FF, #00C6FF); padding: 28px 30px; text-align: center;">
                <h1 style="color: #FFFFFF; margin: 0; font-size: 22px; font-weight: 700;">Crypto Investment Manager</h1>
                <p style="color: rgba(255,255,255,0.85); margin: 6px 0 0; font-size: 14px;">Security Notification</p>
            </div>

            <!-- Body -->
            <div style="padding: 30px;">
                <h2 style="color: #0F172A; font-size: 18px; margin-top: 0;">🔐 New Login Detected</h2>
                <p style="color: #475569;">Hi <b>{user_email}</b>,</p>
                <p style="color: #475569;">A successful login was recorded to your <b>Crypto Investment Manager</b> account.</p>

                <table style="width:100%; background:#F8FAFC; border-radius:8px; padding:16px; margin:20px 0; border-collapse:separate;">
                    <tr>
                        <td style="padding:6px 12px; color:#64748B; font-size:13px; font-weight:600;">ACCOUNT</td>
                        <td style="padding:6px 12px; color:#0F172A; font-size:13px;">{user_email}</td>
                    </tr>
                    <tr>
                        <td style="padding:6px 12px; color:#64748B; font-size:13px; font-weight:600;">DATE & TIME</td>
                        <td style="padding:6px 12px; color:#0F172A; font-size:13px;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
                    </tr>
                    <tr>
                        <td style="padding:6px 12px; color:#64748B; font-size:13px; font-weight:600;">STATUS</td>
                        <td style="padding:6px 12px; color:#16A34A; font-size:13px; font-weight:700;">✅ Successful</td>
                    </tr>
                </table>

                <div style="background:#FFF9C4; border-left:4px solid #FBC02D; border-radius:6px; padding:14px 16px; margin-top:16px;">
                    <p style="margin:0; color:#78350F; font-size:13px;">
                        ⚠️ If this was <b>not you</b>, please secure your account immediately by changing your password.
                    </p>
                </div>
            </div>

            <!-- Footer -->
            <div style="background:#F8FAFC; padding:16px 30px; text-align:center; border-top:1px solid #E2E8F0;">
                <p style="margin:0; color:#94A3B8; font-size:12px;">© 2026 Crypto Intelligence Hub &nbsp;|&nbsp; Automated Security Alert</p>
            </div>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"📧 Login alert sent successfully to {user_email}!")
    except Exception as e:
        print(f"❌ Error sending login alert: {e}")

def load_data():
    """Loads necessary data for the final report."""
    if not os.path.exists(RISK_FILE) or not os.path.exists(INVEST_FILE):
        print("Error: Required files missing.")
        return pd.DataFrame(), pd.DataFrame()
    return pd.read_csv(RISK_FILE), pd.read_csv(INVEST_FILE)

def merge_data(risk_df, invest_df):
    """Merges risk analysis and investment allocation data."""
    if risk_df.empty or invest_df.empty:
        return pd.DataFrame()
    report_df = pd.merge(risk_df, invest_df, on="name", suffixes=('', '_dup'))
    return report_df.loc[:, ~report_df.columns.str.endswith('_dup')]

def format_report(df):
    """Corrects precision and sorts."""
    if df.empty:
        return df
    df["predicted_return"] = df["predicted_return"].round(2)
    df["allocation"] = df["allocation"].round(2)
    return df.sort_values(by="allocation", ascending=False)

def generate_alerts(df):
    """Analyzes data and returns formatted HTML for a professional email."""
    if df.empty:
        return ""

    print("\n⚠ Generating Digital Market Insights...\n")
    
    # Identify highlights for the alert
    # We define "Investment Grade" as assets with positive allocation
    investment_opportunities = df[df["allocation"] > 0].sort_values(by="allocation", ascending=False).head(5)
    
    # Identify high risk assets (top 3 by absolute change)
    high_risk_assets = df[df["risk"] == "High"].sort_values(by="change", key=abs, ascending=False).head(3)

    # Console output for local user
    if not high_risk_assets.empty:
        print(f"🚨 High Risk Detected: {', '.join(high_risk_assets['name'])}")
    if not investment_opportunities.empty:
        print(f"📈 {len(investment_opportunities)} Prime Investment Opportunities Identified!")

    # --- Build Professional HTML Body ---
    date_str = datetime.now().strftime('%B %d, %Y')
    
    html_body = f"""
    <html>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
            <div style="background-color: #1a237e; color: #ffffff; padding: 20px; text-align: center;">
                <h1 style="margin: 0; font-size: 24px;">Crypto Portfolio Intelligence</h1>
                <p style="margin: 5px 0 0; opacity: 0.8;">{date_str} Executive Summary</p>
            </div>
            
            <div style="padding: 20px;">
                <p>Hello,</p>
                <p>Our analysis engine has processed the latest market data. Here are your personalized investment recommendations and risk warnings.</p>
                
                <!-- Section 1: Investment Recommendations -->
                <h3 style="color: #1a237e; border-bottom: 2px solid #1a237e; padding-bottom: 5px;">✅ Recommended Investment Allocation</h3>
                <p style="font-size: 14px; color: #666;">Based on current market volatility and predicted returns, here are the top assets to consider for your portfolio:</p>
                <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                    <thead>
                        <tr style="background-color: #f5f5f5;">
                            <th style="padding: 10px; border: 1px solid #e0e0e0; text-align: left;">Asset</th>
                            <th style="padding: 10px; border: 1px solid #e0e0e0; text-align: center;">Risk Level</th>
                            <th style="padding: 10px; border: 1px solid #e0e0e0; text-align: right;">Allocation (%)</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    for _, row in investment_opportunities.iterrows():
        risk_color = "#fbc02d" if row["risk"] == "Medium" else ("#d32f2f" if row["risk"] == "High" else "#388e3c")
        html_body += f"""
                        <tr>
                            <td style="padding: 10px; border: 1px solid #e0e0e0;"><b>{row['name']}</b></td>
                            <td style="padding: 10px; border: 1px solid #e0e0e0; text-align: center; color: {risk_color};"><b>{row['risk']}</b></td>
                            <td style="padding: 10px; border: 1px solid #e0e0e0; text-align: right;">{row['allocation']:.2f}%</td>
                        </tr>
        """

    html_body += """
                    </tbody>
                </table>

                <!-- Section 2: Risk Analysis -->
                <h3 style="color: #d32f2f; border-bottom: 2px solid #d32f2f; padding-bottom: 5px; margin-top: 30px;">⚠️ High Risk Sensitivity Alert</h3>
                <p style="font-size: 14px; color: #666;">The following assets are currently exhibiting high volatility. Proceed with caution:</p>
                <ul style="padding-left: 20px;">
    """
    
    if not high_risk_assets.empty:
        for _, row in high_risk_assets.iterrows():
            html_body += f"""
                    <li style="margin-bottom: 5px;"><b>{row['name']}</b>: Currently shows a 24h change of <span style="color: #d32f2f;">{row['change']:.2f}%</span>. Risk: <b>{row['risk']}</b></li>
            """
    else:
        html_body += "<li>No critical high-risk assets detected in top movers.</li>"

    html_body += f"""
                </ul>

                <div style="margin-top: 25px; background-color: #e8f5e9; padding: 15px; border-radius: 5px; border-left: 5px solid #43a047;">
                    <h4 style="margin: 0; color: #2e7d32;">💡 Strategist Note</h4>
                    <p style="margin: 5px 0 0; font-size: 14px;">The current market trend favors <b>{df.iloc[0]['name'] if not df.empty else 'diversification'}</b>. Maintaining a balanced allocation across low and medium risk assets is recommended.</p>
                </div>
            </div>
            
            <div style="background-color: #f5f5f5; color: #777; padding: 15px; text-align: center; font-size: 12px;">
                <p style="margin: 0;">This is an automated risk analysis generated by CryptoProject Intelligence.</p>
                <p style="margin: 5px 0 0;">© 2026 Helan Finance Hub | Data source: CoinGecko Analysis Layer.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_body


def display_report(df):
    """Prints the final investment report table to console."""
    if df.empty:
        return
    print("\n📊 Crypto Investment Final Report:\n")
    print(df[["name", "risk", "predicted_return", "allocation"]].head(10).to_string(index=False))

def save_report(df):
    """Saves the final report into data directory."""
    if df.empty:
        return
    df.to_csv(FINAL_REPORT, index=False)
    print(f"\n✅ Report successfully saved at {FINAL_REPORT}")

def main():
    """Main execution flow."""
    risk_df, invest_df = load_data()
    if risk_df.empty or invest_df.empty:
        return

    report_df = merge_data(risk_df, invest_df)
    report_df = format_report(report_df)

    display_report(report_df)
    email_html = generate_alerts(report_df)
    save_report(report_df)
    
    if email_html:
        send_email_alert(email_html)

if __name__ == "__main__":
    main()