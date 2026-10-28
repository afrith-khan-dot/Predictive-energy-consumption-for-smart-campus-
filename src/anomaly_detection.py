import pandas as pd
import numpy as np
import os
import logging
from sklearn.ensemble import IsolationForest

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_anomalies(contamination=0.05):
    # Load cleaned data
    df = pd.read_csv('data/processed/cleaned_energy_dataset.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    # We will use Total Consumption for anomaly detection
    # Using Isolation Forest
    X = df[['Total Consumption']].copy()
    
    # Calculate rolling median as a baseline/expected consumption
    df['Expected_Consumption'] = df['Total Consumption'].rolling(window=7, min_periods=1).median()
    
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    df['Anomaly_Flag'] = iso_forest.fit_predict(X)
    
    # IsolationForest outputs -1 for anomalies and 1 for normal
    df['Is_Anomaly'] = df['Anomaly_Flag'].apply(lambda x: 1 if x == -1 else 0)
    
    # Calculate deviation
    df['Deviation'] = df['Total Consumption'] - df['Expected_Consumption']
    
    # Explanation
    def explain_anomaly(row):
        if row['Is_Anomaly'] == 1:
            if row['Deviation'] > 0:
                return "Unusually HIGH consumption compared to recent median."
            else:
                return "Unusually LOW consumption compared to recent median."
        return "Normal"
        
    df['Explanation'] = df.apply(explain_anomaly, axis=1)
    
    # Filter anomalies
    anomalies = df[df['Is_Anomaly'] == 1].copy()
    
    # Select columns for report
    report_cols = ['Date', 'Total Consumption', 'Expected_Consumption', 'Deviation', 'Is_Anomaly', 'Explanation']
    report = anomalies[report_cols].rename(columns={'Total Consumption': 'Actual_Consumption'})
    
    # Save report
    os.makedirs('outputs', exist_ok=True)
    out_path = 'outputs/energy_anomalies.csv'
    report.to_csv(out_path, index=False)
    
    logging.info(f"Detected {len(report)} anomalies. Saved to {out_path}")
    print(report)

if __name__ == '__main__':
    detect_anomalies()
