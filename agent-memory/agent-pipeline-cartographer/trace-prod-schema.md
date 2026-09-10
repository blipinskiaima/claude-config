---
name: trace-prod-schema
description: Schéma DuckDB trace-prod (courant v34, 2026-09-08), 14 tables (lib/duckdb.py:1363), cohorte liquide 1384 (2026-09-10), cascade lecture A/B/C/D (qc), depth/coverage (qc_metrics), export gsheet "QC read", convention chemins S3 non stockés
metadata:
  type: project
---

## Schéma courant (v34, 2026-09-08) — 14 tables

Source : `/home/blipinski/Pipeline/trace-prod/lib/duckdb.py`, `SCHEMA_VERSION = 34` (ligne 13), liste exhaustive des tables ligne 1363. Vérifié en live sur `database/samples_status.duckdb` (chemin par défaut, `duckdb.py:1090`) : `_schema_version` confirme v34 appliquée le 2026-09-08 16:01:53. **Schéma évolue vite (~1 migration/semaine), toujours re-vérifier avant de citer un numéro de version ou un nom de colonne.**

**samples** (racine) : 1531 lignes au 2026-09-10 (requête live `GROUP BY sample_type`) = **1384 liquid** (871 CGFL + 513 HCL) + 147 solid. `id` INTEGER PK auto, `UNIQUE(sample_name, sample_type, labo)`. ⚠️ `sample_name` seul n'est pas unique (doublons inter-labo type `Colon_1`).

**qc** (duckdb.py:60-89, DDL cascade brute, inchangé depuis v25) : 24 colonnes non-clé `reads_total/mapped/alignments/primary/primary_mapped/frag/28m/with_cpg/unmapped/secondary/supplementary/off_chr1_22/mapq_lt20` (+`_pct` sauf reads_total), liste exacte = constante `QC_COLUMNS` (duckdb.py:732-747). **Aucune colonne depth/coverage dans `qc`** (existent seulement dans `qc_metrics`). Remplie par `lib/checkers_qc.py::QCChecker.check_sample()` (ligne 106) depuis 4 fichiers déjà publiés par Bam2Beta (aucune lecture de BAM, cf docstring checkers_qc.py:1-18) :
- `reads_total` = "nombre de lignes de BAM" (A+B+C+D) ← `QC/Samtools/{S}.nb_reads_total.tsv` (checkers_qc.py:111)
- `reads_primary` = "nombre de molécules" (A+D) ← cramino colonne `num_reads`, `QC/Cramino/{S}.merged.cramino.tsv` (checkers_qc.py:77-92, ligne 112)
- `reads_alignments` (A+C+D) ← cramino `num_alignments` ; `reads_unmapped` (A) ← idxstats ligne `*` col4 (checkers_qc.py:95-104)
- mapped/primary_mapped/secondary/supplementary/off_chr1_22 = soustractions ; `reads_28m`/`reads_mapq_lt20` restent NULL (Preprocess_28M non publié par le pipeline)
- Écriture : `DuckDBService.upsert_qc()` (duckdb.py:1645)

**qc_metrics** (duckdb.py:32-58, 1:1 samples via FK) : `depth` DECIMAL(10,2) et `coverage_percent` DECIMAL(5,2) (lignes 38-39) — les SEULES colonnes `depth`/`coverage_percent` au niveau "sample entier" de toute la base (les autres `depth_*`/`coverage_percent_*` sont des variantes small_fragments/dilution/rarefaction/horaire/threshold/dilution_lung, tables dédiées). Remplies par `lib/checkers.py::get_depth()` (ligne 725, lit `QC/Mosdepth/merged/{S}.merged.mosdepth.summary.txt` ligne "total" col4 via `extractors.py::extract_mosdepth_depth` ligne 205) et `get_coverage()` (ligne 730, lit `.mosdepth.global.dist.txt` avant-dernière ligne col3 via `extract_mosdepth_coverage` ligne 215). Chaîne d'écriture : dict "Depth"/"Coverage" (checkers.py:1002-1003) → mapping `TSV_TO_DB_QC` (duckdb.py:887,893-894 : "Depth"→"depth", "Coverage"→"coverage_percent") → `DuckDBService.upsert_sample()` (duckdb.py:1480) → `_upsert_table("qc_metrics", ...)` (duckdb.py:1504).
⚠️ **Renommage v34** (`_migrate_reads_columns_rename`, duckdb.py:1131) : `nb_reads_total`→`nb_lignes_total`, `nb_reads_aligned`→`nb_molecule`. Anciens libellés TSV ("Nb reads total"/"Nb read alignés") encore acceptés en import via alias dans `TSV_TO_DB_QC` (duckdb.py:889-890). **Corrige mémoire précédente (v24)** qui citait encore `nb_reads_total`/`nb_reads_aligned` — ne plus utiliser ces noms.

## Export gsheet "QC read"

Spreadsheet dédié, ID `1kUk5ShkMiVVUiOugY1ki7v9yfbjmSFjdoDbpHWoKiw0` (`database/gsheets_config.json:76`, clé `qc_read`) — **distinct** du spreadsheet principal trace-prod (`1gm_vB7vTzAq38dgkJFNpgA3Cy_XRlUqunMgoBvKnh6M`, qui porte liquid_CGFL/liquid_HCL/solid_CGFL/probs_*/Plateform/ONT Sample/Small Fragments/Dilution/Rarefaction). Cet ID `1kUk5Shk...` n'apparaît qu'une fois dans tout le repo → aucun autre onglet du pipeline n'y pointe (mais pas de vérification API live du contenu réel du document — pourrait avoir des onglets manuels non référencés dans le code).

Code : `lib/gsheets.py::export_qc()` (ligne 274). Colonnes = `_QC_READ_HEADERS` (gsheets.py:255-269), **16 colonnes dans cet ordre exact** : Sample, Indication, LABO, Total(`reads_total`), puis 12 `*_pct` de `qc` (Mapped/Alignments/Primary/Primary mapped/FRAG/28M/CpG/Unmapped/Secondary/Supplementary/Hors chr1-22/MAPQ<20 %). Lignes triées `ORDER BY labo, sample_name`. Source : `DuckDBService.get_qc_unified()` (duckdb.py:1577) = `qc` LEFT JOIN `samples` + `metadata` (indication = `metadata.class`, fallback par préfixe de nom pour Lung_Alc/Bladder_Urine/Colon sans metadata), **filtré `sample_type='liquid'` uniquement** (jamais solid). CLI : `check_samples.py export-qc` (ligne 566 ; option `--tsv <path>` pour preview local sans toucher au gsheet). Pour ajouter une colonne : l'ajouter à `QC_COLUMNS`/DDL `qc` si nouvelle métrique brute, puis à `_QC_READ_HEADERS` (gsheets.py) — `get_qc_unified()` l'inclut automatiquement via `QC_COLUMNS`.

## Chemins S3 des sorties : aucune colonne ne les stocke

Reconstruits à la volée par convention f-string, dupliquée dans `lib/checkers.py:774,785` et `database/check_samples.py:1472,1476,1532` : merged BAM = `s3://aima-bam-data/processed/MRD/RetD/{sample_type}/{labo}/{sample}/BAM/{sample}.merged.bam` ; données brutes = `s3://aima-bam-data/data/{labo}/{sample_type}/{sample}/` (⚠️ ordre `labo`/`sample_type` inversé entre les deux patterns, vérifié dans les 2 fichiers). Seule adresse S3 littéralement stockée en base : `bam_metadata.pod5_adresse` VARCHAR (duckdb.py:162) — mais c'est l'adresse POD5 en **entrée**, pas une sortie pipeline.

## Convention matrice liquide (plasma / urine / autre) — piège connu (non re-vérifié le 2026-09-10)

`metadata.class`/`category` NE distingue PAS plasma/urine. La matrice se lit dans le NOM : `Bladder_Urine_{01,02}_NNN` vs `Bladder_Blood_{01,02}_NNN`. Contrôles synthétiques `Twist_*`.

⚠️ **Angle mort EQC** (non re-vérifié) : 12 contrôles qualité externes CGFL (`Breast_17/32/47/49/50/52`, `Prostate_2/3/23/37/38/39`) enregistrés comme patients cancer normaux, aucun champ trace-prod ne les marque comme EQC.

## Rebasecalled / réplicats = lignes distinctes, même patient (non re-vérifié)

`_rebasecalled_V{...}` et `_rep1`/`_rep2` sont des `sample_id` distincts héritant du même `metadata.patient_id`/`class`.

## Clé primaire réelle

`samples.id` (surrogate) référencé par FK 1:1 dans qc/qc_metrics/retd_suivis/metadata/probs/bam_metadata/small_fragments_metrics. Clé logique/métier : `UNIQUE(sample_name, sample_type, labo)` — jamais `sample_name` seul.

## Où stocker les VAF sources

- `metadata.gene1_vaf` : VAF tumorale mesurée (VARCHAR libre) — source GSheet
- `qc_metrics.mvaf_v1/v2` (+v10m/v20m/ft092/ft095) : mVAF calculée par raima après Bam2Beta
- Healthy : `metadata.class = 'Healthy'`, `gene1_vaf` = NULL

## Key files

- `/home/blipinski/Pipeline/trace-prod/lib/duckdb.py` — DDL complet, SCHEMA_VERSION=34, migrations (`_migrate_*`)
- `/home/blipinski/Pipeline/trace-prod/lib/checkers_qc.py` — checker cascade `qc` (dédié, 4 fichiers Bam2Beta)
- `/home/blipinski/Pipeline/trace-prod/lib/checkers.py` — checker générique (depth/coverage/mvaf/... → qc_metrics/retd_suivis/bam_metadata)
- `/home/blipinski/Pipeline/trace-prod/lib/gsheets.py` — tous les `export_*()`, un par onglet
- `/home/blipinski/Pipeline/trace-prod/database/gsheets_config.json` — IDs spreadsheet + nom d'onglet par clé
- `/home/blipinski/Pipeline/trace-prod/database/check_samples.py` — CLI principal (Click)
- `/home/blipinski/Pipeline/trace-prod/database/samples_status.duckdb` — DB active (227 Mo au 2026-09-10). De nombreux `*.backup-pre-*.duckdb` dans le même dossier, ne pas confondre.
