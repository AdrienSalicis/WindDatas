# WindDatas – Analyse des données de vent observées et modélisées

\
\
\


WindDatas est un projet Python modulaire et évolutif qui permet d’analyser, comparer et valider des données de vent issues de **stations météo (observées)** et de **modèles climatiques ou API météo (modélisées)**. Son objectif est de fournir une évaluation rigoureuse et transparente des modèles sur la base de données historiques fiables.

---

## Objectifs

- Récupération automatisée des données météo (vents) pour de nombreux sites dans le monde.
- Comparaison rigoureuse des données observées (NOAA, Meteostat) et modélisées (ERA5, NASA POWER, OpenMeteo, MERRA-2, Visual Crossing).
- Analyse statistique complète avec génération de rapports.
- Visualisation interactive des sites et des stations sur un globe.
- Étude approfondie grâce à des notebooks scientifiques détaillés et pédagogiques.

---

## Fonctionnalités principales

- Sélection automatique des deux stations les plus proches (NOAA, Meteostat) avec distances calculées.
- Récupération des métadonnées des stations (altitude, hauteur anémomètre, contexte terrain).
- Extraction des extrêmes journaliers (rafales max) depuis les données horaires NOAA ISD.
- Interface Tkinter pour définir dynamiquement la période d’étude.
- Téléchargement asynchrone et robuste des données ERA5 avec journalisation des mois déjà traités.
- Modules dédiés pour chaque source, activables ou désactivables dynamiquement.
- Génération de rapports Word structurés par pays et sites.
- Exports CSV clairs et organisés.
- Visualisation interactive sur globe HTML des sites et stations associées.
- Notebooks d’analyse avancés : Weibull, Gumbel, roses des vents, radar directionnel, statistiques détaillées.
- Support multi-stations par site (fichiers meteostat1\_x.csv, noaa\_station2\_x.csv, etc.).
- Architecture modulaire avec tests unitaires dans le dossier `tests/`.

---

## Structure du projet

```
WindDatas/
├── script.py
├── modele_sites.csv
├── data/
│   └── <ref_site>/
├── modules/
│   ├── meteostat_fetcher.py
│   ├── noaa_isd_fetcher.py
│   ├── era5_fetcher.py
│   ├── openmeteo_fetcher.py
│   ├── visualcrossing_fetcher.py
│   ├── merra2_fetcher.py
│   ├── meteo_france_fetcher.py
│   ├── source_manager.py
│   ├── comparator.py
│   ├── stats_calculator.py
│   ├── merger.py
│   └── tkinter_ui.py
├── notebooks/
│   └── analyse_vent_TEMPLATE_FINAL_CLEAN_TECHNIQUE.ipynb
├── tests/
├── requirements.txt
├── environment.yml
├── run_winddatas.bat
└── README.md
```

---

## Schéma global du workflow

```
    modele_sites.csv
            │
            ▼
        script.py
            │
 ┌─────────┬─────────┬─────────┐
 ▼         ▼         ▼         ▼
NOAA   Meteostat   ERA5   OpenMeteo/NASA
  │        │         │         │
  ▼        ▼         ▼         ▼
 CSV    CSV1/2     CSV      CSV
            │
            ▼
   Analyse statistique
            │
            ▼
Rapports Word, Graphiques, Globe HTML
```

---

## Installation

### Avec Conda (recommandé)

```
conda env create -f environment.yml
conda activate winddatas
```

### Avec pip (optionnel)

```
pip install -r requirements.txt
```

---

## Utilisation

Lancer le projet :

```
python script.py
```

Ou via Windows :

```
run_winddatas.bat
```

- Interface Tkinter pour sélectionner les dates.
- Données récupérées et analysées automatiquement.
- Export CSV et Word organisés.

---

## Données générées

Pour chaque site dans `data/<NOM_SITE>/` :

- Données CSV (toutes sources)
- Graphiques (histogrammes, Weibull, radar, roses des vents)
- Rapport Word par pays
- Globe HTML interactif

---

## Sources de données intégrées

**Observées :**

- NOAA ISD (2 stations les plus proches, distances calculées)
- Meteostat (2 stations les plus proches, métadonnées enrichies)

**Modélisées :**

- ERA5 (rafales en commentaire configurable)
- Open-Meteo
- NASA POWER
- MERRA-2 (désactivable)
- Visual Crossing (désactivable)
- Meteo-France (intégré dans source\_manager)

---

## Notebooks inclus

- Analyse statistique détaillée des vents
- Ajustements Weibull/Gumbel
- Roses des vents
- Comparaisons directionnelles sur radar
- Détection des valeurs aberrantes

---

## Licence

MIT – Libre d'utilisation et de modification avec attribution.

---

## Documents du projet

- [Roadmap du projet](ROADMAP.md)
- [Workflow Git](WORKFLOW.md)
- [Guide de contribution](CONTRIBUTING.md)

---

## Auteurs

Projet initial : **Adrien Salicis**\
Organisation : **Ciel & Terre International**\
Contact : [adrien.salicis@cieletterre.net](mailto\:adrien.salicis@cieletterre.net), [adrien.salicis@icloud.com](mailto\:adrien.salicis@icloud.com)

