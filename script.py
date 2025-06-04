import os
import time
import pandas as pd
from geopy.distance import geodesic

from modules.utils import load_sites_from_csv
from modules.meteostat_fetcher import get_nearest_stations_info
from modules.source_manager import fetch_observed_sources, fetch_model_source
from modules.comparator import generate_comparison_report
from modules.graphics import plot_wind_direction_distribution
from modules.word_generator import create_word_report_by_country
from modules.globe_visualizer import visualize_sites_on_globe
from modules.tkinter_ui import get_date_range_from_user
from modules.source_strategy import determine_sources
from modules.graphics import plot_wind_direction_distribution

import cdsapi
VC_API_KEY = "EZFV5ZCLVYJBJNRKFNW2U8BCU"

try:
    print("[🧪] Vérification CDSAPI dans script.py (avec clé explicite)...")
    c = cdsapi.Client(
        url="https://cds.climate.copernicus.eu/api",
        key="3ede72e1-0636-4ad5-99ee-723311047e81"
    )
    print("[✅] Client CDSAPI initialisé correctement.")
except Exception as e:
    print(f"[❌] Erreur d'initialisation CDSAPI dans script.py : {e}")


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

        observed = fetch_observed_sources(
            site_info=site,
            site_name=name,
            site_folder=site_folder,
            lat=lat,
            lon=lon,
            start_date=start,
            end_date=end,
            meteostat_id1=station1["id"],
            meteostat_id2=station2["id"],
        )

        model = fetch_model_source(
            site_info=site,
            site_name=name,
            site_folder=site_folder,
            lat=lat,
            lon=lon,
            start_date=start,
            end_date=end,
            api_keys={"visualcrossing": VC_API_KEY}
        )

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
            "data": {
                "meteostat1": observed.get("meteostat1", {}).get("data"),
                "meteostat2": observed.get("meteostat2", {}).get("data"),
                "openmeteo": model.get("openmeteo", {}).get("data"),
                "nasa_power": model.get("nasa_power", {}).get("data"),
                "era5": model.get("era5", {}).get("data"),
                "era5_singlelevels": model.get("era5_singlelevels", {}).get("data")
                # "visualcrossing": model.get("visualcrossing", {}).get("data")  # désactivé pour l'instant

            }
        }

        export_site_data(site_data, site_folder)

        print("\n📝 Comparaison des jeux de données...")

        def find_file(files, key):
            matches = [f for f in files if key in f]
            return matches[0] if matches else None

        files_dict = {
            'meteostat1': find_file(site_data['files'], 'meteostat1'),
            'meteostat2': find_file(site_data['files'], 'meteostat2'),
            'openmeteo': find_file(site_data['files'], 'openmeteo'),
            'nasa_power': find_file(site_data['files'], 'power'),
            'era5': find_file(site_data['files'], 'era5'),
            'era5_singlelevels': find_file(site_data['files'], 'era5_singlelevels')
        }

        files_dict = {k: v for k, v in files_dict.items() if v is not None}

        if len(files_dict) < 2:
            print("[⚠️] Pas assez de données pour comparer – passage au site suivant.")
        else:
            comparison_report = generate_comparison_report(name, site_folder, files_dict)

        distribution_path = plot_wind_direction_distribution(
            site_name=name,
            output_path=site_folder,
            meteostat1=site_data["data"].get("meteostat1"),
            openmeteo=site_data["data"].get("openmeteo"),
            nasa_power=site_data["data"].get("nasa_power"),
            era5=site_data["data"].get("era5"),
            era5_singlelevels=site_data["data"].get("era5_singlelevels")
        )

        if distribution_path:
            site_data['files'].append(distribution_path)

        all_sites_data.append(site_data)

        print("[⏳] Pause de 30 secondes avant le site suivant (OpenMeteo)...")
        time.sleep(30)

    print("\n📝 Génération du rapport Word par pays...")
    create_word_report_by_country(all_sites_data, "data/rapport_meteo.docx")

    print("\n🌐 Génération de la visualisation interactive...")
    output_html = "data/visualisation_globe.html"
    visualize_sites_on_globe(all_sites_data, output_html)
    print(f"✅ Visualisation disponible ici : {output_html}")

    print("\n✅ Script terminé avec succès !")

if __name__ == "__main__":
    main()