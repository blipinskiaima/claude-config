---
name: dilution-eval-unit
description: "Mécanisme \"unit\" pour empiler des cohortes d'éval hors-train (Twist dilution) dans cohort_eval.csv / scores.csv"
metadata: 
  node_type: memory
  type: project
  originSessionId: fb3ec5dd-5832-490c-b425-205887ae9e76
---

Unité d'éval "dilution" (Twist) ajoutée juin 2026 (hors cohorte train figée).

Empiler N cohortes d'éval hors-train dans `cohort_eval.csv` via `unit` :
- `select_cohort_eval.py --sample_name '%_Alc_%,%Twist%'` (patterns OR) ; colonne `unit` par CASE sur sample_name (`alc`/`dilution`/`other`).
- `unique_id` conditionnel Twist = `labo_sample_name` SANS strip rep → garde les 22 reps (sinon collision scores.csv keyé par unique_id).
- `--force-cancer-label` scopé `unit=='alc'` → Twist `label` NULL ; label écrit Int64 nullable ("1"/"" pas "1.0").
- `train.R build_base` transporte `unit`+`sample_name` (tolérant NA). `infer_eval`/`train_combined` INTACTS.
- `eval.R` : `META += unit,sample_name` ; masque `alc = eval_cohort=='eval' & unit=='alc'` → dilution scorée mais HORS KPI → `eval_kpis.csv` inchangé.

Nouvelle cohorte éval hors-train = (1) pattern main.sh `--sample_name`, (2) branche CASE `unit` (+unique_id conditionnel si reps), (3) masque eval.R seulement si truth.

Tower lit Twist dans `scores.csv` (filtre `unit=='dilution'`, score = colonne-combo = clé canonique ; speedvac/cohort_ref implicites dans result/speedvac_{no,yes}/). 22 Twist valides (`Twist_10_8` KO exclu) × 1023 combos × 2 variantes. Additivité prouvée (scores.csv train+Alc + eval_kpis.csv byte-identiques baseline).

Voir [[pipeline-3-etapes]], [[livrables-actuels]].
