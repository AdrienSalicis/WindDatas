## 1. Meteostat – Données observées issues de stations météo

🔗 **Lien API** : [https://dev.meteostat.net/](https://dev.meteostat.net/)

## Fiche Source : Meteostat

### Type de données
- **Observées**, issues de stations météorologiques officielles (SYNOP, METAR, stations nationales).
- Données collectées depuis des sources comme NOAA ISD, DWD (Allemagne), Environment Canada, etc.
- Agrégation et harmonisation assurées par l'équipe Meteostat.

### Hauteur de mesure
- **En principe : 10 mètres au-dessus du sol**, conformément aux recommandations de l’OMM.
- **⚠️ Toutefois**, **aucune garantie** de hauteur homogène : chaque station peut avoir des instruments installés à des hauteurs variables.
- Meteostat **ne fournit pas** la hauteur exacte des instruments via son API, mais suit la norme si les données sources le précisent.

### Période de moyennage
- **Vent moyen (`windspeed_mean`)** : moyenne glissante sur **10 minutes**, selon la **norme OMM/WMO No.8**.
  - Cette période est spécifiée pour les stations SYNOP et METAR, qui sont majoritaires dans Meteostat.

### Rafales (`gust`)
- Représentent le **maximum de vent instantané (3 secondes)** mesuré durant la période précédente (souvent 10 min).
- Lorsque la source le permet, Meteostat inclut la **rafale max sur 3 s**, conformément à la norme WMO.

### Direction du vent
- **Direction d’origine du vent**, exprimée en degrés azimutaux :
  - `0°` = du nord, `90°` = de l’est, `180°` = du sud, `270°` = de l’ouest
- Mesurée sur la même période que la vitesse moyenne (10 min).

### Variables typiques (lorsqu’elles sont disponibles)

| Variable         | Description                           | Unité  |
|------------------|---------------------------------------|------- |
| `windspeed_mean` | Vent moyen sur 10 minutes             | m/s    |
| `wind_direction` | Direction moyenne sur 10 minutes      | degrés |
| `gust`           | Rafale max sur 3 secondes             | m/s    |

### 🔎 Résumé technique

| Élément              | Détail                                        |
|----------------------|-----------------------------------------------|
| Source               | Meteostat (données observées)                 |
| Hauteur anémomètre   | ~10 m (norme WMO si connue, sinon inconnue)   |
| Vent moyen           | Moyenne glissante sur 10 minutes              |
| Rafales              | Max sur 3 secondes (si fourni par la source)  |
| Direction            | Azimut d’origine du vent                      |
| Fréquence temporelle | Généralement horaire ou demi-horaire          |
| Norme suivie         | OMM / WMO No.8                                |

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

## Fiche Source : NOAA ISD (Integrated Surface Dataset)

### Type de données
- **Observées**, enregistrées par des stations météorologiques officielles dans le monde entier.
- Source principale : **ISD (Integrated Surface Dataset)** maintenu par la NOAA (NCEI).
- Données issues de messages METAR, SYNOP, AUTO… centralisés depuis plus de **35 000 stations**.

### Hauteur de mesure
- La **hauteur d’installation des instruments** varie d’une station à l’autre.
- Par convention, la hauteur standard recommandée par la NOAA pour l’anémomètre est **10 mètres**.
- ⚠️ Cette hauteur **n’est pas toujours précisée** dans les fichiers horaires `.csv` accessibles depuis l’interface web.
- Pour connaître la hauteur exacte → se référer au fichier `isd-history.csv` (champ `ELEV` ≠ hauteur d’anémomètre mais utile pour l’environnement de la station).

### Fréquence et période de moyennage
- **Fréquence d’enregistrement** : en général **horaire**, parfois plus fréquent.
- **Vitesse du vent (`WND`)** :
  - Représente la **moyenne sur 2 minutes** avant l’heure d’observation (**source officielle NOAA**).
  - Source : [NOAA ISH Format Documentation (PDF)](https://www.ncei.noaa.gov/pub/data/noaa/ish-format-document.pdf), section WND.
- **Direction du vent (`WND`)** : Direction moyenne du vent sur la même période de 2 minutes.

### Rafales (`GUST`)
- Si présentes, les **rafales (`GUST`)** représentent la **rafale maximale sur 5 secondes** dans l’heure précédant l’observation.
- ⚠️ Toutes les stations ne rapportent pas cette variable (elle est souvent absente dans les anciens fichiers ou certaines régions).

### Direction du vent
- Exprimée en **degrés azimutaux**, standard WMO :
  - `0°` = vent du Nord, `90°` = vent d’Est, etc.
- Valeurs invalides = `999`.

### Format des fichiers bruts NOAA ISD (`.csv`)

| Champ     | Description                              | Exemple                |
|-----------|------------------------------------------|------------------------|
| `DATE`    | Date/heure UTC                           | `2023-01-01T12:00:00`  |
| `WND`     | Direction et vitesse moyenne sur 2 min   | `270,15,9999,1`        |
| `GUST`    | Rafale max sur 5 s                       | `25.1`                 |
| `DRCT`    | Direction du vent (alternative)          | `270`                  |

### Variables typiques extraites pour WindDatas

| Variable         | Description                              | Unité |
|------------------|------------------------------------------|-------|
| `windspeed_mean` | Moyenne sur 2 min (`WND`)                | m/s   |
| `wind_direction` | Direction moyenne (`WND` ou `DRCT`)      | degré |
| `gust`           | Rafale max sur 5 s (`GUST`)              | m/s   |

### 🔎 Résumé technique

| Élément              | Détail                                                       |
|----------------------|--------------------------------------------------------------|
| Source               | NOAA ISD (fichiers horaires, station par station)            |
| Hauteur anémomètre   | En principe 10 m, non systématiquement précisée              |
| Vent moyen           | Moyenne sur 2 minutes avant l'observation                    |
| Rafales              | Max sur 5 secondes dans l’heure précédente (si disponible)   |
| Direction            | Azimut d’origine du vent                                     |
| Fréquence temporelle | En général horaire                                           |
| Norme suivie         | WMO, format ISH / ISD standard NOAA                          |

### 🔗 Références officielles

- NOAA ISD Dataset: [https://www.ncei.noaa.gov/data/global-hourly/](https://www.ncei.noaa.gov/data/global-hourly/)
- Format technique ISD (PDF): [https://www.ncei.noaa.gov/pub/data/noaa/ish-format-document.pdf](https://www.ncei.noaa.gov/pub/data/noaa/ish-format-document.pdf)


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

## Fiche Source : Open-Meteo

### Type de données
- **Données modélisées**, issues de modèles numériques météo open source.
- Fournies par l’API **Open-Meteo**, qui intègre et réinterprète plusieurs jeux de données publics.
- ❗ Ce ne sont **pas** des données observées, mais **des prévisions ou des réanalyses interpolées** spatialement sur grille.

### Modèles utilisés
- Selon la variable, l’heure et la région, Open-Meteo agrège les données de :
  - **ICON** (modèle allemand DWD, haute résolution)
  - **ECMWF** (HRES)
  - **GFS** (modèle global NOAA)
- Pour l’historique (`historical weather`), Open-Meteo utilise des réanalyses ou des prévisions archivées (non précisées avec exactitude dans la doc publique).

### Hauteur de mesure
- Toutes les données de vent sont **standardisées à 10 mètres au-dessus du sol**, conformément aux conventions WMO.
- ⚠️ Il s’agit de **valeurs modélisées à 10 m**, **pas de mesures instrumentées**.

### Fréquence temporelle et période de moyennage
- Fréquence des données : **horaire**.
- `windspeed_10m` : **vent moyen horaire** (correspond à la valeur de vent moyen sur 1 heure issue du modèle météo).
- `windgusts_10m` : **rafale modélisée maximale sur l’heure**.

### Rafales (`windgusts_10m`)
- Représente le **vent rafale modélisé maximal** sur l’heure.
- Peut sous-estimer les pics réels car dépend de la paramétrisation du modèle et de la résolution horizontale (~10–20 km).

### Direction du vent
- `winddirection_10m` : donnée en **degrés azimutaux**, direction **d’origine du vent** :
  - `0°` = Nord, `90°` = Est, etc.
- Moyenne horaire issue du modèle.

### Variables typiques

| Variable            | Description                                  | Unité |
|---------------------|----------------------------------------------|-------|
| `windspeed_10m`     | Vent moyen horaire à 10 m                    | m/s   |
| `windgusts_10m`     | Rafale max horaire modélisée à 10 m          | m/s   |
| `winddirection_10m` | Direction moyenne horaire modélisée à 10 m   | degrés|

### Résumé technique

| Élément              | Détail                                                   |
|----------------------|----------------------------------------------------------|
| Source               | Open-Meteo API                                           |
| Type                 | Modélisation numérique / réanalyse                       |
| Hauteur              | 10 m (standardisée)                                      |
| Vent moyen           | Moyenne horaire modélisée (`windspeed_10m`)              |
| Rafales              | Rafale horaire max modélisée (`windgusts_10m`)           |
| Direction            | Direction azimutale moyenne sur 1h (`winddirection_10m`) |
| Fréquence temporelle | Horaire                                                  |
| Norme suivie         | WMO (hauteur), mais modèle → non conforme aux mesures    |

### ⚠️ Pourquoi Open-Meteo peut surestimer les vents moyens ?

Même si Open-Meteo fournit des valeurs de vent "moyennes", elles peuvent parfois **dépasser celles mesurées en station sur 10 minutes**. Plusieurs raisons techniques expliquent cela :

1. **Exposition théorique du modèle** : la maille de modèle (~10 km) représente souvent un terrain dégagé, non abrité par des obstacles locaux (relief, forêts, bâtiments). Cela peut générer des valeurs plus élevées qu'une station réelle exposée différemment.

2. **Topographie idéalisée** : les modèles utilisent une moyenne de l'altitude/rugosité, ce qui peut surévaluer localement l’intensité du vent.

3. **Interpolation temporelle** : les modèles donnent une valeur unique par heure. Il peut s’agir d’un pic ou d’une valeur non parfaitement moyennée, selon l’étape du modèle.

4. **Définition du vent moyen** : ce n’est pas forcément une moyenne glissante vectorielle (comme en station) mais une sortie modélisée directe, parfois plus proche d’un "instantané représentatif".

5. **Absence de microclimat** : contrairement aux stations réelles, le modèle ne tient pas compte des phénomènes locaux à petite échelle (zone urbaine, vallée fermée, etc).

### 🔗 Références officielles

- Open-Meteo Docs: [https://open-meteo.com/en/docs](https://open-meteo.com/en/docs)
- API Historical Weather: [https://open-meteo.com/en/docs/historical-weather-api](https://open-meteo.com/en/docs/historical-weather-api)


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

## 4. ERA5 – Données de réanalyse ECMWF

🔗 **Lien Copernicus CDS** : [https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels)

## Fiche Source : ERA5 (Copernicus / ECMWF)

### Type de données
- **Réanalyses climatiques modélisées**, produites par le **Centre Européen pour les Prévisions Météorologiques (ECMWF)**.
- Mise à disposition via le programme **Copernicus Climate Data Store (CDS)**.
- Combinaison d’un modèle numérique de prévision du temps (IFS) et de l’assimilation de millions d’observations (stations, satellites, ballons…).

---

### Hauteur de mesure
- Les vents sont fournis à **10 mètres au-dessus du sol** :
  - `10m_u_component_of_wind`
  - `10m_v_component_of_wind`
- Ces composantes sont interpolées à partir des niveaux du modèle, sur une surface moyenne.

---

### Fréquence temporelle et moyenne
- **Données horaires**, soit une résolution temporelle de **1 heure**.
- Les vitesses sont dérivées de :  
  `windspeed = sqrt(u² + v²)`
- Ces valeurs représentent une **moyenne spatiale sur une maille de 31 km** (≈ area average).

---

### Rafales (`10m_wind_gust_since_previous_post_processing`)
- Variable dédiée aux rafales, parfois absente selon les jeux de données.
- Représente le **maximum estimé depuis la dernière étape de post-traitement** (~1 heure).
- ❗ Ne correspond **pas toujours** à la définition WMO (rafale sur 3 secondes).

---

### Direction du vent
- Calculée à partir des composantes U/V :  
  `direction = arctan2(-u, -v)`
- Direction **d’origine du vent**, en degrés azimutaux (0° = nord, 90° = est...).

---

### Variables typiques

| Variable                             | Description                         | Unité |
|--------------------------------------|-------------------------------------|-------|
| `10m_u_component_of_wind`            | Composante est-ouest du vent       | m/s   |
| `10m_v_component_of_wind`            | Composante nord-sud du vent        | m/s   |
| `10m_wind_gust_since_previous_post_processing` | Rafale maximale sur l'heure | m/s   |

---

### Résumé technique

| Élément               | Détail                                              |
|----------------------|-----------------------------------------------------|
| Source               | ERA5 via Copernicus CDS                             |
| Type                 | Données modélisées – réanalyse                      |
| Résolution temporelle| 1 heure                                             |
| Résolution spatiale  | ~31 km (ERA5-Land : ~9 km)                          |
| Hauteur              | 10 m au-dessus du sol                               |
| Vent moyen           | Moyenne horaire sur grille modélisée                |
| Rafales              | Max depuis dernier post-processing (~1 h)           |
| Direction            | Azimut (origine du vent), calculée à partir de U/V |

---

### ⚠️ Limitations et précisions (d'après ECMWF)

> **« Yes, the underestimation is related to the limited spatial resolution of ERA5, and the fact that ERA5 represents an area average. »**  
> — *Hans Hersbach (ECMWF)*

- **ERA5 a tendance à lisser les vents extrêmes**, notamment les rafales locales.
- Les **stations donnent une info ponctuelle**, tandis qu’ERA5 fournit une **valeur moyenne sur un pixel de 31 km × 31 km**.
- Il est **possible** (et conseillé) d’utiliser une **correction empirique** basée sur des comparaisons entre ERA5 et stations.
- **ERA6 est en préparation**, avec meilleure résolution (mais prévue pour ~fin 2026).

---

### Références officielles

- Copernicus Climate Data Store: [https://cds.climate.copernicus.eu/](https://cds.climate.copernicus.eu/)
- ERA5 documentation: [https://confluence.ecmwf.int/display/CKB/ERA5](https://confluence.ecmwf.int/display/CKB/ERA5)
- Réponse officielle ECMWF (Hans Hersbach, juin 2025)


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
---

## 5. NASA POWER – Données modélisées issues de la NASA

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

## Fiche Technique – Métadonnées des Stations Météo

### Pourquoi les métadonnées sont essentielles
Les valeurs de vent mesurées ou modélisées dépendent fortement :
- de **la hauteur de mesure**
- de **l’environnement de la station** (terrain, obstacles, exposition)
- de **la qualité instrumentale**
==> Sans ces métadonnées, toute comparaison entre sources est biaisée.

---

### Métadonnées typiques à collecter (si disponibles)

| Champ                    | Description                                                                |
|--------------------------|----------------------------------------------------------------------------|
| `station_id`             | Identifiant unique de la station (WMO, NOAA ISD, Meteostat…)               |
| `name`                   | Nom de la station                                                          |
| `latitude / longitude`   | Coordonnées géographiques                                                  |
| `elevation`              | Altitude de la station au-dessus du niveau de la mer                       |
| `anemometer_height`      | Hauteur de l’anémomètre au-dessus du sol (souvent 10 m par convention)     |
| `station_type`           | Type de station (aéroport, base militaire, automatique, etc.)              |
| `data_availability`      | Période de fonctionnement / couverture temporelle                          |
| `variables_available`    | Vent moyen, rafales, direction, température, etc.                          |
| `distance_to_site`       | Distance entre la station et le site d’étude                               |
| `roughness_context`      | Contexte du terrain : urbain, rural, montagne, littoral, forêt, etc.       |
| `exposure_score`         | Évaluation qualitative ou semi-quantitative de l’exposition au vent        |

---

### Problèmes fréquemment rencontrés

| Problème                               | Explication                                                                 |
|----------------------------------------|-----------------------------------------------------------------------------|
| Hauteur d’anémomètre inconnue          | Hypothèse par défaut : 10 m (norme WMO), mais peut varier (6–15 m)          |
| Station abritée                        | Influence des arbres, bâtiments, ou micro-relief → sous-estimation du vent  |
| Environnement non documenté            | Pas d’indication sur rugosité, exposition, type de terrain                  |
| Variables absentes / incomplètes       | `GUST` ou `DRCT` parfois manquants, surtout dans les fichiers anciens       |
| Position imprécise                     | Latitude/longitude tronquées à 2 décimales → incertitudes sur la distance   |
| Type de station inconnu                | Peut influencer la calibration et l’entretien des capteurs                  |

---

### Rugosité et contexte terrain – comment l’évaluer ?

#### 1. Observation visuelle (Google Earth, Street View)
- Permet de repérer : forêts, zones urbaines, obstacles, orientation dominante
- Peut être codée en classes de rugosité (`z0`) selon la norme **EN 1991-1-4** (Eurocode)

| Type de terrain          | Rugosité `z0` approx.  | Exemples                             |
|--------------------------|------------------------|--------------------------------------|
| Mer / lac                | 0.0002 – 0.003         | océan, grandes surfaces d’eau        |
| Terrain ouvert plat      | 0.01 – 0.03            | désert, champs, plaine dégagée       |
| Zone semi-ouverte        | 0.05 – 0.1             | prairies, hameaux, villages isolés   |
| Suburbain / urbain bas   | 0.2 – 0.5              | lotissements, petites villes         |
| Centre urbain dense      | 1.0 – 2.0              | grandes villes, gratte-ciel          |
| Forêt / montagne         | > 0.5                  | forêt dense, collines, massifs       |

#### 2. Données satellites ou open data
- CORINE Land Cover, Copernicus, ou SRTM peuvent être utilisés pour estimer l’usage du sol.
- Calcul automatique possible à terme via API ou raster GIS.

#### 3. Approche qualitative (dans WindDatas)
- Pour chaque station, on peut coder une **note d’exposition** de 1 à 5 :
  - 5 = station très exposée (plateau, littoral)
  - 1 = station très abritée (vallée encaissée, forêt, centre-ville)

---

### À intégrer dans WindDatas

Pour chaque station (Meteostat, NOAA, etc.), il est recommandé de stocker :
- La **hauteur de mesure (si connue)**, ou `10 m` par défaut
- La **distance au site**
- Le **type de terrain / rugosité estimée**
- Les **variables disponibles** (pour savoir si comparaison possible)
- Une **note d’exposition (1–5)** et un champ texte libre pour commentaires

---

### Objectif final

> Fournir pour chaque station une **fiche descriptive claire**, avec :
> - Métadonnées techniques
> - Données manquantes ou incertaines
> - Estimations environnementales
> - Fiabilité de la station pour l’analyse du vent
