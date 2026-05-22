---
name: trace-prod-schema
description: Schéma DuckDB trace-prod v8, tables principales, conventions clés, intégration Bam2Beta, absence de notion dilution/simulation
metadata:
  type: project
---

## Schéma v8 (mai 2026) — 8 tables

**samples** (table racine) : `id` INTEGER PK auto, `sample_name` VARCHAR, `sample_type` VARCHAR (liquid/solid), `labo` VARCHAR (CGFL/HCL), `prod_status` (OK/KO/RUNNING), UNIQUE(sample_name, sample_type, labo).

**qc_metrics** (1:1 samples) : métriques reads (nb_reads_total/aligned/epic), depth, coverage, mvaf_v1/v2/v1_10m/v1_20m/v1_ft092/v1_ft095, score_cnv.

**retd_suivis** (1:1 samples) : statuts fichiers BAM/bedmethyl/frag/CNV, seuils méthylation (threshold_20m..1m), ichorcna_score, mvaf_v12, ancestry, sex_proba/predicted, read_start_time, short_read.

**bam_metadata** (1:1 samples) : run_id, barcode, dorado_model, stockage_pod5, pod5_adresse, taille_bam/pod5, bam_horaire.

**metadata** (1:1 samples) : données cliniques GSheet — gene1_vaf, class (Lung/Breast/Healthy...), patient_id, stage, grade, speedvac, cohort, vaf_category, vaf_threshold.

**probs** (1:1 samples) : probabilités déconvolution v1 Epic (16 cols) + Loyfer (31 cols).

**short_read_metrics** (1:1 samples, v8) : métriques subsampling 75-200bp, DECIMAL + probs_short_read.

**_schema_version** : version actuelle = 8.

## Conventions importantes

- Clé logique d'unicité : `(sample_name, sample_type, labo)` — pas d'enum strict, VARCHAR libre
- Combos valides : liquid×(CGFL|HCL), solid×CGFL — solid×HCL = INVALID
- prod_status = OK/KO/RUNNING basé sur présence `Bam2Beta.done` / `Bam2Beta.failed`
- PathConfig.base_dir = `/mnt/aima-bam-data/processed/MRD/RetD/{type}/{labo}/`
- PathConfig.origin_dir = `/mnt/aima-bam-data/data/{labo}/{type}/`
- Rebasecalled : propagation metadata depuis sample original → `{sample}_rebasecalled*` à chaque import-metadata

## Intégration Bam2Beta

- **Aucune écriture directe** de Bam2Beta dans trace-prod. Bam2Beta écrit `Bam2Beta.done` / `Bam2Beta.failed` dans le dossier sample sur NFS/S3.
- trace-prod *lit* ces fichiers lors du `check` pour déterminer `prod_status`.
- Les métriques QC (mVAF, depth, coverage, ichorCNA) sont extraites par trace-prod à partir des fichiers de sortie de Bam2Beta (BETA/, ichorCNA/, QC/) — pas injectées par Bam2Beta.
- Donc : pour les samples dilués, Bam2Beta doit tourner en premier, puis `check` trace-prod peuplera la DB.

## Absence de notion dilution/simulation (mai 2026)

- Aucune colonne `is_dilution`, `target_vaf`, `parent_sample_id`, `healthy_donor_id`, `simulation_origin`.
- Aucune table dédiée aux expériences in silico.
- Pas de flag pour distinguer sample réel vs sample généré.
- Pour ajouter ce support, utiliser le skill `~/.claude/skills/add-trace-prod/` (workflow guidé ALTER TABLE).

## Où stocker les VAF sources

- `metadata.gene1_vaf` : VAF tumorale mesurée (ex : 28.4%, 73.0%, 32.2%) — source GSheet
- `qc_metrics.mvaf_v1/v2` : mVAF calculée par raima après Bam2Beta
- Pour les healthys : `metadata.class = 'Healthy'`, gene1_vaf = NULL

## Key files

- `/home/blipinski/Pipeline/trace-prod/lib/duckdb.py` — DDL complet, SCHEMA_VERSION = 8
- `/home/blipinski/Pipeline/trace-prod/README.md` — documentation schéma
- `/home/blipinski/Pipeline/trace-prod/database/check_samples.py` — CLI principal
- `/home/blipinski/Pipeline/trace-prod/lib/checkers.py` — BaseChecker, LiquidChecker, get_prod_status()
