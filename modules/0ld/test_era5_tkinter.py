import tkinter as tk
from tkinter import simpledialog
from datetime import datetime
import os

from era5_fetcher import save_era5_data

def ask_site_info():
    root = tk.Tk()
    root.withdraw()

    name = simpledialog.askstring("Nom du site", "Nom court du site :")
    lat = float(simpledialog.askstring("Latitude", "Latitude (ex: 48.85) :"))
    lon = float(simpledialog.askstring("Longitude", "Longitude (ex: 2.35) :"))

    start = simpledialog.askstring("Date de début", "YYYY-MM-DD :")
    end = simpledialog.askstring("Date de fin", "YYYY-MM-DD :")

    return {
        "name": name,
        "lat": lat,
        "lon": lon,
        "start": start,
        "end": end
    }

def main():
    site = ask_site_info()

    folder = os.path.join("test_output", site["name"])
    os.makedirs(folder, exist_ok=True)

    result = save_era5_data(
        site_name=site["name"],
        site_folder=folder,
        lat=site["lat"],
        lon=site["lon"],
        start_date=site["start"],
        end_date=site["end"]
    )

    print(f"[✅] Fichier CSV sauvegardé ici : {result['filepath']}")

    import pandas as pd
    df = pd.read_csv(result['filepath'])
    print("\nAperçu des données :")
    print(df.head())

if __name__ == "__main__":
    main()
