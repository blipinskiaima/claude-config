# Context — Feature — 2026-06-22T17:25:46+00:00

**Branche** : main
**Dernier commit** : 029021f — feat(eval): unité d'évaluation "dilution" (scoring des samples Twist)
**Status** : clean (résultats régénérés sous result/, gitignoré)

## Où j'en suis
Feature "unité d'éval dilution (Twist)" TERMINÉE, commitée et poussée (029021f).
Les 22 samples Twist valides sont scorés par les modèles entraînés et écrits dans
result/speedvac_{no,yes}/scores.csv, taggés `unit='dilution'`. Hand-off Tower déjà rédigé.

## Ce qui marche / ce qui foire
- ✓ 2 variantes speedvac re-run OK (313s / 325s, 1023 combos, 0 échec)
- ✓ Additivité prouvée : scores.csv train+Alc + eval_kpis.csv byte-identiques au baseline
- ✓ mvaf_only == feature brute ; combos XGBoost ∈ [0,1] ; 0 NA sur les 22 Twist
- ✓ Reps conservés (unique_id conditionnel) ; Twist_10_8 KO exclu
- ⚠ Dossiers non-suivis `result copy/` + `result_old/` présents (pas touchés — à nettoyer par Boris si artefacts)
- ⚠ Tower doit filtrer `unit=='dilution'` dans scores.csv (intégration côté Tower restante)

## Prochaine étape
Côté Aima-Tower : brancher la lecture des courbes de dilution (filtre `unit=='dilution'`,
score = colonne-combo). Optionnel Feature : mapping pattern→unit en tête de select_cohort_eval.py si plusieurs cohortes éval à venir.
