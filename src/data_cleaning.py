import pandas as pd
import numpy as np
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_data(input_path: str, output_csv: str, output_excel: str):
    logging.info(f"Loading data from {input_path}")
    
    # Read the 'All Data' sheet
    df = pd.read_excel(input_path, sheet_name='All Data')
    
    # 1. Drop completely empty rows
    initial_len = len(df)
    df.dropna(how='all', inplace=True)
    logging.info(f"Dropped {initial_len - len(df)} empty rows.")
    
    # 2. Date conversion
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 3. Handle 'Chiller plant' column which has object type
    df['Chiller plant'] = pd.to_numeric(df['Chiller plant'], errors='coerce')
    
    # Investigate missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        logging.warning(f"Missing values found after coercion:\n{missing[missing > 0]}")
        # Let's fill forward or interpolate?
        # Actually, let's just linearly interpolate any small gaps
        df.interpolate(method='linear', inplace=True)
        logging.info("Interpolated missing values.")
    
    # 4. Check for negative values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        negatives = (df[col] < 0).sum()
        if negatives > 0:
            logging.warning(f"Found {negatives} negative values in {col}. Setting to 0.")
            df.loc[df[col] < 0, col] = 0
            
    # 5. Validate Total Consumption
    gen_cols = ['TNEB Campus HTSC-91', 'TNEB New STP HTSC-178', 'Power Generation by Solar Panels', 
                'Power Generation by Diesel Engines', 'Power Generation by Biogas Engines']
    cons_cols = ['Staff Quarters', 'Academic blocks', 'Hostels', 'Chiller plant', 'STP']
    
    df['Calculated_Total_Gen'] = df[gen_cols].sum(axis=1)
    df['Calculated_Total_Cons'] = df[cons_cols].sum(axis=1)
    
    gen_diff = (df['Total Consumption'] - df['Calculated_Total_Gen']).abs().max()
    cons_diff = (df['Total Consumption'] - df['Calculated_Total_Cons']).abs().max()
    
    logging.info(f"Max difference between Total Consumption and Generation sum: {gen_diff}")
    logging.info(f"Max difference between Total Consumption and Consumption sum: {cons_diff}")
    
    # Drop calculation columns as they were just for validation
    df.drop(columns=['Calculated_Total_Gen', 'Calculated_Total_Cons'], inplace=True)
    
    # 6. Sort by date
    df.sort_values(by='Date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # Save cleaned data
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    df.to_excel(output_excel, index=False)
    logging.info(f"Cleaned data saved to {output_csv} and {output_excel}")
    
    return df

if __name__ == "__main__":
    input_file = "data/raw/College_Energy_Data_July_to_September_2026.xlsx"
    out_csv = "data/processed/cleaned_energy_data.csv"
    out_excel = "data/processed/cleaned_energy_data.xlsx"
    clean_data(input_file, out_csv, out_excel)
