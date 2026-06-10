---
name: pipeline-3-etapes
description: "Pipeline Feature scripts/ — select_cohort → train → eval → publish (état juin 2026)"
metadata: 
  node_type: memory
  originSessionId: b3ac9798-fbc1-465e-a927-aad831034f9b
---

# Pipeline Feature (juin 2026)

## Flux opérationnel

```
select_cohort (train)  → data/cohorts/std_335/cohort.csv
select_cohort (eval)   → alc (~145 v5) si EVAL_ALC=1
train.R                → OOF train + inférence Alc → scores.csv (col eval_cohort)
eval.R                 → spec_XX/eval_kpis.csv (format long)
feature_db.py publish  → runs + eval_kpis dans feature_runs.duckdb
```

`./main.sh --features "..."` ; `EVAL_ALC=1` pour strate Alc.
`./main_bench.sh` : **1023 combos** (10 features) × **Alc** × **spec 0.90+0.95** ; train 1×/combo, 2ᵉ spec via `--no-train`.

## Séparation train / eval

- **Train fixe** : std_335 (50 H + 285 C)
- **Unités d'éval** : 5 strates (filtres sur train) + **alc** (cohorte externe, label=1 forcé, hors fit)
- Seuil : healthy du **train** uniquement

## DB (`feature_runs.duckdb`)

- `runs` : clé `(cohort_train_ref, features, target_spec)`
- `eval_kpis` : clé `(run_id, cohort_eval, model)` — mut, active_nomut, alc, …
- `best_combo` : `--cohort-train`, `--cohort-eval`, `--kpi`

## Règles clés

- trace-prod **read_only** ; baseline = `mvaf_v1` seul
- Cohorte train : **std_335** ; suspects imagerie → `unlabeled.csv` (`--is_suspicious false`)
- select_cohort Alc : `--pool-filter TRUE`, `--force-cancer-label true`, pas de filtre cohort/labo
