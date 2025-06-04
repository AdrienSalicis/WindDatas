import pandas as pd
from meteostat import Stations
from geopy.distance import geodesic

def enrich_modele_sites(csv_path="modele_sites.csv"):
    print(f"[📥] Chargement de {csv_path}...")
    df = pd.read_csv(csv_path)

    required_cols = [
        "meteostat_station1", "meteostat_station2",
        "station_name1", "station_name2",
        "distance_station1_km", "distance_station2_km",
        "elevation_station1", "elevation_station2",
        "anemometer_height1", "anemometer_height2",
        "terrain_context1", "terrain_context2"
    ]

    # Création des colonnes manquantes
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    for idx, row in df.iterrows():
        name = row["name"]
        lat, lon = row["latitude"], row["longitude"]
        print(f"\n[🔎] Traitement du site : {name} ({lat}, {lon})")

        try:
            stations = Stations().nearby(lat, lon).fetch(2)

            if len(stations) >= 1:
                s1 = stations.iloc[0]
                df.at[idx, "meteostat_station1"] = s1.name
                df.at[idx, "station_name1"] = s1["name"]
                df.at[idx, "elevation_station1"] = s1["elevation"]
                df.at[idx, "anemometer_height1"] = ""
                df.at[idx, "terrain_context1"] = ""
                dist1 = geodesic((lat, lon), (s1["latitude"], s1["longitude"])).km
                df.at[idx, "distance_station1_km"] = round(dist1, 2)
                print(f"[✅] Station 1 trouvée : {s1['name']} ({dist1:.2f} km)")

            if len(stations) >= 2:
                s2 = stations.iloc[1]
                df.at[idx, "meteostat_station2"] = s2.name
                df.at[idx, "station_name2"] = s2["name"]
                df.at[idx, "elevation_station2"] = s2["elevation"]
                df.at[idx, "anemometer_height2"] = ""
                df.at[idx, "terrain_context2"] = ""
                dist2 = geodesic((lat, lon), (s2["latitude"], s2["longitude"])).km
                df.at[idx, "distance_station2_km"] = round(dist2, 2)
                print(f"[✅] Station 2 trouvée : {s2['name']} ({dist2:.2f} km)")

        except Exception as e:
            print(f"[⚠️] Erreur pour {name} : {e}")

    df.to_csv(csv_path, index=False)
    print(f"\n[💾] Enregistrement terminé : {csv_path}")

if __name__ == "__main__":
    enrich_modele_sites("modele_sites.csv")
