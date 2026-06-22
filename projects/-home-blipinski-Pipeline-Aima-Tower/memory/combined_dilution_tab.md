---
name: combined-dilution-tab
description: "Page /combined (ex-exploration-beta) : refonte (onglets, params à gauche, défaut SpeedVac) + onglet Dilution piloté par le combo via source unique scores.csv (unité 'dilution', archi α)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5d91e6d3-3672-4492-bcad-6211c89a0d0f
---

# Page `/combined` — refonte + onglet Dilution (2026-06-22)

`/exploration-beta` renommée **`/combined`** (route, fichiers `Combined.tsx`/`combined.ts`/`combined-data.ts`/`combined.py`, endpoints `/api/combined`). Commit refactor `0fb9357` ; feature dilution dans le commit suivant.

## Refonte Combined (5 points)
- Panneaux « Cohorte » + « État de la cohorte » **supprimés** (+ orphelins front/back : endpoint `/cohort-info`, `feature_service.cohort_info`, `_conditions_from_spec`, `import json` orphelin).
- Défaut cohorte d'entraînement = **SpeedVac yes** (`std_522`).
- Panneau Résultat : 2 blocs superposés → **3 onglets** (Initial / Lung-DI par stade / Dilution).
- Nouvelle Card « Paramètres d'évaluation » à gauche (Profondeur + Spécificité cible + Unité d'évaluation, déplacés depuis la droite).

## Onglet Dilution — déblocage multi-features (architecture α)
**Problème** : tracer une courbe de dilution Twist « selon le combo » exige un score par sample Twist. Le `combined_score` est un **modèle XGBoost** (pas une somme pondérée) **non exporté** → Tower (read-only, pas de R) ne peut pas l'inférer.

**Solution retenue = α (pas β)** : le **pipeline Feature score les Twist** (nouvelle unité d'éval `dilution`, sans retoucher la cohorte train) → **source unique** = `result/speedvac_{no,yes}/scores.csv`. Tower reste **READER**. (β = inférence XGBoost dans Tower → rejeté : casse l'archi reader-only, skew train/serve, +dépendance xgboost.)

## Contrat scores.csv (jointure critique Tower ↔ Feature)
- Format **wide** : 13 colonnes méta + ~1022 colonnes-combo. Twist = lignes `unit == 'dilution'` (22 samples ; `Twist_10_8` KO exclu).
- Colonne-combo nommée avec séparateur **`+`** (`mvaf_v1+ichor_x100`), ordre canonique mvaf_v1 d'abord. La clé Combined utilise `,` → **`features.replace(",", "+")`** pour le lookup colonne.
- `speedvac`/`cohort_ref` **implicites dans le chemin** (pas des colonnes).
- mono mvaf_* = feature brute (hors [0,1]) ; multi = proba XGBoost ∈ [0,1].
- Seuil = `quantile_type1(scores[is_healthy & eval_cohort=='train'][combo_col], spec)` — **Tower le dérive lui-même** (le pipeline ne produit pas de seuil).

## Tower
- Backend : `dilution_service.get_combo_series(features, speedvac, target_spec)` (single-pass `csv.reader`+index, rapide sur 1035 cols) + endpoint `/api/combined/dilution`. `get_series` trace-prod + `mvaf_threshold` + `_STATS` + héritage `DuckDBMixin` **retirés**.
- Frontend : hook `useCombinedDilution` (lazy, fetch si onglet actif) + 3ᵉ onglet réutilisant `DilutionChart` (prop `yMinTop=0` = auto-échelle Y pour proba [0,1]).
- **Page `/dilution` autonome supprimée** (route, Sidebar item + icône Droplets, `Dilution.tsx`, `useDilutionSeries`/`DILUTION_STATS`, router `/api/dilution`). `DilutionChart` + type `DilutionPoint` conservés (réutilisés par l'onglet).
- Seuil dilution hérité de Combined : `targetSpec` (90/95/98) + `speedvac`.

## Validé
Smoke test conteneur : mono `mvaf_v1` (seuil 0.6906, % bruts) + multi `mvaf_v1,ichor_x100` (seuil 0.7627, proba décroissante 0.987→0.18) ; ancien `/api/dilution` → 404.

Voir aussi : [[feature_dilution_page]] (V1 trace-prod, obsolète — remplacée), [[feature_pipeline_integration]].
