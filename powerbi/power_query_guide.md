# Power Query Transformation Guide

1. **Import Data:**
   - Open Power BI Desktop.
   - Click **Get Data** -> **MySQL database** (if using the database) OR **Text/CSV** (if using the local `.csv` files in the `data/processed` and `outputs` folders).
   - If importing from CSV, load `cleaned_energy_data.csv`, `energy_forecast.csv`, and `energy_anomalies.csv`.

2. **Data Type Verification:**
   - In Power Query Editor, verify that the `Date` column in all tables is set to the **Date** data type (not Text or DateTime).
   - Ensure all consumption and generation columns (e.g., `tneb_campus_htsc_91`, `solar_generation`, `Total Consumption`) are set to **Decimal Number** or **Whole Number**.
   - Verify `is_anomaly` in the anomalies table is set to **True/False** or **Whole Number** (0/1).

3. **Create a Central Date Table:**
   - Instead of relying on auto-date/time, create a dedicated Date table.
   - You can create this via DAX in the modeling view:
     ```dax
     DateTable = CALENDAR(MIN('energy_readings'[reading_date]), MAX('energy_forecasts'[forecast_date]))
     ```
   - Mark this table as a **Date Table** in Power BI.

4. **Establish Relationships:**
   - Go to the **Model View**.
   - Create a one-to-many relationship from `DateTable[Date]` to:
     - `energy_readings[reading_date]`
     - `energy_forecasts[forecast_date]`
     - `energy_anomalies[anomaly_date]`
   - This allows filtering all visuals by a unified date timeline.

5. **Handling Missing Values:**
   - If any `null` values appear in numeric columns, you can right-click the column in Power Query and select **Replace Values** (e.g., replace `null` with `0`), though our Python script already handles interpolation.
