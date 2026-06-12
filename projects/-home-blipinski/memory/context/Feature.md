# Context — Feature — 2026-06-12T12:00

**Branche** : main
**Dernier commit** : 4ac2adb — feat(pipeline): unités Lung-DI par stade + propagation stage
**Status** : clean

## Où j'en suis
Pipeline Feature : 12 unités d'éval (7 principales + 5 stades Lung-DI précoce actif). Colonne `stage` propagée select → train → scores → eval. Tower `/exploration-beta` branchée (section stades + best combos). Session close : Feature commit `4ac2adb` poussé.

## Ce qui marche / ce qui foire
- ✓ `script/eval.R` : 5 unités `lung_I_III`…`lung_NR` (Lung-DI précoce + active_cancer=Yes + stage)
- ✓ `select_cohort_*.py` + `train.R` : colonne `stage` depuis trace-prod
- ✓ `result/speedvac_{no,yes}/` régénérés (344 / 532 samples train)
- ✓ Tower : section stades Lung-DI + sélecteur best combos étendu (commits Aima-Tower session précédente)
- ✓ +9/+10 nouveaux cancers trace-prod identifiés (9 Bladder sang CGFL communs + HCL_Colon_2 speedvac yes)
- ✗ Rien en suspens identifié

## Prochaine étape
Au besoin : analyser KPIs par stade Lung-DI (meilleurs combos `lung_I`…`lung_NR`) ou décider exclusion des nouveaux Bladder sang.
