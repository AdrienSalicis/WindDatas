
WindDatas – Comparaison de données météorologiques

📌 Objectif du projet :
Ce projet a pour but de comparer les vitesses de vent observées (via des stations météo) et modélisées (via des API comme ERA5, OpenMeteo) pour différents sites dans le monde.

📁 Arborescence du projet :
- script.py : script principal
- modules/ : tous les fichiers Python modulaires (meteostat, era5, comparateur, etc.)
- modele_sites.csv : liste des sites étudiés
- environment.yml : fichier pour créer un environnement conda propre
- run_winddatas.bat : fichier batch pour lancer le projet intelligemment
- data/ : contient les données téléchargées (par site)
- .meteostat/ : cache local utilisé par la bibliothèque Meteostat

🛠️ Installation propre (avec Conda) :
1. Installer [Anaconda](https://www.anaconda.com/products/distribution)
2. Ouvrir Anaconda Prompt
3. Aller dans le dossier du projet :
   cd "chemin\vers\le\dossier\WindDatas"
4. Créer l’environnement :
   conda env create -f environment.yml
5. Activer l’environnement :
   conda activate winddatas

🚀 Lancement :
1. Double-cliquer sur le fichier `run_winddatas.bat`
2. Ce fichier :
   - Vérifie l’environnement conda
   - Vérifie les bibliothèques Python nécessaires
   - Te demande si tu veux lancer le script
   - Lance `script.py`

📦 Dépendances :
Elles sont toutes listées dans le fichier `environment.yml`. Les modules installés incluent :
- numpy==1.26.4
- pandas
- matplotlib
- meteostat (via pip)
- cdsapi
- python-docx
- geopy
- xarray
- netCDF4
- plotly

🐛 En cas d'erreur liée à numpy._core.numeric :
Il faut supprimer le cache local de Meteostat :
1. Fermer le script
2. Supprimer le dossier : C:\Users\<TON NOM>\.meteostat

🧪 Script de test (facultatif) :
Un fichier `test_env.py` peut être créé pour vérifier les imports.

🗒️ Auteur : Adrien Salicis
📅 Dernière mise à jour : 2025-05-07
