import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor

# --- Constants ---
DATA_FILE = "data/crypto_market_data.csv"
OUTPUT_FILE = "data/risk_analysis.csv"

def load_data():
    """Load crypto market data from CSV."""
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return pd.DataFrame()
    return pd.read_csv(DATA_FILE)

def calculate_risk(change):
    """Assign a risk level based on the absolute 24h price change percentage."""
    if pd.isnull(change):
        return "Unknown"
    
    abs_change = abs(change)
    if abs_change < 0.5:
        return "Low"
    elif abs_change < 2:
        return "Medium"
    else:
        return "High"

def predict_return(change):
    """Estimate a predicted return based on 80% of current change."""
    if pd.isnull(change):
        return 0
    return change * 0.8

def analyze_coin(row):
    """Worker function for parallel analysis of a single coin."""
    name = row.get("name", "Unknown")
    change = row.get("price_change_percentage_24h", 0)
    risk = calculate_risk(change)
    
    return {
        "name": name,
        "change": change,
        "risk": risk
    }

def parallel_analysis(df):
    """Runs risk analysis in parallel using threads."""
    results = []
    if df.empty:
        return results
        
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(analyze_coin, row) for _, row in df.iterrows()]
        for future in futures:
            results.append(future.result())
            
    return results

def main():
    """Main execution flow: Load, Parallel Analysis, Predict, Report."""
    df = load_data()
    if df.empty:
        return

    # 1. Parallel Analysis
    results = parallel_analysis(df)
    df_results = pd.DataFrame(results)

    # 2. Add Predicted Return
    # We apply the predict_return function to the "change" column
    df_results["predicted_return"] = df_results["change"].apply(predict_return)

    # 3. Round Values
    df_results["change"] = df_results["change"].round(2)
    df_results["predicted_return"] = df_results["predicted_return"].round(2)

    # 4. Sort by change descending
    df_results = df_results.sort_values(by="change", ascending=False)

    # 5. Display table (Top 10)
    print("\nCrypto Risk & Prediction Analysis (Top 10):")
    print(df_results.head(10).to_string(index=False))

    # 6. Save results
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df_results.to_csv(OUTPUT_FILE, index=False)
    print(f"\nAnalysis saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
