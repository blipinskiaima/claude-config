---
name: label-definitions
description: Définition canonique des truth labels Feature/ — select_cohort.py → train.R / eval.R (validé 2026-06-09)
metadata: 
  node_type: memory
  type: project
  originSessionId: f9efd22e-79ca-4700-9c1b-9accc249f84e
---

# Truth labels — projet Feature/

**Source de vérité code** : `script/select_cohort_train.py` + `select_cohort_eval.py` (CTE `scored`, colonnes `label`, `is_healthy`, `is_mutated`, `is_active_no_mut`, `is_suspicious`).

**VAF** = `metadata.gene1_vaf` castée en float (`vaf_gene1_pct`).

## Positifs (`label = 1`) — 2 cas

| Cas | Règle | Flag |
|---|---|---|
| **Muté** | `vaf > 0` → positif **même si** `active_cancer` n'est pas « Yes » | `is_mutated` |
| **Cancer actif sans mutation** | `vaf = 0` ou NA **et** `active_cancer ∈ {Yes, oui, TRUE, True}` | `is_active_no_mut` |

Les deux cas sont mutuellement exclusifs. Ordre SQL : healthy d'abord, puis muté, puis active_no_mut.

## Négatifs (`label = 0`)

| Règle | Flag |
|---|---|
| `name` contient `"Health"` (insensible à la casse, pattern SQL `%Health%`) | `is_healthy` |

Prime sur la VAF : un sample nommé Health reste négatif même si `vaf > 0`.

## Exclus de l'apprentissage (`label = NA`)

Tout le reste, notamment :

- cancers sans mutation **et** sans `active_cancer = Yes` (ou équivalent du set positif) ;
- `active_cancer = Probable` (ou `probable`) sans VAF > 0 ;
- **imagerie suspecte seule** (`is_suspicious` — regex `imagerie suspecte` / `suspicious imaging` sur `active_cancer`) → **exclue du train**, entre par l'**eval** comme unité `unit='suspect'` (label NULL), scorée par `infer_eval`, hors KPI. Voir [[suspect-eval-unit]].

Filtre cohorte **train** (`select_cohort_train.py`) : `WHERE label IS NOT NULL` (suspects exclus). Les suspects entrent par la cohorte **eval** via `select_cohort_eval.py --include-suspicious`.

## En aval

| Script | Usage |
|---|---|
| `train.R` | train sur `!is.na(label)` ; suspects scorés via `infer_eval` (cohorte eval, `unit='suspect'`). Le bloc `susp` (is.na(label) & is_suspicious dans le flux train) est **dormant** — le train n'a plus de suspects |
| `eval.R` | `cancer_truth = label == 1` ; stratification Mut / Active_NoMut via flags ; `suspect` hors masques = hors KPI (comme `dilution`) |

## Effectif train (référence)

Train = labellisés uniquement (suspects exclus) : **std_335** (speedvac_no, 50 H + ~294 C) / **std_522** (speedvac_yes, 192 H + ~340 C). Les **25** imageries suspectes sont une unité d'**eval** (`unit='suspect'`), hors train.
