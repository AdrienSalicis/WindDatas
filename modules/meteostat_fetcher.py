
import os
import pandas as pd
from meteostat import Stations, Daily
from datetime import datetime
from geopy.distance import geodesic

def get_nearest_stations_info(lat, lon, limit=2):
    stations = Stations().nearby(lat, lon)
    results = stations.fetch(limit)

    info = {}
    for i, (index, row) in enumerate(results.iterrows(), 1):
        dist = geodesic((lat, lon), (row['latitude'], row['longitude'])).km
        info[f"station{i}"] = {
            "id": index,
            "name": row["name"],
            "distance_km": round(dist, 2),
            "latitude": row["latitude"],
            "longitude": row["longitude"]
        }
    return info

def fetch_meteostat_data(site_name, site_folder, lat, lon, start_date, end_date, station_ids=None):
    os.makedirs(site_folder, exist_ok=True)

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    if station_ids is None:
        stations_df = Stations().nearby(lat, lon).fetch(2)
        station_ids = stations_df.index.tolist()

    data_collected = {}

    for i, station_id in enumerate(station_ids, 1):
        print(f"[📡] Téléchargement Meteostat pour station : {station_id}")
        data = Daily(station_id, start, end)
        df = data.fetch().reset_index()

        if df.empty:
            print(f"[⚠️] Pas de données pour Meteostat station {station_id}")
            continue

        df["time"] = pd.to_datetime(df["time"])
        df = df[["time", "wspd", "wpgt", "wdir"]]
        df = df.rename(columns={
            "wspd": "windspeed_mean",
            "wpgt": "windspeed_gust",
            "wdir": "wind_direction"
        })

        filename = f"meteostat{i}_{site_name}.csv"
        filepath = os.path.join(site_folder, filename)
        df.to_csv(filepath, index=False)
        print(f"[✅] Données Meteostat enregistrées : {filepath}")

        data_collected[f"meteostat{i}"] = df

    return data_collected
