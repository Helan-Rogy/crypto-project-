import sqlite3
import pandas as pd
from datetime import datetime

def create_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect("crypto.db")
    return conn

def create_table(conn):
    """Creates the crypto and report tables if they don't already exist."""
    cursor = conn.cursor()
    # Table for raw market data
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
    # Table for processed analysis reports
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        name TEXT,
        risk TEXT,
        predicted_return REAL,
        allocation REAL,
        change_24h REAL,
        generated_at TEXT
    )
    """)
    conn.commit()
    print("Tables created/verified.")

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
    print("Market data inserted into database.")

def insert_report_data(conn, df):
    """Inserts processed report data into the reports table."""
    cursor = conn.cursor()
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for i, row in df.iterrows():
        cursor.execute("""
        INSERT INTO reports (name, risk, predicted_return, allocation, change_24h, generated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row["name"],
            row["risk"],
            row["predicted_return"],
            row["allocation"],
            row["change"],
            now_str
        ))
    conn.commit()
    print("Report data inserted into database.")

def fetch_data(conn):
    """Fetches and displays the first 5 rows from the crypto table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crypto LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def fetch_latest_report(conn):
    """Fetches the latest reports from the database."""
    return pd.read_sql_query("SELECT * FROM reports ORDER BY generated_at DESC", conn)