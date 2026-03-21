import pandas as pd
import os

# --- Constants ---
ANALYSIS_FILE = "data/risk_analysis.csv"

def load_data():
    """Load the previously generated risk analysis data."""
    if not os.path.exists(ANALYSIS_FILE):
        print(f"Error: {ANALYSIS_FILE} not found. Run 'risk_predictor.py' first.")
        return pd.DataFrame()
    return pd.read_csv(ANALYSIS_FILE)

def risk_to_number(risk):
    """Convert categorical risk level to a numerical factor."""
    if risk == "Low":
        return 1
    elif risk == "Medium":
        return 2
    elif risk == "High":
        return 3
    else:
        return 2 # Default to Medium if unknown

def calculate_score(df):
    """Calculate an investment score based on return vs. risk."""
    if df.empty:
        return df
        
    df["risk_num"] = df["risk"].apply(risk_to_number)

    # Score calculation: Higher predicted return / lower risk factor = Better Score
    # We use a simple reward-to-risk ratio.
    df["score"] = df["predicted_return"] / df["risk_num"]
    
    # Fill any NaNs or infinities that might result from division
    df["score"] = df["score"].fillna(0)
    
    # We only care about positive return opportunities for allocation
    df["score"] = df["score"].clip(lower=0) 
    
    return df

def normalize_allocation(df):
    """Determine percentage investment allocation based on scores."""
    if df.empty or df["score"].sum() == 0:
        df["allocation"] = 0
        return df
        
    total_score = df["score"].sum()
    df["allocation"] = (df["score"] / total_score) * 100
    return df

def show_portfolio(df):
    """Display the top investment recommendations."""
    if df.empty:
        return
        
    # Sort by allocation (best opportunities first)
    df = df.sort_values(by="allocation", ascending=False)
    
    df["allocation"] = df["allocation"].round(2)
    df["predicted_return"] = df["predicted_return"].round(2)

    result = df[["name", "risk", "predicted_return", "allocation"]]

    print("\nInvestment Portfolio Recommendation (Top 10):")
    print(result.head(10).to_string(index=False))

def main():
    """Main execution flow for portfolio calculation."""
    df = load_data()
    if df.empty:
        return

    df = calculate_score(df)
    df = normalize_allocation(df)
    show_portfolio(df)

if __name__ == "__main__":
    main()