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
select_cohort_train.py  → cohort_train.csv (--speedvac no|yes)
select_cohort_eval.py   → cohort_eval.csv (Alc ~145)
train.R                 → scores.csv (2^N-1 combos, eval_cohort train|eval, col stage)
eval.R                  → eval_kpis.csv (baseline mvaf_v1 vs combiné, format long)
```

`./script/main.sh` → `result/speedvac_{no,yes}/`. Tower lit directement ces dossiers (plus de `feature_runs.duckdb`).

## Séparation train / eval

- **Train** : std_335 (speedvac_no, 50 H + ~294 C) / std_522 (speedvac_yes, 192 H + ~340 C)
- **Unités d'éval** : 7 principales + 5 stades Lung-DI précoce actif (`lung_I_III`…`lung_NR`) + **alc** (cohorte externe)
- Seuil : healthy du **train** uniquement ; `stage` depuis trace-prod (`metadata.stage`)

## Règles clés

- trace-prod **read_only** ; baseline = `mvaf_v1` seul
- Cohorte train : **std_335** ; suspects imagerie → `unlabeled.csv` (`--is_suspicious false`)
- select_cohort Alc : `--pool-filter TRUE`, `--force-cancer-label true`, pas de filtre cohort/labo
