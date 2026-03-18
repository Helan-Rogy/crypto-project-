from data_loader import fetch_crypto_data, process_data, save_to_csv
from database import create_connection, create_table, insert_data, fetch_data

def main():
    # Step 1: Fetch data
    data = fetch_crypto_data()
    if data is None:
        print("Failed to fetch data.")
        return

    # Step 2: Process data
    df = process_data(data)

    # Step 3: Save CSV
    save_to_csv(df)

    # Step 4: Database interaction
    conn = create_connection()
    create_table(conn)
    insert_data(conn, df)

    # Step 5: Verify by fetching from DB
    print("\nFetching latest records from sqlite3:")
    fetch_data(conn)

    conn.close()

if __name__ == "__main__":
    main()