import requests
import pandas as pd
import os
from datetime import datetime, timedelta

def create_empty_period(start_str, end_str):
    if isinstance(start_str, datetime):
        start_str = start_str.strftime("%Y-%m-%d")
    if isinstance(end_str, datetime):
        end_str = end_str.strftime("%Y-%m-%d")

    start_date = datetime.strptime(start_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_str, "%Y-%m-%d")

    dates = pd.date_range(start=start_date, end=end_date)
    df_empty = pd.DataFrame({
        'date': dates,
        'windspeed_mean': [float('nan')] * len(dates),
        'windspeed_gust': [float('nan')] * len(dates),
        'wind_direction': [float('nan')] * len(dates),
        'u_component_10m': [float('nan')] * len(dates),
        'v_component_10m': [float('nan')] * len(dates),
    })
    return df_empty

def fetch_nasa_power_data(site_name, site_folder, lat, lon, start_date, end_date):
    os.makedirs(site_folder, exist_ok=True)

    NASA_POWER_START_DATE = datetime(1981, 1, 1)
    start_dt = datetime.strptime(start_date, "%Y-%m-%d") if isinstance(start_date, str) else start_date
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") if isinstance(end_date, str) else end_date

    if start_dt < NASA_POWER_START_DATE:
        print("[⚠️] Début d'étude avant 1981, ajout de valeurs vides.")
        cutoff_date_str = (NASA_POWER_START_DATE - timedelta(days=1)).strftime("%Y-%m-%d")
        df_empty = create_empty_period(start_dt.strftime("%Y-%m-%d"), cutoff_date_str)
        start_date_real = NASA_POWER_START_DATE.strftime("%Y-%m-%d")
    else:
        df_empty = None
        start_date_real = start_dt.strftime("%Y-%m-%d")

    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point?"
        f"parameters=WS10M,WD10M,U10M,V10M&community=RE&longitude={lon}&latitude={lat}"
        f"&start={start_date_real.replace('-', '')}&end={end_dt.strftime('%Y%m%d')}&format=JSON"
    )

    print(f"[📡] Appel API NASA POWER pour {site_name}...")

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Erreur API NASA POWER : {response.status_code} - {response.text}")

    data = response.json()
    param = data['properties']['parameter']

    df = pd.DataFrame({
        'date': list(param['WS10M'].keys()),
        'windspeed_mean': list(param['WS10M'].values()),
        'windspeed_gust': list(param['GWS10M'].values()) if 'GWS10M' in param else [float('nan')] * len(param['WS10M']),
        'wind_direction': list(param['WD10M'].values()),
        'u_component_10m': list(param['U10M'].values()),
        'v_component_10m': list(param['V10M'].values())
    })

    df['date'] = pd.to_datetime(df['date'])

    if df_empty is not None:
        df = pd.concat([df_empty, df], ignore_index=True)

    output_path = os.path.join(site_folder, f"power_{site_name}.csv")
    df.to_csv(output_path, index=False)

    print(f"[✅] Données NASA POWER enregistrées : {output_path}")

    return {
        'filename': os.path.basename(output_path),
        'filepath': output_path,
        'latitude': lat,
        'longitude': lon
    }
