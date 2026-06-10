---
name: label-definitions
description: Définition canonique des truth labels Feature/ — select_cohort.py → train.R / eval.R (validé 2026-06-09)
type: project
---

# Truth labels — projet Feature/

**Source de vérité code** : `scripts/select_cohort.py` (CTE `scored`, colonnes `label`, `is_healthy`, `is_mutated`, `is_active_no_mut`, `is_suspicious`).

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
- **imagerie suspecte seule** (`is_suspicious` — regex `imagerie suspecte` / `suspicious imaging` sur `active_cancer`) → **scorés à l'inférence** (`train.R`) mais **pas entraînés** ni dans les KPI (`eval.R` filtre `!is.na(label)`).

Filtre cohorte : `WHERE label IS NOT NULL OR is_suspicious`.

## En aval

| Script | Usage |
|---|---|
| `train.R` | train sur `!is.na(label)` ; inférence sur `is.na(label) & is_suspicious` |
| `eval.R` | `cancer_truth = label == 1` ; stratification Mut / Active_NoMut via flags |

## Effectif std_359 (référence)

359 scorés = 50 H + 285 C labellisés (129 mutés + 156 active_no_mut) + 24 imagerie suspecte.
