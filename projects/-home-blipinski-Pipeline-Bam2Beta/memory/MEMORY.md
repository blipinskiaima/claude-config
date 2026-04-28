# Bam2Beta Project Memory

## Key Facts

- Current version: V1.1.2 (tag V1.1.2, qualifie sur Healthy_826 le 2026-04-08)
- Container: `blipinskiaima/bam2beta:latest` + `blipinskiaima/raima:latest`
- Raima package version: 0.4.13 (0.4.5 contenait `depth_per_region` non exportee, 0.4.13 retrocompatible verifie)
- Pipeline modules: MERGE, BETA (EPIC), BETA_28M (Loyfer), FRAG, CNV, ICHORCNA, SCORE, QC
- Prod profile enables: MERGE + BETA + FRAG + CNV
- Retry strategy: doublement CPU/RAM par tentative, max 10, plafond cpus_max/memory_max

## Verified Findings

- **GRCh38 vs hg38**: resultats strictement identiques sur Healthy_826 (2026-02-20)
  - Les deux FASTA utilisent la convention `chr` prefix
  - GRCh38 "no alt analysis set" = pas de contigs alt/random
  - Scores raima, CNV, fragmentomics, QC metrics: tous identiques
  - See [test-results.md](test-results.md) for details

- **BAM merge verification** (2026-03-13): le merge (samtools cat + sort) ne perd aucune donnee ni metadonnee
  - 3/3 PASS : Breast_1 (CGFL liquid, 44 BAM), Nuclear_4 (HCL liquid, 433 BAM), Colon_0001N8M (CGFL solid, 129 BAM)
  - Reads : Δ=0 flagstat sur toutes les metriques. Metadonnees : 0 @RG/@PG absent, @SQ identiques
  - Headers intra-horaires : 44/44 identiques (verification exhaustive Breast_1)
  - BAM horaires 100% redondants avec le merge
  - See [bam-merge-verification.md](bam-merge-verification.md) for details

- **Volumetrie S3** (2026-03-13): quantification complete des buckets
  - BAM horaires : 30.67 To (supprimables). BAM merges : 18.62 To. RetD complet : 24.86 To
  - POD5 SCW : 75.12 To. POD5 AWS : 66.76 To. Doublons : 11.81 To
  - Total stockage S3 : ~186 To. Economies possibles : ~42.5 To (BAM horaires + doublons POD5)
  - See [s3-volumetry.md](s3-volumetry.md) for details

- [Batch effect investigation](batch-effect-investigation.md) — Investigation complète CGFL vs HCL : 17% FP Healthy HCL (V1), CNV biaisé, pas d'effet taille fragments

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
- `raima_score_loyfer.R` : `max_read_len` conditionnel (solid=Inf, liquid=1000) via `--type` param
- `params.cpu`/`params.memory` remplaces par `params.cpus_max`/`params.memory_max` en V1.0.1

## User Preferences

- Langue de communication: francais
- Utilise skills Claude Code (test_bam2beta, save-code, etc.)
- Prefere les reponses concises avec tableaux de comparaison
- Travaille depuis ~/Run ou ~/Run2 pour les runs Nextflow

## ichorCNA Module (2026-03-20)

- Container: `blipinskiaima/ichorcna:latest` (R + hmmcopy readCounter + ichorCNA + BSgenome.Hsapiens.UCSC.hg38)
- Workflow: `workflow/ichorCNA.nf` — 2 processus (readCounter → runIchorCNA)
- Scripts: `bin/ichorCNA/` (run_readCounter.sh, run_ichorCNA.R, create_panel_of_normals.sh)
- Panel par défaut: Florian (`ichorCNA-panel-of-normals_median.rds`), Broad et custom aussi disponibles
- Dependencies: `/scratch/dependencies/ichorCNA/` (gc_wig, map_wig, centromere, panels)
- Test Healthy_826: TFx=0.026, ploidy=2.306 — PASS
- `getwilds/ichorcna` testé et rejeté (pas de readCounter, pas de libs graphiques png)
- `remotes::install_github` n'installe pas `inst/scripts/` → scripts clonés séparément dans Dockerfile
- `runIchorCNA.R` ne crée pas le outDir → `mkdir -p` nécessaire dans le process NF

## SV Modules — Sniffles2 + Severus + Decoil (V1.2.0, 2026-04-28)

- [SV Modules](sv_modules.md) — Architecture Sniffles2/Severus/Decoil + caveats cliniques (Decoil non validé plasma 5-30x)

## Feedback

- [S3 Never Delete](feedback_s3_no_delete.md) - NEVER delete anything from S3 buckets
- [Bash inline dans process Nextflow](feedback_bash_inline.md) - Boris préfère bash inline dans `script:""""""` plutôt que scripts externes dans `bin/Module/`
