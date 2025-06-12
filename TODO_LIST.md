# État d’Avancement – Point_BLB_LME_SCA.md

## ✅ Réalisé

### 1. Données et sources météo
- ✔️ **Meteostat** : fiche complète (hauteur ~10 m, vent sur 10 min, rafales sur 3 s si dispo)
- ✔️ **Open-Meteo** : fiche complète (vent horaire modélisé, rafales modélisées, question en attente de réponse)
- ✔️ **NOAA ISD** : fiche complète (vent moyenné sur 2 min, rafales sur 5 s)
- ✔️ **ERA5** : fiche rédigée + réponse ECMWF intégrée (aire moyenne 31 km, sous-estimation documentée)
- ✔️ Identification des sources : GFS, ERA5, MERRA-2, etc. intégrées

### 2. Visualisations
- ✔️ Roses des vents discutées
- 🛠️ Génération semi-automatisée en notebook
- 📈 Scripts partiellement présents

### 3. Analyse statistique
- ✔️ **Weibull** : implémentée avec MLE
- ✔️ **Gumbel** : amorcée, extrapolation mentionnée
- ⚠️ Période de retour intégrée mais non uniformisée

### 4. Comparaison inter-sources
- ✔️ NOAA vs Meteostat
- ✔️ ERA5 intégré
- ✔️ NASA POWER & MERRA-2 prévus
- 🛠️ `comparator.py` restructuré (orchestrateur + modules)

### 5. Fiches et présentations
- ✔️ Fiches `.docx` et `.md` pour les sources météo
- 🛠️ Présentation type par site à standardiser

---

## À faire

### 1. Métadonnées des stations
- Récupérer hauteur anémomètre (via API ou CSV enrichi)
- 🛠️ Ajouter contexte terrain, type station, exposition

### 2. Fiches techniques par site
- ❌ À systématiser :
  - Description du site
  - Données météo utilisées
  - Résultats statistiques
  - Graphiques comparatifs

### 3. Données incomplètes et qualité
- ⚠️ Calculer taux de couverture (% de jours mesurés)
- ⚠️ Gérer les valeurs manquantes (NA, -9999)
- ❓ Clarifier les méthodes de calcul RP (toutes directions)

### 5. Rugosité et exposition
- Évaluation semi-auto reportée après la présentation
- Approche OSM / raster à développer

### 6. Global Wind Atlas
- Pas encore intégré
- Idée : croisement potentiel éolien + contexte terrain

---

## Synthèse TODO Priorisée

| Priorité | Action                                                                | Statut     |
|----------|-----------------------------------------------------------------------|------------|
| 🔴       | Fiches Open-Meteo, ERA5, NOAA avec sources                            | ✔️ Fait       |
| 🔴       | Réponse ECMWF (Hans Hersbach)                                         | ✔️ Fait       |
| 🔴       | Slide de synthèse métadonnées                                         | 🟡 À faire    |
| 🟠       | Taux de couverture, valeurs manquantes, RP                            | ❌ À faire    |
| 🟠       | Génération des fiches par site                                        | 🟡 Partiel    |
| 🟢       | Rugosité terrain automatique (z0)                                     | ⏳ Reporté    |
| 🟢       | Intégration Global Wind Atlas                                         | ⏳ En attente |

---

*Dernière mise à jour : 2025-06-12*
