# Context — Feature — 2026-06-09

**Branche** : main
**Dernier commit** : 6188844 — feat(feature_db): best_combo + chemins absolus PNG/CSV en DB
**Status** : clean

## Où j'en suis

Pipeline bout-en-bout opérationnel : `select_cohort.py` → `./main.sh --features` / `main_bench.sh` (511 combos) → train/eval/publish → `feature_runs.duckdb`. `feature_db.py` enrichi : colonnes `png_path` + `csv_path` (chemins absolus) à chaque publish ; commande `best_combo` pour classer les combos par `delta_sens_active_nomut`. Bench `std_359` en cours ou partiellement terminé (tmux BL).

## Ce qui marche / ce qui foire

- ✓ Cohorte std_359 : 359 scorés (50 H + 285 C)
- ✓ `best_combo` : ex. leader `mvaf_v1,probs_loyfer` (+21.8 pp Active_NoMut vs mvaf_v1)
- ✓ publish stocke KPIs + deltas + chemins PNG/CSV absolus
- ✓ Référentiels : `filtres_cohorte_colonnes.tsv`, `features_disponibles.tsv`
- ✗ `eval.R` n'accepte pas `--cohort`/`--features` (lit `run.env`)
- ✗ `main_bench.sh` relance train même si combo déjà en DB (publish skip seulement)

## Prochaine étape

Finir `./main_bench.sh` si incomplet, puis `python3 scripts/feature_db.py best_combo --cohort-ref std_359 --top 10` pour valider le best combo final. Investiguer combos prometteurs (ex. `mvaf_v1,probs_loyfer`).
