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
# Use GitHub Secrets / Streamlit Secrets for the API Key
API_KEY = os.getenv("SERPAPI_KEY") 

def fetch_october_deals():
    params = {
        "engine": "google_flights",
        "departure_id": ORIGIN,
        "arrival_id": DESTINATION,
        "outbound_date": "2026-7-18",
        "return_date": "2026-7-25",
        "currency": "USD",
        "hl": "en",
        "gl": "us",
        "api_key": API_KEY
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Check for errors in the API response first
        if "error" in results:
            print(f"⚠️ API Error Message: {results['error']}")
            return None, None, None

        # Look for the 'best_flights' list
        best_flights = results.get("best_flights", [])
        
        if best_flights:
            top_flight = best_flights[0]
            price = top_flight.get("price")
            
            # Extract first leg details (Airline and Times)
            first_leg = top_flight.get("flights", [{}])[0]
            airline = first_leg.get("airline", "Unknown Airline")
            dep_time = first_leg.get("departure_airport", {}).get("time", "N/A")
            arr_time = first_leg.get("arrival_airport", {}).get("time", "N/A")
            
            time_info = f"{dep_time} to {arr_time}"
            
            return price, airline, time_info
            
        return None, None, None
    except Exception as e:
        print(f"⚠️ Script Error: {e}")
        return None, None, None

if __name__ == "__main__":
    init_db()
    
    # Catch exactly 3 values to avoid the "ValueError: not enough values to unpack"
    price, airline, times = fetch_october_deals()
    
    if price is not None:
        # 1. Save to Database (Ensure database.py save_price accepts 5 arguments)
        save_price(ORIGIN, DESTINATION, price, airline, times)
        
        # 2. Get AI Prediction
        db_path = os.path.join(os.path.dirname(__file__), "flights.db")
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query("SELECT * FROM price_history", conn)
        
        prediction = predict_october_low(df)
        
        # 3. Check for alerts
        min_p, _ = get_stats(ORIGIN, DESTINATION)
        
        status_msg = f"Current: ${price} ({airline}) | AI Predicted: ${prediction}"
        print(status_msg)

        # Alert if current price is 10% lower than predicted OR lower than history
        is_deal = False
        if isinstance(prediction, (int, float)) and price <= (prediction * 0.9):
            is_deal = True
        
        if is_deal or (min_p and price < min_p):
            alert_text = f"🔥 **AI BUY SIGNAL!**\n{airline} found for ${price}.\nSchedule: {times}"
            send_telegram_alert(price, ORIGIN, DESTINATION, alert_text)
            
        # Debug row count
        with sqlite3.connect(db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM price_history").fetchone()[0]
            print(f"📊 Total database rows: {count}")
    else:
        print("❌ No flight data captured this run.")
