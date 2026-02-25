# Data Flow & Value Origins

## 1. hg38_mvaf.tsv / hg38_score.tsv

### Fichiers
- `hg38_mvaf.tsv` — mVAF (methylation Variant Allele Frequency) par sample x pipeline
- `hg38_score.tsv` — score raima par sample x pipeline

### Origine des colonnes numériques

Chaque colonne extrait `mvaf` ou `score` (model=="v1") depuis `*.epic.raima_score.V2.tsv` :

| Colonne | Repertoire source |
|---------|-------------------|
| ONT | `/mnt/aima-bam-data/processed/MRD/RetD/liquid/CGFL/{Sample}/BETA/{Sample}.merged.epic.raima_score.V2.tsv` |
| Standard | `/scratch/short-read/NF_WatchmakerHG38/{Sample}/` |
| QC20 | `/scratch/short-read/NF_WatchmakerHG38QC2040/{Sample}/` |
| QC30 | `/scratch/short-read/NF_WatchmakerHG38QC3040/{Sample}/` |
| BQ30 | `/scratch/short-read/NF_WatchmakerHG38BQ30/{Sample}/` |
| BQ40 | `/scratch/short-read/NF_WatchmakerHG38BQ40/{Sample}/` |
| QC20+BQ30 | `/scratch/short-read/NF_WatchmakerHG38QC2040BQ30/{Sample}/` |
| QC20+BQ40 | `/scratch/short-read/NF_WatchmakerHG38QC2040BQ40/{Sample}/` |
| QC30+BQ30 | `/scratch/short-read/NF_WatchmakerHG38QC3040BQ30/{Sample}/` |
| QC30+BQ40 | `/scratch/short-read/NF_WatchmakerHG38QC3040BQ40/{Sample}/` |

### Script generateur
Aucun script explicite ne genere `hg38_mvaf.tsv`/`hg38_score.tsv`.
La logique est dans `generate_comparison.sh` (fonction `get_hg38_scorev1()`, lignes 38-47, 122-130)
mais ce script ecrit dans `comparison_metrics.tsv`.
Ces fichiers ont probablement ete crees manuellement ou par un script temporaire.

### Colonnes supplementaires (VAF (panel), IsActive, Meta, Cate, Coment)
Ces colonnes N'EXISTENT PAS dans les TSV. Elles viennent de la base DuckDB :

| Colonne affichee | Champ DuckDB | Source |
|---|---|---|
| VAF (panel) | active_cancer | Google Sheets |
| IsActive | active_cancer | Google Sheets |
| Meta | metastatic | Google Sheets |
| Cate | category | Calcule (duckdb.py lignes 646-655) |
| Coment | comments | Google Sheets |

- Schema DuckDB: `/home/blipinski/Pipeline/trace-prod/lib/duckdb.py` (lignes 143-189, 285-310)
- Sync Google Sheets: `/home/blipinski/Pipeline/trace-prod/lib/gsheets.py`
- La combinaison TSV + colonnes DuckDB se fait dans un tableur externe.

---

## 2. comparison_metrics.tsv

### Script generateur
`generate_comparison.sh` -> `/home/blipinski/Pipeline/basespace/comparison_metrics.tsv`

### Extraction des valeurs

```
get_scorev1(file):   awk -F'\t' '$4=="v1"{printf "%.3f\n", $3}' "$f"
get_metric(file,col): awk -F'\t' "NR==2{gsub(/M$/,\"\",\$$col); print \$$col}" "$f"
```

### Sources par pipeline

| Pipeline | Score source | Metrics source |
|----------|-------------|----------------|
| ONT | `CGFL/{Sample}/BETA/*.raima_score.V2.tsv` | DuckDB (qc_metrics: nb_reads_total, nb_reads_aligned, depth, coverage_percent) |
| 5b | `/scratch/short-read/BP_5base/{Sample}/*.raima_score.V2.tsv` | `{Sample}.metrics.tsv` (col2=total, col3=mapped, col7=depth, col10=coverage) |
| WM | `/scratch/short-read/BP_Watchmaker/{Sample}/*.raima_score.V2.tsv` | `{Sample}.metrics.tsv` |
| WMQC | `/scratch/short-read/BP_WatchmakerQC2040/{Sample}/*.raima_score.V2.tsv` | `{Sample}.metrics.tsv` |
| NF WM | `/scratch/short-read/NF_Watchmaker/{Sample}/` | score uniquement |
| NF WMQC20 | `/scratch/short-read/NF_WatchmakerQC2040/{Sample}/` | score uniquement |
| NF WMQC30 | `/scratch/short-read/NF_WatchmakerQC3040/{Sample}/` | score uniquement |
| HG38* | `/scratch/short-read/NF_WatchmakerHG38*/{Sample}/` (fallback: HG38reste*) | score uniquement |
| SubMAPQ20/30/40 | `/scratch/short-read/BP_WatchmakerSubMAPQ*/{Sample}/` | score uniquement |

### Post-traitement
`sed -i 's/\./,/g'` pour convertir les decimales au format francais.

---

## 3. Data Flow Diagram

```
Raw FASTQ (S3/CGFL)
  +-- 01-upload.sh --> BaseSpace (bs upload)
       +-- DRAGEN pipeline (cloud)
            +-- 02-download.sh --> CX_report.txt.gz
                 +-- raima::bedmethyl_dragen --> .bed.gz
                      +-- raima::model_v1 --> .epic.raima_score.V2.tsv

BAM (NF_Watchmaker, /scratch/)
  +-- rastair_call_*.sh --> .rastair_call.txt (par combo MAPQ/BQ)
       +-- 03-score_watchmaker.sh --> copie + scoring
            +-- raima::bedmethyl_rastair --> .bed.gz
                 +-- raima::model_v1 --> .epic.raima_score.V2.tsv

ONT BAM (S3/processed)
  +-- modkit (upstream) --> .merged.epic.raima_score.V2.tsv
  +-- DuckDB (trace-prod) --> QC metrics

generate_comparison.sh
  |-- lit tous les .raima_score.V2.tsv
  |-- lit DuckDB pour ONT QC
  +-- --> comparison_metrics.tsv

Google Sheets --> gsheets.py --> DuckDB metadata
  (VAF panel, IsActive, Meta, Cate, Coment)
  --> combine avec TSV dans tableur externe
```
