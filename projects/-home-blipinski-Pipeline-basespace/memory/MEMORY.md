# Basespace Project Memory

## Project Overview
Pipeline de comparaison de scoring methylation (MRD/liquid biopsy) entre ONT long-read et Illumina short-read (Watchmaker).
16 samples (Breast, Colon, Lung, Healthy). Scripts bash, R via Docker (raima), Python inline (DuckDB).

## Key Files
- See [data-flow.md](data-flow.md) for detailed data origin mapping
- See [architecture.md](architecture.md) for project structure
- See [figures.md](figures.md) for figure generation details

## Summary Files
- `BP_5base/BP_5base_summary.tsv` — 8 samples, colonnes: sample, mvaf, total_reads, mapped_reads, depth, coverage
- `BP_Watchmaker/BP_Watchmaker_all_summary.tsv` — 16 samples, colonnes: sample, mvaf_WM, mvaf_QC2040, mvaf_QClow, total_reads, mapped_reads, depth, coverage (QC = WM uniquement)
- SubMAPQ20/30/40 retirés du summary (résultats dans README sous-projets uniquement)
- Colonnes scorev1 supprimées, mvaf seul conservé
- Données locales BP_* supprimées, summaries extraits depuis S3

## READMEs
- `README.md` — README général : pipelines, samples, protocoles, scores mVAF (9 combos Methylseq + ONT), QC, figures, stockage S3
- `BP_5base/README_bp_5base.md` — pipeline DRAGEN 5base
- `BP_Watchmaker/README_bp_watchmaker.md` — pipeline DRAGEN Watchmaker + variantes
- `NF_Watchmaker_Aima/README_nf_watchmaker_aima.md` — pipeline Nextflow BWA-mem2 custom
- `NF_Watchmaker_Methylseq/README_nf_watchmaker_methylseq.md` — pipeline nf-core/methylseq + matrice MAPQ x BQ
- Structure homogène : 9 sections ## (Samples, Sous-projets, Étapes, Lancement, Fichiers, Stockage, Résultats, Trace S3, Projet source)

## Pipelines par dossier
- `BP_5base/` — DRAGEN 5base (8 samples, terminé, archivé S3)
- `BP_Watchmaker/` — DRAGEN Watchmaker + variantes QC/SubMAPQ (16 samples, terminé, archivé S3)
- `NF_Watchmaker_Aima/` — Nextflow BWA-mem2 (16 samples, en cours : Healthy_767 + Breast_18 scorés)
  - Différence clé : BWA-mem2/rastair (local) vs DRAGEN (BaseSpace cloud)
  - S3 output : `s3://aima-bam-data/processed/short-read/Watchmaker/RetD/{ID}/`
  - Score local : `/scratch/short-read/NF_Watchmaker_Aima/{ID}/`
  - Projet Nextflow source : `/home/blipinski/Pipeline/Watchmaker/`
  - Summary : `nf_watchmaker_aima_summary.tsv` (15 scorés, Colon_3 NA)
- `NF_Watchmaker_Methylseq/` — nf-core/methylseq + rastair (16 samples, 9 combos MAPQ x BQ, terminé)
  - S3 output : `s3://aima-bam-data/processed/short-read/result/NF_WatchmakerHG38{SUFFIX}/{ID}/`

## Important Paths
- ONT data: `/mnt/aima-bam-data/processed/MRD/RetD/liquid/CGFL/`
- Short-read data: `/scratch/short-read/` (NF_WatchmakerHG38* only — BP_* dirs deleted, archivés sur S3)
- S3 archives: `s3://aima-bam-data/processed/short-read/result/BP_{PROJECT}/{SAMPLE}/` (réorganisé mars 2026)
- Référence génomique: hg38 pour tous les pipelines (DRAGEN + Nextflow)
- DuckDB: `/home/blipinski/Pipeline/trace-prod/database/samples_status.duckdb`
- Metadata logic: `/home/blipinski/Pipeline/trace-prod/lib/duckdb.py`
- Google Sheets sync: `/home/blipinski/Pipeline/trace-prod/lib/gsheets.py`

## Conventions
- Sample names: no underscore in scripts (Breast18), with underscore in filesystem (Breast_18)
- Decimal separator: converted to comma (French locale) via `sed 's/\./,/g'`
- Docker images: `blipinskiaima/raima:latest` (R scoring), `rastair:0.8.2` (methylation calling)
- R version: 4.3.3 — ggrepel max 0.9.6 (0.9.7 needs R >= 4.5)
- Git repo: `https://github.com/aima-dx/short-read.git` (branche main)
- Répertoire renommé: basespace/ → short-read/ (mars 2026)
