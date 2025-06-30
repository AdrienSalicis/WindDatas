import os
import time
import pandas as pd
from geopy.distance import geodesic

# 🔧 Modules internes du projet
from modules.utils import load_sites_from_csv
from modules.meteostat_fetcher import get_nearest_stations_info
from modules.source_manager import fetch_observed_sources, fetch_model_source
from modules.comparator import generate_comparison_report
from modules.graphics import plot_wind_direction_distribution
from modules.word_generator import create_word_report_by_country
from modules.globe_visualizer import visualize_sites_plotly
from modules.tkinter_ui import get_date_range_from_user
from modules.station_profiler import generate_station_csv, generate_station_docx

# 🌐 Sources spécifiques
from modules.noaa_station_finder import load_isd_stations, find_nearest_isd_stations
from modules.noaa_isd_fetcher import fetch_isd_series
from modules.meteo_france_station_finder import get_mf_stations_list, find_closest_mf_station
from modules.meteo_france_fetcher import fetch_meteo_france_data

from modules.globe_visualizer import visualize_sites_plotly
from modules.globe_visualizer_pydeck import visualize_sites_pydeck

from modules.report_generator import generate_site_report

import papermill as pm

  
def export_site_data(site_data, site_folder):
    os.makedirs(site_folder, exist_ok=True)
    paths = []

    for key, df in site_data["data"].items():
        if df is not None and not df.empty:
            filename = f"{key}_{site_data['name']}.csv"
            filepath = os.path.join(site_folder, filename)
            df.to_csv(filepath, index=False)
            print(f"[✅] Fichier généré : {filepath}")
            paths.append(filepath)

            if "noaa_station" in key:
                raw_path = os.path.join(site_folder, f"raw_{filename}")
                if hasattr(df, "_raw") and isinstance(df._raw, pd.DataFrame):
                    df._raw.to_csv(raw_path, index=False)
                    print(f"[🧪] CSV brut NOAA ISD sauvegardé : {raw_path}")
        else:
            print(f"[⚠️] Données vides ou absentes pour {key} – fichier non généré.")
    site_data["files"] = paths

def main():
    print("[📁] Répertoire de travail actuel :", os.getcwd())
    print("[🌍] Chargement des sites depuis modele_sites.csv...")
    sites = load_sites_from_csv("modele_sites.csv")
    start, end = get_date_range_from_user()
    if not start or not end:
        print("[❌] Dates non valides. Fin du script.")
        return

    isd_df = load_isd_stations("data/isd-history.csv")
    all_sites_data = []

    for site in sites:
        name = site['name']
        country = site['country']
        lat = float(site['latitude'])
        lon = float(site['longitude'])

        print(f"\n📌 Traitement du site : {name} ({country})")

        site_ref = f"{site['reference']}_{name}"
        site_folder = os.path.join("data", site_ref)
        os.makedirs(site_folder, exist_ok=True)

        stations = get_nearest_stations_info(lat, lon)
        station1 = stations["station1"]
        station2 = stations["station2"]

        noaa_candidates = find_nearest_isd_stations(lat, lon, isd_df)
        noaa_station1 = next((s for s in noaa_candidates if s["file_available"]), None)
        noaa_station2 = next((s for s in noaa_candidates[1:] if s["file_available"]), None)

        noaa_data = {}
        for i, station in enumerate([noaa_station1, noaa_station2], 1):
            if station:
                try:
                    filename = f"noaa_station{i}_{name}.csv"
                    filepath = os.path.join(site_folder, filename)
                    if os.path.exists(filepath):
                        print(f"[⏩] Fichier déjà existant – lecture directe : {filepath}")
                        df = pd.read_csv(filepath)
                    else:
                        df = fetch_isd_series(
                            site_name=name,
                            usaf=station["usaf"],
                            wban=station["wban"],
                            years=list(range(int(start[:4]), int(end[:4]) + 1)),
                            output_dir=site_folder,
                            verbose=True,
                            return_raw=True,
                            station_rank=i
                        )
                    noaa_data[f"noaa_station{i}"] = df
                except Exception as e:
                    print(f"[⚠️] Erreur NOAA station {i} : {e}")

        # meteo_france_data = None
        # if country.upper() in ["FR", "FRANCE"]:
        #     try:
        #         stations_df = get_mf_stations_list()
        #         station_mf = find_closest_mf_station(lat, lon, stations_df)
        #         mf_id = station_mf["id"]
        #         path_mf = fetch_meteo_france_data(mf_id, start, end, name)
        #         df_mf = pd.read_csv(path_mf) if path_mf else None
        #         meteo_france_data = df_mf
        #     except Exception as e:
        #         print(f"[⚠️] Erreur récupération MeteoFrance : {e}")

        try:
            observed = fetch_observed_sources(
                site_info=site,
                site_name=name,
                site_folder=site_folder,
                lat=lat,
                lon=lon,
                start_date=start,
                end_date=end,
                meteostat_id1=station1["id"],
                meteostat_id2=station2["id"]
            )
        except Exception as e:
            print(f"[⚠️] Erreur récupération sources observées : {e}")
            observed = {}

        # if meteo_france_data is not None:
        #     observed["meteofrance"] = {"data": meteo_france_data, "station_id": mf_id}

        try:
            model = fetch_model_source(
                site_info=site,
                site_name=name,
                site_folder=site_folder,
                lat=lat,
                lon=lon,
                start_date=start,
                end_date=end,
                openmeteo_model=None,               # ➜ paramètre modèle (ECMWF IFS etc.)
                gust_correction_factor=None         # ➜ paramètre facteur correctif (commenté si inutilisé)
            )
        except Exception as e:
            print(f"[⚠️] Erreur récupération source modélisée : {e}")
            model = {}

        site_data = {
            "name": name,
            "country": country,
            "latitude": lat,
            "longitude": lon,
            "start": start,
            "end": end,
            "reference": site['reference'],
            "meteostat1": station1,
            "meteostat2": station2,
            "noaa1": noaa_station1,
            "noaa2": noaa_station2,
            "data": {
                "meteostat1": observed.get("meteostat1", {}).get("data"),
                "meteostat2": observed.get("meteostat2", {}).get("data"),
                # "meteofrance": observed.get("meteofrance", {}).get("data"),
                "noaa_station1": noaa_data.get("noaa_station1"),
                "noaa_station2": noaa_data.get("noaa_station2"),
                "openmeteo": model.get("openmeteo", {}).get("data"),
                "nasa_power": model.get("nasa_power", {}).get("data"),
                "era5": model.get("era5", {}).get("data")
            }
        }

        export_site_data(site_data, site_folder)

        try:
            print(f"[⚡] Exécution notebook automatique pour {site_ref}")
            pm.execute_notebook(
                'notebooks/notebook_auto.ipynb',
                f'data/{site_ref}/notebook_executed.ipynb',
                parameters={"site_ref": site_ref}
            )
        except Exception as e:
            print(f"[⚠️] Erreur Papermill pour {site_ref} : {e}")

        all_sites_data.append(site_data)
        generate_site_report(site_data, output_folder="data")

    create_word_report_by_country(all_sites_data, "data/Rapport_WindDatas.docx")
    visualize_sites_plotly(all_sites_data, "visualisation_plotly.html")
    visualize_sites_pydeck(all_sites_data, "visualisation_pydeck.html")
    generate_station_csv(all_sites_data)
    generate_station_docx(all_sites_data)
    generate_comparison_report(all_sites_data)
    plot_wind_direction_distribution(all_sites_data)

if __name__ == "__main__":
    main()
