import requests
import pandas as pd
from datetime import datetime, timezone
import os

API_URL = "https://api.coingecko.com/api/v3/coins/markets"

def fetch_crypto_data():
    """Fetches data from CoinGecko API with improved error handling."""
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": 1,
        "sparkline": "false"  # Explicitly using string 'false' as per API standards
    }
    
    headers = {
        "User-Agent": "CryptoTrackerApp/1.0"  # Adding User-Agent to be safe
    }
    
    try:
        # Added timeout to prevent hanging
        response = requests.get(API_URL, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as he:
        print(f"HTTP error occurred: {he}")
        if response.status_code == 429:
             print("Rate limit reached. Please wait before retrying.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def process_data(data):
    """Converts raw data to a pandas DataFrame and adds a UTC timestamp."""
    if not isinstance(data, list):
        print("Data is not in the expected format (list of records).")
        return pd.DataFrame()
        
    df = pd.DataFrame(data)
    # Using now(timezone.utc) instead of deprecated utcnow()
    df["fetched_at"] = datetime.now(timezone.utc)
    return df

def save_to_csv(df):
    """Saves the DataFrame to a CSV file."""
    if df.empty:
        print("Empty DataFrame, skipping CSV save.")
        return
        
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)  # Using exist_ok=True is cleaner
        
    file_path = os.path.join(output_dir, "crypto_market_data.csv")
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    data = fetch_crypto_data()
    if data:
        df = process_data(data)
        save_to_csv(df)
        print("Data collected and saved successfully.")
    else:
        print("Data collection failed.")