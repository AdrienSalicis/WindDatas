import os
import pandas as pd
import requests
from tqdm import tqdm

def fetch_isd_series(usaf, wban, years, output_dir, site_name="site", verbose=False, return_raw=False):
    base_url = "https://www.ncei.noaa.gov/data/global-hourly/access"
    all_data = []
    raw_concat = []

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

        # Vérifier que les colonnes essentielles sont là
        if 'DATE' not in df.columns or 'WND' not in df.columns:
            if verbose:
                print(f"[⚠️] Colonnes 'DATE' ou 'WND' manquantes pour {usaf}-{wban} en {year}")
            continue

        df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
        df = df.dropna(subset=['DATE'])
        df['date'] = df['DATE'].dt.date

        # Décomposition du champ WND (direction, vitesse, code qualité, rafale, etc.)
        parsed = df['WND'].str.split(',', expand=True)
        df['wind_dir'] = pd.to_numeric(parsed[0], errors='coerce')
        df['wind_speed'] = pd.to_numeric(parsed[3], errors='coerce') / 10  # knots → m/s
        df['wind_speed'] = df['wind_speed'].mask(df['wind_speed'] > 100)

        # Rafales
        if 'GUST' in df.columns:
            df['gust'] = pd.to_numeric(df['GUST'], errors='coerce') / 10
            df['gust'] = df['gust'].mask(df['gust'] > 150)
        else:
            df['gust'] = pd.NA
            if verbose:
                print(f"[⚠️] Colonne GUST absente pour {year}")

        # Direction du vent (si DRCT absent, on peut utiliser wind_dir de WND)
        if 'DRCT' in df.columns:
            df['wind_direction'] = pd.to_numeric(df['DRCT'], errors='coerce')
            df['wind_direction'] = df['wind_direction'].mask((df['wind_direction'] > 360) | (df['wind_direction'] < 0))
        else:
            df['wind_direction'] = df['wind_dir']
            if verbose:
                print(f"[⚠️] Colonne DRCT absente, utilisation de wind_dir issue de WND")

        raw_concat.append(df.copy())

        all_data.append(df[['date', 'wind_speed', 'gust', 'wind_direction']])

    if not all_data:
        print(f"[⚠️] Aucune donnée récupérée pour la station {usaf}-{wban}.")
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
        print(f"\n✅ Données NOAA ISD agrégées sauvegardées pour {site_name} → {output_path}")

    # Ajout de l’attribut _raw pour traçabilité si demandé
    if return_raw:
        agg_df._raw = pd.concat(raw_concat, ignore_index=True)

    return agg_df
