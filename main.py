import os
import pandas as pd
import sqlite3
from serpapi import GoogleSearch
from database import init_db, save_price, get_stats
from notifications import send_telegram_alert
from model import predict_october_low

# Configuration
ORIGIN = "SFO"
DESTINATION = "MCO"

API_KEY = os.getenv("SERPAPI_KEY")

def fetch_october_deals():
    # Using the standard Flights engine for a specific date in October
    params = {
        "engine": "google_flights",
        "departure_id": ORIGIN,
        "arrival_id": DESTINATION,
        "outbound_date": "2026-10-15", # Pick a mid-month date
        "return_date": "2026-10-22",   # 1 week trip
        "currency": "USD",
        "hl": "en",
        "gl": "us",
        "api_key": API_KEY
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # We look at the 'best_flights' category
        best_option = results.get("best_flights", [{}])[0]
        
        if best_option:
            price = best_option.get("price")
            
            # Extracting the details of the first leg
            first_leg = best_option.get("flights", [{}])[0]
            airline = first_leg.get("airline")
            dep_time = first_leg.get("departure_airport", {}).get("time")
            arr_time = first_leg.get("arrival_airport", {}).get("time")
            
            # Formatting a nice string for your database/Telegram
            details = f"{airline} | Dep: {dep_time} | Arr: {arr_time}"
            return price, details
            
        return None, None
    except Exception as e:
        print(f"⚠️ API Error: {e}")
        return None, None

if __name__ == "__main__":
    init_db()
    price, dates = fetch_october_deals()
    
    if price:
        # 1. Save to Database
        save_price(ORIGIN, DESTINATION, price, airline, times)
        
        # 2. Get AI Prediction
        with sqlite3.connect("flights.db") as conn:
            df = pd.read_sql_query("SELECT * FROM price_history", conn)
        
        prediction = predict_october_low(df)
        
        # 3. Logic for Alerts
        min_p, _ = get_stats(ORIGIN, DESTINATION)
        
        status_msg = f"Current: ${price} | AI Predicted: ${prediction}"
        print(status_msg)

        # Trigger alert if it's a new low OR 10% below AI prediction
        is_deal = False
        if isinstance(prediction, (int, float)) and price <= (prediction * 0.9):
            is_deal = True
        
        if is_deal or (min_p and price < min_p):
            alert_text = f"🔥 **AI BUY SIGNAL!**\nFound ${price} for {dates}.\nPrediction was ${prediction}."
            send_telegram_alert(price, ORIGIN, DESTINATION, dates + "\n" + alert_text)

        if price:
            init_db() # Ensure table exists
            save_price(ORIGIN, DESTINATION, price)
        
        # DEBUG: Check if it actually saved
        with sqlite3.connect(os.path.join(os.path.dirname(__file__), "flights.db")) as conn:
            count = conn.execute("SELECT COUNT(*) FROM price_history").fetchone()[0]
            print(f"📊 Total rows now in database: {count}") 
    else:
        print("❌ No price data fetched. Check your API key or parameters.")          
