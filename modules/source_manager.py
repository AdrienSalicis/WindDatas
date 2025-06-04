import os
import pandas as pd
from .meteostat_fetcher import fetch_meteostat_data
from .openmeteo_fetcher import fetch_openmeteo_data
from .nasa_power_fetcher import fetch_nasa_power_data
from .era5_fetcher import save_era5_data
from .source_strategy import determine_sources
#from .era5_fetcher_singlelevels import save_era5_singlelevels_data


def fetch_observed_sources(site_info, site_name, site_folder, lat, lon, start_date, end_date,
                           meteostat_id1=None, meteostat_id2=None, noaa_id=None):
    print(f"[📥] Récupération des données observées...")
    sources = determine_sources(site_info)
    observed_data = {}

    if "meteostat" in sources["observed"]:
        station_ids = [meteostat_id1, meteostat_id2] if meteostat_id1 and meteostat_id2 else None
        files_exist = True
        paths = []

        for i, station_id in enumerate(station_ids or [], 1):
            filename = f"meteostat{i}_{site_name}.csv"
            path = os.path.join(site_folder, filename)
            if not os.path.exists(path):
                files_exist = False
            paths.append(path)

        if files_exist:
            print("[📂] Données Meteostat déjà présentes, chargement des fichiers...")
            for i, path in enumerate(paths, 1):
                df = pd.read_csv(path)
                observed_data[f"meteostat{i}"] = {"data": df, "station_id": station_ids[i-1]}
        else:
            meteostat_all = fetch_meteostat_data(
                site_name=site_name,
                site_folder=site_folder,
                lat=lat,
                lon=lon,
                start_date=start_date,
                end_date=end_date,
                station_ids=station_ids
            )
            observed_data["meteostat1"] = {
                "data": meteostat_all.get("meteostat1"),
                "station_id": meteostat_id1
            }
            observed_data["meteostat2"] = {
                "data": meteostat_all.get("meteostat2"),
                "station_id": meteostat_id2
            }

    return observed_data

def fetch_model_source(site_info, site_name, site_folder, lat, lon, start_date, end_date, api_keys=None):
    print(f"[🧠] Récupération des données modélisées...")
    sources = determine_sources(site_info)
    model_data = {}

    for source in sources["modeled"]:
        if source == "openmeteo":
            filename = f"openmeteo_{site_name}.csv"
            path = os.path.join(site_folder, filename)
            if os.path.exists(path):
                print("[📂] Données OpenMeteo déjà présentes, chargement...")
                df = pd.read_csv(path)
                model_data["openmeteo"] = {"data": df, "filepath": path}
            else:
                try:
                    df = fetch_openmeteo_data(lat, lon, start_date, end_date)
                    df.to_csv(path, index=False)
                    print(f"[✅] Données OpenMeteo enregistrées : {path}")
                    model_data["openmeteo"] = {"data": df, "filepath": path}
                except Exception as e:
                    print(f"[❌] Erreur récupération OpenMeteo : {e}")

        #elif source == "visualcrossing":
        #    filename = f"visualcrossing_{site_name}.csv"
        #    path = os.path.join(site_folder, filename)
        #    if os.path.exists(path):
        #        print("[📂] Données Visual Crossing déjà présentes, chargement...")
        #        df = pd.read_csv(path)
        #        model_data["visualcrossing"] = {"data": df, "filepath": path}
        #    else:
        #        try:
        #           from .visualcrossing_fetcher import fetch_visualcrossing_data
        #            result = fetch_visualcrossing_data(site_name, site_folder, lat, lon, start_date, end_date, api_keys["visualcrossing"])
        #            df = pd.read_csv(result["filepath"])
        #            model_data["visualcrossing"] = {"data": df, "filepath": result["filepath"]}
        #        except Exception as e:
        #            print(f"[❌] Erreur récupération Visual Crossing : {e}")


        elif source == "nasa_power":
            filename = f"power_{site_name}.csv"
            path = os.path.join(site_folder, filename)
            if os.path.exists(path):
                print("[📂] Données NASA POWER déjà présentes, chargement...")
                df = pd.read_csv(path)
                model_data["nasa_power"] = {"data": df, "filepath": path}
            else:
                try:
                    result = fetch_nasa_power_data(site_name, site_folder, lat, lon, start_date, end_date)
                    df = pd.read_csv(result["filepath"])
                    model_data["nasa_power"] = {"data": df, "filepath": result["filepath"]}
                except Exception as e:
                    print(f"[❌] Erreur récupération NASA POWER : {e}")


        elif source == "era5":
            print(f"[🧪] Tentative ERA5 avec : {site_name}, {start_date} → {end_date}")
            filename = f"era5_daily_{site_name}.csv"
            path = os.path.join(site_folder, filename)
            if os.path.exists(path):
                print("[📂] Données ERA5 (daily) déjà présentes, chargement...")
                df = pd.read_csv(path)
                model_data["era5"] = {"data": df, "filepath": path}
            else:
                try:
                    result = save_era5_data(site_name, site_folder, lat, lon, start_date, end_date)
                    if result and os.path.exists(result["filepath_daily"]):
                        df = pd.read_csv(result["filepath_daily"])
                        model_data["era5"] = {"data": df, "filepath": result["filepath_daily"]}
                except Exception as e:
                    print(f"[❌] Erreur récupération ERA5 : {e}")

            #try:
            #    result_single = save_era5_singlelevels_data(site_name, site_folder, lat, lon, start_date, end_date)
            #    if result_single and os.path.exists(result_single["daily_csv"]):
            #        df = pd.read_csv(result_single["daily_csv"])
            #        model_data["era5_singlelevels"] = {"data": df, "filepath": result_single["daily_csv"]}
            #except Exception as e:
            #    print(f"[❌] Erreur récupération ERA5 single-levels : {e}")



    return model_data
