# Context — Feature — 2026-06-09

**Branche** : main
**Dernier commit** : f39b7ba — fix(main): argument --features explicite pour main.sh
**Status** : 2 fichiers modifiés (main.sh, scripts/feature_db.py — WIP best_combo)

## Où j'en suis
Pipeline opérationnel bout-en-bout : `select_cohort.py` (lignes/labels, `ORDER BY` déterministe, gel `data/cohorts/{ref}`, `DEFAULT_SPEC`, `--filters` réservé) → `./main.sh --features` / `launch.sh` → train (features par `sample_id` ; expand `probs_epic` 16 + `probs_loyfer` 31) → eval → publish → `feature_runs.duckdb`. `main_bench.sh` = 511 combos (pool 9). Extraction select_cohort terminée+poussée (b225ad6..88a12b3) ; surcouche main/main_bench/best_combo (c6b3eb4/f39b7ba + WIP).

## Ce qui marche / ce qui foire
- ✓ Cohorte std_359 : 359 scorés (50 H + 285 C) ; baseline mvaf_v1 bit-identique au golden
- ✓ Combo déterministe (`ORDER BY unique_id` corrige la non-repro ~±2pp) ; Active_NoMut figé 60.9%
- ✓ Référentiels : `filtres_cohorte_colonnes.tsv`, `features_disponibles.tsv`
- ✓ publish DB : baseline unique + combos deltas ; `feature_db` ne réécrit plus le manifest
- ✓ Spec/plan : `docs/superpowers/{specs,plans}/2026-06-08-select-cohort*`
- ✗ `eval.R` n'accepte pas `--cohort`/`--features` (lit `run.env`)
- ✗ `main_bench.sh` relance train même si combo déjà en DB
- ✗ Mode filtre dashboard (`filter_spec`→SQL) différé
- ⚠ WIP non-committé : `main.sh` + `feature_db.py` (best_combo)

## Prochaine étape
`./main_bench.sh` puis SQL sur `feature_runs.duckdb` (tri `delta_sens_active_nomut`) → best combo. Ensuite : compilateur `filter_spec`→SQL (mode filtre dashboard).
