import sqlite3
import os
from datetime import datetime

# This ensures the DB is created in the same folder as the script
DB_PATH = os.path.join(os.path.dirname(__file__), "flights.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT,
            destination TEXT,
            price REAL,
            airline TEXT,
            flight_times TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def save_price(origin, destination, price, airline, flight_times):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO price_history (origin, destination, price, airline, flight_times, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (origin, destination, price, airline, flight_times, now))
    
    conn.commit()  # <--- This "pushes" the data to the file
    print(f"✅ Successfully saved ${price} to {DB_PATH}")
    conn.close()

def get_stats(origin, destination):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT MIN(price), AVG(price) FROM price_history 
        WHERE origin = ? AND destination = ?
    ''', (origin, destination))
    row = cursor.fetchone()
    conn.close()
    return row if row else (None, None)
