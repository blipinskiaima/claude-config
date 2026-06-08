# Context — Feature — 2026-06-08

**Branche** : main
**Dernier commit** : (en cours — end-session)
**Status** : commit session select_cohort CLI + train blocs probs + main/main_bench

## Où j'en suis

Pipeline Feature opérationnel bout-en-bout : `select_cohort.py` (args CLI par champ `filtres_cohorte_colonnes.tsv`) → `main.sh FEATURES` → train/eval/publish → `feature_runs.duckdb`. `train.R` expand `probs_epic` (16) et `probs_loyfer` (31). `main_bench.sh` lance 511 combos sur pool 9 features (~30 min).

## Ce qui marche / ce qui foire

- ✓ Cohorte std_359 : 359 scorés, 50 H + 285 C labellisés
- ✓ Référentiels : `filtres_cohorte_colonnes.tsv`, `features_disponibles.tsv`
- ✓ trace-prod schema mémoire à jour (268 cols, 9 tables)
- ✓ publish DB : baseline `mvaf_v1` unique, combos avec deltas
- ✗ `eval.R` n'accepte pas `--cohort`/`--features` (lit `run.env`)
- ✗ `main_bench.sh` relance train même si combo déjà en DB

## Prochaine étape

Lancer `./main_bench.sh` (ou combos ciblés via `./main.sh "..."`) puis requête SQL sur `feature_runs.duckdb` pour identifier le best combo (tri `delta_sens_active_nomut`).
