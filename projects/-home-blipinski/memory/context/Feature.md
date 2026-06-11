# Context — Feature — 2026-06-11T17:42

**Branche** : main
**Dernier commit** : 52aa974 — refactor(pipeline): nouveau pipeline script/ (combos × speedvac × 7 unités)
**Status** : clean (result/, archives/, result_no_lung/ gitignored)

## Où j'en suis
Pipeline Feature entièrement réécrit dans `script/` (combos par feature, variantes speedvac, 7 unités dont lung_di) et branché dans Aima-Tower `/exploration-beta`. Session close : tout committé/poussé (Feature 52aa974 + Aima-Tower 0960bbd), Tower rebuild/redéployée.

## Ce qui marche / ce qui foire
- ✓ `script/` : select_cohort_train/eval, train.R multi-combos (1023), eval.R baseline vs combiné, 7 unités
- ✓ `result/speedvac_{no,yes}/` régénérés (480 / 667 samples)
- ✓ Tower : sélecteur speedvac + spec 98% + best combos par unité + export CSV + 7e facette/colonne (vérifié live)
- ✓ Lung-DI précoce = 28 cancers du train
- ✗ Rien en suspens identifié

## Prochaine étape
Au besoin : analyser les meilleurs combos par unité (notamment lung_di et alc) pour décider des features à retenir.
