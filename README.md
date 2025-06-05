# WindDatas – Analyse des données de vent observées et modélisées

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

WindDatas est un projet Python modulaire permettant d’analyser et de comparer des données de vent issues de stations météo (observées) et de modèles climatiques ou API météo (modélisées). Le but est d'évaluer la fiabilité des modèles en s'appuyant sur des données historiques réelles.

## Objectifs

- Récupérer automatiquement des données météo (vents) pour plusieurs sites à travers le monde.
- Comparer les données modélisées (OpenMeteo, ERA5, NASA POWER) aux données observées (Meteostat, NOAA).
- Générer des graphiques comparatifs, des statistiques et des rapports automatisés.
- Permettre une étude approfondie via des notebooks scientifiques.

## Fonctionnalités

- Sélection automatique des deux stations Meteostat les plus proches de chaque site.
- Récupération des données pour une période donnée.
- Génération de fichiers CSV pour chaque source et chaque site.
- Analyse statistique comparative (écarts, corrélations, jours extrêmes, direction moyenne).
- Génération de rapports `.docx` par pays.
- Visualisation interactive des sites et stations sur un globe HTML.

## Structure du projet

```
WindDatas/
├── data/                  # Fichiers générés automatiquement (non suivis par Git)
├── modules/               # Modules Python (fetchers, comparateur, graphiques, etc.)
├── notebooks/             # Notebooks d’analyse statistique
├── tests/                 # Tests unitaires
├── script.py              # Script principal du projet
├── site_enricher.py       # Enrichissement des métadonnées des sites
├── modele_sites.csv       # Liste des sites étudiés
├── environment.yml        # Dépendances pour Conda
├── requirements.txt       # Dépendances pip
├── run_winddatas.bat      # Script de lancement Windows
├── LICENSE                # Licence du projet (MIT)
└── README.md              # Ce fichier
```

## Installation

### Via Conda (recommandé)

```bash
conda env create -f environment.yml
conda activate winddatas
```

### Via pip (optionnel)

```bash
pip install -r requirements.txt
```

## Utilisation

Lancer le projet via :

```bash
python script.py
```

Ou avec le fichier batch Windows :

```bash
run_winddatas.bat
```

Une interface vous demandera de saisir les dates de début et de fin, puis les données seront automatiquement récupérées, analysées et exportées.

## Tests

Pour exécuter tous les tests unitaires :

```bash
python -m unittest discover -s tests
```

## Données générées

Pour chaque site, un dossier `data/NOM_SITE/` est créé avec :

- Données CSV de chaque source
- Graphiques de comparaison (distribution, radar, etc.)
- Rapport `.docx` regroupé par pays
- Visualisation globe HTML

## Sources de données utilisées

- Meteostat
- Open-Meteo
- ERA5 - Copernicus CDS
- NASA POWER
- NOAA ISD

## Licence

Ce projet est sous licence MIT. Il est librement réutilisable, modifiable et redistribuable avec mention de l’auteur initial. Cela permet à d’autres développeurs ou chercheurs de le reprendre et l’enrichir à l’avenir.

## Contribuer

Voir le guide de contribution : [CONTRIBUTING.md](CONTRIBUTING.md)

## Auteurs

Projet initial développé par Adrien Salicis  
Organisation : Ciel & Terre International  
Contact : adrien.salicis@cieletterre.net, adrien.salicis@icloud.com
