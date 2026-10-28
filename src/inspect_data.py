import pandas as pd
import json

file_path = 'data/raw/College_Energy_Data_July_to_September_2026.xlsx'

print("--- Data Inspection Phase 1 ---")
xls = pd.ExcelFile(file_path)
print(f"Sheet names: {xls.sheet_names}")

if 'All Data' in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name='All Data')
    print("\n--- 'All Data' Info ---")
    df.info()
    
    print("\n--- Missing Values ---")
    print(df.isnull().sum())
    
    print("\n--- Descriptive Statistics ---")
    print(df.describe(include='all').to_string())
    
    print("\n--- First 5 rows ---")
    print(df.head().to_string())
    
    print("\n--- Unique Values in 'Month' ---")
    if 'Month' in df.columns:
        print(df['Month'].value_counts())
else:
    print("Error: 'All Data' sheet not found!")
