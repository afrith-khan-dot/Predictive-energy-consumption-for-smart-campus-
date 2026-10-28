-- Daily and monthly consumption
SELECT month_name, SUM(total_consumption) as monthly_consumption 
FROM energy_readings 
GROUP BY month_name;

-- Peak day consumption
SELECT reading_date, total_consumption 
FROM energy_readings 
ORDER BY total_consumption DESC 
LIMIT 1;

-- Infrastructure-wise consumption averages
SELECT 
    AVG(staff_quarters) as avg_staff,
    AVG(academic_blocks) as avg_academic,
    AVG(hostels) as avg_hostels,
    AVG(chiller_plant) as avg_chiller,
    AVG(stp) as avg_stp
FROM energy_readings;

-- Anomalies summary
SELECT anomaly_date, actual_consumption, expected_consumption, explanation 
FROM energy_anomalies 
WHERE is_anomaly = TRUE;

-- Forecast summary
SELECT forecast_date, predicted_consumption 
FROM energy_forecasts 
ORDER BY forecast_date ASC;
