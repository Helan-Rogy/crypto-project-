import requests
import pandas as pd
from datetime import datetime
import os

API_URL = "https://api.coingecko.com/api/v3/coins/markets"

def fetch_crypto_data():
    """Fetches data from CoinGecko API."""
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }
    
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def process_data(data):
    """Converts raw data to a pandas DataFrame and adds a timestamp."""
    df = pd.DataFrame(data)
    df["fetched_at"] = datetime.utcnow()
    return df

def save_to_csv(df):
    """Saves the DataFrame to a CSV file."""
    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    file_path = os.path.join(output_dir, "crypto_market_data.csv")
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    data = fetch_crypto_data()
    if data:
        df = process_data(data)
        save_to_csv(df)
        print("Data collected and saved successfully.")