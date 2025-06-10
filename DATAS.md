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
```

---

## 2. NOAA ISD – Données observées brutes horaires

🔗 **Lien données** : [https://www.ncei.noaa.gov/data/global-hourly/](https://www.ncei.noaa.gov/data/global-hourly/)

### Données récupérées

| Variable         | Description                   | Unité | Temp. agrégation | Commentaire              |
|------------------|-------------------------------|--------|------------------|---------------------------|
| windspeed_mean   | Vitesse maximale journalière  | m/s    | max journalière  | issue des données horaires |
| windspeed_gust   | Rafale max journalière        | m/s    | max journalière  | si colonne GUST présente   |
| wind_direction   | Direction dominante du vent   | °      | mode journalière | issue de DRCT ou WND       |

### Caractéristiques techniques

- **Hauteur d’observation** : souvent 10 m, mais variable selon les stations
- **Fréquence native** : données horaires (voire toutes les 20 min pour certaines)
- **Couverture historique** : jusqu’à 1929 pour certaines stations
- **Format brut** : décodage requis de WND, DRCT, GUST
- **Type** : données brutes issues de capteurs physiques certifiés (stations officielles NOAA)

### Méthode d’acquisition

```python
# Vérification disponibilité
HEAD https://www.ncei.noaa.gov/data/global-hourly/access/{year}/{usaf}{wban}.csv

# Téléchargement et traitement
pd.read_csv(file_url)

# Parsing des champs
parsed = df['WND'].str.split(',', expand=True)
df['wind_dir'] = parsed[0].astype(float)
df['wind_speed'] = parsed[3].astype(float) / 10

df['gust'] = df['GUST'].astype(float) / 10 if 'GUST' in df.columns else np.nan
df['wind_direction'] = df['DRCT'].astype(float) if 'DRCT' in df.columns else df['wind_dir']

# Agrégation journalière
df_daily = df.groupby('date').agg({
    'wind_speed': 'max',
    'gust': 'max',
    'wind_direction': lambda x: x.mode().iloc[0] if not x.dropna().empty else np.nan
})
```

---

## 3. Open-Meteo – Données modélisées via API

🔗 **Lien API** : [https://open-meteo.com/](https://open-meteo.com/)

### Données récupérées

| Variable         | Description                   | Unité | Temp. agrégation  |
|------------------|-------------------------------|--------|-------------------|
| windspeed_mean   | Vitesse moyenne du vent       | m/s    | journalière       |
| windspeed_gust   | Rafale maximale               | m/s    | journalière       |
| wind_direction   | Direction moyenne             | °      | moyenne horaires  |

### Caractéristiques techniques

- **Hauteur modélisée** : 10 m
- **Sources** : modèles météorologiques globaux
- **Type** : données de réanalyse ou prévision reconstituée
- **Qualité** : dépend du relief, du maillage local, et du modèle sous-jacent (ICON, GFS...)
- **Avantages** : API gratuite, rapide, sans clé obligatoire

### Méthode d’acquisition

```python
# Données journalières : rafale + moyenne
url_daily = f"https://archive-api.open-meteo.com/v1/archive?...&daily=windspeed_10m_max,windspeed_10m_mean"

# Données horaires pour direction
url_hourly = f"https://archive-api.open-meteo.com/v1/archive?...&hourly=winddirection_10m"

# Fusion des deux
pd.merge(df_daily, df_dir, on="time", how="left")
```

---

## 4. NASA POWER – Données modélisées issues de la NASA

🔗 **Lien API** : [https://power.larc.nasa.gov/](https://power.larc.nasa.gov/)

### Données récupérées

| Variable           | Description                   | Unité | Temp. agrégation |
|--------------------|-------------------------------|--------|------------------|
| windspeed_mean     | Vitesse moyenne du vent       | m/s    | journalière      |
| windspeed_gust     | Rafales (si disponibles)      | m/s    | journalière      |
| wind_direction     | Direction moyenne             | °      | journalière      |
| u_component_10m    | Vent zonal                    | m/s    | journalière      |
| v_component_10m    | Vent méridien                 | m/s    | journalière      |

### Caractéristiques techniques

- **Hauteur modélisée** : 10 m
- **Maillage spatial** : 0.5° (~55 km)
- **Type** : données de réanalyse satellitaire (MERRA)
- **Période** : depuis 1981
- **Limitation** : rafales souvent absentes avant 2001

### Méthode d’acquisition

```python
url = (
  f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=WS10M,WD10M,U10M,V10M"
  f"&latitude={lat}&longitude={lon}&start={start}&end={end}&format=JSON"
)
response = requests.get(url)
data = response.json()['properties']['parameter']
```

---

## 5. ERA5 – Données de réanalyse ECMWF

🔗 **Lien Copernicus CDS** : [https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels)

### Données récupérées

| Variable               | Description                       | Unité | Temp. agrégation |
|------------------------|------------------------------------|--------|------------------|
| 10m_u_component_of_wind | Composante zonale du vent         | m/s    | horaire          |
| 10m_v_component_of_wind | Composante méridienne du vent     | m/s    | horaire          |
| windspeed_mean         | Vitesse moyenne reconstruite       | m/s    | max journalière  |
| wind_direction         | Direction moyenne reconstruite     | °      | moyenne journalière |

### Caractéristiques techniques

- **Hauteur modélisée** : 10 m
- **Sources** : réanalyse basée sur mesures satellites + assimilations numériques ECMWF
- **Résolution** : 0.25° (~30 km)
- **Période** : depuis 1940
- **Qualité** : très homogène et fiable, mais peut sous-estimer les extrêmes

### Méthode d’acquisition (via CDSAPI)

```python
request = {
  "variable": ["10m_u_component_of_wind", "10m_v_component_of_wind"],
  "date": f"{start}/{end}",
  "location": {"latitude": lat, "longitude": lon},
  "data_format": "csv"
}
c.retrieve("reanalysis-era5-single-levels-timeseries", request).download(...)
```
