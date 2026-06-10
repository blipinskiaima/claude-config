---
name: int-gration-pipeline-feature-page-exploration-beta
description: "Tower lit (read-only) les résultats du pipeline ~/Pipeline/Feature pour la page /exploration-beta. Contraintes d'exécution, schéma DB, endpoints, gotchas."
metadata: 
  node_type: memory
  type: project
  originSessionId: 2fea8339-c2d3-4481-b396-f4f250f7f6ce
---

# /exploration-beta — connexion au pipeline Feature (2026-06-09)

Nouvelle page Tower qui expose les résultats du banc de test de features
`~/Pipeline/Feature/` (combos de features cancer/healthy, cohorte figée `std_359`).

## Principe : Tower est un READER, pas un exécuteur

```
Hôte : bash main.sh --features "..."  →  écrit feature_runs.duckdb + result/{combo}/{png,csv}
        │  (R/Rscript + write — UNIQUEMENT sur l'hôte)
        ▼  bind-mount /home/blipinski/Pipeline → /pipeline:ro
Tower (conteneur) ── lecture read-only à chaque requête ──▶ affiche PNG + CSV + best combos
```

**Pourquoi Tower ne peut PAS exécuter `main.sh`** (décision d'archi, demandée à Boris) :
1. Le conteneur n'a **pas de R/Rscript** (Dockerfile = python:3.12-slim + Node seulement).
2. `/pipeline` est monté **`:ro`** → `main.sh` ne peut pas écrire `result/` ni la DB.
3. Cohérent avec l'archi Tower (reader de DuckDB alimentées par daemons hôte).

→ Stratégie retenue : **affichage seul**. Le bouton « Exécuter » lit la DB ; si le combo
n'est pas calculé, on affiche la commande `bash main.sh --features "..."` à lancer sur l'hôte.

## Gotcha : `feature_db.py best_combo` non lançable en subprocess

Même `best_combo` (qui ne fait que lire) est INLANÇABLE depuis le conteneur : son
`connect()` ouvre la DB en **read-write** (CREATE TABLE IF NOT EXISTS + migrations) → échoue
sur le mount `:ro`. **Solution** : rejouer la même requête SQL en **read-only** dans
`src/feature_service.py::best_combos()` (même `ORDER BY delta_sens_active_nomut DESC, tie
sens_active_nomut DESC, features ASC`, garde anti-injection sur le nom de colonne KPI).

## Clé canonique des combos (ordre indifférent)

`src/feature_service.py::normalize_features()` est une **copie exacte** de
`feature_db.py::normalize_features` : `mvaf_v1` en premier, puis tri alpha. Donc
`ichor_x100,mvaf_v1` ≡ `mvaf_v1,ichor_x100` → même clé, même ligne DB (index unique
`(cohort_ref, features)`). Vérifié : Tower == benchmark sur tous les ordres.

## Schéma `feature_runs.duckdb` (lu par Tower)

- Table `results` : `cohort_ref`, `features` (clé canonique), `is_baseline`, sens_* + delta_*,
  `path`, **`png_path`**, **`csv_path`** (chemins ABSOLUS hôte), `run_at`. Index unique (cohort_ref, features).
- Table `cohorts` : `cohort_ref`, `preset`, `n_scored`, `nb_healthy`, `nb_cancer`, `frozen_at`.
- Manifest figé `data/cohorts/std_359/manifest.json` : `filter_spec` (conditions) + composition
  (359 = 50 sains + 285 cancer + 24 autres). **Source des conditions** affichées (pas de hardcode Tower).

## Réécriture des chemins absolus

`png_path`/`csv_path` sont des chemins hôte `/home/blipinski/Pipeline/Feature/...`. Dans le
conteneur, `FeatureService.resolve_artifact()` réécrit le préfixe
`/home/blipinski/Pipeline` → `/pipeline` si le chemin original n'existe pas (marche en local ET conteneur).

## Fichiers

| Couche | Fichier |
|---|---|
| Config | `src/config.py` — `feature_db_path` (docker `/pipeline/Feature/...` / local) |
| Service | `src/feature_service.py` — normalize, get_result, best_combos, cohort_info, resolve_artifact |
| Router | `backend/routers/exploration_beta.py` — `/result` `/png` `/best-combos` `/cohort-info` |
| Enregistrement | `backend/main.py` |
| Hooks | `frontend/src/lib/exploration-beta.ts` (TanStack) |
| Données figées | `frontend/src/lib/exploration-beta-data.ts` (FEATURE_NAMES + COHORT_FILTERS désactivés) |
| Page | `frontend/src/pages/ExplorationBeta.tsx` |
| Route + nav | `frontend/src/App.tsx` (pleine largeur) + `Sidebar.tsx` (Telescope, groupe Biologie) |

## Mise à jour des données → PAS de restart Tower

Le bind-mount est live + connexion read-only fraîche par requête → quand Boris relance
`main.sh` (hôte), Tower voit la DB à jour immédiatement (prouvé : conteneur voit le même
COUNT que l'hôte sans restart). Seul le cache front TanStack (`staleTime` best-combos 60s,
cohort-info 5min) → un F5 rafraîchit tout de suite.

## Contrôles « Meilleurs combos » + Venn (2026-06-09)

- **Venn composition** dans « État de la cohorte » : positifs (`nb_cancer`) / négatifs (`nb_healthy`) / suspects (`n_other`), groupes **exclusifs** (le recouvrement central = convention visuelle, pas une vraie intersection). Pur frontend (consomme `CohortInfo`), aucun backend. Layout 50/50 Venn | conditions.
- **Best combos cliquables** : clic sur une ligne → `setSelectedFeatures(features.split(","))` + `setSubmitted(features)` → le Résultat s'affiche. Combo issu du benchmark donc `found=true` garanti ; `submitted === featureStr` donc pas de warning « sélection modifiée ».
- **Top N (5/10/20/50) + filtres présence/absence** : `best_combos(cohort_ref, top, kpi, include, exclude)`, `include`/`exclude` en CSV. Filtre **AVANT** `ORDER BY ... LIMIT` → le Top N porte sur les combos filtrés. Présence = **ET** (toutes présentes), absence = **aucune** ; sélecteurs mutuellement exclusifs côté UI.
- **Gotcha token-safe (réutilisable)** : pour tester la présence d'une feature dans la clé canonique `"a,b,c"`, utiliser `list_contains(string_split(features, ','), ?)` en **paramètre lié** — JAMAIS `LIKE '%mvaf_v1%'` qui matcherait aussi `mvaf_v12`/`mvaf_v13`. Vérifié contre la DB (0 fuite substring).
- CSV Résultat : colonnes `nb_healthy`/`nb_cancer` masquées dans `KpiTable` (compo déjà donnée par le Venn).

## Rollback

Tag git `pre-exploration-beta` (avant toute la feature).
