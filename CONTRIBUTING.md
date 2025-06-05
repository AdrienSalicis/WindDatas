# Guide de contribution – WindDatas

Merci de votre intérêt pour WindDatas ! Même si ce projet est personnel à ce stade, il est conçu pour être extensible et collaboratif. Voici quelques règles et bonnes pratiques pour contribuer de manière efficace.

## Pré-requis

- Python 3.9 ou supérieur
- Environnement Conda basé sur `environment.yml`
- Connaissances recommandées : API météo, traitement de données, statistiques, Git

## Installer le projet

```bash
git clone git@github.com:AdrienSalicis/WindDatas.git
cd WindDatas
conda env create -f environment.yml
conda activate winddatas
```

## Structure de branche

- `main` : branche stable, version validée
- `dev` : branche de développement général
- `feature/<nom>` : nouvelles fonctionnalités
- `bugfix/<nom>` : corrections de bugs

## Convention de commits

Utiliser des messages clairs et structurés :

- `feat:` pour une fonctionnalité
- `fix:` pour une correction de bug
- `refactor:` pour une réorganisation sans changement fonctionnel
- `test:` pour ajout ou modification de tests
- `docs:` pour la documentation

Exemples :
```bash
git commit -m "feat: ajout du fetcher MERRA-2"
git commit -m "fix: correction du bug sur la direction du vent NOAA"
```

## Tests

Avant tout push, lancer les tests :

```bash
python -m unittest discover -s tests
```

## Propositions et issues

- Utilisez les **Issues GitHub** pour signaler un problème ou proposer une amélioration.
- Toute **Pull Request** doit être testée, commentée, et pointer vers `dev`.

## Contact

Auteur : Adrien Salicis  
Email : adrien.salicis@cieletterre.net  
Organisation : Ciel & Terre International

---

Merci pour vos contributions 🙌
