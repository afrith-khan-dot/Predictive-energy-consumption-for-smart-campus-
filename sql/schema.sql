CREATE DATABASE IF NOT EXISTS smart_campus_energy;
USE smart_campus_energy;

CREATE TABLE IF NOT EXISTS energy_readings (
    reading_id INT AUTO_INCREMENT PRIMARY KEY,
    reading_date DATE UNIQUE NOT NULL,
    month_name VARCHAR(20),
    tneb_campus_htsc_91 FLOAT,
    tneb_new_stp_htsc_178 FLOAT,
    solar_generation FLOAT,
    diesel_generation FLOAT,
    biogas_generation FLOAT,
    staff_quarters FLOAT,
    academic_blocks FLOAT,
    hostels FLOAT,
    chiller_plant FLOAT,
    stp FLOAT,
    total_consumption FLOAT
);

CREATE TABLE IF NOT EXISTS energy_forecasts (
    forecast_id INT AUTO_INCREMENT PRIMARY KEY,
    forecast_date DATE UNIQUE NOT NULL,
    predicted_consumption FLOAT,
    model_used VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS energy_anomalies (
    anomaly_id INT AUTO_INCREMENT PRIMARY KEY,
    anomaly_date DATE UNIQUE NOT NULL,
    actual_consumption FLOAT,
    expected_consumption FLOAT,
    deviation FLOAT,
    is_anomaly BOOLEAN,
    explanation VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS model_metrics (
    metric_id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(50),
    mae FLOAT,
    rmse FLOAT,
    r2_score FLOAT,
    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
