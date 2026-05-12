---
name: Sens_Active redéfini = cancer_truth (2026-05-11)
description: Sur /exploration tableau Sensibilité stratifiée VAF, colonne "Cancer actif" utilise `cancer_truth` (= mutated_flag OR active_cancer_flag) au lieu de `active_cancer_flag` strict. Demande Michael.
type: project
originSessionId: b5968421-79e5-45cf-aaae-72538f63856a
---
## Quoi

`src/exploratory_compute.py:548` modifié :
```python
# avant
"Sens_Active": stat(df["active_cancer_flag"]),
# après
"Sens_Active": stat(df["cancer_truth"]),
```

Conséquence visible sur https://tower.aima-diagnostics.com/exploration :
- Sans filtre : dénominateur "Cancer actif" passe de 270 → 288 (+18 mutated-only)
- `?indications=Colon` : 67 → 69 (+2 samples CGFL/Colon_32 et HCL/Colon_32 mutated avec `active_cancer` NaN ou "No")

## Why

Demande de Michael : un sample avec VAF>0 est une vérité biologique cancer, même si la metadata clinique `active_cancer` est manquante / "no" / "unknown". Cas typique = MRD post-chirurgie (rémission clinique avec ctDNA résiduel détectable).

Conséquence acceptée : Tower diverge du pipeline R d'origine (`exploratory-analysis-CGFL-HCL`) sur cette colonne. La validation cell-by-cell vs R main ne tient plus pour `Sens_Active`. Si Michael veut aligner R, il faudra modifier `07_*.R` côté R.

## How to apply

- **Ne pas re-débattre** : décision Michael, pas une bizarrerie de code.
- `Sens_Active_NoMut` reste sur son mask propre (`active_cancer_flag & ~mutated_flag`) — métrique distincte "cliniquement actif sans signal moléculaire".
- Modif uncommitted sur `main`. À commit/push si tu veux pérenniser au prochain rebuild d'image (sinon un `git reset .` la perdrait).
- Tests : `tests/test_exploratory_compute.py` ne couvre pas `Sens_Active` → rien cassé par cette modif. Les 4 échecs `TestRegressionVsR` sur `N_Cancer` (331 vs 298 snapshot R) sont indépendants : la base a divergé du snapshot R car +33 nouveaux cancers depuis la dernière calibration.

## Différence dénominateurs entre tableau haut et stratifié

`Performance Detection` (KPI haut) utilise cohorte `cancer_detection` (retire TNE/Nuclear seulement).
`Sensibilité stratifiée` utilise cohorte `stratified` (retire TNE/Nuclear **ET** Bladder_Blood, 56 samples retirés dont 43 actifs).

Donc même après la modif : N_Cancer KPI (331) ≠ Cancer actif stratifié (288). L'écart résiduel = filtre Bladder_Blood, **conservé**. Bladder_Blood = panel hors-cible méthylation, biaiserait artificiellement les stats actif-sans-mutation.
