---
name: exploration-score-source-toggle
description: "Page /exploration : toggle Score mVAF v1 / v1.4 (param score_source) pilotant toute la page. Archi du threading + fix bug pré-existant des 4 endpoints graphes."
metadata: 
  node_type: memory
  type: project
  originSessionId: 40f01e64-a595-4d60-9984-3f51e4b9baf2
---

# Page `/exploration` — toggle Score mVAF v1 / v1.4 (2026-07-03)

Sélecteur **Score** (panneau gauche, sous Centre) qui bascule la colonne pilotant
sensibilité/spécificité de **toute** la page (tables Sens/Spé + tous les graphes).
Défaut = `mvaf_v1` (non-destructif, garde la validation R). Demande Boris.

## La colonne pivot unique

Toute la page repose sur **une seule colonne aliasée `score`** dans `_DUCKDB_QUERY`
(`exploratory_compute.py`). Tous les calculs (`_compute_threshold`, sens/spec,
by_indication/stage, ROC, dotplot…) lisent `df["score"]`. **Changer `score` = changer
toute la page.** C'est le seul levier.

## `score_source` = `mvaf_v1` | `mvaf_v14`

| | Colonne source | Table | Type |
|---|---|---|---|
| `mvaf_v1` (défaut) | `q.mvaf_v1` | `qc_metrics` | **float propre** |
| `mvaf_v14` | `r.mvaf_v14` | `retd_suivis` | **VARCHAR virgule FR, défaut `'KO'`** |

- Parsing dans `_load_from_duckdb` : `pd.to_numeric(str.replace(",", "."), errors="coerce")` → `'KO'`/vide → NaN.
- **Swap dans `_prepare_base_dataset(all_res, center, score_source)`** : si `mvaf_v14`, `df["score"]=df["mvaf_v14"]` **AVANT** le filtre `df[df["score"].notna()]` → les samples sans v1.4 (~12) sortent naturellement de la cohorte (défini par le score sélectionné).
- Seuil = `quantile_type6(healthy score, target_spec)` dérivé par Tower → **scale-agnostique**, donc la différence d'échelle v1 vs v1.4 est gérée automatiquement.

## Threading (mirroir de `dorado_version`)

`score_source` est plombé exactement comme `dorado_version` (pattern existant) :
- **Clé de cache** : `_get_prepared` / `_get_prepared_for_graphics` (dict key) + `compute()` `@lru_cache`.
- **11 méthodes câblées** à la page : `compute`, `compute_cohort_cascade` (swap manuel sur `base.assign` — copie, ne mute pas `_base_df`), `compute_cohort_samples`, `get_scores`, `get_cancer_vaf_scores`, `depth_sweep`, `temporal_drift`, `get_filtered_dataset`, `get_mvaf_dotplot_data`, `get_methylation_vs_vaf_data`, `get_bladder_data`, `get_qc_data`.
- **Non câblées** (database.py / non exposées) laissées au défaut `mvaf_v1` : `sample_level_ml_view`, `get_misclassified_features`, `compare_centres`, `get_calibration_data`, `get_scores_by_kit` (le défaut de `_get_prepared` suffit).
- Router : `ExplorationFilters.score_source` + `_to_compute_kwargs` / `_slider_kw_only` / `_explore_kw_no_depth` + depth-sweep inline.
- Front : type `ScoreSource` + `DEFAULT_FILTERS` (`exploration.ts`), `ScorePills` sidebar (draft + Appliquer, comme Centre), permalink `?score=` (`exploration-url.ts`), chip récap « Score » (`Exploration.tsx`).

## Bug pré-existant corrigé au passage (4 endpoints graphes MORTS sur main)

`/qc-data`, `/mvaf-dotplot`, `/methylation-vaf`, `/bladder` **plantaient déjà** (vérifié vs git HEAD) :
- dotplot/methylation/bladder passaient `filters.min_depth` en **2ᵉ positionnel** = `dorado_version` → `TypeError: multiple values for dorado_version`. Fix : retirer le positionnel, `min_depth` vient déjà de `_slider_kw_only`.
- `/qc-data` utilisait `_slider_kw_only` (qui a `min_depth`) mais `get_qc_data()` n'a pas ce param. Fix : utiliser `_explore_kw_no_depth`.

Ces 4 onglets graphiques étaient donc inaccessibles avant cette session → refonctionnels.

## Validé (live conteneur, vraie DB)

`compute` ALL : **v1 = 78.5% (336/428) / 88.4% (198/224)**, **v1.4 = 81.7% (343/420) / 85.3% (191/224)**.
Cohorte v14 perd ~8 cancers (sans v1.4). Les 8 endpoints répondent 200 en v1 ET v14.
Gotcha test : `_load_from_duckdb` fait un `duckdb.connect(read_only=True)` **sans retry** → 500 pendant qu'un job trace-prod (`check_samples update-column`) tient le lock write. Tester sur copie de la DB.

Voir aussi : [[exploration_v2_3_design]], [[spec_ciblee_vs_realisee]], [[project_sens_active_cancer_truth]].
