import pandas as pd
import os
import requests
from geopy.distance import geodesic


def load_isd_stations(csv_path):
    """
    Charge et nettoie le fichier isd-history.csv
    """
    df = pd.read_csv(csv_path, dtype=str)
    df.columns = df.columns.str.strip()
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Détection automatique des noms de colonnes possibles
    elevation_col = next((col for col in df.columns if col.strip().upper() in ['ELEV', 'ELEV(M)']), None)
    begin_col = next((col for col in df.columns if col.strip().upper() == 'BEGIN'), None)
    end_col = next((col for col in df.columns if col.strip().upper() == 'END'), None)

    rename_map = {}
    if elevation_col:
        rename_map[elevation_col] = 'ELEV'
    if begin_col:
        rename_map[begin_col] = 'BEGIN'
    if end_col:
        rename_map[end_col] = 'END'

    df.rename(columns=rename_map, inplace=True)

    # Convertir les colonnes nécessaires si elles existent
    for col in ['LAT', 'LON', 'ELEV', 'BEGIN', 'END']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['LAT', 'LON'])
    return df


def test_isd_station_availability(usaf, wban, year):
    """
    Vérifie si le fichier NOAA ISD pour un identifiant et une année existe réellement.
    """
    url = f"https://www.ncei.noaa.gov/data/global-hourly/access/{year}/{usaf}-{wban}-{year}.csv.gz"
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def find_nearest_isd_stations(site_lat, site_lon, isd_df, max_distance_km=80, n=5):
    """
    Trouve les n stations ISD les plus proches dans un rayon de max_distance_km
    et vérifie leur accessibilité effective via l'URL NOAA.
    """
    station_list = []

    for _, row in isd_df.iterrows():
        station_coord = (row['LAT'], row['LON'])
        site_coord = (site_lat, site_lon)
        dist_km = geodesic(site_coord, station_coord).km

        if dist_km <= max_distance_km:
            begin = int(row['BEGIN']) if 'BEGIN' in row and not pd.isna(row['BEGIN']) else None
            end = int(row['END']) if 'END' in row and not pd.isna(row['END']) else None
            years_available = None
            if begin and end:
                begin_year = int(str(begin)[:4])
                end_year = int(str(end)[:4])
                years_available = list(range(begin_year, end_year + 1))

            # Test réel d’accessibilité du fichier .csv.gz pour la dernière année
            is_valid = test_isd_station_availability(row.get('USAF'), row.get('WBAN'), end_year) if end_year else False

            station_list.append({
                "usaf": row.get('USAF'),
                "wban": row.get('WBAN'),
                "station_id": f"{row.get('USAF')}-{row.get('WBAN')}",
                "name": row.get('STATION NAME', 'Unknown').title(),
                "country": row.get('CTRY'),
                "latitude": row['LAT'],
                "longitude": row['LON'],
                "elevation_m": row.get('ELEV', None),
                "distance_km": round(dist_km, 2),
                "begin": begin,
                "end": end,
                "years_available": years_available,
                "file_available": is_valid
            })

    # Trier par distance et retourner les n premiers
    station_list.sort(key=lambda x: x['distance_km'])
    return station_list[:n]


# Exemple d'utilisation
if __name__ == "__main__":
    path_to_csv = "data/isd-history.csv"
    if not os.path.exists(path_to_csv):
        print(f"[❌] Fichier introuvable : {path_to_csv}")
    else:
        df_stations = load_isd_stations(path_to_csv)
        stations = find_nearest_isd_stations(45.5, 4.8, df_stations)
        if stations:
            print("\n[📍] Stations NOAA les plus proches :")
            for station in stations:
                print("\n---------------------------")
                for k, v in station.items():
                    print(f"- {k}: {v}")
        else:
            print("[⚠️] Aucune station trouvée dans le rayon défini.")
