import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from model import predict_october_low

st.set_page_config(page_title="October Flight Tracker", page_icon="✈️")

st.title("✈️ SFO to MCO: October 2026 Tracker")
st.markdown("This dashboard tracks the cheapest October flights found by your AI bot.")

# Load Data
def load_data():
    with sqlite3.connect("flights.db") as conn:
        df = pd.read_sql_query("SELECT * FROM price_history ORDER BY timestamp DESC", conn)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

df = load_data()

if not df.empty:
    # --- TOP METRICS ---
    col1, col2, col3 = st.columns(3)
    latest_price = df.iloc[0]['price']
    min_price = df['price'].min()
    ai_pred = predict_october_low(df)

    col1.metric("Current Lowest", f"${latest_price}")
    col2.metric("All-Time Low", f"${min_price}")
    col3.metric("AI Prediction (Tomorrow)", f"${ai_pred}")

    # --- PRICE CHART ---
    st.subheader("Price Trend Over Time")
    fig = px.line(df, x='timestamp', y='price', title="Cheapest October Deals Found Each Day",
                 labels={'price': 'Price (USD)', 'timestamp': 'Date Tracked'})
    fig.update_traces(mode="lines+markers", line_color="#1f77b4")
    st.plotly_chart(fig, use_container_width=True)

    # --- DATA TABLE ---
    if st.checkbox("Show raw history"):
        st.dataframe(df)
else:
    st.info("No data found yet. Run main.py to collect your first flight price!")