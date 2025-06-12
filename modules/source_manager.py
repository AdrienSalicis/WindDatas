# source_manager.py
import os
import pandas as pd
from modules.meteostat_fetcher import fetch_meteostat_data
from modules.era5_fetcher import save_era5_data
from modules.nasa_power_fetcher import fetch_nasa_power_data
from modules.openmeteo_fetcher import save_openmeteo_data

def fetch_observed_sources(site_info, site_name, site_folder, lat, lon,
                            start_date, end_date, meteostat_id1=None, meteostat_id2=None):
    observed = {}

    # Meteostat Station 1
    try:
        if meteostat_id1:
            df_meteo = fetch_meteostat_data(site_name, site_folder, lat, lon, start_date, end_date, station_ids=[meteostat_id1])
            df1 = df_meteo.get("meteostat1")
            if df1 is not None and not df1.empty:
                observed["meteostat1"] = {"data": df1, "station_id": meteostat_id1}
            else:
                print(f"[⚠️] Données Meteostat station1 ({meteostat_id1}) absentes.")
    except Exception as e:
        print(f"[⚠️] Erreur Meteostat 1 : {e}")

    # Meteostat Station 2
    try:
        if meteostat_id2:
            df_meteo = fetch_meteostat_data(site_name, site_folder, lat, lon, start_date, end_date, station_ids=[meteostat_id2])
            df2 = df_meteo.get("meteostat1")  # Le fichier sera nommé meteostat1 si appelé seul
            if df2 is not None and not df2.empty:
                observed["meteostat2"] = {"data": df2, "station_id": meteostat_id2}
            else:
                print(f"[⚠️] Données Meteostat station2 ({meteostat_id2}) absentes.")
    except Exception as e:
        print(f"[⚠️] Erreur Meteostat 2 : {e}")

    return observed


def fetch_model_source(site_info, site_name, site_folder, lat, lon, start_date, end_date):
    model = {}

    # OpenMeteo
    try:
        openmeteo_result = save_openmeteo_data(site_name, site_folder, lat, lon, start_date, end_date)
        if openmeteo_result and "data" in openmeteo_result:
            model["openmeteo"] = openmeteo_result
        else:
            print("[⚠️] Aucune donnée OpenMeteo récupérée.")
    except Exception as e:
        print(f"[⚠️] Erreur OpenMeteo : {e}")

    # NASA POWER
    try:
        df_nasa = fetch_nasa_power_data(lat, lon, start_date, end_date)
        if df_nasa is not None and not df_nasa.empty:
            model["nasa_power"] = {"data": df_nasa}
        else:
            print("[⚠️] Données vides pour NASA POWER")
    except Exception as e:
        print(f"[⚠️] Erreur NASA POWER : {e}")

    # ERA5
    try:
        era5_result = save_era5_data(site_name, site_folder, lat, lon, start_date, end_date)
        if era5_result and os.path.exists(era5_result["filepath"]):
            df_era5 = pd.read_csv(era5_result["filepath"])
            df_era5_daily = pd.read_csv(era5_result["filepath_daily"])
            model["era5"] = {"data": df_era5, "daily": df_era5_daily}
        else:
            print("[⚠️] Données vides ou fichier manquant pour ERA5")
    except Exception as e:
        print(f"[⚠️] Erreur ERA5 : {e}")

    return model
