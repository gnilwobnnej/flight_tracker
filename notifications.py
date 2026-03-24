import requests
import os

def send_telegram_alert(price, origin, destination, dates):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if token and chat_id:
        # Professional formatting for your 2026 tracker
        message = (
            f"🚀 **Price Drop Alert!**\n\n"
            f"📍 **Route:** {origin} ➡️ {destination}\n"
            f"💰 **New Low:** `${price}`\n"
            f"📅 **Dates Found:** {dates}\n\n"
            f"Check Google Flights quickly before it changes!"
        )
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id, 
            "text": message, 
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to send Telegram alert: {e}")