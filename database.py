import sqlite3
from datetime import datetime

DB_NAME = "flights.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS price_history 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, origin TEXT, 
                      destination TEXT, price REAL, timestamp DATETIME)''')

def save_price(origin, destination, price):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO price_history (origin, destination, price, timestamp) VALUES (?, ?, ?, ?)",
                     (origin, destination, price, datetime.now()))

def get_stats(origin, destination):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MIN(price), AVG(price) FROM price_history WHERE origin = ? AND destination = ?", 
                       (origin, destination))
        return cursor.fetchone()