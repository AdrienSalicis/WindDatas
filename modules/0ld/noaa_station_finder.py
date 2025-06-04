
import pandas as pd
from geopy.distance import geodesic

STATION_METADATA_PATH = "isd-history.csv"

def load_station_metadata():
    df = pd.read_csv(STATION_METADATA_PATH)
    df["LAT"] = pd.to_numeric(df["LAT"].astype(str).str.strip(), errors="coerce")
    df["LON"] = pd.to_numeric(df["LON"].astype(str).str.strip(), errors="coerce")
    df["USAF"] = df["USAF"].astype(str).str.zfill(6)
    df["WBAN"] = df["WBAN"].astype(str).str.zfill(5)
    df = df.dropna(subset=["LAT", "LON"])
    return df

def find_nearest_noaa_station(lat, lon, country_code=None, verbose=True):
    df = load_station_metadata()

    def safe_distance(row):
        try:
            return geodesic((lat, lon), (float(row["LAT"]), float(row["LON"]))).km
        except Exception:
            return float("inf")

    df["distance_km"] = df.apply(safe_distance, axis=1)
    df = df[df["distance_km"] != float("inf")]

    # 🔥 Filtrage des WBAN=99999 (stations incomplètes)
    df = df[df["WBAN"] != "99999"]

    if df.empty:
        raise ValueError(f"Aucune station NOAA valide trouvée autour de ({lat}, {lon})")

    nearest = df.sort_values("distance_km").iloc[0]
    station_id = f"{nearest['USAF']}-{nearest['WBAN']}"

    if verbose:
        print(f"[📍] Station NOAA la plus proche (valide) : {station_id} – {nearest['STATION NAME']} ({nearest['CTRY']}) à {nearest['distance_km']:.2f} km")

    return {
        "station_id": station_id,
        "name": nearest["STATION NAME"],
        "country": nearest["CTRY"],
        "latitude": nearest["LAT"],
        "longitude": nearest["LON"],
        "distance_km": round(nearest["distance_km"], 2),
        "begin": nearest["BEGIN"],
        "end": nearest["END"]
    }
