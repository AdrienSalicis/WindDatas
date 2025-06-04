import cdsapi
import os
import zipfile
import pandas as pd
import numpy as np
from datetime import datetime

def save_era5_daily(site_name, site_folder, hourly_df):
    daily = hourly_df.set_index("time").resample("D").agg({
        "windspeed_10m": "max",
        "windspeed_mean": "max",  # ou "mean" si tu préfères
        "wind_direction": "mean"
    }).reset_index()

    filename = f"era5_daily_{site_name}.csv"
    filepath = os.path.join(site_folder, filename)
    daily.to_csv(filepath, index=False)
    return filepath

def read_era5_csv(filepath):
    df = pd.read_csv(filepath)
    df = df.rename(columns={"valid_time": "time"})
    df["time"] = pd.to_datetime(df["time"], errors='coerce')
    df = df.dropna(subset=["time", "u10", "v10"])

    df["u10"] = df["u10"].astype(float)
    df["v10"] = df["v10"].astype(float)

    df["windspeed_10m"] = np.sqrt(df["u10"]**2 + df["v10"]**2)
    df["wind_direction"] = (180 / np.pi) * np.arctan2(df["u10"], df["v10"])
    df["wind_direction"] = (df["wind_direction"] + 180) % 360

    df["windspeed_mean"] = df["windspeed_10m"]  # Ajout clé pour compatibilité

    return df[["time", "windspeed_10m", "windspeed_mean", "wind_direction"]]

def save_era5_data(site_name, site_folder, lat, lon, start_date, end_date):
    print(f"[📡] Téléchargement ERA5 (timeseries CSV) pour {site_name}...")

    os.makedirs(site_folder, exist_ok=True)
    dataset = "reanalysis-era5-single-levels-timeseries"
    request = {
        "variable": [
            "10m_u_component_of_wind",
            "10m_v_component_of_wind"
        ],
        "location": {
            "longitude": float(lon),
            "latitude": float(lat)
        },
        "date": f"{start_date}/{end_date}",
        "data_format": "csv"
    }

    temp_zip = os.path.join(site_folder, f"era5_temp_{site_name}.zip")

    # === Diagnostic CDSAPI ===
    print("[🧪] Tentative de création du client CDSAPI...")
    print("[🧪] Utilisation du fichier .cdsapirc (par défaut ou forcé)")

    if os.path.exists(os.path.expanduser("~/.cdsapirc")):
        print("[✅] Fichier ~/.cdsapirc détecté.")
    else:
        print("[❌] Fichier ~/.cdsapirc non trouvé.")

    print("[🧾] Variables d’environnement (extrait) :")
    import pprint
    pprint.pprint({k: v for k, v in os.environ.items() if "CDS" in k or "cds" in k})

    try:
        c = cdsapi.Client(
            url="https://cds.climate.copernicus.eu/api",
            key="3ede72e1-0636-4ad5-99ee-723311047e81"
        )
    except Exception as e:
        print(f"[❌] Erreur lors de la création du client CDSAPI : {e}")
        return None

    # === Téléchargement ===
    try:
        c.retrieve(dataset, request).download(temp_zip)
    except Exception as e:
        print(f"[❌] Erreur API ERA5 : {e}")
        return None

    # === Extraction et traitement du CSV ===
    try:
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall(site_folder)
            extracted_files = zip_ref.namelist()

        csv_file = [f for f in extracted_files if f.endswith(".csv")]
        if not csv_file:
            raise Exception("Aucun fichier CSV trouvé dans le ZIP téléchargé.")

        temp_csv = os.path.join(site_folder, csv_file[0])
        df_final = read_era5_csv(temp_csv)
        
        if df_final.empty:
            print("[❌] Fichier ERA5 vide après traitement.")
            return None

        final_csv = os.path.join(site_folder, f"era5_{site_name}.csv")
        df_final.to_csv(final_csv, index=False)

        os.remove(temp_csv)
        os.remove(temp_zip)

        # === Agrégation journalière ERA5 ===
        df_daily = df_final.set_index("time").resample("D").agg({
            "windspeed_10m": "max",
            "windspeed_mean": "max",  # ou "mean" selon usage
            "wind_direction": "mean"
        }).reset_index()

        daily_csv = os.path.join(site_folder, f"era5_daily_{site_name}.csv")
        df_daily.to_csv(daily_csv, index=False)
        print(f"[📁] Fichier ERA5 journalier généré : {daily_csv}")

        print(f"[✅] Données ERA5 sauvegardées : {final_csv}")
        return {
            "filename": os.path.basename(final_csv),
            "filepath": final_csv,
            "filepath_daily": daily_csv,
            "latitude": lat,
            "longitude": lon
        }


    except Exception as e:
        print(f"[❌] Erreur traitement ERA5 : {e}")
        return None
    
