import unittest
import json
import os

class TestPassiveZones(unittest.TestCase):
    def test_passive_outdoor_spaces_categorization(self):
        json_path = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'campus_locations.json')
        self.assertTrue(os.path.exists(json_path), "campus_locations.json should exist")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            locations = json.load(f)
            
        passive_keys = [
            'Empty Playground', 'Empty Playgorund', 'Agri Playground', 
            'Cricket Ground', 'Football Ground', 'Lake', 'Herbal Garden', 
            'Smart Agri Fields', 'Tennis Court 1', 'Basket Ball Court'
        ]
        
        for key in passive_keys:
            if key in locations:
                self.assertEqual(
                    locations[key]['category'], 
                    'Passive Outdoor Space', 
                    f"{key} should be classified as 'Passive Outdoor Space'"
                )

if __name__ == '__main__':
    unittest.main()
