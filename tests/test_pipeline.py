import unittest
import pandas as pd
import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from feature_engineering import create_features

class TestPipeline(unittest.TestCase):
    
    def setUp(self):
        # Create a mock dataframe for testing
        dates = pd.date_range(start='2026-07-01', periods=10, freq='D')
        self.mock_df = pd.DataFrame({
            'Date': dates,
            'Total Consumption': [20000, 21000, 19500, 22000, 23000, 21000, 20500, 19000, 18500, 24000]
        })
        
    def test_feature_engineering(self):
        result_df = create_features(self.mock_df)
        
        # Check if lag and rolling features are created
        self.assertIn('Lag_1', result_df.columns)
        self.assertIn('Rolling_Mean_3', result_df.columns)
        
        # Check if rows with NaNs (due to shift) are dropped
        # We used Lag_7, so the first 7 rows should be dropped
        # 10 rows - 7 = 3 rows remaining
        self.assertEqual(len(result_df), 3)
        
    def test_data_files_exist(self):
        # Check if outputs exist
        self.assertTrue(os.path.exists('data/processed/cleaned_energy_data.csv'))
        self.assertTrue(os.path.exists('outputs/energy_forecast.csv'))
        self.assertTrue(os.path.exists('outputs/energy_anomalies.csv'))
        self.assertTrue(os.path.exists('models/energy_model.pkl'))

if __name__ == '__main__':
    unittest.main()
