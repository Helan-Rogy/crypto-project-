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
RECEIVER_EMAIL = "helanrogyhel@gmail.com"
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

    print("\n⚠ Investment Alerts:\n")
    
    # Identify highlights for the alert
    high_risk = df[(df["allocation"] > 1) & (df["risk"] == "High")].head(3)
    high_return = df[df["predicted_return"] > 5].sort_values(by="predicted_return", ascending=False).head(3)

    # Console output for local user
    if not high_risk.empty:
        print(f"🚨 High Risk Detected: {', '.join(high_risk['name'])}")
    if not high_return.empty:
        print(f"📈 High Return Opportunities Detected!")

    # --- Build Professional HTML Body ---
    date_str = datetime.now().strftime('%B %d, %Y')
    
    html_body = f"""
    <html>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
            <div style="background-color: #1a237e; color: #ffffff; padding: 20px; text-align: center;">
                <h1 style="margin: 0; font-size: 24px;">Crypto Insight Report</h1>
                <p style="margin: 5px 0 0; opacity: 0.8;">{date_str}</p>
            </div>
            
            <div style="padding: 20px;">
                <p>Hello,</p>
                <p>Your crypto portfolio analysis is complete. Here are the latest market insights based on current volatility and trends.</p>
                
                <h3 style="color: #1a237e; border-bottom: 2px solid #1a237e; padding-bottom: 5px;">🔥 Top 5 Recommended Assets</h3>
                <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                    <thead>
                        <tr style="background-color: #f5f5f5;">
                            <th style="padding: 10px; border: 1px solid #e0e0e0; text-align: left;">Asset Name</th>
                            <th style="padding: 10px; border: 1px solid #e0e0e0; text-align: center;">Risk</th>
                            <th style="padding: 10px; border: 1px solid #e0e0e0; text-align: right;">Pred. Return</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    for _, row in df.head(5).iterrows():
        risk_color = "#d32f2f" if row["risk"] == "High" else "#388e3c"
        html_body += f"""
                        <tr>
                            <td style="padding: 10px; border: 1px solid #e0e0e0;"><b>{row['name']}</b></td>
                            <td style="padding: 10px; border: 1px solid #e0e0e0; text-align: center; color: {risk_color};"><b>{row['risk']}</b></td>
                            <td style="padding: 10px; border: 1px solid #e0e0e0; text-align: right;">{row['predicted_return']:.2f}%</td>
                        </tr>
        """

    html_body += """
                    </tbody>
                </table>
                
                <div style="margin-top: 25px; background-color: #fff9c4; padding: 15px; border-radius: 5px; border-left: 5px solid #fbc02d;">
                    <h4 style="margin: 0; color: #f57f17;">⚠ Action Recommended</h4>
                    <p style="margin: 5px 0 0; font-size: 14px;">High volatility detected in top movers. Consider rebalancing your portfolio to maintain risk levels.</p>
                </div>
            </div>
            
            <div style="background-color: #f5f5f5; color: #777; padding: 15px; text-align: center; font-size: 12px;">
                <p style="margin: 0;">This is an automated risk analysis generated by CryptoProject.</p>
                <p style="margin: 5px 0 0;">© 2026 Helan Finance Hub | All Assets and Data are based on CoinGecko API.</p>
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