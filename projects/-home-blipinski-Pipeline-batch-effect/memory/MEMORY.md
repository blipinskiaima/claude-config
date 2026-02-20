# Batch Effect Project — Memory

## Project Overview

Analyse du batch effect entre centres HCL (188 samples) et CGFL (519 samples) sur données ONT (Oxford Nanopore).
- **Répertoire travail** : `/scratch/batch_effect/`
- **Documentation** : `~/Pipeline/batch_effect/README.md`
- **Données S3** : `s3://aima-bam-data/data/{HCL,CGFL}/liquid/` (profil `scw`)

## Data Structure

- 707 rapports TSV (3 colonnes: Categorie/Parametre/Valeur) dans `/scratch/batch_effect/{hcl,cgfl}/`
- Matrice de base : `/scratch/batch_effect/batch_matrix.tsv` (21 colonnes, 708 lignes)
- **Matrice enrichie** : `/scratch/batch_effect/batch_matrix_enriched.tsv` (31 colonnes, 708 lignes)
- Résumé batch effect : `/scratch/batch_effect/batch_summary.txt`
- **Résumé metadata** : `/scratch/batch_effect/batch_metadata_summary.txt`
- Scripts : `generate_reports.sh`, `build_matrix.sh`, `enrich_matrix.py`

## Key Findings — Batch Effect

### CGFL : 3 générations techniques (chronologique)

| Période | Basecaller | MinKNOW | Guppy | Modèle | Flowcell | Samples |
|---|---|---|---|---|---|---|
| sept 2022 | Guppy | non tracé | v7.9.8 | hac@v3.3 | R9.4.1 | 10 |
| nov 2024 → mars 2025 | Guppy | non tracé | v7.6.7/v7.9.8 | hac@v4.1.0/v5.0.0 | R10.4.1 | 52 |
| mars → sept 2025 | Dorado | v6.2.6 | — | hac@v4.3.0 | R10.4.1 | 153 |
| sept 2025 → fév 2026 | Dorado | v6.5.14 | — | hac@v5.0.0 | R10.4.1 | 304 |

### HCL : config unique
- Dorado / MinKNOW v6.5.14 / hac@v5.0.0 / PromethION / A100 / R10.4.1

### Confounding (BAM headers)
- **GPU** : totalement confounded (A100=HCL, A800/Quadro=CGFL)
- **Guppy** : 62 samples, 100% CGFL, 100% Lung_Alc
- **Healthy** : 5 params CONFOUNDED entre HCL (v5.0.0) et CGFL (v4.3.0)
- Sans Lung_Alc : seul GPU reste CONFOUNDED

### Confounding (metadata trace-prod)
- **kit** : CONFOUNDED (NBD114-96=CGFL, SQK-NBD114.24=HCL)
- **extraction_protocol** : CONFOUNDED (Apostle/Promega/Qiagen=CGFL, Maxwell=HCL)
- **dorado_version_gsheet** : PARTIEL (7.6.7=CGFL only, 7.9.8=partagé)
- **reads_per_flowcell** : p=1.1e-40 (HCL=239M vs CGFL=149M)
- **barcode_number** : ns, **samples_per_run** : ns
- **library_yield/quantity/volume/quantity_loaded** : données CGFL uniquement
- Couverture metadata : 152/188 HCL, 284/519 CGFL ; 5 samples "bis" sans correspondance

## Référence génomique — PAS de batch effect

- Tous les 707 BAM alignés sur `GCA_000001405.15_GRCh38_no_alt_analysis_set.fa` (195 contigs)
- Bam2Beta utilise `/scratch/dependencies/genomes/hg38/hg38.fa` (455 contigs = 194 partagés + 260 ALT + pas chrEBV)
- **Impact nul** sur les beta values CpG : séquences identiques sur les 194 contigs partagés
- chrEBV perdu silencieusement par modkit (log warning, non pertinent pour méthylation humaine)
- DuckDB trace-prod : `/home/blipinski/Pipeline/trace-prod/database/samples_status.duckdb`

## Alignement

- Tous alignés avec **minimap2** sur `GCA_000001405.15_GRCh38_no_alt_analysis_set.fa`
- Dorado/MinKNOW (645) : minimap2 intégré, version minimap2 **non tracée** dans @PG
- Guppy v7.6.7 (24) : minimap2 v2.27 standalone via `--align_ref`
- Guppy v7.9.8 (38) : minimap2 v2.28 standalone via `--align_ref`

## Technical Notes

- Version Dorado non tracée dans BAM (placeholder `modbase_model_version_id` dans @RG DS)
- Version modbase (5mCG_5hmCG@vX) tracée uniquement dans Guppy BAMs
- Tous en HAC (high accuracy), aucun SUP/FAST
- Pas de POD5 source dans les BAM (tags fn/ns/ts absents)
- Cancer types HCL : colon, healthy, lung, pancreas
- Cancer types CGFL : breast, colon, healthy, lung, lung_alc, ovary, pancreas, prostate

## Bash Gotcha

- awk dans heredoc `cat << 'SCRIPT'` : ne pas utiliser `!=` directement dans les commandes bash inline, utiliser heredoc avec quotes simples autour de SCRIPT pour éviter l'échappement du `!`

## Détails → voir topic files
- [batch-effect-details.md](batch-effect-details.md) — tableaux croisés complets
