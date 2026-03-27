import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

def predict_october_low(df):
    """
    Predicts the cheapest price available for October 
    based on historical 'Explore' trends.
    """
    # Safety check: We need a few days of data to make a guess
    if len(df) < 3:
        # If no data, return a placeholder or the last price
        return df['price'].iloc[0] if not df.empty else 0.0

    # 1. Feature Engineering
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # What day of the week was the search done?
    df['search_day_of_week'] = df['timestamp'].dt.dayofweek
    
    # Lead time: How many days until October 1st?
    july_start = datetime(2026, 7, 17)
    df['days_until_july'] = (july_start - df['timestamp']).dt.days
    
    # 2. Prepare Features (X) and Target (y)
    X = df[['search_day_of_week', 'days_until_july']]
    y = df['price']
    
    # 3. Train the Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # 4. Predict for Tomorrow
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_day = tomorrow.weekday()
    tomorrow_lead = (july_start - tomorrow).days
    
    prediction = model.predict([[tomorrow_day, tomorrow_lead]])[0]
    
    return round(float(prediction), 2)
