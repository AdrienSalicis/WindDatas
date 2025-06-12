# meteo_france_station_finder.py

import requests
import pandas as pd
from geopy.distance import geodesic
import time

BASE_URL = "https://public-api.meteofrance.fr/public/DPClim/v1"
API_KEY = "Bearer eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI4Zjk4NjNiZC0xZjZmLTRkNDItYTg3OC01ODk3YzZjODBkNjAiLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6IlYxSnFIVHpSUWFHNG0xVnNFQTBmS3lrM2xkY2EiLCJuYmYiOjE3NDk3MjM3MzAsImF6cCI6IlYxSnFIVHpSUWFHNG0xVnNFQTBmS3lrM2xkY2EiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnJcL29hdXRoMlwvdG9rZW4iLCJleHAiOjE3NDk3MjczMzAsImlhdCI6MTc0OTcyMzczMCwianRpIjoiYzk1NTNlYjQtNDA3ZC00NmJlLTlmZDctMGJiYmQ0ODU4NGZhIiwiY2xpZW50X2lkIjoiVjFKcUhUelJRYUc0bTFWc0VBMGZLeWszbGRjYSJ9.MCiXDZ3JR0o1lf-_wpGx_nGisfmFQgDxque6Zk09xmHkWI_RwLSDgjUKVhFjXGXe-rcbkhSQIolKs_dfMoS0oAl37qjIiyuLErF7_A3ephMiDliQT4ZCX6aK6gi5J_2WDpp1VjLz1CZihDQ4q00s4ad1ZLqVnbiMN0vMqIcPCiQWtWAFfNbnGXbfLVugEnWyhZXAs4DXCBez3NmSfxNnO2XsOts4cbVPHU77X38Z7lRNrrfSYrpKXq6jkeeHHuAxXUgF0RLNoHi9dMPceYlfK_4PXYhCFSwOsm0NdD5AiAuCH7Oz6rjU11lN8mNDRLjpph19eef1Bblw6vgD5kT3mw"

HEADERS = {
    "accept": "application/json",
    "Authorization": API_KEY
}

def get_mf_stations_list(frequency="quotidienne"):
    url = f"{BASE_URL}/liste-stations/{frequency}"
    departements = list(range(1, 96)) + [971, 972, 973, 974, 976]
    stations = []

    for dep in departements:
        r = requests.get(url, headers=HEADERS, params={"id-departement": str(dep)})
        if r.status_code == 200:
            stations.extend(r.json())
        elif r.status_code == 429:
            time.sleep(5)
            continue
        else:
            print(f"[MF] Erreur {r.status_code} pour département {dep}")
        time.sleep(0.4)

    df = pd.DataFrame(stations)
    df.rename(columns={"lat": "latitude", "lon": "longitude"}, inplace=True)
    return df

def find_closest_mf_station(lat, lon, df):
    df = df.copy()
    df["distance_km"] = df.apply(lambda row: geodesic((lat, lon), (row["latitude"], row["longitude"])).km, axis=1)
    return df.sort_values("distance_km").iloc[0]

if __name__ == "__main__":
    stations_df = get_mf_stations_list()
    station = find_closest_mf_station(43.6045, 1.4440, stations_df)
    print(station[["id", "nom", "latitude", "longitude", "distance_km"]])