# Context — Feature — 2026-06-10

**Branche** : main
**Dernier commit** : (en cours — end-session)
**Status** : bench `./main_bench.sh` lancé en tmux (BL2)

## Où j'en suis

Architecture train/eval découplée implémentée : cohorte train std_335 fixe, cohorte eval Alc optionnelle (`EVAL_ALC=1`), 6 unités d'éval (5 strates + alc), DB `runs` + `eval_kpis`, bench 1023 combos × 2 specs (0.90/0.95).

## Ce qui marche / ce qui foire

- ✓ `./main.sh` sans Alc (5 strates) + avec `EVAL_ALC=1` (6 strates, 480 scores)
- ✓ `eval_kpis.csv` format long + publish DB + migration anciens `results`
- ✓ `main_bench.sh` : Alc par défaut, dual spec, `--no-train` sur 2ᵉ spec, `--skip-done`
- ✓ fix `read_run_env()` eval.R (liste vs vecteur)
- ✗ `data/cohorts/std_0/` artefact vide (select Alc avant fix filtres) — ne pas utiliser

## Prochaine étape

Laisser tourner `./main_bench.sh` (ou `--skip-done` si reprise). Puis `best_combo --cohort-train std_335 --cohort-eval alc` une fois combos en DB.
