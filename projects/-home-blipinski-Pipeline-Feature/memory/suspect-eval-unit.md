---
name: suspect-eval-unit
description: "Unité d'éval 'suspect' (imageries suspectes) — flag --include-suspicious côté Feature + onglet dotplot côté Aima-Tower (juin 2026)"
metadata: 
  node_type: memory
  type: project
  originSessionId: f9efd22e-79ca-4700-9c1b-9accc249f84e
---

Unité d'éval **`suspect`** (imageries suspectes) ajoutée juin 2026, sur le modèle de [[dilution-eval-unit]] : sans vérité-terrain (`label` NULL), hors KPI, onglet visuel Tower.

**Définition** : `active_cancer ~ 'imagerie suspecte'|'suspicious imaging'` (regex `imagerie\s*suspecte|suspicious\s*imaging`, = colonne `is_suspicious`). **25 samples**, tous HCL, cohort « Lung-DI précoce ». Biologiquement = les Lung-DI précoce **non confirmés** (frères non-labellisés des unités `lung_*`) ; mécaniquement = traités comme `dilution` (hors KPI).

**État antérieur (corrigé)** : les suspects n'étaient scorés **nulle part** — `select_cohort_train.py` finit par `WHERE label IS NOT NULL` (les exclut), et le bloc `susp` de `train.R` est **dormant**. (La mémoire [[label-definitions]] disait à tort `WHERE label IS NOT NULL OR is_suspicious`.)

**Dev 1 — Feature** (`main`, commits `f08e582`+`47ce642`) :
- `select_cohort_eval.py` : flag `--include-suspicious` → (a) ajoute `OR regexp_matches(m.active_cancer, …)` **dans** la clause sample_name (helper `suspect_match(col)`), (b) branche `CASE … THEN 'suspect'`. `--force-cancer-label` reste scopé `alc` → suspects `label` NULL.
- `main.sh` : flag sur l'appel eval **uniquement** (pas le train). `train.R`/`eval.R` **inchangés** (suspect hors masques eval.R = hors KPI, comme dilution).
- Additivité **prouvée** sur les 2 variantes : `eval_kpis.csv` byte-identique, scores train/alc/dilution 0 diff (yes 699×2047, no 511×2047).

**Dev 2 — Aima-Tower** (`main`, 5 commits) : `dilution_service.get_suspect_scores()` (filtre `unit=='suspect'`, seuil healthy-train, liste plate + `n_above`/`n_total`) ; route `GET /api/combined/suspect` ; `useCombinedSuspect` + type `CombinedSuspect` (combined.ts) ; composant `SuspectChart.tsx` (dotplot jitter + ligne seuil) ; onglet « Suspects » dans `Combined.tsx` (après Dilution). `EVAL_UNITS`/feature_service/feature_curves **inchangés**. Endpoint live : 25 points, 6 au-dessus du seuil mvaf_v1@95% (std_522).

**Pattern réutilisable** (nouvelle cohorte éval sans truth) : (1) sélection dans `select_cohort_eval.py` + branche `CASE unit`, (2) `get_<unit>_scores` calqué sur dilution, (3) route + hook + composant + onglet Tower. Voir [[dilution-eval-unit]], [[pipeline-3-etapes]].
