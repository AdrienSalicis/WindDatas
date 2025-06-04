import os
import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox
from meteostat import Stations, Daily
from datetime import datetime
import requests

# ------------------------------
# Boîte de dialogue pour date
# ------------------------------
def get_date_input(prompt):
    root = tk.Tk()
    root.withdraw()
    date_str = simpledialog.askstring("Entrée de la date", prompt)
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        messagebox.showerror("Erreur", "Format attendu : YYYY-MM-DD")
        return get_date_input(prompt)

# ------------------------------
# Récupère les données Meteostat
# ------------------------------
def get_meteostat_data(site_name, lat, lon, start, end):
    try:
        stations = Stations().nearby(lat, lon)
        station = stations.fetch(1)
        if station.empty:
            print(f"[⚠️] Aucune station Meteostat pour {site_name}")
            return None

        station_id = station.index[0]
        print(f"[📡] Station sélectionnée pour {site_name} : {station.loc[station_id]['name']} (ID: {station_id})")

        data = Daily(station_id, start, end)
        data = data.fetch()

        if data.empty:
            print(f"[⚠️] Aucune donnée disponible pour {site_name} entre {start} et {end}")
            return None

        data.reset_index(inplace=True)
        df = data[["time", "wspd", "snow"]].copy()
        df.rename(columns={"time": "date", "wspd": "wind_speed", "snow": "snowfall"}, inplace=True)
        return df
    except Exception as e:
        print(f"[ERROR] Problème lors de la récupération des données Meteostat pour {site_name} : {e}")
        return None

# ------------------------------
# Appelle l'API OpenMeteo
# ------------------------------
def get_openmeteo_data(site_name, lat, lon, start, end):
    try:
        start_str = start.strftime("%Y-%m-%d")
        end_str = end.strftime("%Y-%m-%d")
        url = (
            f"https://archive-api.open-meteo.com/v1/archive"
            f"?latitude={lat}&longitude={lon}"
            f"&start_date={start_str}&end_date={end_str}"
            f"&daily=windspeed_10m_max,snowfall_sum"
            f"&timezone=auto"
        )
        response = requests.get(url)
        if response.status_code != 200:
            print(f"[ERROR] OpenMeteo - Erreur de requête: {response.status_code}")
            return None
        json_data = response.json()
        df = pd.DataFrame({
            "date": json_data["daily"]["time"],
            "wind_speed": json_data["daily"]["windspeed_10m_max"],
            "snowfall": json_data["daily"]["snowfall_sum"]
        })
        return df
    except Exception as e:
        print(f"[ERROR] OpenMeteo - Exception: {e}")
        return None

# ------------------------------
# Fonction principale
# ------------------------------
def main():
    df_sites = pd.read_csv("modele_sites.csv", delimiter=";", encoding="utf-8")
    
    start = get_date_input("Entrez la date de début (YYYY-MM-DD) :")
    end = get_date_input("Entrez la date de fin (YYYY-MM-DD) :")

    for _, row in df_sites.iterrows():
        site_name = row["Nom"]
        lat = float(row["Latitude"])
        lon = float(row["Longitude"])
        print(f"\n📍 Traitement de {site_name}...")

        # Création du dossier
        output_dir = os.path.join("data", site_name.replace(" ", "_"))
        os.makedirs(output_dir, exist_ok=True)

        # ------------------ Meteostat ------------------
        meteostat_df = get_meteostat_data(site_name, lat, lon, start, end)
        if meteostat_df is not None:
            meteostat_csv = os.path.join(output_dir, f"meteostat_{site_name.replace(' ', '_')}.csv")
            meteostat_df.to_csv(meteostat_csv, index=False)
            print(f"[✅] Données Meteostat sauvegardées dans : {meteostat_csv}")
        else:
            print(f"[⚠️] Aucune donnée Meteostat pour {site_name}")

        # ------------------ OpenMeteo ------------------
        openmeteo_df = get_openmeteo_data(site_name, lat, lon, start, end)
        if openmeteo_df is not None:
            openmeteo_csv = os.path.join(output_dir, f"openmeteo_{site_name.replace(' ', '_')}.csv")
            openmeteo_df.to_csv(openmeteo_csv, index=False)
            print(f"[✅] Données OpenMeteo sauvegardées dans : {openmeteo_csv}")
        else:
            print(f"[⚠️] Aucune donnée OpenMeteo pour {site_name}")

if __name__ == "__main__":
    main()
