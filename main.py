import pandas as pd
import os
from data_loader import fetch_crypto_data, process_data, save_to_csv
from database import create_connection, create_table, insert_data, insert_report_data, fetch_data
import risk_predictor
import investment_calculator
import report_generator

def main():
    print("🚀 Starting Crypto Intelligence Pipeline...")

    # Step 1: Fetch and Process Raw Data
    print("\n--- Phase 1: Data Collection ---")
    raw_json = fetch_crypto_data()
    if raw_json is None:
        print("❌ Failed to fetch data from API.")
        return

    df_market = process_data(raw_json)
    save_to_csv(df_market)
    print(f"✅ Collected data for {len(df_market)} coins.")

    # Step 2: Risk Analysis
    print("\n--- Phase 2: Risk & Prediction Analysis ---")
    risk_results = risk_predictor.parallel_analysis(df_market)
    df_risk = pd.DataFrame(risk_results)
    df_risk["predicted_return"] = df_risk["change"].apply(risk_predictor.predict_return)
    
    # Save intermediate risk analysis
    os.makedirs("data", exist_ok=True)
    df_risk.to_csv("data/risk_analysis.csv", index=False)
    print("✅ Risk analysis complete.")

    # Step 3: Investment Allocation
    print("\n--- Phase 3: Portfolio Optimization ---")
    df_invest = investment_calculator.calculate_score(df_risk.copy())
    df_invest = investment_calculator.normalize_allocation(df_invest)
    df_invest.to_csv("data/investment_mix.csv", index=False)
    print("✅ Investment mix calculated.")

    # Step 4: Final Report & Integration
    print("\n--- Phase 4: System Integration & Reporting ---")
    final_report = report_generator.merge_data(df_risk, df_invest)
    final_report = report_generator.format_report(final_report)
    report_generator.save_report(final_report)
    
    # Database Integration
    conn = create_connection()
    create_table(conn)
    insert_data(conn, df_market)
    insert_report_data(conn, final_report)
    
    print("\n--- Phase 5: Notifications ---")
    email_html = report_generator.generate_alerts(final_report)
    if email_html:
        report_generator.send_email_alert(email_html)
    
    print("\n✅ Pipeline execution finished successfully!")
    conn.close()

if __name__ == "__main__":
    main()