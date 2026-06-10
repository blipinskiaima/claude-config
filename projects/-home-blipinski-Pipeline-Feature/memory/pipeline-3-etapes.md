---
name: pipeline-3-etapes
description: "Pipeline Feature scripts/ — select_cohort → train → eval → publish (état juin 2026, post-extraction)"
metadata: 
  node_type: memory
  originSessionId: b3ac9798-fbc1-465e-a927-aad831034f9b
---

# Pipeline Feature (juin 2026, post-extraction select_cohort)

**Pas de dossier `memory/` dans le repo** — doc projet : `CLAUDE.md`, `.claude/rules/`, `archives/`, `docs/superpowers/`.

## Flux opérationnel (orchestré par launch.sh, 4 étapes)

```
scripts/select_cohort.py  → data/cohorts/{std_N}/cohort.csv  (+ gel manifest.json/samples.tsv si inédit)
scripts/train.R --cohort  → result/{std_N}/{combo}/scores.csv  (+ run.env OUT/COHORT_REF)
scripts/eval.R            → result/{std_N}/{combo}/stratified_sensitivity.csv + PNG
scripts/feature_db.py     → feature_runs.duckdb  (cohorts + results KPIs)
```

`./main.sh "mvaf_v1,ichor_x100"` ou `./scripts/launch.sh` enchaînent select → train → eval → publish.
`./main_bench.sh` : 511 combos (pool 9 features), `COHORT` exporté une fois.

## Séparation des responsabilités (décision design 2026-06-08)

- **select_cohort.py = quelles LIGNES** (filtres+dedup+labels ; pilotable dashboard à terme). Très simple : 1 SQL paramétré. `ORDER BY unique_id` → folds/KPIs **déterministes** (l'ancien combo était non-reproductible ~±2pp).
- **train.R = quelles COLONNES** (`--cohort` lit le CSV, charge `--features` par `sample_id`, XGBoost OOF ou baseline `mvaf_only`).
- Lien **explicite `--cohort`** (pas via run.env). Voir [[feedback-feature-pipeline-design]].
- Spec/plan : `docs/superpowers/specs|plans/2026-06-08-select-cohort*`.

## Règles clés

- trace-prod **read_only** ; cohorte = preset `lung_valtech_nosv_bladder_blood` (`DEFAULT_SPEC` dans select_cohort.py, sérialisée au manifest).
- Seuil eval : `quantile(healthy, target_spec=0.95, type=1)`.
- Labels : voir [[label-definitions]] (canon juin 2026).
- Cohorte **std_359** : 359 scorés (335 labellisés = 50 H + 285 cancer ; +24 imagerie suspecte).

## Identité cohorte + gel

`COHORT_REF = std_{nrow}` (lignes label∨suspect). Gel figé `data/cohorts/{ref}/` (manifest.json + samples.tsv, versionnés) ; `cohort.csv` = working file **gitignoré**. `feature_db.py` insère en DB via `COHORT_REF` (run.env) et **ne réécrit pas** le manifest de select_cohort.

## Filtres cohorte CLI (juin 2026)

`select_cohort.py` : 1 arg par ligne de `filtres_cohorte_colonnes.tsv` (défaut = preset std_359). Référentiel features : `features_disponibles.tsv`. Blocs `probs_epic`/`probs_loyfer` expandus dans `train.R` (16+31 cols XGBoost).

## Archives repo

`archives/` : ancien grid 01–06, refresh_cohort, score_one_combo, dossier `features/`, `data/snapshots/` (+ `archives/data/`), ancien `memory/`.
