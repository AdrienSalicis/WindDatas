
import os
import requests
import pandas as pd
from datetime import datetime

def fetch_noaa_api_data(site_name, site_folder, station_id, start_date, end_date):
    os.makedirs(site_folder, exist_ok=True)

    url = "https://www.ncei.noaa.gov/access/services/data/v1"
    params = {
        "dataset": "global-hourly",
        "stations": station_id,
        "startDate": start_date,
        "endDate": end_date,
        "format": "csv",
        "includeStationName": "1",
        "includeAttributes": "false",
        "dataTypes": "WND"
    }

    print(f"[📡] Appel API NOAA pour la station {station_id}...")
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"[❌] Erreur API NOAA : {response.status_code} - {response.text}")
        return None

    output_path = os.path.join(site_folder, f"noaa_api_{site_name}_raw.csv")
    with open(output_path, "wb") as f:
        f.write(response.content)

    try:
        df = pd.read_csv(output_path)
        print(f"[🔍] Colonnes disponibles pour {station_id} : {df.columns.tolist()}")

        if "WND" not in df.columns:
            print(f"[⚠️] Colonne 'WND' absente dans les données NOAA pour {station_id}. Données ignorées.")
            os.remove(output_path)
            return None

        df["DATE"] = pd.to_datetime(df["DATE"], errors='coerce')
        df = df.dropna(subset=["DATE"])

        wnd_parts = df["WND"].astype(str).str.split(",", expand=True)
        if wnd_parts.shape[1] < 4:
            print(f"[⚠️] Contenu mal formé de la colonne 'WND' pour {station_id} :")
            print(wnd_parts.head(5).to_string(index=False, header=False))
            os.remove(output_path)
            return None

        df["wind_direction"] = pd.to_numeric(wnd_parts[0], errors='coerce')
        df["windspeed_mean"] = pd.to_numeric(wnd_parts[3], errors='coerce') / 10  # NOAA en 0.1 m/s

        daily = df.groupby(df["DATE"].dt.date).agg({
            "windspeed_mean": ["mean", "max"],
            "wind_direction": "mean"
        }).reset_index()

        daily.columns = ["date", "windspeed_mean", "windspeed_gust", "wind_direction"]

        final_path = os.path.join(site_folder, f"noaa_api_{site_name}.csv")
        daily.to_csv(final_path, index=False)

        print(f"[✅] Données NOAA traitées enregistrées : {final_path} ({len(daily)} jours)")
        return {
            "filepath": final_path,
            "station_id": station_id,
            "rows": len(daily),
            "data": daily
        }

    except Exception as e:
        print(f"[⚠️] Fichier NOAA CSV illisible ou parsing KO : {e}")
        os.remove(output_path)
        return None
