from modules.noaa_station_finder import load_isd_stations, find_nearest_isd_stations
import os

if __name__ == "__main__":
    latitude = 44.21
    longitude = 4.74
    csv_path = "data/isd-history.csv"

    print("[🔍] Chargement des stations NOAA...")
    if not os.path.exists(csv_path):
        print(f"[❌] Fichier introuvable : {csv_path}")
    else:
        isd_df = load_isd_stations(csv_path)
        print(f"[✅] {len(isd_df)} stations chargées")

        print(f"[📡] Recherche des 5 stations les plus proches autour de ({latitude}, {longitude})")
        stations = find_nearest_isd_stations(latitude, longitude, isd_df, max_distance_km=80, n=5)

        if stations:
            print("\n✅ Résultat :")
            for i, station in enumerate(stations, start=1):
                print(f"\n--- Station {i} ---")
                for key, value in station.items():
                    print(f"- {key}: {value}")
        else:
            print("❌ Aucune station trouvée.")
