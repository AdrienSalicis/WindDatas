import pandas as pd
from meteostat import Stations, Daily
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

# ----------------------------------------------------
# Demander les dates à l’utilisateur
# ----------------------------------------------------
def demander_dates():
    root = tk.Tk()
    root.withdraw()
    debut = simpledialog.askstring("Date de début", "Format YYYY-MM-DD :")
    fin = simpledialog.askstring("Date de fin", "Format YYYY-MM-DD :")
    try:
        datetime.strptime(debut, "%Y-%m-%d")
        datetime.strptime(fin, "%Y-%m-%d")
        return debut, fin
    except:
        messagebox.showerror("Erreur", "Format de date invalide.")
        return demander_dates()

# ----------------------------------------------------
# Choisir la station météo
# ----------------------------------------------------
def choisir_station_tkinter(stations):
    root = tk.Tk()
    root.withdraw()

    options = [
        f"{i+1}. {row['name']} ({round(row['distance'],1)} km, {row['country']})"
        for i, (_, row) in enumerate(stations.iterrows())
    ]

    choix = simpledialog.askstring(
        "Choix de la station",
        "Stations disponibles :\n" + "\n".join(options) + "\n\nEntrez le numéro :"
    )
    if choix is None:
        return None
    try:
        index = int(choix) - 1
        return stations.iloc[index]
    except:
        messagebox.showerror("Erreur", "Numéro invalide.")
        return None

# ----------------------------------------------------
# MAIN
# ----------------------------------------------------
def main():
    df_sites = pd.read_csv("modele_sites.csv", delimiter=";", encoding="utf-8")
    start_date, end_date = demander_dates()
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    for _, row in df_sites.iterrows():
        name = row["Nom"]
        lat = row["Latitude"]
        lon = row["Longitude"]

        print(f"\n📍 Traitement de {name} (lat={lat}, lon={lon})...")

        stations = Stations().nearby(lat, lon).fetch(10)
        if stations.empty:
            print("❌ Aucune station trouvée.")
            continue

        selected = choisir_station_tkinter(stations)
        if selected is None:
            print("⛔ Aucune station sélectionnée.")
            continue

        print(f"📡 Station sélectionnée : {selected['name']} (ID: {selected.name})")

        try:
            data = Daily(selected.name, start_dt, end_dt).fetch()
            if data.empty:
                print("⚠️ Aucune donnée météo pour cette période.")
                continue

            data.reset_index(inplace=True)
            data["station_id"] = selected.name
            data.to_csv(f"{name}_meteo.csv", index=False)
            print(f"✅ Données enregistrées dans {name}_meteo.csv")
        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
