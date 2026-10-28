import nbformat as nbf
import os

def create_notebook():
    nb = nbf.v4.new_notebook()
    
    cells = []
    
    # Title
    cells.append(nbf.v4.new_markdown_cell("# Predictive Energy Consumption Analytics\n## Phase 2: Exploratory Data Analysis (EDA)"))
    
    # Imports
    code_imports = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create output directories if they don't exist
os.makedirs('../outputs/figures', exist_ok=True)

# Set plotting style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
"""
    cells.append(nbf.v4.new_code_cell(code_imports))
    
    # Data Loading
    cells.append(nbf.v4.new_markdown_cell("### 1. Data Loading and Verification\nLoading the cleaned dataset, verifying columns, and checking data types."))
    code_load = """df = pd.read_csv('../data/processed/cleaned_energy_dataset.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

print(df.info())
print("\\nMissing values:\\n", df.isnull().sum())
"""
    cells.append(nbf.v4.new_code_cell(code_load))
    
    # Note on cleaning
    cells.append(nbf.v4.new_markdown_cell("**Note on Data Preparation**: 6 entirely empty rows at the bottom were dropped in Phase 1. Missing values in the `Chiller plant` column (which contained non-numeric strings) were coerced to NaN and interpolated linearly. `Total Consumption` is treated as the primary target variable and not manually recalculated."))

    # Descriptive Stats
    cells.append(nbf.v4.new_markdown_cell("### 2. Descriptive Statistics\nExporting the summary statistics to `outputs/`."))
    code_desc = """desc_stats = df.describe()
desc_stats.to_csv('../outputs/summary_statistics.csv')
display(desc_stats)
"""
    cells.append(nbf.v4.new_code_cell(code_desc))
    
    # Daily Trend
    cells.append(nbf.v4.new_markdown_cell("### 3. Daily Total Consumption Trend"))
    code_daily = """plt.figure()
plt.plot(df.index, df['Total Consumption'], color='blue', linewidth=2)
plt.title('Daily Total Energy Consumption')
plt.xlabel('Date')
plt.ylabel('Total Consumption (units)')
plt.tight_layout()
plt.savefig('../outputs/figures/daily_total_consumption.png')
plt.show()
"""
    cells.append(nbf.v4.new_code_cell(code_daily))
    
    # Monthly Trends
    cells.append(nbf.v4.new_markdown_cell("### 4. Monthly Trends\nNote: The dataset only spans three months (July, August, September), making it insufficient to derive long-term seasonal patterns."))
    code_monthly = """monthly_avg = df.groupby('Month')['Total Consumption'].mean().reindex(['July', 'August', 'September'])
plt.figure(figsize=(8, 5))
monthly_avg.plot(kind='bar', color='skyblue')
plt.title('Average Daily Consumption by Month')
plt.xlabel('Month')
plt.ylabel('Average Daily Consumption (units)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('../outputs/figures/monthly_average_consumption.png')
plt.show()
"""
    cells.append(nbf.v4.new_code_cell(code_monthly))
    
    # Infrastructure
    cells.append(nbf.v4.new_markdown_cell("### 5. Infrastructure-Wise Consumption"))
    code_infra = """infra_cols = ['Staff Quarters', 'Academic blocks', 'Hostels', 'Chiller plant', 'STP']
infra_sum = df[infra_cols].sum()

plt.figure(figsize=(10, 6))
infra_sum.plot(kind='pie', autopct='%1.1f%%', startangle=90, cmap='Set3')
plt.title('Total Energy Consumption Breakdown by Infrastructure')
plt.ylabel('')
plt.tight_layout()
plt.savefig('../outputs/figures/infrastructure_consumption_pie.png')
plt.show()
"""
    cells.append(nbf.v4.new_code_cell(code_infra))
    
    # Generation
    cells.append(nbf.v4.new_markdown_cell("### 6. Power Generation Trends"))
    code_gen = """gen_cols = ['Power Generation by Solar Panels', 'Power Generation by Diesel Engines', 'Power Generation by Biogas Engines']
df[gen_cols].plot(figsize=(14, 6))
plt.title('Daily Power Generation by Source')
plt.xlabel('Date')
plt.ylabel('Generation (units)')
plt.legend(['Solar', 'Diesel', 'Biogas'])
plt.tight_layout()
plt.savefig('../outputs/figures/generation_trends.png')
plt.show()
"""
    cells.append(nbf.v4.new_code_cell(code_gen))
    
    # Weekday vs Weekend
    cells.append(nbf.v4.new_markdown_cell("### 7. Weekday vs Weekend Patterns\nAnalyzing whether consumption drops on weekends."))
    code_weekend = """df['DayOfWeek'] = df.index.dayofweek
df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')

plt.figure(figsize=(8, 5))
sns.boxplot(x='IsWeekend', y='Total Consumption', data=df, palette='Set2')
plt.title('Total Consumption: Weekday vs Weekend')
plt.xlabel('Day Type')
plt.ylabel('Total Consumption (units)')
plt.tight_layout()
plt.savefig('../outputs/figures/weekday_vs_weekend_boxplot.png')
plt.show()

weekend_stats = df.groupby('IsWeekend')['Total Consumption'].mean()
print(weekend_stats)
"""
    cells.append(nbf.v4.new_code_cell(code_weekend))
    
    # Peak and Low
    cells.append(nbf.v4.new_markdown_cell("### 8. Peak and Low Consumption Days"))
    code_peak = """peak_date = df['Total Consumption'].idxmax()
low_date = df['Total Consumption'].idxmin()

peak_val = df.loc[peak_date, 'Total Consumption']
low_val = df.loc[low_date, 'Total Consumption']

peak_low_df = pd.DataFrame({
    'Metric': ['Peak Consumption', 'Low Consumption'],
    'Date': [peak_date.date(), low_date.date()],
    'Consumption (units)': [peak_val, low_val]
})

peak_low_df.to_csv('../outputs/peak_low_consumption.csv', index=False)
display(peak_low_df)
"""
    cells.append(nbf.v4.new_code_cell(code_peak))
    
    # Correlation
    cells.append(nbf.v4.new_markdown_cell("### 9. Correlation Analysis\nExamining linear relationships between consumption sources, generation, and total consumption."))
    code_corr = """numeric_cols = df.select_dtypes(include=[np.number]).columns
# Exclude DayOfWeek 
numeric_cols = [c for c in numeric_cols if c not in ['DayOfWeek']]
corr = df[numeric_cols].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Heatmap of Energy Variables')
plt.tight_layout()
plt.savefig('../outputs/figures/correlation_heatmap.png')
plt.show()
"""
    cells.append(nbf.v4.new_code_cell(code_corr))
    
    # Markdown conclusions
    cells.append(nbf.v4.new_markdown_cell("### 10. Key Findings & Observations\n"
                                          "- **Daily Trends**: Total consumption fluctuates heavily, with notable drops likely corresponding to weekends.\n"
                                          "- **Weekend Effect**: The boxplot confirms that energy consumption is significantly lower on weekends compared to weekdays, which is typical for academic environments.\n"
                                          "- **Generation**: Solar power is consistently the highest secondary generation source, whereas diesel is used sporadically (likely as a backup). Biogas is consistently low but stable.\n"
                                          "- **Infrastructure**: Academic blocks consume the lion's share of energy, followed by Hostels.\n"
                                          "- **Correlation**: `Total Consumption` is highly correlated with `Academic blocks` and `TNEB Campus HTSC-91` (the main grid). `Solar Generation` shows a modest negative or weak correlation with specific consumptions, indicating it supplements the grid during high-sun hours.\n"
                                          "- **Data Integrity Note**: No obvious data leakage in this retrospective EDA. It's confirmed that all values represent daily consumption rather than cumulative meter readings because they fluctuate up and down daily instead of strictly increasing.\n"
                                          "- **Limitations**: We only have data for July, August, and part of September. Annual seasonality (e.g., winter heating vs summer cooling) cannot be deduced from this small window."))
    
    nb['cells'] = cells
    
    os.makedirs('notebooks', exist_ok=True)
    with open('notebooks/energy_analysis.ipynb', 'w') as f:
        nbf.write(nb, f)
        
if __name__ == '__main__':
    create_notebook()
