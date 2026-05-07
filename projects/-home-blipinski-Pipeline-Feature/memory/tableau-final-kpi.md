---
name: Tableau final KPI Feature
description: Tableau de référence du projet Feature/ pour comparer les features testées — ligne = KPI, colonne = feature. Boris ajoute une colonne par nouvelle feature testée. Quand il dit "résultat à comparer", il parle de ce tableau.
type: project
originSessionId: 35ba0796-87d1-48a8-900c-d868f78cbadf
---
# Tableau final — projet Feature/

Convention validée le 2026-05-07. Format : **ligne = KPI, colonne = feature testée**.

**Why:** Boris a explicitement défini cette convention après le 1er comparatif. Il veut une vue synoptique unique pour suivre l'évolution des features testées et leur impact sur sens/spé.

**How to apply:** À chaque test d'une nouvelle feature dans `Feature/features/{nom}/`, **ajouter 2 colonnes** au tableau (Michael, Feature current) avec les mêmes KPI (AUC ALL/CGFL/HCL, Sens à target_spec 0.95 et 0.90 stratifié All/LowVAF/HighVAF/Active no mut). Quand Boris demande un comparatif, présenter sous cette forme.

## Convention KPI

```
   target_specificity = 0.95  → "Sens@95%" (standard ISO 15189)
   target_specificity = 0.90  → "Sens@90%" (complément)
   threshold = quantile(scores_healthy, target_spec, type=1)
   AUC          = score-rank based, indépendant du seuil
   N samples    = après cascade de filtres (cf. cohort-filters-cascade.md)
                  diffère selon les features sélectionnées (NA cascade)
```

Voir [cohort-filters-cascade.md](cohort-filters-cascade.md) et [target-specificity.md](target-specificity.md).

## État actuel (6 features testées au 2026-05-07)

| KPI | mVAF v1 (M) | mVAF v1 (F) | frag2 (M) | frag2 (F) | frag1 (M) | frag1 (F) | frag1+2 (M) | frag1+2 (F) | frag-diff (M) | frag-diff (F) | frag1+2+cnv (M) | frag1+2+cnv (F) | props_epic (M) | props_epic (F) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **N samples** | 456 | 459 | 456 | 459 | 456 | 459 | 456 | 459 | 456 | 459 | 456 | 459 | **413** | **412** |
| **AUC ALL** | 0.9090 | 0.9058 | 0.9459 | 0.9417 | 0.9445 | 0.9410 | 0.9493 | 0.9441 | 0.9447 | 0.9418 | **0.9642** | **0.9612** | 0.9418 | 0.9472 |
| **AUC HCL** | 0.9093 | 0.9021 | 0.9766 | 0.9717 | 0.9678 | 0.9640 | 0.9767 | 0.9754 | 0.9758 | 0.9722 | **0.9833** | **0.9832** | 0.9730 | 0.9717 |
| **AUC CGFL** | 0.9192 | 0.9192 | 0.9001 | 0.8959 | 0.8979 | 0.8932 | 0.8986 | 0.8929 | 0.8986 | 0.8964 | 0.9029 | 0.8973 | 0.8919 | 0.9066 |
| **Sens@95% All cancers** | 78.79% | 78.28% | 82.58% | 82.77% | 76.52% | 77.15% | 83.33% | 83.90% | 82.95% | 80.52% | **86.36%** | **86.14%** | 81.61% | 82.69% |
| **Sens@95% Low VAF (0-2%)** | 76.60% | 76.00% | 85.11% | 86.00% | 80.85% | 82.00% | 85.11% | 86.00% | 85.11% | 84.00% | n/a | n/a | n/a | n/a |
| **Sens@95% High VAF (>2%)** | 99.07% | 99.07% | 97.20% | 96.30% | 98.13% | 98.15% | 97.20% | 97.22% | 98.13% | 95.37% | n/a | n/a | n/a | n/a |
| **Sens@95% Active no mut** | 60.00% | 58.72% | 67.27% | 67.89% | 53.64% | 54.13% | 69.09% | 69.72% | 67.27% | 64.22% | **73.64%** | **74.31%** | 67.29% | 67.92% |
| **Sens@90% All cancers** | 84.85% | 84.27% | 86.36% | 89.14% | 87.88% | 86.89% | 86.36% | 86.14% | 85.61% | 85.77% | **90.91%** | 89.89% | 85.44% | 89.23% |
| **Sens@90% Active no mut** | 69.09% | 67.89% | 74.55% | 77.98% | 76.36% | 74.31% | 74.55% | 72.48% | 72.73% | 72.48% | **83.64%** | **80.73%** | 73.83% | 80.19% |

### Features XGBoost par colonne

| Colonne | Features XGBoost | N |
|---|---|---|
| `frag2` (= ref Michael) | mvaf, ichor×100, **frag_mode2** | 456/459 |
| `frag1` | mvaf, ichor×100, **frag_mode1** | 456/459 |
| `frag1+2` | mvaf, ichor×100, frag_mode1, frag_mode2 | 456/459 |
| `frag-diff` | mvaf, ichor×100, **frag_mode1 - frag_mode2** | 456/459 |
| `frag1+2+cnv` | mvaf, ichor×100, frag_mode1, frag_mode2, **score_cnv** | 456/459 |
| `props_epic` | 16 cols EPIC v1 (`prop_blood_0`, … `prop_testis_0`), frag_mode1, frag_mode2, ichor×100 (= **19 features**) | **413/412** (cohorte réduite — props EPIC dispo 605/709) |

### Conclusion provisoire

🥇 **`frag1+2+cnv`** = vainqueur clair :
- AUC ALL : 0.9612 → 0.9642 (+0.015 vs frag1+2)
- Sens@95% Active_NoMut : 73.6–74.3 % (+4.6 pp vs frag1+2)
- Sens@90% Active_NoMut : 80.7–83.6 % (+6.2 à +9.1 pp vs frag1+2) ★★

→ **`score_cnv` était la feature manquante**. À adopter en prochaine version du Combined.

⚠ **`props_epic`** : pas de gain et **perd 10 % cohorte** (props EPIC NA pour 47 samples). À écarter.

`frag-diff` ≈ frag2 (équivalent), `frag1` seul décroche sur Active_NoMut.

## Origine des chiffres

- **mVAF v1 (baseline)** : col `mvaf_v1` du snapshot Parquet Feature current (`cohort/snapshot_2026-05-06_v4.parquet`), seuil = `quantile(healthy_scores, target_spec, type=1)` via `10_*.R` — 459 samples (192 H + 267 C).
- **Combined (Michael, ref figée 27/04)** : `rds/all_res_v5_all.rds` (Michael, 27/04) enrichi avec ichor/frag/speedvac depuis trace-prod, → `build_combined_score()` (XGBoost 5-fold) → `10_*.R`. 456 samples.
- **Combined (Feature, current)** : snapshot Parquet v4 du 2026-05-06 22:02 (valeurs trace-prod à jour) → `build_combined_score()` → `10_*.R`. 459 samples (cohorte v3 avant fix bis = 449, +5 fix bis CGFL, +5 nouveaux Lung HCL, -2 Lung_23/84 perdus à cause de "probable" non matché).

Détails de la validation Michael ↔ Feature : `~/Pipeline/Feature/features/combined_mvaf_ichor_fragmode2/validation/poc/` (preuve bit-exact à cohorte égale) et `.../current/` (analyse à jour).

## Modèle Combined

Features XGBoost (5-fold stratifié, max_depth=3, lr=0.1, subsample=0.8, colsample=0.8, nrounds=100, seed=42) :
1. `mvaf_v1` (méthylation raima)
2. `frag_mode2` (mode 2 KDE longueurs reads)
3. `ichor_tf × 100` (ichorCNA tumor fraction)

`frag_mode1` est mentionné dans le README de Michael mais **n'est pas** dans le modèle (incohérence README ↔ code 09).

## Prochaines colonnes à venir

Quand Boris teste une nouvelle feature : nommer la colonne avec le nom du dossier `features/{nom}/`, source = Feature current (snapshot trace-prod le plus à jour au moment du test).
