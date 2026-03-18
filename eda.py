import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    """Load crypto market data from CSV."""
    df = pd.read_csv("data/crypto_market_data.csv")
    return df

def basic_info(df):
    """Print basic dataset information and the first few rows."""
    print("\nDataset Info:")
    print(df.info())
    print("\nFirst 5 rows:")
    print(df.head())

def check_missing(df):
    """Check for missing values in the dataset."""
    print("\nMissing Values:")
    print(df.isnull().sum())

def statistics(df):
    """Show descriptive statistics for the numerical columns."""
    print("\nStatistics:")
    print(df.describe())

def top_movers(df):
    """Identify and print the top 5 gainers and losers in the last 24h."""
    print("\nTop 5 Gainers:")
    print(df.sort_values(by="price_change_percentage_24h", ascending=False)[["name","price_change_percentage_24h"]].head())

    print("\nTop 5 Losers:")
    print(df.sort_values(by="price_change_percentage_24h")[["name","price_change_percentage_24h"]].head())

def plot_market_cap(df):
    """Visualize the top 10 cryptos by market capitalization."""
    top10 = df.sort_values(by="market_cap", ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.bar(top10["name"], top10["market_cap"], color="skyblue")
    plt.xticks(rotation=45)
    plt.title("Top 10 Cryptos by Market Cap")
    plt.xlabel("Coin")
    plt.ylabel("Market Cap")
    plt.tight_layout()
    plt.show()

def plot_price_distribution(df):
    """Visualize the distribution of current prices."""
    plt.figure(figsize=(10, 6))
    plt.hist(df["current_price"], bins=50, color="green", alpha=0.7)
    plt.title("Price Distribution")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

def plot_price_vs_marketcap(df):
    """Explore the relationship between price and market capitalization using a scatter plot."""
    plt.figure(figsize=(10, 6))
    plt.scatter(df["current_price"], df["market_cap"], alpha=0.5, color="orange")
    plt.xscale('log')
    plt.yscale('log')
    plt.title("Price vs Market Cap (Log Scale)")
    plt.xlabel("Price")
    plt.ylabel("Market Cap")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Load the data
    df = load_data()

    # Step 1: Basic Information
    basic_info(df)

    # Step 2: Check for Missing Values
    check_missing(df)

    # Step 3: Statistical Summary
    statistics(df)

    # Step 4: Analyze top gainers and losers
    top_movers(df)

    # Step 5: Visualizations
    plot_market_cap(df)
    plot_price_distribution(df)
    plot_price_vs_marketcap(df)