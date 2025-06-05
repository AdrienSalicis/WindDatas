# Workflow Git – Projet WindDatas

Ce fichier décrit les règles de contribution, la gestion des branches et les bonnes pratiques Git à appliquer sur le projet WindDatas.

---

## Structure des branches

| Branche         | Rôle                                      |
|-----------------|--------------------------------------------|
| `main`          | Version stable publiée (taguées)           |
| `dev`           | Développement actif, fusion des features   |
| `feature/...`   | Nouvelles fonctionnalités spécifiques      |
| `bugfix/...`    | Corrections de bugs isolés                 |
| `docs/...`      | Modifications de documentation             |

---

## Convention de commits

Utiliser les préfixes suivants :

- `feat:` pour une nouvelle fonctionnalité
- `fix:` pour une correction de bug
- `chore:` pour des tâches mineures (ex : mise à jour de doc)
- `refactor:` pour une réorganisation sans ajout de fonctionnalité
- `test:` pour les tests unitaires ou correctifs
- `docs:` pour la documentation pure

Exemples :

```bash
git commit -m "feat: ajout du fetcher MERRA-2"
git commit -m "fix: gestion des dates manquantes dans Meteostat"
git commit -m "docs: ajout d'un lien vers le globe interactif"
```

---

## Cycle de développement standard

1. Cloner le projet
2. Créer une nouvelle branche depuis `dev`
   ```bash
   git checkout dev
   git checkout -b feature/nom-fonctionnalite
   ```
3. Développer, tester localement
4. Committer puis push :
   ```bash
   git push -u origin feature/nom-fonctionnalite
   ```
5. Ouvrir une Pull Request vers `dev`
6. Après validation, fusionner dans `dev`
7. Fusionner `dev` → `main` uniquement pour une version taguée

---

## Versionnage

Suivi sémantique :

- `v1.1.0` → ajout de fonctionnalités majeures
- `v1.1.1` → correctifs mineurs
- `v2.0.0` → changements de structure ou rétrocompatibilité rompue

Les versions stables sont marquées avec :
```bash
git tag v1.1.0
git push origin v1.1.0
```

---

## Travail collaboratif

- Utiliser les Issues pour signaler ou planifier les tâches
- Rester aligné avec la roadmap
- Documenter les contributions

