import os
import requests
import gzip
from datetime import datetime
import pandas as pd

GHCN_BASE_URL = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily"

def download_ghcnh_file(station_id, destination):
    filename = f"{station_id}.dly"
    url = f"{GHCN_BASE_URL}/all/{filename}"
    local_path = os.path.join(destination, filename)

    if os.path.exists(local_path):
        return local_path

    print(f"[📡] Téléchargement GHCNh : {url}")
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, "wb") as f:
            f.write(response.content)
        return local_path
    else:
        print(f"[❌] Erreur GHCNh ({station_id}) : {response.status_code}")
        return None

def parse_ghcnh_file(filepath, start_date, end_date):
    start_year = int(start_date[:4])
    end_year = int(end_date[:4])

    data = []

    with open(filepath, "r") as file:
        for line in file:
            station = line[0:11]
            year = int(line[11:15])
            month = int(line[15:17])
            element = line[17:21]

            if element not in ["WSF2", "WSFG"]:  # vitesse et rafales de vent (en 0.1 knots)
                continue
            if year < start_year or year > end_year:
                continue

            for day in range(1, 32):
                value = line[21 + (day - 1) * 8:26 + (day - 1) * 8].strip()
                if value == "-9999":
                    continue
                try:
                    date = datetime(year, month, day)
                    if not (datetime.strptime(start_date, "%Y-%m-%d") <= date <= datetime.strptime(end_date, "%Y-%m-%d")):
                        continue

                    value = float(value) * 0.514444  # knots → m/s
                    data.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "variable": "windspeed_gust" if element == "WSFG" else "windspeed_mean",
                        "value": value
                    })
                except:
                    continue

    if not data:
        return None

    df = pd.DataFrame(data)
    df = df.pivot(index="date", columns="variable", values="value").reset_index()
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date")

def save_ghcnh_data(site_name, site_folder, station_id, start_date, end_date, verbose=True):
    os.makedirs(site_folder, exist_ok=True)
    local_path = download_ghcnh_file(station_id, site_folder)

    if not local_path:
        return None

    df = parse_ghcnh_file(local_path, start_date, end_date)

    if df is not None:
        csv_path = os.path.join(site_folder, f"ghcnh_{site_name}.csv")
        df.to_csv(csv_path, index=False)
        if verbose:
            print(f"[✅] Données GHCNh enregistrées : {csv_path}")
        return {
            "filepath": csv_path,
            "station_id": station_id,
            "data": df
        }
    else:
        if verbose:
            print(f"[⚠️] Aucune donnée exploitable pour GHCNh {station_id}.")
        return None
