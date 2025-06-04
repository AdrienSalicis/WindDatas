Wind Datas – Comparaison des données météo observées et modélisées

Ce projet Python permet de comparer les données de vent **observées par des stations météo** (ex: Meteostat, NOAA GHCN/ISD) avec celles **modélisées par des API** météo (comme OpenMeteo ou ERA5). Il est conçu pour fonctionner de manière modulaire, avec une interface Tkinter et des visualisations graphiques et interactives.

---

Objectifs du projet

- Identifier les stations météo proches de sites GPS donnés
- Récupérer des données historiques (vent moyen, rafales, direction)
- Comparer les résultats des sources observées et des modèles
- Générer :
  - des rapports automatiques (CSV, Word)
  - des graphiques (radar, ligne, globe interactif)

---

Structure attendue du projet

```
WindDatas/
│
├── script.py                  # Script principal
├── run_project.bat            # Lanceur Windows
├── requirements.txt           # Dépendances du projet
├── modele_sites.csv           # Liste des sites à traiter
├── data/                      # Résultats par site
├── modules/                   # Tous les modules Python (fetchers, comparateurs, etc.)
└── venv/                      # Environnement virtuel Python (optionnel mais recommandé)
```

---


Lancer le projet


Option 1 – Via le script `.bat`

Double-cliquer sur le fichier :
```
run_project.bat
```
> ⚠️ Assurez-vous d'avoir un environnement Python fonctionnel avec les bonnes dépendances.

---



Option 2 – Manuellement depuis le terminal

 1. Placez-vous dans le dossier du projet
```bash
cd chemin/vers/WindDatas
```

 2. (Facultatif) Activez votre environnement virtuel
```bash
venv\Scripts\activate  # Windows
```

 3. Installez les dépendances
```bash
pip install -r requirements.txt
```

 4. Lancez le script principal
```bash
python script.py
```

---

Le fichier `requirements.txt`

Voici les principales dépendances :
- `meteostat` : accès aux stations météo observées
- `requests`, `pandas`, `numpy` : pour le traitement des données
- `matplotlib`, `plotly` : visualisation
- `python-docx` : génération de rapports Word
- `geopy` : calcul des distances GPS

---

Résultats

Pour chaque site :
- Des fichiers CSV sont générés pour chaque source de données
- Un rapport Word par pays est généré dans `data/rapport_meteo.docx`
- Une carte interactive est créée dans `data/visualisation_globe.html`

---

En cas de problème

- Si `meteostat2` ou `noaa` ne génèrent pas de fichiers, cela peut venir de l'absence de données disponibles sur la période.
- Vérifiez que le terminal affiche des logs de type `[⚠️] Pas de données pour ...`.

Bon vent ! 💨