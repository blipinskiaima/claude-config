---
name: Investigation multi-version Dorado
description: Résultats de l'investigation multi-version basecalling sur les Healthy HCL — impact des modèles Dorado sur les faux positifs mVAF
type: project
---

## Objectif

Comparer l'impact des modèles Dorado (V4.2.0, V4.3.0, V5.0.0, V5.2.0) sur les Faux Positifs mVAF chez les Healthy HCL.

## Samples testés

**Faux Positifs** (mVAF > 0) : Healthy_4, Healthy_11, Healthy_12, Healthy_25, Healthy_34
**Vrais Négatifs** (mVAF = 0) : Healthy_3, Healthy_8, Healthy_14, Healthy_23, Healthy_26

## Résultats clés

### V5.2.0 perd ~24% des reads primaires
Healthy_11 : 25.1M primary reads (V5.2.0) vs ~33M (V4.2-V5.0). Dorado 1.4.0 applique un filtre qualité plus strict.

### Concordance des appels de méthylation
Les appels méthylé/non-méthylé concordent entre toutes les versions sur les sites CpG communs. Différences mineures dans les valeurs ML (±5, normal entre basecallers).

### Trimming résolu
`--kit-name SQK-NBD114-24 --trim all` → delta=0 avec MinKNOW (reads identiques en longueur).

### Builds Dorado identiques
CDN standalone (0.9.6+0949eb8d) et BS 7.9.8 (0.9.6+49e25e9) produisent des résultats strictement identiques.

## État du batch (dernière mise à jour)

- Healthy_4 : 4/4 versions OK, uploadées S3
- Healthy_11 : 4/4 versions OK, uploadées S3
- 8 samples restants : batch V4.3.0/V5.0.0/V5.2.0 en cours

## Questions ouvertes

1. Impact de la perte de reads V5.2.0 sur le mVAF
2. V4.2.0 pour les 8 samples restants — nécessaire ?
3. Analyse comparative mVAF entre versions — en attente des résultats complets

**Why:** Investigation batch effect — le modèle de basecalling est une source potentielle de biais inter-centres.
**How to apply:** Toujours tracer la version Dorado utilisée. Résultats multi-version à intégrer dans l'analyse batch effect CGFL vs HCL.
