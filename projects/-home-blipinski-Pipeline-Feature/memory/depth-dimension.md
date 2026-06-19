---
name: depth-dimension
description: "La dimension depth (0.25/0.5/1/2X) est live à l'éval dans Feature/ ET Aima-Tower — sémantique, gotchas non-évidents"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5d51cf45-2c21-4a60-80fe-edddc40c6ab0
---

# Dimension depth à l'évaluation (livrée 2026-06-18)

Nouvelle dimension d'éval **en plus de `target_spec`** : décline sens/spéc à `depth >= 0.25 / 0.5 / 1 / 2`. Implémentée end-to-end sur 2 repos.

**Feature/** (`main` @ `1a90cac`) :
- `select_cohort_*.py` exportent `depth` (OUTPUT_COLS) ; `train.R` la porte en passthrough dans `scores.csv` ; `eval.R --depths "0.25 0.5 1 2"` ajoute une colonne `depth` à `eval_kpis.csv` (lignes ×4 : depth × target_spec × combo × unité). `main.sh` câble `--depths`.
- Design + plan : `docs/superpowers/specs/2026-06-18-depth-dimension-eval-design.md` et `docs/superpowers/plans/2026-06-18-depth-dimension-eval.md`.

**Aima-Tower** (`main` @ `5255ac9`) : `/exploration-beta` a un `<select>` Profondeur (≥0.25×…≥2×) à côté de Spécificité cible. Param `depth` dans `feature_service`/`feature_curves`/router `exploration_beta` + hooks `useFeatureResult`/`useBestCombos`.

## Sémantique (Option 1 — choix Boris)
Pour chaque `d`, le **seuil est recalculé** sur les healthy train `depth>=d` (pas figé), sens/spéc sur la sous-cohorte `depth>=d`. Caveat : peu de healthy à 2X (speedvac_no=29, yes=145) → seuil quantifié, lire à haute depth avec prudence.

## Gotchas non-évidents
- **Cohorte train INCHANGÉE** (plancher 0.25) ; les scores XGBoost sont **bit-identiques** : `depth` est un passthrough, aucun ré-entraînement. (Prouvé par diff golden vs new.)
- **Tower : 2 consommateurs.** Les *tables* (best_combos/legacy_csv) lisent `eval_kpis.csv` → filtre `depth == valeur`. Les *courbes Plotly* sont **recalculées côté Tower depuis `scores.csv`** → filtre `depth >= valeur` avant `_curves_core`. ⇒ `depth` doit être **par-sample dans `scores.csv`**, pas seulement dans `eval_kpis.csv`.
- **`result/` est gitignoré** (`.gitignore:33`) dans Feature/ → pas committé, régénérable via `main.sh`. La Tower le lit sur disque (`feature_root/result/speedvac_{no,yes}/`).
- Rétrocompat Tower : filtre depth ignoré si la colonne `depth` est absente du CSV (ancien format).

Voir [[pipeline-3-etapes]], [[target-specificity]].
