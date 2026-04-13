# Memory — basecall

## Contexte

Projet R&D de re-basecalling des POD5 Oxford Nanopore avec Dorado standalone (Docker GPU).
Objectif : investiguer les faux positifs mVAF chez les Healthy HCL.

## Architecture

- Script `basecall.sh` : idempotent avec logging
- Docker image `pod2bam:0.9.6` (base ontresearch/dorado)
- Comparaison MinKNOW intégré vs Dorado standalone
- Deux références : hg38 et GRCh38 no_alt
- 10 samples Healthy, dont 1 faux positif (Healthy_4, mVAF=1.244)

## Points clés

- Pas de repo git — projet exploratoire
- Le README sert de lab notebook (commandes exécutées avec dates)
- Lié au projet Pod2Bam (image Docker partagée)
