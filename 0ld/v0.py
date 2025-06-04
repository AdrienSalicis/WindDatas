import pandas as pd
import requests
import tkinter as tk
from tkinter import simpledialog, messagebox

# ----------------------------------------------------
# FONCTION POUR OBTENIR LES DONNÉES MÉTÉO
# ----------------------------------------------------
def get_meteostat_data(lat, lon, start_date, end_date, api_key):
    # Requête pour obtenir les stations les plus proches
    url = f"https://meteostat.p.rapidapi.com/stations/nearest"
    headers = {
        "X-RapidAPI-Host": "meteostat.p.rapidapi.com",
        "X-RapidAPI-Key": api_key
    }
    
    params = {
        "lat": lat,
        "lon": lon,
        "limit": 1  # Limiter à 1 station pour éviter trop de résultats
    }
    
    print(f"[DEBUG] Requête vers l'API avec latitude={lat} et longitude={lon}")
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"[ERROR] Erreur lors de la récupération des stations proches: {response.status_code}")
        return None
    
    stations = response.json().get('data', [])
    if len(stations) == 0:
        print(f"[INFO] Aucune station proche trouvée pour latitude={lat}, longitude={lon}.")
    return stations

# ----------------------------------------------------
# UTILITAIRE: Boîte de dialogue pour choisir une station météo
# ----------------------------------------------------
def choisir_station_tkinter(stations):
    root = tk.Tk()
    root.withdraw()

    options = [f"{s['name']} ({s['distance']} km, depuis {s['first_observation']})" for s in stations]
    choix = simpledialog.askstring(
        "Choix de la station météo",
        "Choisissez une station météo parmi :\n" +
        "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(options)) +
        "\n\nEntrez le numéro :"
    )
    if choix is None:
        messagebox.showinfo("Annulé", "Aucune station sélectionnée.")
        return None
    try:
        index = int(choix) - 1
        if 0 <= index < len(stations):
            return stations[index]
        else:
            messagebox.showerror("Erreur", "Numéro invalide.")
            return None
    except ValueError:
        messagebox.showerror("Erreur", "Entrée non valide.")
        return None

# ----------------------------------------------------
# FONCTION PRINCIPALE
# ----------------------------------------------------
def main():
    # Charger le fichier CSV contenant les coordonnées des sites
    df = pd.read_csv("modele_sites.csv", delimiter=";", encoding="utf-8")
    print("Colonnes du fichier CSV:", df.columns)
    
    # Paramètres de la période
    start_date = "1963-01-01"
    end_date = "2024-12-31"
    
    # Clé API RapidAPI pour Meteostat (remplace par ta clé)
    api_key = "592e309736msh8c900d0b07512c8p151e20jsnbdee347f6c87"  # Mets ta clé API ici
    
    for _, row in df.iterrows():
        name = row["Nom"]
        lat = row["Latitude"]
        lon = row["Longitude"]
        print(f"\nTraitement de {name}...")
        
        # Obtenir les stations proches via Meteostat
        stations = get_meteostat_data(lat, lon, start_date, end_date, api_key)
        
        if stations is None or len(stations) == 0:
            print(f"[INFO] Aucune station proche trouvée pour {name}.")
            continue
        
        # Demander à l'utilisateur de choisir une station parmi celles récupérées
        station = choisir_station_tkinter(stations)
        
        if station is None:
            print(f"[INFO] Aucune station sélectionnée pour {name}.")
            continue
        
        # Utilisation de la station choisie pour récupérer les données météorologiques
        station_id = station['id']
        print(f"[INFO] Récupération des données de la station {station_id}...")
        
        # URL pour récupérer les données historiques
        data_url = f"https://meteostat.p.rapidapi.com/history/daily"
        headers = {
            "X-RapidAPI-Host": "meteostat.p.rapidapi.com",
            "X-RapidAPI-Key": api_key
        }
        data_params = {
            "station": station_id,
            "start": start_date,
            "end": end_date,
            "vars": "wspd",  # Variable pour la vitesse du vent
        }
        
        data_response = requests.get(data_url, headers=headers, params=data_params)
        
        if data_response.status_code == 200:
            data = data_response.json()['data']
            wind_data = []
            for entry in data:
                wind_data.append({
                    "date": entry['date'],
                    "station_id": station_id,
                    "wind_speed": entry['wspd']
                })
            wind_df = pd.DataFrame(wind_data)
            
            # Sauvegarder les données dans un fichier CSV
            wind_df.to_csv(f"{name}_meteo.csv", index=False)
            print(f"[INFO] Données enregistrées pour {name}.")
        else:
            print(f"[ERROR] Erreur lors de la récupération des données pour la station {station_id}: {data_response.status_code}")
            
if __name__ == "__main__":
    main()
