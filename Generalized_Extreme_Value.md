
# Analyse des Lois d’Extrêmes – GEV, Gumbel, Weibull et Fréchet

## 🎯 Objectif

Modéliser des **vents extrêmes** pour évaluer des valeurs critiques comme les **vents de retour 50 ans**, utiles dans les calculs de structures, parcs éoliens, etc.  
On utilise pour cela les **lois d’extrêmes**, notamment la **GEV** (Generalized Extreme Value) et ses déclinaisons.

---

## 1. Introduction à la loi des extrêmes généralisée (GEV)

La loi GEV est une famille de lois qui décrit l’asymptote de la distribution des **maxima (ou minima)** d’une série de variables aléatoires indépendantes et identiquement distribuées (i.i.d.).

### Forme générale (loi GEV)

\[
F(x) = \exp\left( -\left[ 1 + \xi \cdot \left( \frac{x - \mu}{\sigma} \right) \right]^{-1/\xi} \right), \quad \text{si } 1 + \xi \cdot \left( \frac{x - \mu}{\sigma} \right) > 0
\]

- \( \mu \) : paramètre de localisation
- \( \sigma > 0 \) : paramètre d’échelle
- \( ξ \) : paramètre de forme (clé pour différencier les lois)

---

## 2. Les trois cas de la loi GEV

| Loi        | Valeur de \( ξ \) | Comportement de la queue   | Cas d’application typique         |
|------------|-------------------|----------------------------|-----------------------------------|
| **Gumbel** | \( ξ = 0 \)       | Exponentielle décroissante | Rafales de vent, températures     |
| **Fréchet**| \( ξ > 0 \)       | Queue lourde               | Crues, séismes, valeurs extrêmes  |
| **Weibull**| \( ξ < 0 \)       | Queue bornée               | Résistance de matériaux, vitesses max limitées |

---

## 3. Détail des lois individuelles

### Loi de Gumbel (\( ξ = 0 \))

- Distribution classique des maxima
- Pas de valeur maximale théorique
- Fonction de densité :
  \[
  f(x) = \frac{1}{\beta} \exp\left( -\left( \frac{x - \mu}{\beta} + e^{- \frac{x - \mu}{\beta}} \right) \right)
  \]

- Quantile de retour pour une période \( T \) :
  \[
  v_T = \mu - \beta \cdot \ln(-\ln(1 - 1/T))
  \]

---

### Loi de Fréchet (\( ξ > 0 \))

- S’applique aux distributions à **queue lourde**
- Valeurs extrêmes très grandes possibles
- Moins adaptée au vent sauf cas ultra spécifiques

---

### Loi de Weibull extrême (\( ξ < 0 \))

- Queue **bornée** : valeur maximale théorique
- Bon pour décrire une limite physique supérieure
- Plus adaptée à la **résistance** ou au vent si on observe un plafond physique clair

---

## 4. Quand utiliser quelle loi ?

| Donnée              | Loi recommandée | Justification technique                       |
|---------------------|------------------|-----------------------------------------------|
| Rafales extrêmes    | **Gumbel**        | Maxima annuels/journaliers, queue expo.       |
| Vitesse de vent moyenne | **Weibull**   | Distribution continue, production éolienne    |
| Phénomènes ultra rares (crues, séismes) | **Fréchet** | Valeurs rares et extrêmes, queue lourde      |

---

## 5. Ajustement en Python

```python
from scipy.stats import gumbel_r, genextreme

# Gumbel
params = gumbel_r.fit(data)
v_50 = gumbel_r.ppf(1 - 1/50, *params)

# GEV général
gev_params = genextreme.fit(data)
xi = gev_params[0]  # le paramètre ξ
```

---

## 6. Visualisation de la période de retour

La période de retour est liée à la **probabilité de non-dépassement** :

\[
F(x) = 1 - \frac{1}{T}
\]

On calcule donc \( x \) tel que : 

\[
x = F^{-1}\left(1 - \frac{1}{T}\right)
\]

---

## 7. Conclusion

- La **loi GEV** permet de tester la validité de Gumbel via l’estimation du paramètre \( \xi \)
- Pour les **vents extrêmes**, on utilise presque toujours :
  - **Gumbel** (rafales extrêmes)
  - **Weibull** (vent moyen classique)
- Vérifier la pertinence de la loi utilisée permet d’améliorer la **fiabilité des prédictions**

