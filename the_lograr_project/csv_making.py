import sqlite3
import csv

try:
    # Connect to SQLite database
    conn = sqlite3.connect('server/businesses.db')
    cursor = conn.cursor()

    # Query to select all data from the 'businesses' table
    query = "SELECT * FROM businesses"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Write to CSV file with UTF-8 encoding
    with open('businesses.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)  # Write header
        writer.writerows(rows)         # Write data

    print("Data exported successfully to businesses.csv")

except sqlite3.Error as e:
    print(f"SQLite error: {e}")

finally:
    # Close the connection
    if conn:
        conn.close()
