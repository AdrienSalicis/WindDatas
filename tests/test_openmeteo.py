import unittest
import pandas as pd
from modules.openmeteo_fetcher import fetch_openmeteo_data

class TestOpenMeteoFetcher(unittest.TestCase):
    def test_fetch_openmeteo_data_basic(self):
        # Coordonnées : Paris
        lat = 48.8566
        lon = 2.3522
        start = "2023-01-01"
        end = "2023-01-10"

        df = fetch_openmeteo_data(lat, lon, start, end)

        # Vérifie que c’est un DataFrame et qu’il n’est pas vide
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)

        # Vérifie les colonnes attendues
        for col in ['time', 'windspeed_mean', 'windspeed_gust', 'wind_direction']:
            self.assertIn(col, df.columns)

if __name__ == '__main__':
    unittest.main()
