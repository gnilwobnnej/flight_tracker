import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from database import DB_PATH

st.set_page_config(page_title="October SFO-MCO Tracker", layout="wide")

st.title("July 18th Flight Price Tracker (SFO ➡️ MCO)")
st.subheader("AI-Powered Price Monitoring & Prediction")

# 1. Load Data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    # Added 'dates' to the query if you updated your database.py to save it
    df = pd.read_sql_query("SELECT * FROM price_history ORDER BY timestamp DESC", conn)
    conn.close()
    return df

df = load_data()

if not df.empty:
    # 2. Key Metrics
    current_price = df.iloc[0]['price']
    last_price = df.iloc[1]['price'] if len(df) > 1 else current_price
    price_diff = current_price - last_price
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Best Price", f"${current_price}", f"{price_diff}$", delta_color="inverse")
    col2.metric("October Floor (Min)", f"${df['price'].min()}")
    col3.metric("Data Points Collected", len(df))

    # 3. Price Trend Chart
    st.write("### 📈 Price Trend Over Time")
    fig = px.line(df, x='timestamp', y='price', markers=True, 
                 title="SFO to MCO Price History",
                 labels={'timestamp': 'Check-in Time', 'price': 'Price (USD)'})
    st.plotly_chart(fig, use_container_width=True)

    # 4. Raw Data Table
    st.write("### 📋 Recent Searches")
    st.dataframe(df, use_container_width=True)
    
else:
    st.info("No data found yet. Run your GitHub Action to collect the first price!")

# 5. Sidebar Setup
st.sidebar.header("Tracker Settings")
st.sidebar.write("**Route:** SFO ➡️ MCO")
st.sidebar.write("**Target Month:** July 18th 2026")

if st.sidebar.button("Clear Cache"):
    st.cache_data.clear()
    st.rerun()
