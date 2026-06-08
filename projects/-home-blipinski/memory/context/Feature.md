# Context — Feature — 2026-06-08

**Branche** : main
**Dernier commit** : f39b7ba — fix(main): argument --features explicite pour main.sh
**Status** : clean

## Où j'en suis

Pipeline Feature opérationnel bout-en-bout : `select_cohort.py` (args CLI) → `./main.sh --features "..."` → train/eval/publish → `feature_runs.duckdb`. `train.R` expand `probs_epic` (16) et `probs_loyfer` (31). `main_bench.sh` lance 511 combos sur pool 9 features (~30 min). Syntaxe CLI finalisée : `--features` obligatoire (plus d'argument positionnel).

## Ce qui marche / ce qui foire

- ✓ Cohorte std_359 : 359 scorés, 50 H + 285 C labellisés
- ✓ Référentiels : `filtres_cohorte_colonnes.tsv`, `features_disponibles.tsv`
- ✓ publish DB : baseline `mvaf_v1` unique, combos avec deltas
- ✓ `main.sh --features` + `main_bench.sh` alignés (commit f39b7ba)
- ✗ `eval.R` n'accepte pas `--cohort`/`--features` (lit `run.env`)
- ✗ `main_bench.sh` relance train même si combo déjà en DB

## Prochaine étape

Lancer `./main_bench.sh` (ou combos ciblés via `./main.sh --features "..."`) puis requête SQL sur `feature_runs.duckdb` pour identifier le best combo (tri `delta_sens_active_nomut`).
