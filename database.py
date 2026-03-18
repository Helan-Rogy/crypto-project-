import sqlite3
import pandas as pd

def create_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect("crypto.db")
    return conn

def create_table(conn):
    """Creates the crypto table if it doesn't already exist."""
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crypto (
        name TEXT,
        symbol TEXT,
        price REAL,
        market_cap REAL,
        volume REAL,
        fetched_at TEXT
    )
    """)
    conn.commit()
    print("Table created/verified.")

def insert_data(conn, df):
    """Inserts rows from a DataFrame into the crypto table."""
    cursor = conn.cursor()
    for i, row in df.iterrows():
        cursor.execute("""
        INSERT INTO crypto (name, symbol, price, market_cap, volume, fetched_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row["name"],
            row["symbol"],
            row["current_price"],
            row["market_cap"],
            row["total_volume"],
            str(row["fetched_at"])
        ))
    conn.commit()
    print("Data inserted into database.")

def fetch_data(conn):
    """Fetches and displays the first 5 rows from the crypto table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crypto LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        print(row)