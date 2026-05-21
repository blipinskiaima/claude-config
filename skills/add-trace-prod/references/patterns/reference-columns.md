# Colonnes modèles — Patterns à copier

Liste de colonnes existantes à utiliser comme modèle selon le besoin.

## Table retd_suivis

### `bam_status` — Status check simple (pattern le plus courant)

```
DDL          : bam_status VARCHAR DEFAULT 'KO'
STATUS_COLS  : OUI (parsing strict OK/KO/WARNING)
Source       : présence fichier S3
Helper S3    : _s3_exists
Check        : BaseChecker.check_bam (ligne ~88)
update-col   : pattern simple ('checker')
Export       : "BAM" dans _LIQUID_QC et _SOLID_QC
```

À reproduire si : status binaire OK/KO basé sur présence d'1 fichier.

### `ichorcna_score` — Valeur extraite + KO si absent

```
DDL          : ichorcna_score VARCHAR DEFAULT 'KO'
STATUS_COLS  : NON (VARCHAR libre, peut contenir "0,01271")
Source       : lecture TSV ichorCNA/{sample}.params.txt
Helper S3    : _s3_read_text
Check        : BaseChecker.check_ichorcna (ligne ~179)
update-col   : pattern simple ('checker')
Export       : "IchorCNA" entre "Score CNV" et "Frag Mode1"
```

À reproduire si : valeur numérique avec virgule + fallback KO.

### `read_start_time` — Présence fichier volumineux (pas de lecture)

```
DDL          : read_start_time VARCHAR DEFAULT 'KO'
STATUS_COLS  : NON
Source       : présence fichier 3-4 GB (read_start_time.tsv)
Helper S3    : _s3_exists (pas _s3_read_text !)
Check        : BaseChecker.check_read_start_time (ligne ~213)
update-col   : pattern simple ('checker')
Export       : "Read Start Time" entre "Sex Predicted" et "BAM/Short Read"
```

À reproduire si : fichier trop gros à lire, on veut juste savoir s'il existe.

### `ancestry` — Argmax sur header TSV

```
DDL          : ancestry VARCHAR DEFAULT 'NA'
STATUS_COLS  : NON (texte libre, ex "Europe (East)")
Source       : lecture TSV IV/{sample}.ancestry.tsv (header + 1 ligne)
Helper S3    : _s3_read_text
Check        : BaseChecker.check_ancestry (ligne ~219)
update-col   : pattern simple ('checker')
Export       : "Ancestry" entre "Frag Mode2" et "Sex Proba"
```

À reproduire si : parsing TSV avec header, retourne le nom de colonne avec max value.

### `frag_mode1` / `frag_mode2` — Valeurs depuis ligne 2 d'un TSV

```
DDL          : frag_mode1 VARCHAR DEFAULT 'NA'
STATUS_COLS  : NON
Source       : lecture TSV Fragmentomics/filtered/{sample}.fragmentomics_modes.tsv ligne 2 col idx
Helper S3    : _s3_read_text
update-col   : pattern simple ('checker')
Export       : "Frag Mode1", "Frag Mode2" entre "IchorCNA" et "Ancestry"
```

À reproduire si : valeur extraite par index ligne/colonne d'un TSV.

### `short_read` (v7) — Listing récursif + preserve

```
DDL          : short_read VARCHAR DEFAULT 'KO'
STATUS_COLS  : NON
Source       : listing S3 récursif d'un bucket mirror ({labo}_short_read)
Helper S3    : _s3_ls_recursive
Check        : BaseChecker.check_short_read (ligne ~219) — retourne Optional[str]
update-col   : pattern PRESERVE — fonction _update_short_read
Export       : "Short Read" entre "Read Start Time" et "BAM"
```

À reproduire si : check coûteux sur S3, preserve obligatoire.

## Table qc_metrics

### `mvaf_v1` — DECIMAL avec virgule décimale

```
DDL          : mvaf_v1 DECIMAL(10,4)
NUMERIC_COLS : OUI (parsing _parse_numeric, virgule→point)
Source       : lecture TSV BETA/{sample}.merged.epic.raima_score.V2.tsv
Helper S3    : _s3_read_text
Check        : BaseChecker.get_mvaf
update-col   : pattern simple ('checker')
Export       : "mVAF v1" dans _LIQUID_QC
```

À reproduire si : valeur numérique avec précision (DECIMAL).

### `mvaf_v1_10m` — DECIMAL avec paramètre extra (depth)

```
DDL          : mvaf_v1_10m DECIMAL(10,4)
NUMERIC_COLS : OUI
Source       : BETA/{sample}.10M.epic.raima_score.V2.tsv
Helper S3    : _s3_read_text
Check        : BaseChecker.get_mvaf_rarefied(sd, sample, depth) — accepte 3e arg
update-col   : pattern simple avec extra : ('qc_metrics', 'get_mvaf_rarefied', 'checker', '10M')
Export       : "mVAF v1 10M" / "mVAF v1 20M"
```

À reproduire si : même check répété avec un paramètre variant (depth, threshold).

## Table bam_metadata

### `bam_horaire` — Listing récursif S3 + preserve (premier exemple historique)

```
DDL          : bam_horaire VARCHAR DEFAULT 'KO'
STATUS_COLS  : NON
Source       : listing S3 récursif s3://aima-bam-data/data/{labo}/{type}/{sample}/
Helper S3    : aws s3 ls --recursive direct (via _check_bam_horaire dans check_samples.py)
update-col   : pattern PRESERVE — fonction _update_bam_horaire
Export       : "BAM Horaire" dans _BAM_COLS
```

À reproduire si : check sur un autre dossier S3 que `processed/MRD/RetD/`.

### `dorado_model` — Extraction depuis BAM (samtools)

```
DDL          : dorado_model VARCHAR
NUMERIC_COLS : NON
Source       : header RG du BAM (samtools view -H)
Helper       : BAMExtractor.get_metadata_for_sample (extractors.py)
update-col   : pattern 'bam' : ('bam_metadata', 'dorado_model', 'bam', None)
Export       : "Dorado Model" dans _BAM_COLS
```

À reproduire si : la valeur vient d'une extraction BAM, pas d'un check S3.

### `reads_per_flowcell` — Agrégat sur run_id

```
DDL          : reads_per_flowcell DECIMAL(10,2)
Source       : moyenne nb_reads_total des samples partageant le même run_id
update-col   : pattern 'aggregate' : ('bam_metadata', None, 'aggregate', None)
Dispatch     : _update_aggregate_column (check_samples.py)
Export       : "Read par flowcell" dans _BAM_COLS
```

À reproduire si : valeur calculée par agrégation SQL sur plusieurs samples.

## Table metadata (gsheet only)

### `stage`, `grade`, `speedvac`, `cohort` (v3-v5)

```
DDL          : VARCHAR (NULL)
NUMERIC_COLS : NON
Source       : colonne d'une gsheet VAF (CGFL + HCL)
Mapping      : "Header Gsheet": "db_col" dans TSV_TO_DB_METADATA
import       : via tp import-metadata liquid CGFL (gspread fetch)
update-col   : N/A — pas de check_*() ni dispatch
Export       : "Header Gsheet" dans _LIQUID_QC OU dans export-ont-samples
Harmonization: HARMONIZATION_RULES["<col>"] = {"yes": "Yes", "Lung-DI precoce": "Lung-DI précoce", ...}
```

À reproduire si : donnée 100% gsheet, jamais calculée par check_*().

## Tableau de synthèse — choisir un modèle

| Q4 source | Q7 erreur S3 | Modèle à copier |
|---|---|---|
| Présence fichier S3 (petit) | KO strict | `bam_status` |
| Présence fichier S3 (gros) | KO strict | `read_start_time` |
| Lecture TSV → valeur | KO/NA strict | `ichorcna_score`, `ancestry`, `frag_mode1` |
| Listing S3 récursif | Preserve | `short_read`, `bam_horaire` |
| Valeur numérique TSV | KO/NULL strict | `mvaf_v1` |
| Extraction BAM | KO strict | `dorado_model` |
| Agrégat SQL | N/A | `reads_per_flowcell` |
| Gsheet clinical | N/A | `stage`, `cohort` |
