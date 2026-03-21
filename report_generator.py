import pandas as pd
import os

# --- Constants ---
RISK_FILE = "data/risk_analysis.csv"
INVEST_FILE = "data/investment_mix.csv"
FINAL_REPORT = "data/final_report.csv"

def load_data():
    """Loads necessary data for the final report."""
    if not os.path.exists(RISK_FILE) or not os.path.exists(INVEST_FILE):
        print(f"Error: Required files missing. Ensure {RISK_FILE} and {INVEST_FILE} are generated.")
        return pd.DataFrame(), pd.DataFrame()
    
    risk_df = pd.read_csv(RISK_FILE)
    invest_df = pd.read_csv(INVEST_FILE)

    return risk_df, invest_df

def merge_data(risk_df, invest_df):
    """Merges risk analysis and investment allocation data on common coin name."""
    if risk_df.empty or invest_df.empty:
        return pd.DataFrame()
    
    # Merge based on "name"
    report_df = pd.merge(risk_df, invest_df, on="name", suffixes=('', '_dup'))
    
    # Drop any duplicate columns created by merging (if any)
    report_df = report_df.loc[:, ~report_df.columns.str.endswith('_dup')]
    
    return report_df

def format_report(df):
    """Corrects precision and sorts for the final report."""
    if df.empty:
        return df
        
    df["predicted_return"] = df["predicted_return"].round(2)
    df["allocation"] = df["allocation"].round(2)
    
    # Sort by the best investment opportunities
    df = df.sort_values(by="allocation", ascending=False)
    
    
    return df

def display_report(df):
    """Prints the final investment report to output."""
    if df.empty:
        print("Report is empty.")
        return
        
    print("\n📊 Crypto Investment Final Report:\n")
    print(df[["name", "risk", "predicted_return", "allocation"]]
          .head(10)
          .to_string(index=False))

def save_report(df):
    """Saves the final report into data directory."""
    if df.empty:
        return
    df.to_csv(FINAL_REPORT, index=False)
    print(f"\n✅ Report successfully saved at {FINAL_REPORT}")

def main():
    """Main execution flow for generating the final investment report."""
    risk_df, invest_df = load_data()

    if risk_df.empty or invest_df.empty:
        return

    report_df = merge_data(risk_df, invest_df)
    report_df = format_report(report_df)

    display_report(report_df)
    save_report(report_df)

if __name__ == "__main__":
    main()