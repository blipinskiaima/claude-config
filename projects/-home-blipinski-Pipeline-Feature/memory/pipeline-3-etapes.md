---
name: pipeline-3-etapes
description: Pipeline Feature standardisé scripts/01-04 + scripts/bin grid — juin 2026
---

# Pipeline Feature (état juin 2026)

**Pas de dossier `memory/` dans le repo** — doc projet : `README.md`, `.claude/rules/`, `archives/`.

## Flux opérationnel

```
scripts/01_prepare_cohort.py     → cohort/snapshot_*.parquet + experiments/input.tsv
scripts/02_train_combined.R    → runs/<prefix>.{csv,json}
scripts/03_evaluate.R            → runs/<run>/eval/*.csv (tables)
scripts/04_plot_investigation.R  → runs/<run>/eval/plots/
scripts/bin/grid_search.py       → experiments/feature_runs.duckdb
scripts/bin/analyze.py           → top-K depuis DuckDB
```

Helpers R : `scripts/bin/R/eval_helpers.R` (sourcés par 03 et 04).

## Règles clés

- trace-prod **read_only** ; filtres techniques en 01 ; filtres analytiques (rep/TNE/Bladder_Blood, depth≥0.25) en 02
- Seuil eval : `quantile(healthy, target_spec, type=1)` — aligné 02/03/04
- Label : healthy=0 ; muté ou actif sans mut=1
- Cohorte eval typique post-02 : ~480 labellisés (288 cancer, 192 healthy) — ≠ 307 exploratory (filtres bladder)

## Grid

- `experiments/pool.yaml` : mvaf obligatoire, combos taille 3–8
- Cache `combo_id` dans `feature_runs.duckdb`
- `grid_search` appelle `scripts/02` (plus `score_one_combo.R`)

## Livrables

- **Nouveau** : `runs/combined_v{N}_{slug}/` (README, cohort figé, `new/` + `old/` avec 02–04)
- **Historique** : `archives/features/combined_v2_probs`, v3/v4, validations Michael
- Skill : `/run-new-feature`

## Archives repo

`archives/` : ancien code (refresh_cohort, prepare_inputs, score_one_combo, build_combined_score_flex, dossier `features/`), ancien `memory/` (projects-knowledge-base, session-exports).
