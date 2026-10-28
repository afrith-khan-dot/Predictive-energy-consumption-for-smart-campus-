# Power BI Dashboard Implementation Guide

## Page 1: Executive Overview
**Objective:** Provide a high-level summary of campus energy consumption.

- **KPI Cards:**
  - Total Energy Consumption
  - Average Daily Consumption
  - Peak Daily Consumption
  - Total Solar, Diesel, and Biogas Generation (use separate cards)
- **Line Chart (Consumption Trend):**
  - X-Axis: `DateTable[Date]`
  - Y-Axis: `Total Consumption`
- **Gauge Chart:**
  - Value: Forecasted Consumption (next 7 days sum)

## Page 2: Infrastructure Analysis
**Objective:** Break down consumption by campus building/category.

- **Slicers:** Date range (slider), Month (dropdown).
- **Stacked Bar Chart:**
  - X-Axis: `DateTable[Date]`
  - Y-Axis: `staff_quarters`, `academic_blocks`, `hostels`, `chiller_plant`, `stp` (stacked).
- **Donut Chart:**
  - Values: Sums of the above 5 infrastructure categories.
  - *Tip:* Ensure you are comparing apples-to-apples (all in units of energy).

## Page 3: Prediction & Anomaly Analysis
**Objective:** Review model performance, forecasted values, and detected anomalies.

- **Line Chart (Actual vs Forecast):**
  - X-Axis: `DateTable[Date]`
  - Y-Axis 1 (Actual): `Total Consumption` from `energy_readings`
  - Y-Axis 2 (Forecast): `Predicted_Consumption` from `energy_forecasts`
  - *Note:* The lines will connect at the present day if modeled correctly.
- **Table Visual (Anomalies):**
  - Columns: `Date`, `Actual_Consumption`, `Expected_Consumption`, `Deviation`, `Explanation`
  - Filter: `is_anomaly = 1`
- **KPI Card:** Anomaly Count

## Page 4: Renewable Energy & Efficiency
**Objective:** Analyze power generation sources and identify efficiency opportunities.

- **Area Chart (Generation Mix):**
  - X-Axis: `DateTable[Date]`
  - Y-Axis: `solar_generation`, `diesel_generation`, `biogas_generation`
- **KPI Card:** Renewable Contribution % (DAX measure)
- **Scatter Plot (Efficiency check):**
  - X-Axis: `solar_generation`
  - Y-Axis: `tneb_campus_htsc_91` (Grid consumption)
  - *Insight:* Does high solar generation consistently correlate with low grid draw?
