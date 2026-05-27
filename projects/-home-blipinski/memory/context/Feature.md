# Context — Feature — 2026-05-26T14:00+02:00

**Branche** : main
**Dernier commit** : 55c4136 — feat: étend le pool avec probes EPIC/Loyfer + features short_read (3 livrables)
**Status** : clean (sauf `Je veux étendre ce script pour entraîner.ini` non-tracké volontaire — notes perso Boris)

## Où j'en suis

Session terminée — pool Feature étendu de 7 → 11 features candidates avec ajout des **blocs probes** (EPIC 16 + Loyfer 31) et **2 features short_read** (`mvaf_v1_short_read` + `ichor_short_read_x100`). Trois livrables complets produits et committés sur `github.com/aima-dx/Feature.git` (remote nouveau, push initial). Skill `/run-new-feature` créé pour orchestrer les futurs tests.

Prochaine décision en attente : adoption ou non des features short_read au pool de prod (gain démontré +4.6 pp Sens@95% Active_NoMut, couverture 99.6%).

## Ce qui marche / ce qui foire

- ✓ Pool étendu avec succès, support des blocs (`source_cols` pluriel) ajouté à `grid_search.py`
- ✓ Livrable `combined_v2_probs` : adoption probes confirmée (+14.5 pp KPI clé sur n=480)
- ✓ Livrable `combined_v4_short_read` : ajout short_read validé rigoureusement (cohortes 478 vs 480, +4.6 pp KPI clé)
- ✓ Skill `/run-new-feature` testé 2 fois avec succès (orchestre les 9 briques du workflow)
- ✓ Remote `origin` configuré + push initial sur `github.com/aima-dx/Feature.git`
- ⚠ `feature_runs.duckdb` à 1392 runs — combos avec short_read invalidés/recalculés 2 fois (n=478 final)
- ⚠ Twist_1pct ajouté en cohorte raw (734 samples) mais filtré par label NA (cohorte effective inchangée n=480/478)

## Prochaine étape

**Décision Boris** : adopter (ou non) `mvaf_v1_short_read` + `ichor_short_read_x100` au pool de production. Si adoption recommandée :
1. Test de robustesse via 5 seeds XGBoost différents (vérifier que +4.6 pp n'est pas du bruit)
2. Validation sur cohorte indépendante (Alcapone ou nouveaux samples)
3. Push de la décision dans `raima` / pipeline de production
