# ✅ Retours et Points d’Amélioration – BLB, LME, SCA

## 1. Données et Sources Météo

### LME – Étude Longchamps
- Analyser les données issues de LME sur le site de Longchamps.
- Comparaison entre OpenMeteo et Météo France.

### Meteostat
- Vérifier la **hauteur d’anémomètre** des stations utilisées.
- Clarifier :
  - Vent moyen, vent de rafales
  - Durée de lissage (1h, 10 min ?)
  - Type de profil utilisé pour ramener le vent à 0.5 m

### OpenMeteo
- Relire en détail les définitions des variables.
- Fréquence de mesure : horaire ? 10 min ?
- Déterminer **le vent maximal à considérer**.
- Clarifier :
  - Durée du vent moyenné
  - Hauteur des mesures
  - Repère de direction utilisé

### Données Stations
- Collecter un **maximum d’informations** :
  - Nom, site, altitude, qualité, exposition
  - Fiabilité des valeurs (wind quality, flags)
  - Clarifier les sources et standards

---

## 2. Visualisations

### Roses des vents
- Largeur du faisceau, direction, fréquence, intensité.
- Générer plusieurs graphiques si nécessaire.
- Créer un **script automatique** pour les roses (cf. LME).

---

## 3. Analyse Statistique

### Général
- Analyser rapidement :
  - Dates disponibles
  - Nombre de données
  - Type de données

### Lois statistiques
- **Weibull** (cf. fichier LME) :
  - Estimation des paramètres : méthode du Maximum de Vraisemblance (MLE), comparaison Swiss Wind
- **Gumbel** :
  - Méthode RLA
  - Extrapolation 10 → 50 ans
- Ne pas utiliser une seule donnée brute sans contexte de période de retour.

### Références
- Fichier BLB avec données de crues
- Outil Vortex (logiciel de données de vents extrêmes)
- BLB + Vortex disponibles sur SharePoint

---

## 4. Comparaisons Inter-Sources

- Comparer **NOAA** vs **Meteostat**
- Étudier les données **MERRA-2** (modèle de réanalyse) vs **NASA POWER**
- Prévoir intégration des données **Copernicus ERA5**
- Identifier les **sources exactes** des modèles (ex : GFS, ERA, MERRA...)

---

## 5. Fiches & Présentations

### Fiche technique par site
- Inclure :
  - Description du site
  - Sources météo utilisées
  - Données disponibles
  - Visualisation/graphique
  - Résultats statistiques

### Présentation d’un site type
- Ajouter :
  - Photos du site
  - Résultats par source météo
  - Comparatifs visuels
  - Variabilité des paramètres (hauteur, durée, modèle météo)
  - Bilan global

---

## 6. Qualité des Données

- Taux de couverture (% de jours mesurés)
- Valeurs vides et partielles → méthode de gestion
- RP (Return Period) :
  - Demander les périodes de retour par modèle météo
  - Toutes directions confondues

---

## 7. Références supplémentaires

- **Global Wind Atlas** pour enrichir l’analyse (potentiel éolien global).

---

