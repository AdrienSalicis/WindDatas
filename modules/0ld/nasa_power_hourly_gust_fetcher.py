import os
import requests
import pandas as pd
from datetime import datetime, timedelta

def create_empty_gust_period(start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date)
    return pd.DataFrame({
        'date': dates,
        'gust_10m': [float('nan')] * len(dates)
    })

def fetch_nasa_power_hourly_gust(site_name, site_folder, lat, lon, start_date, end_date):
    os.makedirs(site_folder, exist_ok=True)

    GUST_AVAILABLE_START = datetime(2001, 1, 1)
    start_dt = datetime.strptime(start_date, "%Y-%m-%d") if isinstance(start_date, str) else start_date
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") if isinstance(end_date, str) else end_date

    df_before_2001 = None
    if start_dt < GUST_AVAILABLE_START:
        print("[⚠️] Les rafales ne sont disponibles qu'à partir du 01-01-2001. Ajout de NaN avant cette date.")
        df_before_2001 = create_empty_gust_period(start_dt, GUST_AVAILABLE_START - timedelta(days=1))
        start_dt = GUST_AVAILABLE_START

    url = (
        f"https://power.larc.nasa.gov/api/temporal/hourly/point?"
        f"parameters=GWS10M&community=RE&longitude={lon}&latitude={lat}"
        f"&start={start_dt.strftime('%Y%m%d')}&end={end_dt.strftime('%Y%m%d')}&format=JSON"
    )

    print(f"[📡] Appel API NASA POWER (hourly gusts) pour {site_name}...")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erreur API NASA POWER hourly : {response.status_code} - {response.text}")

    data = response.json()
    raw_values = data['properties']['parameter']['GWS10M']

    records = []
    for key, val in raw_values.items():
        try:
            dt = datetime.strptime(key, "%Y%m%d%H")
            records.append({'datetime': dt, 'gust_10m': val})
        except Exception:
            continue

    df_hourly = pd.DataFrame(records)
    df_hourly['date'] = df_hourly['datetime'].dt.date
    df_daily = df_hourly.groupby('date')['gust_10m'].max().reset_index()
    df_daily['date'] = pd.to_datetime(df_daily['date'])

    if df_before_2001 is not None:
        df_daily = pd.concat([df_before_2001, df_daily], ignore_index=True)

    output_path = os.path.join(site_folder, f"power_gust_{site_name}.csv")
    df_daily.to_csv(output_path, index=False)

    print(f"[✅] Rafales max journalières enregistrées : {output_path}")

    return {
        'filename': os.path.basename(output_path),
        'filepath': output_path,
        'data': df_daily
    }
