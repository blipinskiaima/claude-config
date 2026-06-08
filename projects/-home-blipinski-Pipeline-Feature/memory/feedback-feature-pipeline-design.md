---
name: feedback-feature-pipeline-design
description: Préférences de design de Boris pour le pipeline scripts/ de Feature/ — simplicité radicale des scripts de sélection + args explicites sans état caché
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b3ac9798-fbc1-465e-a927-aad831034f9b
---

# Préférences design — pipeline Feature/

## 1. Scripts de sélection de cohorte = très simples, vraiment

`select_cohort.py` (et tout script de sélection de données dans Feature/) doit rester
**très simple** : une requête SQL paramétrée par des filtres, point. Pas d'abstraction
spéculative, pas de couche de config, pas de classes inutiles.

**Why:** Boris l'a demandé explicitement et avec insistance (« le script doit être très
simple vraiment, c'est une requête SQL à partir de filtres ») lors du design de
l'extraction `select_cohort.py` (2026-06-08). Le mode baseline/défaut est le cœur et doit
rester trivial à lire.
**How to apply:** quand tu implémentes/refactorises un script de data-selection ici,
résiste à la tentation d'ajouter de la généricité. Le compilateur `filter_spec → SQL`
arbitraire (mode dashboard) est explicitement **différé** — ne le construis pas tant que
ce n'est pas demandé. Voir [[pipeline-3-etapes]].

## 2. Args explicites, zéro état caché

Pour les nouveaux liens entre étapes du pipeline, Boris préfère **passer les chemins en
arguments CLI explicites** plutôt que via un fichier d'état implicite (`run.env`).

**Why:** au design de l'orchestration select_cohort→train (2026-06-08), il a choisi
« full explicite (`--cohort`), zéro état caché » plutôt que le lien implicite via run.env.
**How to apply:** privilégie `--arg chemin` pour les nouveaux seams. `run.env` reste
toléré pour le lien existant train→eval→publish (ne pas le casser sans raison), mais ne
l'étends pas aux nouveaux liens.
