import requests

api_key = '592e309736msh8c900d0b07512c8p151e20jsnbdee347f6c87'  # Remplace par ta clé API
lat = 44.15
lon = 4.72

url = f"https://api.meteostat.net/v1/stations/nearby?lat={lat}&lon={lon}&limit=5"
headers = {'x-api-key': api_key}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("Stations proches :", data)
else:
    print("Erreur lors de la récupération des stations : ", response.status_code)

