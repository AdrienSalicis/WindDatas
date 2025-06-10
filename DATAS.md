## 1. Meteostat – Données observées issues de stations météo

🔗 **Lien API** : [https://dev.meteostat.net/](https://dev.meteostat.net/)

### Données récupérées

| Variable         | Description                     | Unité | Temp. agrégation  | Disponibilité |
|------------------|----------------------------------|--------|--------------------|----------------|
| windspeed_mean   | Vitesse moyenne du vent         | m/s    | Moyenne journalière | Excellente (Europe/US) |
| windspeed_gust   | Rafale max journalière          | m/s    | Max journalière     | Variable       |
| wind_direction   | Direction moyenne du vent       | °      | Moyenne journalière | Bonne          |

### Caractéristiques techniques

- **Hauteur d’observation** : 10 m (standard météo, peut varier selon la station)
- **Sources** : données issues de stations physiques, maintenues par des services nationaux
- **Qualité** : excellente pour les régions couvertes (Europe, Amérique du Nord), variable ailleurs

### Méthode d’acquisition

```python
from meteostat import Stations, Daily

# Sélection des stations proches
stations = Stations().nearby(lat, lon).fetch(2)

# Téléchargement des données journalières
data = Daily(station_id, start, end).fetch().reset_index()

# Renommage des colonnes
df = df[["time", "wspd", "wpgt", "wdir"]]
df = df.rename(columns={
    "wspd": "windspeed_mean",
    "wpgt": "windspeed_gust",
    "wdir": "wind_direction"
})
