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
    params = {
        "engine": "google_travel_explore",
        "departure_id": ORIGIN,
        "arrival_id": DESTINATION,
        "month": "10",
        "currency": "USD",
        "api_key": API_KEY
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        if "results" in results and len(results["results"]) > 0:
            top_deal = results["results"][0]
            return top_deal.get("price"), top_deal.get("extensions", ["Dates unknown"])[0]
        return None, None
    except Exception as e:
        print(f"⚠️ API Error: {e}")
        return None, None

if __name__ == "__main__":
    init_db()
    price, dates = fetch_october_deals()
    
    if price:
        # 1. Save to Database
        save_price(ORIGIN, DESTINATION, price)
        
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