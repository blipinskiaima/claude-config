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
| `NF_Watchmaker_Aima/nf_watchmaker_aima.sh` | Nextflow BWA-mem2 + rastair + raima (16 samples, en cours) |
| `generate_comparison.sh` | Agregation finale -> comparison_metrics.tsv |

## Output Files

| Fichier | Contenu |
|---------|---------|
| `comparison_metrics.tsv` | Table complete: scores + QC metrics (20 pipelines x 16 samples) |
| `hg38_mvaf.tsv` | mVAF HG38 uniquement (10 variantes filtrage x 16 samples) |
| `hg38_score.tsv` | Score raima HG38 uniquement (10 variantes filtrage x 16 samples) |
| `BP_5base_summary.tsv` | Summary 5base: mvaf + QC metrics (8 samples) |
| `BP_Watchmaker_all_summary.tsv` | Summary Watchmaker consolidé: mvaf WM/QC2040/QClow + QC metrics WM (16 samples) |
| `info.txt` | Documentation formats CX report, bedmethyl, BAM tags |
| `result/generate_figures.R` | 5 figures ggplot2 (remplace generate_figures.py) |
| `result/fig[1-5]_*.png` | 5 PNG publication-ready |

## 16 Samples

Cancer: Breast18, Colon3, Colon12, Colon13, Colon25, Colon50, Colon62, Colon63, Colon9, Lung8, Lung12, Lung13
Healthy: Healthy634, Healthy637, Healthy767, Healthy769

Subset 5base (8): Breast18, Colon25, Colon50, Colon62, Healthy634, Healthy767, Lung12, Lung8
Subset HG38reste (7): Colon13, Colon3, Colon50, Colon62, Colon9, Lung12, Lung8

## Execution Order (dependency chain)

```
1. 01-upload.sh            → uploads FASTQ to BaseSpace
2. [DRAGEN runs in cloud]  → produces CX_report, metrics.json, BAMs
3. 02-download.sh          → downloads + scores BP_ pipelines
   subsample_strategie.sh  → (optional) MAPQ sub-sample → re-upload
4. rastair_call_hg38_mapq.sh / hg38reste / mapq20 / breast18
5. 03-score_watchmaker.sh / hg38reste + 04-score_healthy.sh
6. generate_comparison.sh  → comparison_metrics.tsv
7. [Manual] hg38_mvaf.tsv, hg38_score.tsv
8. result/generate_figures.R → 5 PNG figures
```

## Commands

- `bash rastair_call_hg38_mapq.sh` — run rastair calling (HG38)
- `bash 03-score_watchmaker.sh` — run scoring (HG38)
- `SAMPLES=Breast18 bash 03-score_watchmaker.sh` — single sample
- `bash generate_comparison.sh` — aggregate results
- `docker run --rm -v $PWD:$PWD blipinskiaima/raima:latest Rscript result/generate_figures.R` — figures

## Design Patterns

- **Skip-if-exists**: tous les scripts verifient `[[ -f "$out" ]]` avant traitement
- **PIPELINES array**: `NAME:DIR` pairs, parsed via `${entry%%:*}` / `${entry#*:}`
- **Associative arrays**: `DATA["${SAMPLE}_key"]` pour collecter avant ecriture
- **Docker inline R**: `docker run blipinskiaima/raima:latest Rscript -e '...'`
- **Background parallelism**: `& + wait -n` avec compteur MAX_PARALLEL
- **Dual sample names**: `to_sample_name()` / `to_ont_name()` — Breast18 <-> Breast_18
- **French decimals**: `sed -i 's/\./,/g'` sur tous les TSV outputs

## Gotchas

1. `subsample_strategie.sh` ends with stray token (`SYNLSYMM34...`) — WIP scratchpad, non-executable
2. `hg38_mvaf.tsv` / `hg38_score.tsv` — no generating script, created manually
3. BP_ directories deleted — comparison_metrics.tsv shows NA for BP_ columns
4. Fig1 WM QC data hardcoded in R (lines 81-84), not from comparison_metrics.tsv
5. `raima::model_v1` uses `bedMethyl_select = 1:4` everywhere — must match model
6. nOT/nOB params from mbiasparser — per-sample, do not change without re-running
7. HG38reste = 7 samples subset (Colon13,3,50,62,9, Lung12,8); `get_hg38_scorev1()` has fallback logic
8. Docker mount `/mnt/temp/florian` required for raima model weights — always
9. R 4.3.3 → ggrepel <= 0.9.6

## External Dependencies

- Docker: `blipinskiaima/raima:latest` (R scoring), `rastair:0.8.2` (methylation calling)
- Nextflow: source `/home/blipinski/Pipeline/export/nextflow.sh`, workflow `/home/blipinski/Pipeline/Watchmaker/`
- BaseSpace CLI: `bs` pour upload/download
- AWS S3: `aws --profile scw` pour acces S3 Scaleway (ONT + short-read archives)
- DuckDB: `/home/blipinski/Pipeline/trace-prod/database/samples_status.duckdb`
- trace-prod: `/home/blipinski/Pipeline/trace-prod/` (duckdb.py, gsheets.py, checkers.py)
