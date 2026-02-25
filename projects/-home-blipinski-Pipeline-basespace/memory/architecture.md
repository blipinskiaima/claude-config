# Project Architecture

## Scripts (execution order)

| Script | Role |
|--------|------|
| `01-upload.sh` | Upload FASTQ vers BaseSpace (projets 5base + Watchmaker) |
| `02-download.sh` | Download CX_report DRAGEN + scoring raima (Docker) |
| `rastair_call_mapq20.sh` | rastair call MAPQ30 sur BAMs result2 (16 samples) |
| `rastair_call_mapq20_breast18.sh` | rastair call MAPQ20 pour Breast_18 uniquement |
| `rastair_call_hg38_mapq.sh` | rastair call matrice 3x3 MAPQ/BQ sur HG38 BAMs |
| `rastair_call_hg38reste_mapq.sh` | idem pour HG38reste (7 samples) |
| `03-score_watchmaker.sh` | Scoring loop sur 9 variantes HG38 pipeline |
| `03-score_watchmaker_hg38reste.sh` | Scoring loop sur 9 variantes HG38reste |
| `04-score_healthy.sh` | Scoring Healthy769 variantes (avec parallelisme) |
| `subsample_strategie.sh` | Sous-echantillonnage par MAPQ -> re-upload -> re-score |
| `generate_comparison.sh` | Agregation finale -> comparison_metrics.tsv |

## Output Files

| Fichier | Contenu |
|---------|---------|
| `comparison_metrics.tsv` | Table complete: scores + QC metrics (20 pipelines x 16 samples) |
| `hg38_mvaf.tsv` | mVAF HG38 uniquement (10 variantes filtrage x 16 samples) |
| `hg38_score.tsv` | Score raima HG38 uniquement (10 variantes filtrage x 16 samples) |
| `info.txt` | Documentation formats CX report, bedmethyl, BAM tags |

## 16 Samples

Cancer: Breast18, Colon3, Colon12, Colon13, Colon25, Colon50, Colon62, Colon63, Colon9, Lung8, Lung12, Lung13
Healthy: Healthy634, Healthy637, Healthy767, Healthy769

Subset 5base (8): Breast18, Colon25, Colon50, Colon62, Healthy634, Healthy767, Lung12, Lung8
Subset HG38reste (7): Colon13, Colon3, Colon50, Colon62, Colon9, Lung12, Lung8

## Design Patterns

- **Skip-if-exists**: tous les scripts verifient `[[ -f "$out" ]]` avant traitement
- **PIPELINES array**: `NAME:DIR` pairs pour iterer les variantes de filtrage
- **Associative arrays**: `DATA["${SAMPLE}_key"]` pour collecter avant ecriture
- **Docker inline R**: `docker run blipinskiaima/raima:latest Rscript -e '...'`
- **Background parallelism**: `& + wait -n` avec compteur MAX_PARALLEL

## External Dependencies

- Docker: `blipinskiaima/raima:latest` (R scoring), `rastair:0.8.2` (methylation calling)
- BaseSpace CLI: `bs` pour upload/download
- AWS S3: `aws-scw` profile pour acces donnees ONT
- DuckDB: `/home/blipinski/Pipeline/trace-prod/database/samples_status.duckdb`
- trace-prod: `/home/blipinski/Pipeline/trace-prod/` (duckdb.py, gsheets.py, checkers.py)
