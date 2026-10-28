import pandas as pd
import numpy as np
import os
import json

def analyze_and_clean(file_path):
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    report_lines = ["# Data Quality Report - Phase 1\n"]
    
    # 1. Inspect sheets
    xls = pd.ExcelFile(file_path)
    report_lines.append(f"**Available Sheets**: {', '.join(xls.sheet_names)}\n")
    report_lines.append("Selected '**All Data**' as the consolidated dataset.\n")
    
    # Load All Data
    df = pd.read_excel(xls, sheet_name='All Data')
    
    # Basic info
    report_lines.append(f"**Original Row Count**: {len(df)}")
    report_lines.append(f"**Original Column Count**: {len(df.columns)}")
    report_lines.append(f"**Columns**: {', '.join(df.columns)}\n")
    
    # Check data types
    report_lines.append("### Data Types")
    for col, dtype in df.dtypes.items():
        report_lines.append(f"- `{col}`: {dtype}")
    report_lines.append("\n")
    
    # Duplicate rows
    duplicates = df.duplicated().sum()
    report_lines.append(f"**Duplicate Rows**: {duplicates}\n")
    
    # Missing values
    missing = df.isnull().sum()
    report_lines.append("### Missing Values (Original)")
    for col, val in missing.items():
        report_lines.append(f"- `{col}`: {val}")
    report_lines.append("\n")
    
    # Observation on empty rows
    empty_rows = df.isnull().all(axis=1).sum()
    if empty_rows > 0:
        report_lines.append(f"**Note**: Found {empty_rows} completely empty rows at the end of the dataset. These will be removed.\n")
        df.dropna(how='all', inplace=True)
        
    # Check Chiller plant type
    if df['Chiller plant'].dtype == object:
        # Investigate why
        non_numeric = df[pd.to_numeric(df['Chiller plant'], errors='coerce').isnull() & df['Chiller plant'].notnull()]
        report_lines.append(f"**Chiller Plant Issues**: Found non-numeric values. Example: {non_numeric['Chiller plant'].unique() if len(non_numeric) > 0 else 'None'}. Coercing to numeric.\n")
        df['Chiller plant'] = pd.to_numeric(df['Chiller plant'], errors='coerce')
        
    # Interpolate missing values in middle of dataset
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    df.interpolate(method='linear', inplace=True)
    
    # Investigate STP
    stp_missing = df['STP'].isnull().sum()
    report_lines.append(f"**STP Column Analysis**: After empty-row removal and linear interpolation, missing values in STP: {stp_missing}.\n")

    # Date range
    date_min = df['Date'].min()
    date_max = df['Date'].max()
    report_lines.append(f"**Date Range**: {date_min.date()} to {date_max.date()}\n")
    
    # Validate Total Consumption
    gen_cols = ['TNEB Campus HTSC-91', 'TNEB New STP HTSC-178', 'Power Generation by Solar Panels', 
                'Power Generation by Diesel Engines', 'Power Generation by Biogas Engines']
    cons_cols = ['Staff Quarters', 'Academic blocks', 'Hostels', 'Chiller plant', 'STP']
    
    df['Calc_Total_Gen'] = df[gen_cols].sum(axis=1)
    df['Calc_Total_Cons'] = df[cons_cols].sum(axis=1)
    
    df['Gen_Diff'] = (df['Total Consumption'] - df['Calc_Total_Gen']).abs()
    df['Cons_Diff'] = (df['Total Consumption'] - df['Calc_Total_Cons']).abs()
    
    max_gen_diff = df['Gen_Diff'].max()
    max_cons_diff = df['Cons_Diff'].max()
    
    report_lines.append("### Total Consumption Validation")
    report_lines.append(f"- Max difference vs Generation Sum: {max_gen_diff}")
    report_lines.append(f"- Max difference vs Infrastructure Consumption Sum: {max_cons_diff}")
    report_lines.append("Conclusion: 'Total Consumption' does not perfectly equal the sum of generating sources or consuming infrastructure in every row. It should be used as the primary target variable, but discrepancies exist in the dataset.\n")
    
    df.drop(columns=['Calc_Total_Gen', 'Calc_Total_Cons', 'Gen_Diff', 'Cons_Diff'], inplace=True)
    
    # Numeric Summary
    report_lines.append("### Numeric Summary Statistics")
    report_lines.append("```text")
    report_lines.append(df.describe().to_string())
    report_lines.append("```\n")
    
    # Save report
    with open('outputs/data_quality_report.md', 'w') as f:
        f.write('\n'.join(report_lines))
        
    # Save cleaned dataset
    df.to_csv('data/processed/cleaned_energy_dataset.csv', index=False)
    
    print("Phase 1 completed. Report saved to outputs/data_quality_report.md and cleaned data to data/processed/cleaned_energy_dataset.csv")

if __name__ == '__main__':
    analyze_and_clean('data/raw/College_Energy_Data_July_to_September_2026.xlsx')
