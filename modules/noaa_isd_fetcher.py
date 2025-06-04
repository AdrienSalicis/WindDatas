import os
import pandas as pd
import requests
from tqdm import tqdm
from collections import Counter

def fetch_isd_series(usaf, wban, years, output_dir, site_name="site", verbose=False):
    base_url = "https://www.ncei.noaa.gov/data/global-hourly/access"

    all_data = []

    for year in tqdm(years, desc=f"Fetching NOAA {usaf}-{wban}"):
        file_url = f"{base_url}/{year}/{usaf}{wban}.csv"
        if verbose:
            print(f"[📥] Téléchargement {file_url}")

        try:
            df = pd.read_csv(file_url)
        except Exception as e:
            if verbose:
                print(f"[❌] Erreur pour {usaf}-{wban} {year} : {e}")
            continue

        # Extraction des données utiles
        if 'DATE' not in df.columns or 'WND' not in df.columns:
            if verbose:
                print(f"[⚠️] Colonnes manquantes dans {usaf}{wban}_{year}.csv")
            continue

        df = df[['DATE', 'WND'] + [c for c in ['GUST', 'DRCT'] if c in df.columns]]

        # Traitement de la date
        df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
        df = df.dropna(subset=['DATE'])
        df['date'] = df['DATE'].dt.date

        # Décomposition et nettoyage des vents
        df['wind_speed'] = pd.to_numeric(df['WND'].str.split(',', expand=True)[3], errors='coerce') / 10
        df['wind_speed'] = df['wind_speed'].mask(df['wind_speed'] > 100)  # Valeurs aberrantes

        # Rafales
        if 'GUST' in df.columns:
            df['gust'] = pd.to_numeric(df['GUST'], errors='coerce') / 10
            df['gust'] = df['gust'].mask(df['gust'] > 150)
        else:
            df['gust'] = pd.NA

        # Direction du vent
        if 'DRCT' in df.columns:
            df['wind_direction'] = pd.to_numeric(df['DRCT'], errors='coerce')
            df['wind_direction'] = df['wind_direction'].mask((df['wind_direction'] > 360) | (df['wind_direction'] < 0))
        else:
            df['wind_direction'] = pd.NA

        all_data.append(df[['date', 'wind_speed', 'gust', 'wind_direction']])

    if not all_data:
        print(f"[⚠️] Aucune donnée récupérée pour la station.")
        return None

    full_df = pd.concat(all_data, ignore_index=True)

    # Agrégation par jour
    agg_df = full_df.groupby("date").agg({
        "wind_speed": "max",
        "gust": "max",
        "wind_direction": lambda x: x.mode().iloc[0] if not x.dropna().empty else pd.NA
    }).reset_index()

    agg_df.rename(columns={
        "wind_speed": "windspeed_mean",
        "gust": "windspeed_gust"
    }, inplace=True)

    # Export final
    os.makedirs(output_dir, exist_ok=True)
    csv_name = f"noaa_isd_{site_name}_{usaf}{wban}.csv"
    output_path = os.path.join(output_dir, csv_name)
    agg_df.to_csv(output_path, index=False)

    if verbose:
        print(f"\n✅ Données NOAA ISD récupérées avec succès pour {site_name}")
        print(agg_df.head())

    return agg_df
