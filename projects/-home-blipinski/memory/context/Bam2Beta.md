# Context — Bam2Beta — 2026-08-12T10:37:00+00:00

**Branche** : main
**Dernier commit** : c1590d3 — docs: QC/Samtools dans l'arborescence des sorties (n50_ratio.tsv)
**Status** : 9 fichiers modifiés — dont 5 appartenant à une AUTRE session (voir plus bas)

## Où j'en suis
Instruction du **palier 1 du doc QC-seuils** (5 candidats de métriques QC) et livraison de
la métrique retenue. Le ratio **N50/N75 avant/après filtre 1 kb** est mesuré sur les 1 324
samples liquid, les TSV rétrospectifs sont sur S3, et le calcul est câblé dans `Extract_read`.
Point d'arrêt : feature terminée et poussée.

## Ce qui marche / ce qui foire
- ✓ `a95a36b` — N50/N75 dans `Extract_read` : 28 insertions, 0 ligne modifiée. Testé
  end-to-end, sortie **identique octet par octet** au rétrospectif (`Healthy_826`, `Breast_6`)
- ✓ 1 324 `n50_ratio.tsv` sur S3 (811 CGFL + 513 HCL), vérifiés par scan récursif, 0 écrasement
- ✓ Palier 1 instruit : MAD **écarté** (redondant), N50 **retenu**, `coverage_percent`
  **écarté** (corr 0,97 avec depth). Verdicts portés dans `docs/QC-seuils-biopsie-liquide.md`
- ✓ Finding : `Breast_6` = contamination gDNA authentique (99 % aligné en continu, max 57 kb),
  ratio 24,44 → 1,11 après filtre. 9 plasmas > 50 % de masse en reads > 1 kb, dont 5 rendus
- ✓ Finding : le « taux de mapping » du doc n'en est pas un — il mesure les **alignements
  multiples**. Deux artefacts distincts : concatémères de ligation (CGFL `Lung_Alc`, morceaux
  dispersés au hasard) vs reads palindromiques (HCL `Colon`, même locus brin opposé)
- ✗ `docs/QC-seuils`, `workflow/beta.nf` (idxstats), `frag.nf` (Length_Distribution_Plot),
  `bin/length_distribution/`, `NOTE_READ.txt` : **modifiés par une autre session**, non
  commités. La section « méthylation globale CpG » du doc contient des chiffres que je n'ai
  pas produits et ne peux pas certifier
- ✗ `conformity/check-run-output.sh` ne vérifie aucun fichier de `QC/Samtools/` — le
  `n50_ratio.tsv` est hors contrat de qualification
- ✗ Aucun seuil de rendu fixé sur le ratio : à calibrer **par matrice** (plasma 1,10 vs
  urine 1,78, distributions disjointes) et **dans le sens haut seulement**

## Prochaine étape
Trancher le sort des modifications de l'autre session (commit ou abandon), puis décider si
`n50_ratio.tsv` entre dans `check-run-output.sh` — ce qui le ferait basculer dans la
qualification ISO 15189.
