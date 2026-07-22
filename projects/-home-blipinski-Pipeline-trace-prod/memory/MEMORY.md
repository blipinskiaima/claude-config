# trace-prod Memory

## Feedback / règles de travail
- [Scratch workspace + BAM read-only](feedback_scratch_workspace.md) — analyses ad-hoc dans /scratch/boris/<topic>/, source BAM/POD5 strictement en lecture seule
- [Rebasecalled POD5 — ne pas propager](feedback_rebasecalled_pod5.md) — laisser NULL après update-column stockage_pod5, ne pas copier depuis l'original
- [STATUS_COLUMNS = OK/KO/WARNING strict](feedback_status_columns.md) — y mettre une VARCHAR libre (ichorcna_score) → _parse_status() écrase tout en KO
- [Probs loyfer manquantes = décalage extraction](feedback_probs_loyfer_lag.md) — loyfer NULL + epic OK → props_loyfer généré après la dernière passe loyfer (pas un bug). Fix `probs -P`. `-s` mono-sample → boucler

## Schemas & features
- [Schema v6 — colonnes IV/QC](project_schema_v6_iv_qc.md) — 4 colonnes retd_suivis (read_start_time, ancestry, sex_proba, sex_predicted), path IV/ sœur de QC/
- [Schema v7 — short_read](project_schema_v7_short_read.md) — retd_suivis.short_read, 6 dossiers S3 dans le mirror {labo}_short_read (liquid only). Gotcha `s3 ls --recursive` = clés complètes
- [Schema v8 — short_read_metrics](project_schema_v8_short_read_metrics.md) — table 28 colonnes (FK sample_id), CLI check-short-read indépendante + export-short-read-like
- [Schema v9 — dilution](project_schema_v9_dilution.md) — table AUTONOME 64 col (PK sample_name, pas de FK), 480 samples, préfixe .merged → BaseChecker sans override, CLI sans args type/labo
- [Schema v10 — frag softclipped](project_schema_v10_frag_sc.md) — 3 col retd_suivis, calque EXACT du frag v1, source Fragmentomics/filtered_softclipped. Quirk NA vs KO selon check/update-column
- [Schema v11 — mvaf_v13 + frag_score_v2_sc](project_schema_v11_mvaf_v13_frag_score.md) — 2 col VARCHAR liquid only, mvaf_v13 calque mvaf_v12 (raima V1.3)
- [Schema v12 — bootstrap](project_schema_v12_bootstrap.md) — retd_suivis.bootstrap OK/KO, présence S3 bootstrap_v1.tsv, pattern preserve via _s3_exists
- [Schema v13 — mvaf_v14](project_schema_v13_mvaf_v14.md) — calque mvaf_v13 SAUF cols[1] (V1.4 à 3 colonnes) + format_mvaf4() (jamais de notation scientifique)
- [Schema v14 — bootstrap_props](project_schema_v14_bootstrap_props.md) — calque EXACT de bootstrap (v12), fichier bootstrap_v1.props.tsv
- [Schema v18 — themelio_score](project_schema_v18_themelio.md) — retd_suivis liquid only, score Thémélio BAM2BETA, CSV THEMELIO/{s}.themelio_predictions.csv L2C2, virgule précision complète, calque mvaf_v14. ⚠ chemin réel THEMELIO/ (pas OUTPUT/)
- [Schema v19 — too_predicted_class + too_final_decision](project_schema_v19_too.md) — 2 col retd_suivis liquid only, classifieur TOO BAM2BETA, CSV TOO/{s}.too5_predictions.csv col 9 + col 20, texte brut (indications). ⚠ parsing module csv OBLIGATOIRE (virgule interne dans confidence_stratum col 10)
- [Schema v16/v17 — rarefaction](project_schema_v16_rarefaction.md) — table AUTONOME, PK composite (sample_name, labo) depuis v17 (collision inter-labo), niveaux 20M/10M/5M/2M/1M, calque dilution. Pipeline terminé 15/07/2026 : 1355 lignes, PROD OK 100%, toutes métriques remplies
- [Mode probs --probs_bootstrap](project_probs_bootstrap_mode.md) — probs epic = moyenne des 200 réplicats bootstrap, écrase les 16 col epic (NULL si absent), réversible via probs --probs
- [Colonnes v2-v7 — index](project_columns_index.md) — colonnes v2-v7 + patterns transversaux (collision mapping TSV_TO_DB, gene1_vaf raima, rebasecalled propagation, NFS-first, export ONT)

## Données & infra
- [Infra POD5/BAM/export](reference_infra_pod5_bam_export.md) — extraction barcode (+ workaround logs Pod2Bam), POD5 storage 6 colonnes, structure S3 AWS/SCW, BETA_28M, ordre export, IchorCNA, date_done, gsheet config, CLI defaults
- [Frag softclip vs trim barcode](project_frag_softclip_trim.md) — AlCapone re-basecallé offline hétérogène (trim ON/OFF). frag_mode v1 gonflé jusqu'à +148bp sur ~81 samples ; **seul frag_mode_sc est fiable** en cross-cohorte
- [Samples Twist](project_twist_samples.md) — 11 samples liquid CGFL (titration enrichissement Twist), pas un type/cohorte/commande
- [HCL Verification](project_hcl_verification.md) — 275 samples vérifiés, transfert raw→S3 intègre, raw purgé 12/03/2026
- [Script pod5_verification](reference_pod5_verification.md) — génération de pod5_verification.tsv

## Architecture
- CLI entry : `database/check_samples.py` (Click) — Core : `lib/checkers.py`, `lib/duckdb.py`, `lib/utils.py`, `lib/extractors.py`
- S3 fallback : `lib/s3_fallback.py` — SmartPath hérite de Path, download S3 transparent via boto3
- DB : `database/samples_status.duckdb`. Schéma = source unique `DuckDBService.SCHEMA` (lib/duckdb.py)
- Checkers dédiés (n'héritent pas tous pareil) : `checkers_short_read.py` (override 4 méthodes, préfixe minLen75), `checkers_dilution.py` + `checkers_rarefaction.py` (BaseChecker sans override, préfixe .merged)

## Key Mappings (lib/)
- `COLUMN_MAPPING` : display → DB column. `NUMERIC_COLUMNS` : cast DECIMAL à l'import. `STATUS_COLUMNS` : OK/KO/WARNING strict uniquement
- `LIQUID_HEADERS` / `SOLID_HEADERS` (utils.py) : ordre des colonnes export. `_BAM_COLS` : ordre export BAM
- `COLUMN_CHECKERS` (check_samples.py) : colonne → méthode checker pour `update-column` (+ variantes `DILUTION_` / `RAREFACTION_`)

## DuckDB Gotchas
- **`CREATE TABLE AS SELECT` perd les PK/FK** — toujours DDL original + `INSERT INTO ... SELECT` pour les migrations
- UPSERT crée des blocs morts (copy-on-write) → `clean-database` compacte. ⚠ Ajouter toute nouvelle table à `compact()` (sinon perte au prochain clean)
- **Single writer lock** → `update-column` / `check` séquentiels, jamais en parallèle (CGFL puis HCL)
- Conversion euro : virgule→point + KO/NA→NULL avant insert

## Conventions
- Combos valides : liquid×(CGFL|HCL), solid×CGFL. Solid×HCL invalide
- Statuts : OK, KO, WARNING (+ RUNNING pour prod_status). Format euro : virgule décimale, DD-MM-YYYY
- Manquant : "NA" en export, NULL en DB. Table `samples` : colonne `sample_type` (pas `type`)

Détails par colonne : `~/Pipeline/trace-prod/README.md` (Tables 2/3/4) et `~/Pipeline/trace-prod/CLAUDE.md`.
