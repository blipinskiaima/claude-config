# Memory — trace-platform

## Architecture

- CLI Python (Click) pour le tracking des échantillons clients sur la plateforme AIMA
- Base DuckDB : `platform.duckdb` — schema v12 (12 migrations successives)
- Export vers Google Sheets via gspread
- **Scan 100% S3 (boto3, profil scw), plus de mount /mnt** : découverte (list_objects_v2) + staging tmpdir pour le contenu (petits TSV, mtime S3 préservé) + BAM via URL présignée (samtools view -H, header seul, pas les 8Go). Le mount s3fs est non fiable (dossiers fantômes, mtimes incohérents) — abandonné.

## Points clés

- Projet en production, utilisé pour le suivi des échantillons clients
- Fait partie du trio traçabilité : trace-prod + trace-platform + trace-workflow → Aima-Tower
- Schema DB v12 : v10 = override `samples.case` (PROD/DEV niveau sample), v11 = drop `report_date` (plus de PDF), v12 = `creation_date` (date du 1er objet S3 uploadé via LastModified ; tri export récents en haut)
- run_status : WAITING (état 0, pas de .dl-complete) → RUNNING → SUCCESSED/WARNING/FAILED ; ARCHIVED (rétention) posé hors-calcul par `check_platform.py archive` (DEV >2 mois, sticky). bioit ne requiert PLUS rapport_pdf (aligné v11)
- PROD granulaire : `PROD_CUTOFFS` dans check_platform.py (un compte passe prod à partir d'une date d'upload). **case effectif = COALESCE(samples.case, labs_users.case, 'PROD')** — compte détecté mais NON déclaré dans labs_users (TSV) = PROD par défaut (non archivé). Aligné aussi dans Aima-Tower services.py
- Commandes : `check --new` (incrémental, ajoute seulement) vs `check` (full = nouveaux + re-scan WAITING/RUNNING, pas les terminaux) ; `delete` (unitaire), `prune` (purge samples absents de S3, backup auto), `daemon` (check --new + re-scan récents Nj + export, en boucle/tmux). En prod : cron check+export toutes les 30 min
- Occultation export gsheet : snapshot figé `data/export_hidden_samples.tsv` (168 Bladder blood/urine masqués, futurs visibles). `*.tsv` gitignorés (locaux, comme export_labs_users.tsv)

## Conventions

- Les workflows terminaux (SUCCEEDED/FAILED/CANCELLED) ne sont pas re-syncés
- `CREATE TABLE AS SELECT` ne préserve pas les PK — utiliser DDL + INSERT INTO
