# Template CLAUDE.md pour nouveaux projets AIMA

Utiliser ce template lors de la création d'un nouveau projet dans ~/Pipeline/.
Copier et adapter les sections pertinentes.

```markdown
# {Nom du projet}

{Description en 1-2 lignes : quoi, pourquoi, pour qui}

## Tech Stack

- **{Langage principal}** — {version}
- **{Framework}** — {version}
- **{Base de données}** — {si applicable}
- **Docker** — image `blipinskiaima/{nom}:{version}`

## Position dans le pipeline AIMA

{Schéma ASCII montrant en amont / en aval}

**En amont** : {quels projets/données alimentent ce projet}
**En aval** : {quels projets/outils consomment les sorties}

## Structure

{Arborescence des dossiers/fichiers principaux}

## Commandes

{Commandes principales : lancer, tester, déployer}

## Conventions

- {Convention 1}
- {Convention 2}

## Points critiques

{NEVER, ALWAYS, CRITICAL — règles spécifiques au projet}
```
