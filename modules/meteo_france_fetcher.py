# meteo_france_fetcher.py

import os
import requests
import time
import pandas as pd

BASE_URL = "https://public-api.meteofrance.fr/public/DPClim/v1"
API_KEY = "Bearer eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI4Zjk4NjNiZC0xZjZmLTRkNDItYTg3OC01ODk3YzZjODBkNjAiLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6IlYxSnFIVHpSUWFHNG0xVnNFQTBmS3lrM2xkY2EiLCJuYmYiOjE3NDk3MTU2NzYsImF6cCI6IlYxSnFIVHpSUWFHNG0xVnNFQTBmS3lrM2xkY2EiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnJcL29hdXRoMlwvdG9rZW4iLCJleHAiOjE3NDk3MTkyNzYsImlhdCI6MTc0OTcxNTY3NiwianRpIjoiNzg2YTgxNjYtMGJmZC00OTIwLThjMmYtNzNkZDEzOTA4ODZiIiwiY2xpZW50X2lkIjoiVjFKcUhUelJRYUc0bTFWc0VBMGZLeWszbGRjYSJ9.k0rhFKmW6wUUkDzLUMzWZ7fB7tui0k9DgA51lKUwJl-ApKPFojB7dLWmYZjyydQsuZOkfw9Z9RbL1RhRxwOoZ-oBFmkXxoJS-W9nR-PtN7d5A-0IZugYJZJCJjZjM76op9c5nxSg5ov6HmideFfPn3HSLv8J4d45vmfCP4ME6xINQk-YFVlq6KooRQKFq76NNV4t3aHiY2oSdzKmQVmcC1vsYUe9_b6okVz_fKCUonLj_QhDxTlh9MiZXgV-b2_UB2EKznfOza7qlFJyjkGQtnvxZKZbk8aWG0JofJuXf3xyCyspUJLRoZgDb8JlPdNn6Bt3oiiZ65n5aW7qsxJS4w"

HEADERS = {
    "accept": "text/csv",
    "Authorization": API_KEY
}

def create_climate_request(station_id, start, end, frequency="quotidienne"):
    url = f"{BASE_URL}/commande-station/{frequency}"
    params = {
        "id-station": station_id,
        "date-deb-periode": start + "T00:00:00Z",
        "date-fin-periode": end + "T23:59:59Z"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 202:
        raise Exception(f"[MF] ❌ Erreur commande : {response.status_code}")
    return response.json().get("id-cmde")

def download_climate_file(order_id, output_path, max_wait=60):
    url = f"{BASE_URL}/commande/fichier"
    for _ in range(max_wait):
        r = requests.get(url, headers=HEADERS, params={"id-cmde": order_id})
        if r.status_code == 201:
            with open(output_path, "wb") as f:
                f.write(r.content)
            return
        elif r.status_code == 204:
            time.sleep(2)
        else:
            raise Exception(f"[MF] ❌ Erreur téléchargement : {r.status_code}")
    raise TimeoutError("[MF] Timeout dépassé")

def fetch_meteo_france_data(station_id, start_date, end_date, site_name, frequency="quotidienne"):
    print(f"[MF] Récupération Météo-France pour {site_name}...")
    try:
        order_id = create_climate_request(station_id, start_date, end_date, frequency)
        out_path = os.path.join("data", site_name, f"meteo_france_{site_name}.csv")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        download_climate_file(order_id, out_path)
        print(f"[MF] ✅ Fichier enregistré : {out_path}")
        return out_path
    except Exception as e:
        print(f"[MF] ❌ Échec : {e}")
        return None