# Memory — trace-platform

## Architecture

- CLI Python (Click) pour le tracking des échantillons clients sur la plateforme AIMA
- Base DuckDB : `platform.duckdb` — schema v11 (11 migrations successives)
- Export vers Google Sheets via gspread
- Stockage S3 Scaleway via boto3

## Points clés

- Projet en production, utilisé pour le suivi des échantillons clients
- Fait partie du trio traçabilité : trace-prod + trace-platform + trace-workflow → Aima-Tower
- Schema DB v11 : QC metrics, statuts, métadonnées BAM. v10 = override `samples.case` (PROD/DEV niveau sample), v11 = drop `report_date` (plus de PDF)
- run_status : WAITING (état 0, pas de .dl-complete) → RUNNING → SUCCESSED/WARNING/FAILED ; ARCHIVED (rétention) posé hors-calcul par `check_platform.py archive` (DEV >2 mois, sticky)
- PROD granulaire : `PROD_CUTOFFS` dans check_platform.py (un compte passe prod à partir d'une date d'upload). case effectif = COALESCE(samples.case, labs_users.case)
- Commande `--new` pour les updates incrémentaux (évite le reprocessing)

## Conventions

- Les workflows terminaux (SUCCEEDED/FAILED/CANCELLED) ne sont pas re-syncés
- `CREATE TABLE AS SELECT` ne préserve pas les PK — utiliser DDL + INSERT INTO
