# source_manager.py
# Centralise la récupération des données météo pour un site donné (observées et modélisées)

import os
from modules.meteostat_fetcher import fetch_meteostat_data
from modules.noaa_isd_fetcher import fetch_noaa_isd_data
from modules.openmeteo_fetcher import fetch_openmeteo_data
from modules.era5_fetcher import fetch_era5_data
from modules.nasa_power_fetcher import fetch_nasa_power_data
from modules.meteo_france_fetcher import fetch_meteo_france_data

def fetch_observed_sources(site_data: dict) -> dict:
    """
    Récupère les données observées (stations) : Meteostat, NOAA ISD, Météo-France
    """
    observed = {}

    name = site_data["name"]
    lat = site_data["latitude"]
    lon = site_data["longitude"]
    start = site_data["start"]
    end = site_data["end"]

    print(f"[📡] Téléchargement Meteostat pour station : {site_data['meteostat1']}")
    observed["meteostat1"] = fetch_meteostat_data(site_data['meteostat1'], name, start, end, station_index=1)

    print(f"[📡] Téléchargement Meteostat pour station : {site_data['meteostat2']}")
    observed["meteostat2"] = fetch_meteostat_data(site_data['meteostat2'], name, start, end, station_index=2)

    print(f"[📡] Téléchargement NOAA ISD pour {name}")
    observed["noaa_isd"] = fetch_noaa_isd_data(lat, lon, name, start, end)

    print(f"[📡] Téléchargement Météo-France pour {name}")
    observed["meteo_france"] = fetch_meteo_france_data(lat, lon, name, start, end)

    return observed


def fetch_model_source(site_data: dict) -> dict:
    """
    Récupère les données modélisées : ERA5, OpenMeteo, NASA POWER
    """
    model = {}

    name = site_data["name"]
    lat = site_data["latitude"]
    lon = site_data["longitude"]
    start = site_data["start"]
    end = site_data["end"]

    print(f"[📡] Téléchargement OpenMeteo pour {name}")
    model["openmeteo"] = fetch_openmeteo_data(lat, lon, name, start, end)

    print(f"[📡] Téléchargement NASA POWER pour {name}")
    model["nasa_power"] = fetch_nasa_power_data(lat, lon, name, start, end)

    print(f"[📡] Téléchargement ERA5 (Timeseries CSV compressé) pour {name}")
    model["era5"] = fetch_era5_data(lat, lon, name, start, end)

    return model
