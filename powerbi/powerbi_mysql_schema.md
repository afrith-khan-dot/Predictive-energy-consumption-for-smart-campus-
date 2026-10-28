# Power BI to MySQL Integration Guide

This guide details how to integrate the Microsoft Power BI dashboard with the `smart_campus_energy` MySQL database generated in Phase 4. 

## 1. Connection Setup
- Open Power BI Desktop.
- Go to **Get Data** -> **More...** -> **MySQL database**.
- Enter your server host (e.g., `localhost:3306`) and database name (`smart_campus_energy`).
- Provide credentials as configured in `.env`.
- Select **Import** or **DirectQuery**. *Import mode is recommended* for fast dashboard responsiveness unless you require near real-time updates.

## 2. Table Schemas & Data Types
Load the following tables from the database into your Power BI Data Model:

### A. `energy_readings` (Fact Table)
- **Primary Key**: `reading_id`
- **Date Column**: `reading_date` (Format as Date)
- **Values**: Campus energy usages and generation data.
- **Use Case**: Primary data source for historical energy tracking, infrastructure pie charts, and monthly trend analytics.

### B. `energy_forecasts` (Fact Table)
- **Primary Key**: `forecast_id`
- **Date Column**: `forecast_date` (Format as Date)
- **Values**: `predicted_consumption`
- **Use Case**: Powers the next 7-day predictive analytics line chart.

### C. `energy_anomalies` (Fact Table)
- **Primary Key**: `anomaly_id`
- **Date Column**: `anomaly_date` (Format as Date)
- **Values**: `actual_consumption`, `deviation`, `explanation`
- **Use Case**: Used for highlighting anomalous points on historical line charts and building an "Anomalies Summary" table visual. 

### D. `model_metrics` (Dimension/Info Table)
- **Primary Key**: `metric_id`
- **Use Case**: Static KPI cards to display MAE and RMSE, establishing trust in the model's performance on the dashboard.

## 3. Creating a Dedicated Date Table
To link `energy_readings`, `energy_forecasts`, and `energy_anomalies` together, you **MUST** create a unified Date Table in Power BI.

**DAX for Date Table:**
```dax
DimDate = CALENDAR(
    MIN(MIN(energy_readings[reading_date]), MIN(energy_anomalies[anomaly_date])),
    MAX(energy_forecasts[forecast_date])
)
```
*Be sure to add standard columns like Month, Year, and Day of Week to `DimDate`.*

## 4. Establishing Relationships
Go to the **Model View** in Power BI and establish the following relationships (One-to-Many, Single Direction):
1. `DimDate[Date]` ➔ `energy_readings[reading_date]`
2. `DimDate[Date]` ➔ `energy_forecasts[forecast_date]`
3. `DimDate[Date]` ➔ `energy_anomalies[anomaly_date]`

## 5. Dashboard Page Mapping
- **Executive Overview**: Driven by `energy_readings` (Aggregated KPIs) + `DimDate`
- **Infrastructure Analysis**: Driven by `energy_readings` (Staff Quarters, Hostels, Academic Blocks, etc.)
- **Prediction & Anomaly**: Driven by a combined line chart mapping `energy_readings[total_consumption]` and `energy_forecasts[predicted_consumption]` via `DimDate`. Anomalies act as a scatter plot overlay using `energy_anomalies[actual_consumption]`. `model_metrics` provides KPIs.
- **Renewable Energy**: Driven by `energy_readings` (Solar, Biogas).

## 6. Refresh Considerations
Set up Scheduled Refresh in Power BI Service:
1. Ensure the Power BI On-premises Data Gateway is installed if MySQL is hosted locally/on-prem.
2. Schedule refresh triggers right after the daily Python ETL job (`src/load_to_mysql.py`) completes to ensure users see the latest anomalies and forecasts every morning.
