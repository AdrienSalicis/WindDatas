import os
import requests
import pandas as pd
from datetime import datetime
import io


def fetch_visualcrossing_data(site_name, site_folder, lat, lon, start_date, end_date, api_key):
    os.makedirs(site_folder, exist_ok=True)

    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    all_data = []

    for year in range(start_dt.year, end_dt.year + 1):
        year_start = max(datetime(year, 1, 1), start_dt)
        year_end = min(datetime(year, 12, 31), end_dt)

        url = (
            f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
            f"{lat},{lon}/{year_start.date()}/{year_end.date()}"
            f"?unitGroup=metric"
            f"&elements=datetime,windspeed,windgust,winddir"
            f"&include=days"
            f"&key={api_key}"
            f"&contentType=csv"
        )

        print(f"[📡] Requête Visual Crossing pour {site_name} – année {year}...")

        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"[❌] Erreur Visual Crossing API : {response.status_code} - {response.text}")

        df = pd.read_csv(io.StringIO(response.text))


        df = df.rename(columns={
            "datetime": "time",
            "windspeed": "windspeed_mean",
            "windgust": "windspeed_gust",
            "winddir": "wind_direction"
        })
        df["time"] = pd.to_datetime(df["time"])
        df = df[["time", "windspeed_mean", "windspeed_gust", "wind_direction"]]

        all_data.append(df)

    df_final = pd.concat(all_data, ignore_index=True)
    output_path = os.path.join(site_folder, f"visualcrossing_{site_name}.csv")
    df_final.to_csv(output_path, index=False)

    print(f"[✅] Données Visual Crossing enregistrées : {output_path}")

    return {
        "filename": os.path.basename(output_path),
        "filepath": output_path,
        "latitude": lat,
        "longitude": lon
    }
