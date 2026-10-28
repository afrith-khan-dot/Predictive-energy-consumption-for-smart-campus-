import nbformat as nbf
import os

def create_eda_notebook():
    nb = nbf.v4.new_notebook()
    
    # Markdown Cell 1
    text1 = """# Predictive Energy Consumption Analytics for Smart Campus Infrastructure
## Exploratory Data Analysis
This notebook covers:
- Dataset overview and descriptive statistics
- Daily consumption trends
- Monthly energy consumption comparisons
- Consumption by campus building or infrastructure category
- Solar, diesel, and biogas generation trends
- Correlation analysis
- Peak-consumption and low-consumption days
"""
    
    # Code Cell 1
    code1 = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

# Load the cleaned dataset
df = pd.read_csv('../data/processed/cleaned_energy_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df.head()"""
    
    text2 = """### Dataset Overview and Descriptive Statistics"""
    
    code2 = """print(df.info())
display(df.describe())
"""

    text3 = """### Daily Consumption Trends"""
    
    code3 = """plt.figure(figsize=(12, 5))
plt.plot(df.index, df['Total Consumption'], marker='o', linestyle='-')
plt.title('Daily Total Energy Consumption')
plt.ylabel('Consumption (units)')
plt.xlabel('Date')
plt.grid(True)
plt.show()"""

    text4 = """### Consumption by Campus Building / Infrastructure"""
    
    code4 = """cons_cols = ['Staff Quarters', 'Academic blocks', 'Hostels', 'Chiller plant', 'STP']
df[cons_cols].sum().plot(kind='bar', figsize=(10, 5))
plt.title('Total Consumption by Infrastructure Category')
plt.ylabel('Consumption (units)')
plt.xticks(rotation=45)
plt.show()"""

    text5 = """### Power Generation Trends (Solar, Diesel, Biogas)"""
    
    code5 = """gen_cols = ['Power Generation by Solar Panels', 'Power Generation by Diesel Engines', 'Power Generation by Biogas Engines']
df[gen_cols].plot(figsize=(12, 6))
plt.title('Power Generation by Source')
plt.ylabel('Generation (units)')
plt.xlabel('Date')
plt.grid(True)
plt.show()"""

    text6 = """### Correlation Analysis"""
    
    code6 = """numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()"""
    
    text7 = """### Peak and Low Consumption Days"""
    
    code7 = """peak_day = df['Total Consumption'].idxmax()
low_day = df['Total Consumption'].idxmin()
print(f"Peak Consumption Day: {peak_day.date()} with {df.loc[peak_day, 'Total Consumption']} units")
print(f"Low Consumption Day: {low_day.date()} with {df.loc[low_day, 'Total Consumption']} units")"""

    nb['cells'] = [
        nbf.v4.new_markdown_cell(text1),
        nbf.v4.new_code_cell(code1),
        nbf.v4.new_markdown_cell(text2),
        nbf.v4.new_code_cell(code2),
        nbf.v4.new_markdown_cell(text3),
        nbf.v4.new_code_cell(code3),
        nbf.v4.new_markdown_cell(text4),
        nbf.v4.new_code_cell(code4),
        nbf.v4.new_markdown_cell(text5),
        nbf.v4.new_code_cell(code5),
        nbf.v4.new_markdown_cell(text6),
        nbf.v4.new_code_cell(code6),
        nbf.v4.new_markdown_cell(text7),
        nbf.v4.new_code_cell(code7)
    ]
    
    os.makedirs('notebooks', exist_ok=True)
    with open('notebooks/energy_analysis.ipynb', 'w') as f:
        nbf.write(nb, f)
        
    print("Notebook 'energy_analysis.ipynb' created successfully.")

if __name__ == '__main__':
    create_eda_notebook()
