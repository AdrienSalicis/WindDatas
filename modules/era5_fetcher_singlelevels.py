import cdsapi
import os
import zipfile
import pandas as pd
import numpy as np
from datetime import datetime

def read_era5_single_csv(filepath):
    df = pd.read_csv(filepath)
    df = df.rename(columns={"valid_time": "time"})
    df["time"] = pd.to_datetime(df["time"], errors='coerce')
    df = df.dropna(subset=["time", "u10", "v10"])

    df["u10"] = df["u10"].astype(float)
    df["v10"] = df["v10"].astype(float)

    df["windspeed_10m"] = np.sqrt(df["u10"]**2 + df["v10"]**2)
    df["wind_direction"] = (180 / np.pi) * np.arctan2(df["u10"], df["v10"])
    df["wind_direction"] = (df["wind_direction"] + 180) % 360

    df["windspeed_mean"] = df["windspeed_10m"]

    return df[["time", "windspeed_10m", "windspeed_mean", "wind_direction"]]

def save_era5_singlelevels_data(site_name, site_folder, lat, lon, start_date, end_date):
    print(f"[📡] ERA5 single-levels pour {site_name} ({lat}, {lon}) de {start_date} à {end_date}")
    os.makedirs(site_folder, exist_ok=True)

    start_year = int(start_date[:4])
    end_year = int(end_date[:4])
    all_dfs = []

    for year in range(start_year, end_year + 1):
        filename_zip = os.path.join(site_folder, f"era5_single_{site_name}_{year}.zip")
        final_csv = os.path.join(site_folder, f"era5_{site_name}_{year}.csv")

        if os.path.exists(final_csv):
            print(f"[⏭️] Données déjà présentes pour {year}, saut...")
            df = pd.read_csv(final_csv)
            all_dfs.append(df)
            continue

        print(f"[⏳] Téléchargement ERA5 pour l’année {year}...")

        request = {
            "product_type": "reanalysis",
            "variable": [
                "10m_u_component_of_wind",
                "10m_v_component_of_wind",
                # "10m_wind_gust_since_previous_post_processing"
            ],
            "year": str(year),
            "month": [f"{m:02d}" for m in range(1, 13)],
            "day": [f"{d:02d}" for d in range(1, 32)],
            "time": [f"{h:02d}:00" for h in range(24)],
            "area": [lat + 0.025, lon - 0.025, lat - 0.025, lon + 0.025],  # [N, W, S, E]
            "format": "zip"
        }

        try:
            c = cdsapi.Client()
            c.retrieve("reanalysis-era5-single-levels", request).download(filename_zip)
        except Exception as e:
            print(f"[❌] Erreur téléchargement ERA5 pour {year} : {e}")
            continue

        try:
            with zipfile.ZipFile(filename_zip, 'r') as zip_ref:
                zip_ref.extractall(site_folder)
                extracted_files = zip_ref.namelist()

            csv_file = [f for f in extracted_files if f.endswith(".csv")][0]
            temp_csv = os.path.join(site_folder, csv_file)
            df = read_era5_single_csv(temp_csv)
            df.to_csv(final_csv, index=False)
            all_dfs.append(df)

            os.remove(temp_csv)
            os.remove(filename_zip)

        except Exception as e:
            print(f"[❌] Erreur traitement ERA5 {year} : {e}")
            continue

    if not all_dfs:
        print(f"[⚠️] Aucune donnée récupérée pour {site_name}")
        return None

    df_concat = pd.concat(all_dfs)
    df_concat = df_concat[df_concat["time"] >= start_date]
    df_concat = df_concat[df_concat["time"] <= end_date]

    df_daily = df_concat.set_index("time").resample("D").agg({
        "windspeed_10m": "max",
        "windspeed_mean": "mean",
        "wind_direction": "mean",
        # "wind_gust": "max"
    }).reset_index()

    final_path = os.path.join(site_folder, f"era5_daily_{site_name}.csv")
    df_daily.to_csv(final_path, index=False)

    print(f"[✅] Données journalières ERA5 finalisées pour {site_name} : {final_path}")
    return {
        "daily_csv": final_path,
        "hourly_df": df_concat  # optionnel si besoin d’extra analyse
    }
