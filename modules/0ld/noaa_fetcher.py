
import os
import requests
import pandas as pd
from datetime import datetime
from zipfile import ZipFile
from io import BytesIO

GSOD_BASE_URL = "https://www.ncei.noaa.gov/data/global-summary-of-the-day/access"

def fetch_noaa_data(station_id, start_year, end_year):
    usaf, wban = station_id.split("-")
    collected_data = []
    missing_years = []

    for year in range(int(start_year), int(end_year) + 1):
        url = f"{GSOD_BASE_URL}/{year}/{usaf}-{wban}.csv"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                df = pd.read_csv(BytesIO(response.content))
                df["YEAR"] = year
                collected_data.append(df)
            else:
                missing_years.append(year)
        except Exception as e:
            print(f"[❌] Erreur {year} : {e}")
            missing_years.append(year)

    if missing_years:
        print(f"[⚠️] Données NOAA indisponibles pour {station_id} de {missing_years[0]} à {missing_years[-1]}.")

    if collected_data:
        return pd.concat(collected_data, ignore_index=True)
    else:
        return None

def save_noaa_data(site_name, site_folder, station_id, start_date, end_date):
    os.makedirs(site_folder, exist_ok=True)

    start_year = datetime.strptime(start_date, "%Y-%m-%d").year
    end_year = datetime.strptime(end_date, "%Y-%m-%d").year

    print(f"[📡] Téléchargement des données NOAA pour {station_id} de {start_year} à {end_year}...")

    df = fetch_noaa_data(station_id, start_year, end_year)
    if df is not None:
        filepath = os.path.join(site_folder, f"noaa_{site_name}.csv")
        df.to_csv(filepath, index=False)
        print(f"[✅] Données NOAA enregistrées : {filepath}")
        return {
            "filepath": filepath,
            "station_id": station_id,
            "metadata": {
                "years_available": df["YEAR"].nunique(),
                "total_rows": len(df)
            }
        }
    else:
        print("[⚠️] Aucune donnée NOAA récupérée.")
        return None
