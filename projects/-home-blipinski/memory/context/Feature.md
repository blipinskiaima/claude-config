# Context — Feature — 2026-06-11

**Branche** : main
**Dernier commit** : a22a12c — feat: cohorte eval Alc, eval_kpis et bench 1023×dual-spec
**Status** : clean (untracked : eval_v2.r, data/cohorts/std_{0,145,335}, unlabeled.csv)

## Où j'en suis

Session pédagogique sur le pipeline eval : effectifs std_359 (359 scorés = 335 labellisés + 24 imagerie suspecte), canon labels documenté (`label-definitions.md`), déroulé train.R / eval.R et logique sens-spé (seuil = quantile healthy @ target-spec, sensibilité par strate cancer). Repo déjà sur archi train/eval découplée (std_335 train, Alc optionnel, dual-spec 0.90/0.95) — commit a22a12c.

## Ce qui marche / ce qui foire

- ✓ Canon labels : muté (vaf>0) + active_no_mut ; healthy %Health% ; NA + is_suspicious inférence seule
- ✓ eval.R : inputs = scores.csv (label, is_healthy, is_mutated, vaf, active_cancer, mvaf_v1, combined_score)
- ✓ eval.R restauré intact (pas de modif parasite) ; eval_v2.r abandonné (untracked, hors pipeline)
- ✗ data/cohorts/std_0/ artefact vide — ne pas utiliser

## Prochaine étape

Bench `./main_bench.sh` si en cours (tmux). Puis `best_combo --cohort-train std_335 --cohort-eval alc` quand DB remplie.
