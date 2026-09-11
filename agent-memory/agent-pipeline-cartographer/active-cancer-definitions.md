---
name: active-cancer-definitions
description: Consommateurs de metadata.active_cancer (raima, Aima-Tower, Feature, Bam2Beta/TOO, exploratory-analysis-CGFL-HCL) et les définitions divergentes de "cancer actif" — traitement de Suspicion/probable/External quality control
metadata:
  type: project
---

## Constat général (scan live 2026-09-11)

Valeurs brutes actuelles (`SELECT active_cancer, COUNT(*) FROM metadata GROUP BY 1`, trace-prod) :
None(520), Yes(443), No(104), imagerie suspecte(25), Suspicion(18), probable(13), External quality
control sample(13). Harmonisation trace-prod (`lib/harmonization.py:29-33`) ne mappe que
`"image suspecte"→"Suspicion"` et `"oui"→"Yes"/"non"→"No"` — **"imagerie suspecte" (25 lignes)
échappe à la règle** (1 mot d'écart avec la clé exacte), reste brut en DB. Gsheet label complet :
`"Presence of an active cancer (sampling at active disease, no post-op)"` (`trace-prod/lib/duckdb.py:1011`).

## Règle canonique AIMA (3 projets identiques : exploratory-analysis → Aima-Tower → Feature)
`normalize_active_cancer` = valeur (lowercase+trim) ∈ `{"yes","oui","y","1","true"}` :
- **Origine** : `exploratory-analysis-CGFL-HCL/02_sensitivity_specificity.R:46-48` (fonction) +
  `cancer_truth = mutated_flag | active_cancer_flag` (L74-76).
- **Port Python** : `Aima-Tower/src/exploratory_compute.py:33` (`ACTIVE_CANCER_TRUE`) + `_add_flags()`
  L326-339 : `cancer_truth = mutated_flag | active_cancer_flag | indication∈{TNE,Nuclear,Bladder_Blood,
  Bladder_Urine}` — le carve-out indication est **ajouté** côté Python, absent du R original (qui gère
  TNE/Nuclear/Bladder_Blood par exclusion de nom dans `apply_analysis_filters_*`, pas par le flag).
- **Feature** : doc `.claude/rules/04-cohort-reference.md:58-61` (même formule, sans carve-out) +
  `script/eval.R:69` (code identique, lowercase).
- Sous cette règle : Suspicion / imagerie suspecte / probable / External quality control sample / No /
  NULL → **False** (sauf mutation vaf>0 ou carve-out indication côté Tower). Aima-Tower documente
  explicitement l'exclusion pour "probable"/"External quality control" : `exploratory_compute.py:1736`
  ("Les samples ambigus (active_cancer='probable', 'External quality control'…) sont exclus").

## 2 variantes divergentes (sets différents, case-sensitive)
- **raima** `R/evaluate-score.R:268` : `is_active = active_cancer %in% c("YES","SUSPICION")` (toupper) —
  inclut Suspicion nommément, MAIS **n'est pas la vérité terrain du sens/spec principal**
  (`pos_all` L313 = `is_tumoral` seul, basé sur `Gene 1 Mutation status`, sans lien avec active_cancer) ;
  is_active ne sert qu'à un sous-groupe descriptif (L388-398, sg0/sg1). ⚠️ Source = gsheet clinique brute
  via `R/download-data.R:11` (gsheet ID `1v1KUuCoMQV4Qk5jfbHLxhrUK6q_FETLiH8TuCQMdNxA`, PAS l'export
  trace-prod) → la cellule brute vaut "image suspecte"/"imagerie suspecte" (confirmé par
  harmonization.py), jamais littéralement "Suspicion" → la branche SUSPICION est probablement **morte
  en pratique** (inférence non vérifiée en direct sur le gsheet).
- **Bam2Beta/TOO + exploratory-analysis/tumor_of_origin** (fichier vendored, `diff too_common.R` = 0
  hors 2 lignes d'en-tête/source) : `Bam2Beta/bin/TOO/too_common.R:432` =
  `active_cancer %in% c("Yes","oui","TRUE","True",TRUE)` — case-SENSITIVE, sans "y"/"1"/lowercase
  "true". Même résultat pratique que la règle canonique sur les valeurs actuelles (aucune n'est "YES"
  tout majuscule), mais littéralement différent. **Tourne en production** (classifieur TOO de Bam2Beta,
  cf. trace-prod schema v19).
- **Feature SQL** (`select_cohort_train.py:225`, `select_cohort_eval.py:238`) : même set que TOO
  `IN ('Yes','oui','TRUE','True')` pour `is_active_no_mut`/`label` — 3ᵉ implémentation littérale du
  même héritage.

## Bucket "suspect" séparé (Feature + exploratory-analysis ; PAS Aima-Tower/raima/TOO)
`Feature/script/select_cohort_eval.py:75-76` `suspect_match()` = regex
`imagerie\s*suspecte|suspicious\s*imaging` sur `lower(trim(active_cancer))` → catégorie `unit='suspect'`,
**hors-KPI**, `label` NULL par défaut, activé via `--include-suspicious`. Doc :
`Feature/docs/superpowers/specs/2026-06-25-unite-suspect-eval-design.md:45-46` (arbre de décision) +
`Feature/README.md:67`. Cohérent avec `exploratory-analysis-CGFL-HCL/README.md:214` ("imagerie suspecte
ne sont pas entraînés, reçoivent un score par inférence — moyenne des 5 modèles fold"). ⚠️ Cette regex
matche les 25 "imagerie suspecte" bruts mais PAS les 18 "Suspicion" harmonisés (substring absent) — gap
symétrique à celui de raima (chacun rate la moitié de la population "suspecte" réelle selon la source
qu'il lit).

## Colonne active_cancer_clinical (distincte de active_cancer)
Existe dans le schéma (`trace-prod/lib/duckdb.py:275`, gsheet label "...according clinical files, needed
for cancer samples without mutation") et exposée dans les filtres Aima-Tower (`src/pages.py:981,1944` —
commentaire "0 distinct (vide)") mais **vide en pratique**, non utilisée dans aucun calcul de flag observé.

## Doc externe référencée (non lue, hors scope Pipeline)
`exploratory_compute.py` docstring + commentaires citent "Exis 1.1 (doc SD-02)" comme source
réglementaire du seuil et de la cohorte — Google Doc externe, jamais lu par cet agent.
