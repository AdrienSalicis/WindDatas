# noaa_isd_fetcher.py
import os
import pandas as pd
import requests
from tqdm import tqdm

def fetch_isd_series(usaf, wban, years, output_dir, site_name="site", verbose=False, return_raw=False, station_rank=None):
    base_url = "https://www.ncei.noaa.gov/data/global-hourly/access"
    all_data = []
    raw_concat = []

    if station_rank:
        print(f"[📡] Téléchargement des données NOAA ISD pour station {station_rank} ({usaf}-{wban})")

    print(f"[📥] Téléchargement des fichiers NOAA {usaf}-{wban} sur {len(years)} an(s)...")
    for i, year in enumerate(tqdm(years, desc=f"{usaf}-{wban}", ncols=80), 1):
        file_url = f"{base_url}/{year}/{usaf}{wban}.csv"
        if verbose:
            print(f"  └─ {i}/{len(years)} : Téléchargement {file_url}")

        try:
            df = pd.read_csv(file_url)
        except Exception as e:
            if verbose:
                print(f"[❌] Erreur pour {usaf}-{wban} {year} : {e}")
            continue

        if 'DATE' not in df.columns or 'WND' not in df.columns:
            if verbose:
                print(f"[⚠️] Colonnes 'DATE' ou 'WND' manquantes pour {usaf}-{wban} en {year}")
            continue

        df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
        df = df.dropna(subset=['DATE'])
        df['date'] = df['DATE'].dt.date

        parsed = df['WND'].str.split(',', expand=True)
        df['wind_dir'] = pd.to_numeric(parsed[0], errors='coerce')
        df['wind_speed'] = pd.to_numeric(parsed[3], errors='coerce') / 10
        df['wind_speed'] = df['wind_speed'].mask(df['wind_speed'] > 100)

        gust_used = "GUST"
        if 'GUST' in df.columns:
            df['gust'] = pd.to_numeric(df['GUST'], errors='coerce') / 10
            df['gust'] = df['gust'].mask(df['gust'] > 150)
        else:
            df['gust'] = df.groupby('date')['wind_speed'].transform('max')
            gust_used = "WND"

        if 'DRCT' in df.columns:
            df['wind_direction'] = pd.to_numeric(df['DRCT'], errors='coerce')
        else:
            df['wind_direction'] = df['wind_dir']

        df['wind_direction'] = df['wind_direction'].mask(
            (df['wind_direction'] > 360) | (df['wind_direction'] < 0) | (df['wind_direction'] == 999)
        )

        raw_concat.append(df.copy())
        all_data.append(df[['date', 'wind_speed', 'gust', 'wind_direction']])

    if not all_data:
        print(f"[⚠️] Aucune donnée récupérée pour la station {usaf}-{wban}.")
        return None

    full_df = pd.concat(all_data, ignore_index=True)

    agg_df = full_df.groupby("date").agg({
        "wind_speed": "max",
        "gust": "max",
        "wind_direction": lambda x: x.mode().iloc[0] if not x.dropna().empty else pd.NA
    }).reset_index()

    agg_df.rename(columns={
        "wind_speed": "windspeed_mean",
        "gust": "windspeed_gust"
    }, inplace=True)

    rank = station_rank if station_rank else "X"
    final_csv = os.path.join(output_dir, f"noaa_station{rank}_{site_name}.csv")
    agg_df.to_csv(final_csv, index=False)

    if verbose:
        print(f"\n✅ NOAA ISD journalier (source={gust_used}) sauvegardé → {final_csv}")

    if return_raw:
        agg_df._raw = pd.concat(raw_concat, ignore_index=True)

    return agg_df
