# Basespace Project Memory

## Project Overview
Pipeline de comparaison de scoring methylation (MRD/liquid biopsy) entre ONT long-read et Illumina short-read (Watchmaker).
16 samples (Breast, Colon, Lung, Healthy). Scripts bash, R via Docker (raima), Python inline (DuckDB).

## Key Files
- See [data-flow.md](data-flow.md) for detailed data origin mapping
- See [architecture.md](architecture.md) for project structure

## Important Paths
- ONT data: `/mnt/aima-bam-data/processed/MRD/RetD/liquid/CGFL/`
- Short-read data: `/scratch/short-read/`
- DuckDB: `/home/blipinski/Pipeline/trace-prod/database/samples_status.duckdb`
- Metadata logic: `/home/blipinski/Pipeline/trace-prod/lib/duckdb.py`
- Google Sheets sync: `/home/blipinski/Pipeline/trace-prod/lib/gsheets.py`

## Conventions
- Sample names: no underscore in scripts (Breast18), with underscore in filesystem (Breast_18)
- Decimal separator: converted to comma (French locale) via `sed 's/\./,/g'`
- Docker images: `blipinskiaima/raima:latest` (R scoring), `rastair:0.8.2` (methylation calling)
