import pandas as pd
import numpy as np
import logging
import pickle
import os
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from feature_engineering import create_features

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def evaluate_model(name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    logging.info(f"{name} - MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.2f}")
    return {'MAE': mae, 'RMSE': rmse, 'R2': r2}

def train_and_evaluate():
    # Load data
    df = pd.read_csv('data/processed/cleaned_energy_dataset.csv')
    df = create_features(df)
    
    # Target and features
    target = 'Total Consumption'
    features = ['DayOfWeek', 'DayOfMonth', 'Month', 'IsWeekend', 
                'Lag_1', 'Lag_7', 'Rolling_Mean_3', 'Rolling_Mean_7']
    
    X = df[features]
    y = df[target]
    
    # Chronological split (last 14 days as test set)
    split_index = len(df) - 14
    X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
    y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]
    
    logging.info(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples.")
    
    # Naive Baseline (predict using last observed value, i.e., Lag_1)
    # Wait, simple naive forecast is the previous day's consumption (Lag_1)
    naive_pred = X_test['Lag_1']
    logging.info("Evaluating Naive Baseline")
    evaluate_model("Naive Baseline", y_test, naive_pred)
    
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    
    results = {}
    best_model = None
    best_name = ""
    best_score = float('inf') # MAE
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        metrics = evaluate_model(name, y_test, preds)
        results[name] = metrics
        
        if metrics['MAE'] < best_score:
            best_score = metrics['MAE']
            best_model = model
            best_name = name
            
    logging.info(f"Best Model Selected: {best_name} with MAE: {best_score:.2f}")
    
    # Retrain best model on all available data for future predictions
    best_model.fit(X, y)
    
    # Save the model
    os.makedirs('models', exist_ok=True)
    with open('models/energy_model.pkl', 'wb') as f:
        pickle.dump({'model': best_model, 'features': features}, f)
        
    logging.info("Model saved successfully.")

if __name__ == '__main__':
    train_and_evaluate()
