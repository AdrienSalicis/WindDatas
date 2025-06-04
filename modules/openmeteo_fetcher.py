import os
import requests
import pandas as pd
from datetime import datetime

def fetch_openmeteo_data(lat, lon, start_date, end_date):
    # Daily data (gust + mean)
    url_daily = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}"
        f"&daily=windspeed_10m_max,windspeed_10m_mean&timezone=auto"
    )

    response_daily = requests.get(url_daily)
    if response_daily.status_code != 200:
        raise Exception(f"Erreur API OpenMeteo (daily) : {response_daily.status_code} - {response_daily.text}")
    
    data_daily = response_daily.json().get("daily", {})
    df_daily = pd.DataFrame(data_daily)
    df_daily["time"] = pd.to_datetime(df_daily["time"])

    df_daily = df_daily.rename(columns={
        "windspeed_10m_max": "windspeed_gust",
        "windspeed_10m_mean": "windspeed_mean"
    })

    # Hourly data (wind direction)
    url_hourly = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}"
        f"&hourly=winddirection_10m&timezone=auto"
    )

    response_hourly = requests.get(url_hourly)
    if response_hourly.status_code != 200:
        raise Exception(f"Erreur API OpenMeteo (hourly) : {response_hourly.status_code} - {response_hourly.text}")

    data_hourly = response_hourly.json().get("hourly", {})
    df_hourly = pd.DataFrame(data_hourly)
    df_hourly["time"] = pd.to_datetime(df_hourly["time"])

    # Moyenne journalière des directions horaires
    df_hourly["date"] = df_hourly["time"].dt.date
    df_dir = df_hourly.groupby("date")["winddirection_10m"].mean().reset_index()
    df_dir = df_dir.rename(columns={"date": "time", "winddirection_10m": "wind_direction"})
    df_dir["time"] = pd.to_datetime(df_dir["time"])

    # Fusion finale
    df_final = pd.merge(df_daily, df_dir, on="time", how="left")

    return df_final

def save_openmeteo_data(site_name, site_folder, lat, lon, start_date, end_date):
    df = fetch_openmeteo_data(lat, lon, start_date, end_date)

    filename = f"openmeteo_{site_name}_lat{lat:.2f}_lon{lon:.2f}.csv"
    filepath = os.path.join(site_folder, filename)
    df.to_csv(filepath, index=False)

    return {
        'filename': filename,
        'filepath': filepath,
        'latitude': lat,
        'longitude': lon
    }
