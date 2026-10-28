import pandas as pd
import logging
import sys
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import get_db_connection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_existing_dates(engine, table_name, date_column):
    try:
        with engine.connect() as conn:
            query = text(f"SELECT {date_column} FROM {table_name}")
            result = conn.execute(query)
            # Fetch dates as strings (YYYY-MM-DD)
            return set(str(row[0]) for row in result)
    except Exception as e:
        # Table might not exist yet
        return set()

def load_data_to_mysql():
    engine = get_db_connection()
    if not engine:
        logging.error("Database connection failed. Ensure MySQL is running and .env is configured.")
        logging.info("Falling back to offline validation...")
        offline_validation()
        return

    try:
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logging.info("Database connection successful.")
    except Exception as e:
        logging.error(f"Database connection failed: {e}. Ensure MySQL is running and .env is configured.")
        logging.info("Falling back to offline validation...")
        offline_validation()
        return

    try:
        # 1. Load Readings
        df_readings = pd.read_csv('data/processed/cleaned_energy_dataset.csv')
        df_readings['Date'] = pd.to_datetime(df_readings['Date']).dt.date.astype(str)
        rename_map = {
            'Date': 'reading_date',
            'Month': 'month_name',
            'TNEB Campus HTSC-91': 'tneb_campus_htsc_91',
            'TNEB New STP HTSC-178': 'tneb_new_stp_htsc_178',
            'Power Generation by Solar Panels': 'solar_generation',
            'Power Generation by Diesel Engines': 'diesel_generation',
            'Power Generation by Biogas Engines': 'biogas_generation',
            'Staff Quarters': 'staff_quarters',
            'Academic blocks': 'academic_blocks',
            'Hostels': 'hostels',
            'Chiller plant': 'chiller_plant',
            'STP': 'stp',
            'Total Consumption': 'total_consumption'
        }
        df_readings.rename(columns=rename_map, inplace=True)
        cols_to_keep = list(rename_map.values())
        df_readings = df_readings[[c for c in cols_to_keep if c in df_readings.columns]]
        
        existing_readings = get_existing_dates(engine, 'energy_readings', 'reading_date')
        df_readings_new = df_readings[~df_readings['reading_date'].isin(existing_readings)]
        
        if not df_readings_new.empty:
            df_readings_new.to_sql('energy_readings', con=engine, if_exists='append', index=False)
            logging.info(f"energy_readings table populated with {len(df_readings_new)} new rows.")
        else:
            logging.info("No new rows to insert into energy_readings (duplicates prevented).")

        # 2. Load Forecasts
        df_forecasts = pd.read_csv('outputs/energy_forecast.csv')
        df_forecasts.rename(columns={
            'Date': 'forecast_date',
            'Predicted_Consumption': 'predicted_consumption',
            'Model_Used': 'model_used'
        }, inplace=True)
        
        existing_forecasts = get_existing_dates(engine, 'energy_forecasts', 'forecast_date')
        df_forecasts_new = df_forecasts[~df_forecasts['forecast_date'].isin(existing_forecasts)]
        
        if not df_forecasts_new.empty:
            df_forecasts_new.to_sql('energy_forecasts', con=engine, if_exists='append', index=False)
            logging.info(f"energy_forecasts table populated with {len(df_forecasts_new)} new rows.")
        else:
            logging.info("No new rows to insert into energy_forecasts.")

        # 3. Load Anomalies
        df_anomalies = pd.read_csv('outputs/energy_anomalies.csv')
        df_anomalies.rename(columns={
            'Date': 'anomaly_date',
            'Actual_Consumption': 'actual_consumption',
            'Expected_Consumption': 'expected_consumption',
            'Deviation': 'deviation',
            'Is_Anomaly': 'is_anomaly',
            'Explanation': 'explanation'
        }, inplace=True)
        
        existing_anomalies = get_existing_dates(engine, 'energy_anomalies', 'anomaly_date')
        df_anomalies_new = df_anomalies[~df_anomalies['anomaly_date'].isin(existing_anomalies)]
        
        if not df_anomalies_new.empty:
            df_anomalies_new.to_sql('energy_anomalies', con=engine, if_exists='append', index=False)
            logging.info(f"energy_anomalies table populated with {len(df_anomalies_new)} new rows.")
        else:
            logging.info("No new rows to insert into energy_anomalies.")

        # 4. Load Model Metrics
        # As per Phase 3 logs, Linear Regression was chosen.
        df_metrics = pd.DataFrame([{
            'model_name': 'Linear Regression',
            'mae': 4058.60,
            'rmse': 5124.41,
            'r2_score': -0.56
        }])
        df_metrics.to_sql('model_metrics', con=engine, if_exists='append', index=False)
        logging.info("model_metrics table populated.")

        # Validation phase
        with engine.connect() as conn:
            r_count = conn.execute(text("SELECT COUNT(*) FROM energy_readings")).scalar()
            f_count = conn.execute(text("SELECT COUNT(*) FROM energy_forecasts")).scalar()
            a_count = conn.execute(text("SELECT COUNT(*) FROM energy_anomalies")).scalar()
            m_count = conn.execute(text("SELECT COUNT(*) FROM model_metrics")).scalar()
            logging.info(f"Validation successful. Final row counts - Readings: {r_count}, Forecasts: {f_count}, Anomalies: {a_count}, Metrics: {m_count}")

    except Exception as e:
        logging.error(f"Failed to load data to MySQL: {e}")

def offline_validation():
    logging.info("Performing offline validation checking row counts in CSVs...")
    try:
        r_count = len(pd.read_csv('data/processed/cleaned_energy_dataset.csv'))
        f_count = len(pd.read_csv('outputs/energy_forecast.csv'))
        a_count = len(pd.read_csv('outputs/energy_anomalies.csv'))
        logging.info(f"Offline Validation successful. Row counts from files - Readings: {r_count}, Forecasts: {f_count}, Anomalies: {a_count}")
    except Exception as e:
        logging.error(f"Offline validation failed: {e}")

if __name__ == '__main__':
    load_data_to_mysql()
