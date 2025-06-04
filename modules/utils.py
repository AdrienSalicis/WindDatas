import os
import pandas as pd
from geopy.distance import geodesic

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def load_sites_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df.to_dict(orient='records')



def calculate_distance_km(coord1, coord2):
    try:
        return round(geodesic(coord1, coord2).km, 2)
    except Exception as e:
        print(f"[❌] Erreur lors du calcul de distance : {e}")
        return None
