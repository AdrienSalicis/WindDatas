import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO
from tqdm import tqdm

def fetch_noaa_hourly_data(usaf, wban, start_date, end_date, verbose=True):
    """
    Télécharge les données horaires NOAA pour une station (USAF-WBAN) via l'API ADS
    Agrège par jour pour extraire :
    - vent moyen journalier maximal (windspeed_mean)
    - rafale maximale (windspeed_gust)
    - direction dominante (winddirection_mean)
    """
    station_id = f"{usaf}-{wban}"
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    all_data = []

    for year in tqdm(range(start_dt.year, end_dt.year + 1), desc=f"Fetching NOAA {station_id}", disable=not verbose):
        year_start = max(start_dt, datetime(year, 1, 1))
        year_end = min(end_dt, datetime(year, 12, 31))

        url = (
            f"https://www.ncei.noaa.gov/access/services/data/v1?"
            f"dataset=global-hourly&stations={station_id}&startDate={year_start.strftime('%Y-%m-%d')}"
            f"&endDate={year_end.strftime('%Y-%m-%d')}&format=csv&dataTypes=WND"
        )

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            df = pd.read_csv(StringIO(response.text))

            if "WND" not in df.columns:
                if verbose:
                    print(f"[⚠️] Données manquantes pour {year}")
                continue

            df['DATE'] = pd.to_datetime(df['DATE']).dt.date
            df = df.dropna(subset=['WND'])

            # Parsing du champ WND : direction, speed, flag, gust, gust flag
            parsed = df['WND'].str.split(',', expand=True)
            df['wind_dir'] = pd.to_numeric(parsed[0], errors='coerce')
            df['wind_speed'] = pd.to_numeric(parsed[1], errors='coerce')
            df['wind_gust'] = pd.to_numeric(parsed[3], errors='coerce')

            # Filtrage des valeurs impossibles
            df = df[(df['wind_speed'] < 999.9) & (df['wind_dir'] <= 360)]

            daily = df.groupby('DATE').agg({
                'wind_speed': 'max',
                'wind_gust': 'max',
                'wind_dir': lambda x: x.mode().iloc[0] if not x.mode().empty else None
            }).reset_index()

            daily.rename(columns={
                'DATE': 'time',
                'wind_speed': 'windspeed_mean',
                'wind_gust': 'windspeed_gust',
                'wind_dir': 'winddirection_mean'
            }, inplace=True)

            all_data.append(daily)

        except Exception as e:
            if verbose:
                print(f"[❌] Erreur pour {station_id} {year} : {e}")

    if not all_data:
        return pd.DataFrame(columns=['time', 'windspeed_mean', 'windspeed_gust', 'winddirection_mean'])

    full_df = pd.concat(all_data).drop_duplicates(subset='time').sort_values('time')
    return full_df


def save_noaa_data_for_site(site_name, usaf, wban, start_date, end_date, index, output_dir="data", verbose=True):
    df = fetch_noaa_hourly_data(usaf, wban, start_date, end_date, verbose=verbose)

    site_folder = os.path.join(output_dir, site_name)
    os.makedirs(site_folder, exist_ok=True)
    output_path = os.path.join(site_folder, f"noaa_station{index}_{site_name}.csv")

    df.to_csv(output_path, index=False)
    if verbose:
        print(f"[✅] Données NOAA station{index} sauvegardées : {output_path}")

    return output_path
