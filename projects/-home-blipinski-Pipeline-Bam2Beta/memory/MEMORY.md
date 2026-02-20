# Bam2Beta Project Memory

## Key Facts

- Current version: V1.0.1 (tag V1.0.0 qualifie, V1.0.1 en dev)
- Container: `blipinskiaima/bam2beta:latest` + `blipinskiaima/raima:latest`
- Raima package version: 0.4.3 (0.4.5 contient `depth_per_region` non exportee, casse le CNV)
- Pipeline modules: MERGE, BETA (EPIC), BETA_28M (Loyfer), FRAG, CNV, SCORE, QC
- Prod profile enables: MERGE + BETA + FRAG + CNV + SCORE

## Verified Findings

- **GRCh38 vs hg38**: resultats strictement identiques sur Healthy_826 (2026-02-20)
  - Les deux FASTA utilisent la convention `chr` prefix
  - GRCh38 "no alt analysis set" = pas de contigs alt/random
  - Scores raima, CNV, fragmentomics, QC metrics: tous identiques
  - See [test-results.md](test-results.md) for details

## Debugging Insights

- **raima 0.4.5 casse Raima_process_CNV** : `depth_per_region` n'est pas exportee dans 0.4.5. Fix: utiliser raima 0.4.3 dans le Dockerfile.
- **Container raima:latest doit etre rebuild** apres modification du Dockerfile — sinon Docker utilise l'ancienne image cachee.
- Le test GRCh38 a fonctionne avec l'ancien cache Docker (raima 0.3.2 dans le container) car `Raima_process_CNV` n'appelle pas `depth_per_region` dans cette version.

## Architecture Notes

- `main.nf` orchestre les modules via conditionals (`params.BETA`, `params.FRAG`, etc.)
- Channels: BAM_METADATA fournit [sample_id, bam, bai] a tous les modules
- BED files en `/scratch/dependencies/bed/` ciblent chr1-22+X+Y uniquement
- CNV utilise des bins de 100kb avec filtres de longueur de reads configurable
- Le champ `mVAF` a ete renomme `TF` (tumor fraction) dans commit 7837cd0

## User Preferences

- Langue de communication: francais
- Utilise skills Claude Code (test_bam2beta, save-code, etc.)
- Prefere les reponses concises avec tableaux de comparaison
- Travaille depuis ~/Run ou ~/Run2 pour les runs Nextflow
