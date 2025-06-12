
import os
import pandas as pd
import cdsapi
from datetime import datetime, timedelta

def save_era5_data(site_name, lat, lon, start, end, output_dir):
    output_zip = os.path.join(output_dir, f"era5_singlelevels_{site_name}.zip")
    output_csv = os.path.join(output_dir, f"era5_singlelevels_{site_name}.csv")

    if os.path.exists(output_csv):
        print(f"[📂] Données ERA5 (single levels) déjà présentes, chargement...")
        return output_csv

    print(f"[🧪] Requête ERA5 single levels : {site_name}, {start} → {end}")

    c = cdsapi.Client()

    try:
        c.retrieve(
            "reanalysis-era5-single-levels",
            {
                "product_type": "reanalysis",
                "variable": [
                    "10m_u_component_of_wind",
                    "10m_v_component_of_wind",
                    "10m_wind_gust_since_previous_post_processing"
                ],
                "year": [str(y) for y in range(int(start[:4]), int(end[:4]) + 1)],
                "month": [f"{m:02d}" for m in range(1, 13)],
                "day": [f"{d:02d}" for d in range(1, 32)],
                "time": [f"{h:02d}:00" for h in range(24)],
                "format": "csv",
                "area": [lat + 0.125, lon - 0.125, lat - 0.125, lon + 0.125],
            },
            output_zip,
        )
    except Exception as e:
        print(f"[❌] Erreur de téléchargement ERA5 : {e}")
        return None

    # Extraction CSV
    import zipfile
    with zipfile.ZipFile(output_zip, "r") as zip_ref:
        zip_ref.extractall(output_dir)

    # Suppression du zip
    os.remove(output_zip)

    return output_csv

def read_era5_single_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)
        df["time"] = pd.to_datetime(df["time"])

        # Calcul des vitesses moyennes à partir des composantes
        df["windspeed_mean"] = (df["u10"]**2 + df["v10"]**2)**0.5
        df["wind_direction"] = (180 / 3.14159) * (pd.np.arctan2(df["u10"], df["v10"])) + 180

        # Agrégation journalière
        df["date"] = df["time"].dt.date
        daily = df.groupby("date").agg({
            "windspeed_mean": "max",
            "wind_direction": "mean"
        }).reset_index()

        # Rafales
        if "10m_wind_gust_since_previous_post_processing" in df.columns:
            df["windspeed_gust"] = df["10m_wind_gust_since_previous_post_processing"]
            gusts = df.groupby("date").agg({
                "windspeed_gust": "max"
            }).reset_index()
            daily = pd.merge(daily, gusts, on="date", how="left")

        daily = daily.rename(columns={"date": "time"})
        return daily

    except Exception as e:
        print(f"[❌] Erreur lecture ERA5 single levels : {e}")
        return pd.DataFrame()
