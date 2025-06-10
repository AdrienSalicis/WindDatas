import os
import time
import pandas as pd
from geopy.distance import geodesic

# Modules internes
from modules.utils import load_sites_from_csv
from modules.meteostat_fetcher import get_nearest_stations_info
from modules.source_manager import fetch_observed_sources, fetch_model_source
from modules.comparator import generate_comparison_report
from modules.graphics import plot_wind_direction_distribution
from modules.word_generator import create_word_report_by_country
from modules.globe_visualizer import visualize_sites_on_globe
from modules.tkinter_ui import get_date_range_from_user
from modules.source_strategy import determine_sources
from modules.station_profiler import generate_station_csv, generate_station_docx

# NOAA – ajout
from modules.noaa_station_finder import load_isd_stations, find_nearest_isd_stations
from modules.noaa_isd_fetcher import fetch_isd_series

# Vérification client CDSAPI
import cdsapi
try:
    print("Vérification CDSAPI dans script.py...")
    c = cdsapi.Client(
        url="https://cds.climate.copernicus.eu/api",
        key="3ede72e1-0636-4ad5-99ee-723311047e81"
    )
    print("[✅] Client CDSAPI initialisé correctement.")
except Exception as e:
    print(f"[❌] Erreur d'initialisation CDSAPI : {e}")


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

            # Export CSV brut pour NOAA ISD si présent dans les clés
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

    all_sites_data = []
    isd_csv_path = "data/isd-history.csv"
    isd_df = load_isd_stations(isd_csv_path)

    for site in sites:
        name = site['name']
        country = site['country']
        lat = float(site['latitude'])
        lon = float(site['longitude'])

        print(f"\nTraitement du site : {name} ({country})")

        site_ref = f"{site['reference']}_{name}"
        site_folder = os.path.join("data", site_ref)
        os.makedirs(site_folder, exist_ok=True)

        # Récupération des 2 stations Meteostat les plus proches
        stations = get_nearest_stations_info(lat, lon)
        station1 = stations["station1"]
        station2 = stations["station2"]

        # Données observées (Meteostat uniquement ici)
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

        # Détection des 2 stations NOAA les plus proches (dans un rayon de 80 km)
        noaa_candidates = find_nearest_isd_stations(lat, lon, isd_df)
        noaa_station1 = next((s for s in noaa_candidates if s["file_available"]), None)
        noaa_station2 = next((s for s in noaa_candidates[1:] if s["file_available"]), None)

        # Téléchargement NOAA ISD (données horaires → agrégées)
        noaa_data = {}
        for i, station in enumerate([noaa_station1, noaa_station2], 1):
            if station:
                df_noaa = fetch_isd_series(
                    site_name=name,
                    usaf=station["usaf"],
                    wban=station["wban"],
                    years=list(range(int(start[:4]), int(end[:4]) + 1)),
                    output_dir=site_folder,
                    verbose=True,
                    return_raw=True
                )
                noaa_data[f"noaa_station{i}"] = df_noaa

        # Données modélisées
        model = fetch_model_source(
            site_info=site,
            site_name=name,
            site_folder=site_folder,
            lat=lat,
            lon=lon,
            start_date=start,
            end_date=end,
            api_keys={"visualcrossing": "EZFV5ZCLVYJBJNRKFNW2U8BCU"}
        )

        # Structuration finale du jeu de données du site
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
                "noaa_station1": noaa_data.get("noaa_station1"),
                "noaa_station2": noaa_data.get("noaa_station2"),
                "openmeteo": model.get("openmeteo", {}).get("data"),
                "nasa_power": model.get("nasa_power", {}).get("data"),
                "era5": model.get("era5", {}).get("data"),
                "era5_singlelevels": model.get("era5_singlelevels", {}).get("data")
            }
        }

        # Sauvegarde des fichiers CSV
        export_site_data(site_data, site_folder)

        # Génération fiche station
        station_data = generate_station_csv(name, site_data, station1, station2, noaa_station1, noaa_station2)
        generate_station_docx(name, station_data, os.path.join(site_folder, f"stations_{name}.docx"))


        # Comparaison statistique
        print("\nComparaison des jeux de données...")
        def find_file(files, key):
            matches = [f for f in files if key in f]
            return matches[0] if matches else None

        files_dict = {
            'meteostat1': find_file(site_data['files'], 'meteostat1'),
            'meteostat2': find_file(site_data['files'], 'meteostat2'),
            'noaa_station1': find_file(site_data['files'], 'noaa_station1'),
            'noaa_station2': find_file(site_data['files'], 'noaa_station2'),
            'openmeteo': find_file(site_data['files'], 'openmeteo'),
            'nasa_power': find_file(site_data['files'], 'power'),
            'era5': find_file(site_data['files'], 'era5'),
            'era5_singlelevels': find_file(site_data['files'], 'era5_singlelevels')
        }
        files_dict = {k: v for k, v in files_dict.items() if v is not None}

        if len(files_dict) < 2:
            print("[⚠️] Pas assez de données pour comparer – passage au site suivant.")
        else:
            generate_comparison_report(name, site_folder, files_dict)

        # Graphe de distribution directionnelle
        distribution_path = plot_wind_direction_distribution(
            site_name=name,
            output_path=site_folder,
            meteostat1=site_data["data"].get("meteostat1"),
            meteostat2=site_data["data"].get("meteostat2"),
            noaa_station1=site_data["data"].get("noaa_station1"),
            noaa_station2=site_data["data"].get("noaa_station2"),
            openmeteo=site_data["data"].get("openmeteo"),
            nasa_power=site_data["data"].get("nasa_power"),
            era5=site_data["data"].get("era5"),
            era5_singlelevels=site_data["data"].get("era5_singlelevels")
        )
        if distribution_path:
            site_data['files'].append(distribution_path)

        all_sites_data.append(site_data)

        print("[⏳] Pause de 30 secondes avant le site suivant...")
        time.sleep(30)

    # Rapport Word final
    print("\nGénération du rapport Word par pays...")
    create_word_report_by_country(all_sites_data, "data/rapport_meteo.docx")

    # Carte interactive globe
    print("\nGénération de la visualisation interactive...")
    output_html = "data/visualisation_globe.html"
    visualize_sites_on_globe(all_sites_data, output_html)
    print(f"✅ Visualisation disponible ici : {output_html}")

    print("\n✅ Script terminé avec succès !")


if __name__ == "__main__":
    main()
