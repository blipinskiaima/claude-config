---
name: exis-alignment
description: "Alignement de /exploration sur le modèle Exis 1.1 (mVAF v1.4) : seuil quantile type 1, exclusion nommée CGFL_26BM01841, sélecteur Cohorte Avancés/Précoce, rupture assumée vs R main."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4dce2525-c204-49e3-b772-79405ebe19b5
  modified: 2026-07-24T12:42:34.505Z
---

# Alignement Exis 1.1 — page /exploration (2026-07-24)

Le PDF SD-02 « Exis 1.1 » = le score **mVAF v1.4**. La page /exploration a été alignée pour
reproduire ce rapport au chiffre près. Trois changements + threading complet.

## 1. Seuil : quantile type 1 (et non type 6)

Le pipeline Exis (`exploratory-analysis-CGFL-HCL/misc_analyses/compare_univariate_stats/R/univariate_sens_spec_utils.R:154`)
calcule le seuil par `quantile(healthy, target, type=1)` (inverse ECDF, **valeur observée**).
La Tower faisait `type=6` (weibull, interpolé). Sur les 224 sains : type 1 → **0,0042** (score
d'un vrai sain, borne basse du plateau), type 6 → 0,0072 (interpolé). **Même spécificité**
(213/224) mais 3 cancers (0,0047/0,0052/0,0071) tombent entre les deux → type 1 = +3 en sensibilité.

`_quantile_r_type6` renommé `_quantile_r_type1`, corps `method="inverted_cdf"`. Appliqué
PARTOUT (aussi `depth_sweep` + graphes dist/ROC dans `exploration.py`). **type 1 pour TOUS
les scores** (v1 ET v1.4, choix Boris) → **rompt** l'équivalence cell-by-cell vs R main (type 6).
`TestRegressionVsR` désactivé (skip) ; snapshots TestDefaultV500/SpeedVac re-figés.

## 2. Exclusion nommée CGFL_26BM01841

Le rapport Exis l'exclut (`REGULATORY_EXCLUDED_UNIQUE_IDS`). Dans la Tower :
`_EXCLUDED_UNIQUE_IDS = frozenset({"CGFL_26BM01841"})`, filtré dans `_prepare_base_dataset`
après la construction de `unique_id` → se propage à tous les callsites.

## 3. Sélecteur Cohorte Avancés / Précoce

Param `cohort_mode` dans `_apply_user_filters` (healthy toujours préservé) :
- `advanced` (défaut) : `healthy | cohort != 'Lung-DI précoce'` → §2.2, Lung 77/85.
- `early` : `healthy | (cohort == 'Lung-DI précoce' & active_cancer_flag)` → §2.3, 11/27.

⚠ Le §2.3 du PDF compte `active_cancer = Yes` **strict** (pas `cancer_truth`) : exclut
Lung_132 (muté VAF 0,4 mais clinique « probable »). D'où le `& active_cancer_flag` spécifique
au mode early. Le mode advanced, lui, utilise `cancer_truth` (= §2.2).

Threadé comme `score_source` : `compute` + `compute_cohort_cascade` (nouvelle étape panneau) +
`compute_cohort_samples` + get_scores/depth_sweep/temporal_drift/cancer_vaf/methylation/
filtered_dataset + router (`_slider_kw_only`, `_explore_kw_no_depth`, endpoints depth-sweep/figure).
Les vues de dispersion (qc/dotplot/bladder, qui font `_prepare_base_dataset` direct) acceptent
`cohort_mode` mais ne l'appliquent pas (**paramètre inerte**, parité kwargs). Front : `CohortPills`
sidebar + `DEFAULT_FILTERS` + permalink `?cohort=` + chip récap.

## Résultat vérifié (prod, 24/07/2026)

Réglages Exis (mVAF v1.4, Avancés, 95 %) : seuil 0,0042, spéc 95,1 % (213/224), sens 82 %
(214/261), Lung 77/85, MutHigh 107/107, MutLow 37/47, par stade §2.3 I/II/III exacts.
**Tous les numérateurs = PDF exact.** Seul écart accepté : `Prostate_21` (passé cancer le
23/07, après le PDF du 06/07 ; donnée, pas méthode ; +1 dénominateur en faux négatif).

Commits `f3a4783` (volets 1-3) + `c913356` (threading + §2.3). Tag `pre-exis-alignment`.
User guide + comparaison dans le Google Doc `1dOYIB-...`.
Voir aussi : [[exploration_score_source_toggle]], [[qara_tower_skill]].
