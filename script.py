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
from modules.globe_visualizer import visualize_sites_on_globe
from modules.tkinter_ui import get_date_range_from_user
from modules.station_profiler import generate_station_csv, generate_station_docx

# 🌐 Sources spécifiques
from modules.noaa_station_finder import load_isd_stations, find_nearest_isd_stations
from modules.noaa_isd_fetcher import fetch_isd_series
from modules.meteo_france_station_finder import find_nearest_mf_station
from modules.meteo_france_fetcher import fetch_meteofrance_data


def export_site_data(site_data, site_folder):
    """💾 Sauvegarde tous les fichiers CSV des sources disponibles pour un site."""
    os.makedirs(site_folder, exist_ok=True)
    paths = []

    for key, df in site_data["data"].items():
        if df is not None and not df.empty:
            filename = f"{key}_{site_data['name']}.csv"
            filepath = os.path.join(site_folder, filename)
            df.to_csv(filepath, index=False)
            print(f"[✅] Fichier généré : {filepath}")
            paths.append(filepath)

            # ⚠️ Si NOAA, on sauvegarde aussi la version brute si disponible
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

    # 📄 Chargement des sites à traiter
    print("[🌍] Chargement des sites depuis modele_sites.csv...")
    sites = load_sites_from_csv("modele_sites.csv")

    # 📆 Période d’étude définie par l’utilisateur
    start, end = get_date_range_from_user()
    if not start or not end:
        print("[❌] Dates non valides. Fin du script.")
        return

    # 📂 Chargement de la base de stations NOAA ISD
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

        # 🔎 1. Récupération des stations METEOSTAT
        stations = get_nearest_stations_info(lat, lon)
        station1 = stations["station1"]
        station2 = stations["station2"]

        # 🌐 2. Recherche des 2 stations NOAA ISD les plus proches
        noaa_candidates = find_nearest_isd_stations(lat, lon, isd_df)
        noaa_station1 = next((s for s in noaa_candidates if s["file_available"]), None)
        noaa_station2 = next((s for s in noaa_candidates[1:] if s["file_available"]), None)

        noaa_data = {}
        for i, station in enumerate([noaa_station1, noaa_station2], 1):
            if station:
                df = fetch_isd_series(
                    site_name=name,
                    usaf=station["usaf"],
                    wban=station["wban"],
                    years=list(range(int(start[:4]), int(end[:4]) + 1)),
                    output_dir=site_folder,
                    verbose=True,
                    return_raw=True
                )
                noaa_data[f"noaa_station{i}"] = df

        # 🇫🇷 3. Récupération MeteoFrance (si site en France)
        meteo_france_data = None
        if country.upper() in ["FR", "FRANCE"]:
            station_mf = find_nearest_mf_station(lat, lon)
            meteo_france_data = fetch_meteofrance_data(
                station_id=station_mf["id"],
                site_name=name,
                output_dir=site_folder,
                start_date=start,
                end_date=end
            )

        # 📊 4. Données observées – fusion METEOSTAT + MF
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

        if meteo_france_data is not None:
            observed["meteofrance"] = {"data": meteo_france_data, "station_id": station_mf["id"]}

        # 📡 5. Données modélisées – OpenMeteo, NASA Power, ERA5
        model = fetch_model_source(
            site_info=site,
            site_name=name,
            site_folder=site_folder,
            lat=lat,
            lon=lon,
            start_date=start,
            end_date=end
        )

        # 🧩 Fusion finale
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
                "meteofrance": observed.get("meteofrance", {}).get("data") if "meteofrance" in observed else None,
                "noaa_station1": noaa_data.get("noaa_station1"),
                "noaa_station2": noaa_data.get("noaa_station2"),
                "openmeteo": model.get("openmeteo", {}).get("data"),
                "nasa_power": model.get("nasa_power", {}).get("data"),
                "era5": model.get("era5", {}).get("data"),
                "era5_singlelevels": model.get("era5_singlelevels", {}).get("data")
            }
        }

        # 💾 Sauvegarde CSV + bruts
        export_site_data(site_data, site_folder)

        # 📑 Génération des fiches stations
        station_data = generate_station_csv(name, site_data, station1, station2, noaa_station1, noaa_station2)
        generate_station_docx(name, station_data, os.path.join(site_folder, f"stations_{name}.docx"))

        # 📈 Rapport comparatif
        files_dict = {k: f for k in site_data["files"] for key in site_data["data"] if key in f}
        if len(files_dict) >= 2:
            generate_comparison_report(name, site_folder, files_dict)
        else:
            print("[⚠️] Pas assez de données pour une comparaison.")

        # 🌪 Radar de directions moyennes
        radar = plot_wind_direction_distribution(
            site_name=name,
            output_path=site_folder,
            **site_data["data"]
        )
        if radar:
            site_data['files'].append(radar)

        all_sites_data.append(site_data)

        #print("[⏳] Pause de 30 secondes avant le prochain site.")
        #time.sleep(30)

    # 📘 Rapport final par pays
    print("\n📘 Génération du rapport Word par pays.")
    create_word_report_by_country(all_sites_data, "data/rapport_meteo.docx")

    # 🌍 Visualisation interactive
    print("\n🌍 Génération de la visualisation interactive.")
    output_html = "data/visualisation_globe.html"
    visualize_sites_on_globe(all_sites_data, output_html)
    print(f"✅ Visualisation disponible ici : {output_html}")

    print("\n🎉 Script terminé avec succès !")


if __name__ == "__main__":
    main()
