import pandas as pd
import numpy as np
import pickle
import os
import logging
from feature_engineering import create_features

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def predict_future(days=7):
    # Load model
    with open('models/energy_model.pkl', 'rb') as f:
        model_data = pickle.load(f)
        
    model = model_data['model']
    features = model_data['features']
    
    # Load historical data to build lag features
    df = pd.read_csv('data/processed/cleaned_energy_dataset.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    last_date = df['Date'].max()
    historical_consumption = df['Total Consumption'].tolist()
    
    predictions = []
    current_date = last_date
    
    for i in range(days):
        current_date += pd.Timedelta(days=1)
        
        # Build features for current_date
        day_of_week = current_date.dayofweek
        day_of_month = current_date.day
        month = current_date.month
        is_weekend = 1 if day_of_week >= 5 else 0
        
        # Lag features
        lag_1 = historical_consumption[-1]
        lag_7 = historical_consumption[-7] if len(historical_consumption) >= 7 else lag_1
        
        rolling_mean_3 = np.mean(historical_consumption[-3:])
        rolling_mean_7 = np.mean(historical_consumption[-7:])
        
        X_input = pd.DataFrame([{
            'DayOfWeek': day_of_week,
            'DayOfMonth': day_of_month,
            'Month': month,
            'IsWeekend': is_weekend,
            'Lag_1': lag_1,
            'Lag_7': lag_7,
            'Rolling_Mean_3': rolling_mean_3,
            'Rolling_Mean_7': rolling_mean_7
        }])
        
        X_input = X_input[features]  # Ensure order matches
        
        pred = model.predict(X_input)[0]
        predictions.append({
            'Date': current_date.strftime('%Y-%m-%d'),
            'Predicted_Consumption': pred,
            'Model_Used': type(model).__name__
        })
        
        # Append prediction to history to use as lag for next iterations
        historical_consumption.append(pred)
        
    forecast_df = pd.DataFrame(predictions)
    
    os.makedirs('outputs', exist_ok=True)
    out_path = 'outputs/energy_forecast.csv'
    forecast_df.to_csv(out_path, index=False)
    logging.info(f"Generated {days}-day forecast and saved to {out_path}")
    print(forecast_df)

if __name__ == '__main__':
    predict_future()
