import pandas as pd
import os
from datetime import datetime
from modules.noaa_station_finder import load_isd_stations, find_nearest_isd_stations
from modules.noaa_isd_fetcher import fetch_isd_series

# === Paramètres ===
modele_sites_path = "modele_sites.csv"
isd_history_path = "data/isd-history.csv"

# === Interface Console ===
site_name = input("Nom du site présent dans modele_sites.csv : ").strip()
start = input("Date de début (YYYY-MM-DD) : ").strip()
end = input("Date de fin (YYYY-MM-DD) : ").strip()

start_year = int(start[:4])
end_year = int(end[:4])
years = list(range(start_year, end_year + 1))

# === Chargement des données ===
sites_df = pd.read_csv(modele_sites_path)
row = sites_df[sites_df["name"] == site_name]

if row.empty:
    print(f"[❌] Site '{site_name}' introuvable dans modele_sites.csv.")
    exit()

lat, lon = row.iloc[0]["latitude"], row.iloc[0]["longitude"]

# === Recherche des stations NOAA ===
isd_df = load_isd_stations(isd_history_path)
stations = find_nearest_isd_stations(lat, lon, isd_df, max_distance_km=80, n=2)

if not stations:
    print(f"[❌] Aucune station NOAA trouvée à proximité de {site_name}")
    exit()

# === Récupération des données pour chaque station ===
for i, station in enumerate(stations, 1):
    usaf, wban = station["usaf"], station["wban"]
    print(f"\n[📡] Téléchargement station{i} : {station['station_id']} ({station['distance_km']} km)")

    output_dir = os.path.join("Test_NOAA_" + site_name, f"station{i}")
    os.makedirs(output_dir, exist_ok=True)

    fetch_isd_series(
        usaf=usaf,
        wban=wban,
        years=years,
        output_dir=output_dir,
        site_name=site_name,
        verbose=True
    )

print(f"\n✅ Données sauvegardées dans le dossier : Test_NOAA_{site_name}/")
