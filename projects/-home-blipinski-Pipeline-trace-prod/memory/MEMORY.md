# trace-prod Memory

## Architecture
- CLI entry: `database/check_samples.py` (Click)
- Core: `lib/checkers.py`, `lib/duckdb.py`, `lib/utils.py`, `lib/extractors.py`
- S3 fallback: `lib/s3_fallback.py` — SmartPath inherits Path, transparent S3 download via boto3
- DB: DuckDB file at `database/samples_status.duckdb`
- Schema single source of truth: `DuckDBService.SCHEMA` (lib/duckdb.py)

## Key Mappings (lib/)
- `COLUMN_MAPPING` dict: display names → DB column names
- `NUMERIC_COLUMNS` set: columns with DECIMAL casting on import
- `LIQUID_HEADERS`, `SOLID_HEADERS` (utils.py): export column order
- `COLUMN_CHECKERS` (check_samples.py): column name → checker method for `update-column`
- `_BAM_COLS` (utils.py): BAM column export order

## DuckDB Gotchas
- UPSERT creates dead blocks (copy-on-write) — use `clean-database` to compact
- `CREATE TABLE AS SELECT` loses PK/FK — always use DDL + INSERT INTO SELECT
- European decimal conversion: comma→dot + KO/NA→NULL before insert
- DuckDB single writer lock — cannot run concurrent queries during update-column

## mVAF Filtered Columns
- `mvaf_v1_ft092`, `mvaf_v1_ft095` — thresholds 0.92 and 0.95
- Checker: `get_mvaf_filter()` in BaseChecker
- Added to: schema, mappings, NUMERIC_COLUMNS, headers, COLUMN_CHECKERS

## POD5 Storage System (bam_metadata)
- Columns: `stockage_pod5` (AWS/SCW/AWS+SCW/NULL), `sample_type_pod5`, `taille_pod5`, `pod5_adresse`
- Update: `update-column stockage_pod5` → updates all 4 columns together
- Dispatch: COLUMN_CHECKERS type='storage' → `_update_pod5_storage()`

### S3 Structure
- Bucket: `aima-pod-data`, 2 providers (AWS profil `aws`, SCW profil `scw`)
- CGFL formats: `pod5_pass/{sample}/`, `pod5/` flat, `pod5_repN/`, racine `.pod5`
- CGFL matching: run_id[:8] → S3 hash, fallback sample_name dans pod5_pass/
- HCL: dossiers `{sample_name}/` avec POD5 directement dedans
- Dedup (`_dedup_cgfl_folders()`): `=OK` > original > `=moche`

### Dorado Model Split
- `dorado_model` + `dorado_model_version` — split sur `@` dans BAMExtractor._parse_rg_line
- gsheet "dorado version" = software version (ex: 7.6.7), DB = model version (ex: v4.3.0)

## Sample Counts (liquid CGFL, mars 2026)
- 519 total, 394 AWS, 21 SCW, 104 NULL (anciens Lung_Alc sans POD5 sur S3)
- 114 non-Lung_Alc AWS avec dorado model v4.3.0 → 27 adresses POD5 uniques
- 272 non-Lung_Alc AWS toutes versions → 66 adresses POD5 uniques
- 94 adresses POD5 uniques total AWS (vs ~96 dossiers physiques S3, delta = dedup =moche)
- POD5 moyen: 153.70 GiB global, 179.67 GiB HCL
- BAM moyen: ~8.66 GiB (seulement 8 samples renseignés, update-column taille_bam à compléter)

## GSheet Config
- Config: `database/gsheets_config.json`
- metadata_CGFL: spreadsheet `1v1KUuCoMQV4Qk5jfbHLxhrUK6q_FETLiH8TuCQMdNxA`, worksheet "VAF"
- metadata_HCL: spreadsheet `1XcWPn3_PT1atR-i5DmOM1t0ldgb5_PnxhQUwNUxWpQg`, worksheet "VAF"
- Fetch: `fetch-gsheet metadata_CGFL` / `fetch-gsheet metadata_HCL`

## Conventions
- Valid combos: liquid×(CGFL|HCL), solid×CGFL only
- Status: OK, KO, WARNING
- European format: comma decimals, DD-MM-YYYY dates
- Missing: "NA" in exports, NULL in DB
- samples table: colonne `sample_type` (pas `type`)
