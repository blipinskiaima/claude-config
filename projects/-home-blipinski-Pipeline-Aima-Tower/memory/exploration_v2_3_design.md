---
name: Exploration v2.3 — Design des filtres et cohortes
description: Patterns clés de la refonte /exploration : filtres dynamiques, cohortes duales Sens/Spé vs Graphique, validation R cell-by-cell, helpers backend
type: project
originSessionId: 5bfbec5e-fc97-4d4e-a697-549503f02ef9
---
# Refonte page /exploration (v2.3, avril 2026)

## Validation cell-by-cell vs R main

Tower ≡ pipeline R (`~/Pipeline/exploratory-analysis-CGFL-HCL` branch `main`) **strictement identique** au target=0.85 ET 0.90, mode ge5, sans filtres avancés. Vérifié sur DB du 30 avril 2026 :
- detection_global (3 centres × 9 cols)
- summary_stratified_detection_global (5 metrics)
- by_indication_global (8 indications)

R02 = `02_sensitivity_specificity.R` qui appelle `raima::evaluate_score` avec `quantile(type=6)` ≡ `np.quantile(method="weibull")`.

## 2 cohortes distinctes par design (cohérent avec R)

| Vue Tower | N typique HCL | Source R | Filtre |
|---|---|---|---|
| **Cohort alert Sens/Spé** (sub-tab Tableaux) | 271 | R02 | `cancer_truth ∪ healthy_flag` strict |
| **Cohort Graphique** (sub-tab Graphiques) | 306-308 | R04 (`qc_plot`) | tous samples post-filtre, intermédiaires inclus |

Implémentation : alert affichée selon `Input("exploration-subtabs", "active_tab")` dans `update_exploration_filter_info`. **Why:** cohérence avec le pipeline R qui sépare ces 2 vues. **How to apply:** ne JAMAIS unifier les 2 chiffres. Tableaux = R02, Graphiques = R04.

## Pattern "tout sélectionné = no-op" (helpers backend)

Les multi-select Phase 1 (Active cancer, Dorado), Phase 2a (Stage, Class, Metastatic, Category, Extraction), Phase 2b dynamiques (~28 filtres) doivent :
- Pré-sélectionner toutes les valeurs distinctes par défaut (visibilité UX du défaut)
- Backend traite "tout coché" comme "pas de filtre" (no-op) → préserve les samples avec NULL dans la colonne

3 helpers dans `callbacks.py` :
- `_active_cancer_param(active_mode)` : Phase 1 active_cancer
- `_legacy_set_or_none(table, col, sel)` : Phase 2a (stage, class, metastatic, category, extraction_protocol)
- `_build_exploration_dynamic_filters(values, ids, ...)` : Phase 2b dynamiques

Pour chacun : `if frozenset(sel) >= frozenset(distinct): return None  # → backend skip`.

**Why:** sinon `isin(all_values)` exclut les samples avec NaN dans la colonne (bug active_cancer = 4 cancer perdus). **How to apply:** tout nouveau filtre multi-select doit passer par un helper équivalent.

## TNE/Nuclear visibles graphiques uniquement

`_get_prepared(centre, "cancer_detection", dorado)` filtre TNE+Nuclear via `_RE_FILTER_INDICATIONS_CANCER`. Utilisé par `compute()` (tableaux).

`_get_prepared_for_graphics(centre, dorado)` ne filtre que les réplicats techniques (rep|moche|bis|ter|quater). Utilisé par `get_filtered_dataset()` (graphiques Avancé).

`get_indications()` lit depuis la prep graphics → dropdown contient TNE/Nuclear/Healthy/Unknown. Sélectionner TNE côté tableau = sans effet (filtré upstream). Sélectionner TNE côté graphique = visible.

## Healthy carve-out asymétrique

`_apply_user_filters` applique le carve-out healthy pour tous les filtres metadata clinique :
```python
if indications is not None:
    out = out[out["healthy_flag"] | out["indication"].isin(indications)]
```

→ Healthy toujours préservé pour les TABLEAUX (calibrage du seuil quantile).

Côté GRAPHIQUE Avancé, le filtre Healthy est respecté explicitement après get_filtered_dataset :
```python
if indications and not any(i.startswith("Health") for i in indications):
    df = df[~df["healthy_flag"]]
```

→ User peut désélectionner Healthy pour le boxplot uniquement.

## Onglet Avancé (graphique)

Copie du pattern Analytics > Avancé : split_by / group_by / color_by (12 colonnes catégorielles) + metric_y (17 numériques) + log_y + Apply dédié. Reuse `build_boxplot()` de `exploration_graphs.py`.

Différence vs Analytics : utilise `get_filtered_dataset()` (df pandas in-memory déjà filtré) au lieu de SQL fresh via `filters_service.fetch_matching()`. Cohérent avec les autres tabs Exploration.

`include_all=True` activé quand centre=ALL et split=labo → 3 subplots ALL+CGFL+HCL alignés.

Aliases ajoutés au df avant build_boxplot (Tower utilise `which`, `class_raw`, etc. au lieu des noms Analytics) :
```python
for ui_name, df_name in [("labo", "which"), ("class", "class_raw"), ("category", "category_raw"),
                          ("dorado_model_version", "version_raw"),
                          ("nb_reads_total", "reads_million"), ("mvaf_v1", "score")]:
    if df_name in df.columns and ui_name not in df.columns:
        df[ui_name] = df[df_name]
```

## Validation invariante : test partition SpeedVac

`tests/test_exploratory_compute.py::TestSpeedVacFilter::test_speedvac_partition_invariant` :
```
N_Cancer(only) + N_Cancer(exclude) == N_Cancer(all)  # disjoint et exhaustif
```
Ce test résiste à la dérive DB (croissance cohorte). Pattern à répliquer pour valider d'autres filtres binaires (rebasecalled).
