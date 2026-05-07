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
- `update-column` runs must be **sequential** (not parallel) due to single writer lock

## Export GSheet Column Order (liquid)
- Removed 6 individual rarefaction columns (20M..1M), replaced by single "Rarefaction" (computed at export)
- Removed "QC" column from both liquid and solid exports
- "Taille BAM (GiB)" réintégrée dans l'export (calculée via NFS stat, entier GiB)
- "BEDMETH EPICS" moved right after "BAM"
- "Dorado Model" moved before "Version Dorado Model"
- Rarefaction logic: OK if all thresholds ≤ nb_reads_total are OK, KO if any isn't, OK if no applicable threshold (< 1M reads)

## Rarefaction Consolidation (display-only)
- `_RAREFACTION_THRESHOLDS = {"20M": 20, "15M": 15, "10M": 10, "5M": 5, "2M": 2, "1M": 1}`
- Implemented in both `GSheetsService._consolidated_rarefaction()` and `DuckDBService._consolidated_rarefaction()`
- NOT stored in DB — computed at export time from `nb_reads_total` + `threshold_*` columns

## Date Done Bug Fix (update-column)
- `update-column date_done` was failing: checker returns DD-MM-YYYY but DuckDB DATE column expects YYYY-MM-DD
- `_parse_date()` conversion only existed in `upsert_sample()` path, not in `update-column` path
- Fixed in `check_samples.py` update_column(): added date format conversion for `column == 'date_done'`

## BAM Metadata Extraction
- `BAMExtractor._extract_with_samtools()`: timeout increased 10s → 30s, added 1 retry on timeout
- Columns extracted by `check`: dorado_model, dorado_model_version, run_id, barcode, taille_bam
- Columns NOT extracted by `check`: reads_per_flowcell, samples_per_run (aggregate, via `update-column`)
- Barcode extraction: from BAM filename (`barcode\d+` regex), NOT from RG header
- **Rebasecalled samples** have no barcode in filename or RG header → barcode stays NA
  - Workaround: extract from Pod2Bam align logs at `/mnt/aima-bam-data/processed/Pod2Bam/RetD/{run}/*/align/{sample}.log`
  - Log line `command: dorado aligner ... {run_id}_barcode{N}.bam` contains the barcode
  - 36 rebasecalled barcodes recovered this way (CGFL liquid, mars 2026)
  - 82 older rebasecalled (V4.3.0/V4.2.0) have no Pod2Bam logs → barcode remains NA

## POD5 Storage System (bam_metadata)
- Columns: `stockage_pod5`, `sample_type_pod5`, `taille_pod5`, `pod5_adresse`, `nb_pod5`, `pod5_completude`
- Update: `update-column stockage_pod5` → updates all 6 columns together
- Dispatch: COLUMN_CHECKERS type='storage' → `_update_pod5_storage()`
- `check` ne lance plus `_update_pod5_storage()` — uniquement via `update-column`
- `taille_pod5` calculée via `aws s3 ls --summarize` (entier GiB, cache `_s3_size_gib()`)
- `pod5_completude` = `round(nb_pod5 / (max_index + 1) * 100)` — détecte fichiers POD5 manquants
  - > 100% = multi-run mixing (indices de flowcells différents dans même dossier)
- `taille_bam` calculée via `aws s3 ls --summarize --profile=scw` sur le merged BAM S3 (entier GiB)
- `nb_bam` + `bam_completude` calculés via `aws s3 ls --recursive --profile=scw` sur BAM raw
- `bam_completude` = nb_bam / (max_index + 1) × 100, special case: 1 BAM = 100%
- "Nb POD5" et "Nb BAM" retirés de l'export GSheet (colonnes internes uniquement)
- "Complétude BAM" ajoutée à l'export GSheet

### S3 Structure
- Bucket: `aima-pod-data`, 2 providers (AWS profil `aws`, SCW profil `scw`)
- AWS path: `s3://aima-pod-data/CGFL/liquid/{run}/`
- SCW path: `s3://aima-pod-data/data/CGFL/liquid/{run}/` (same but with `data/` prefix)
- CGFL formats: `pod5_pass/{sample}/`, `pod5/` flat, `pod5_repN/`, racine `.pod5`
- CGFL matching: run_id[:8] → S3 hash, fallback sample_name dans pod5_pass/
- HCL: dossiers `{sample_name}/` avec POD5 directement dedans
- HCL raw NANO: `/mnt/aima-bam-data/data/HCL/raw/NANO{NN}_{YY}_N{X}/no_sample_id/{run_id}/`
- Dedup (`_dedup_cgfl_folders()`): `=OK` > original > `=moche`

### POD5 Verification (mars 2026)
- CGFL liquid: 462 detected, 112 not (104 Lung_Alc + 8 Colon rep without POD5 address)
- AWS+SCW: tailles identiques 148/148, nombre diff de 1 (fichier metadata extra côté AWS)
- Concordance gsheet CGFL (Sample name / Run number): 285/293 oui, 8 non (Colon_17-20_rep sans adresse DB)
- POD5 index contiguity: AWS 89/93 runs 100%, SCW 33/36 runs 100%
- 3 runs ~74% (mars 2025, anciens), 1 run 98.6% (7 indices manquants)

### Dorado Model Split
- `dorado_model` + `dorado_model_version` — split sur `@` dans BAMExtractor._parse_rg_line
- gsheet "dorado version" = software version (ex: 7.6.7), DB = model version (ex: v4.3.0)

## Sample Counts (liquid CGFL, mars 2026)
- 628 in DB (mars 2026, après ajout rebasecalled V5.0.0)
- Stockage: 285 AWS, 148 AWS+SCW, 37 SCW, 104 NULL (anciens Lung_Alc)
- 93 unique AWS addresses, 36 unique SCW addresses

## GSheet Config
- Config: `database/gsheets_config.json`
- metadata_CGFL: spreadsheet `1v1KUuCoMQV4Qk5jfbHLxhrUK6q_FETLiH8TuCQMdNxA`, worksheet "VAF"
- metadata_HCL: spreadsheet `1XcWPn3_PT1atR-i5DmOM1t0ldgb5_PnxhQUwNUxWpQg`, worksheet "VAF"
- Fetch: `fetch-gsheet metadata_CGFL` / `fetch-gsheet metadata_HCL`

## Scripts utilitaires (dev/)
- `dev/pod5_verification_gen.py` — génère `pod5_verification.tsv` (vérification croisée POD5 AWS/SCW pour CGFL, filtre rebasecalled)
- `dev/hcl_verification_gen.py` — génère `hcl_verification.tsv` (vérification croisée POD5/BAM raw↔S3 pour HCL)
- `dev/hcl_correspondance_rapports.tsv` — correspondance 66 runs NANO Dir / Run Number / Adresse Rapport
- `rapport/` — 36 rapports HTML Dorado copiés depuis SCW

## BETA_28M Check (avril 2026, BREAKING)
- `check_beta_28m()` exige **44 fichiers réels** (size > 0) + **≤ 1 ghost** (size = 0). Avant : tolérait 44 ou 45 sans distinguer ghost vs réel → faux-positif "44 total = 43 réels + 1 ghost"
- Les 2 flags `--combine-mods` + `--combine-strands` dans le log chr22 restent obligatoires
- Méthode `_has_single_ghost()` supprimée, remplacée par comptage direct via `_s3_ls_lines()`
- Audit avril 2026 : 1 faux-positif détecté = `Healthy_26_rebasecalled_V4.3.0` (HCL) — `chr18.bedMethyl.gz` manquant (43 réels + 1 ghost)

## CLI Defaults (avril 2026)
- Jobs par défaut : **4** pour `check`, `update-column`, `probs` (revert du 12→4 car 12 saturait S3)
- `update-column --sample` accepte multiple samples (`-s sample1 -s sample2`)
- `_update_pod5_storage()` et `_update_bam_sizes()` supportent le filtrage par samples via `sample_filter`

## HCL Verification (mars 2026)
- [Détails complets](project_hcl_verification.md)

## IchorCNA Column (mars 2026)
- Column: `ichorcna_score` in `retd_suivis` — VARCHAR, NOT in STATUS_COLUMNS
- Value: tumor fraction with comma decimal (ex: "0,01271") or "KO" if absent
- Source: `{sample_dir}/ichorCNA/{sample}.params.txt`, line 2, col 2 (tab-separated)
- S3 read-only via `_s3_read_text()`, fallback NFS
- [STATUS_COLUMNS gotcha](feedback_status_columns.md)

## mVAF v1.2 Column (mars 2026)
- Column: `mvaf_v12` in `retd_suivis` — VARCHAR, NOT in STATUS_COLUMNS
- Value: raima score v1.2 with comma decimal (ex: "0,0105373") or "KO" if absent
- Source: `{sample_dir}/BETA/{sample}.merged.epic.raima_score.V1.2.tsv`, line 2, col 2 (tab-separated)
- S3 read-only via `_s3_read_text()`, fallback NFS
- Export position: between "mVAF v1" and "mVAF v2"

## Barcode Fallback via bam_list.txt (mars 2026)
- When no `.bam` files in `origin_dir`, `BAMExtractor._barcode_from_bam_list()` reads `{sample}_bam_list.txt`
- Extracts barcode from first line filename (regex `barcode\d+`)
- S3-first via `_s3_read_text()`, fallback NFS
- For rebasecalled samples: barcode copied from original sample (same run = same barcode)
- HCL rebasecalled POD5 columns also copied from original (same POD5 data)

## BAM Completude Fallback via bam_list.txt (mars 2026)
- When `_update_bam_sizes()` finds no BAM on S3, `_bam_count_from_list()` reads `{sample}_bam_list.txt`
- Counts `.bam` lines and extracts max index from filename (`_{N}.bam` suffix)
- Completude = count / (max_index + 1) × 100
- Affects Bladder_Blood samples where BAM raw no longer on S3 (only txt files remain)

## Conventions
- Valid combos: liquid×(CGFL|HCL), solid×CGFL only
- Status: OK, KO, WARNING
- European format: comma decimals, DD-MM-YYYY dates
- Missing: "NA" in exports, NULL in DB
- samples table: colonne `sample_type` (pas `type`)

## Schema v2/v3/v4/v5 Migration (avril-mai 2026)
- SCHEMA_VERSION bumped 1→2→3→4→5 dans `lib/duckdb.py`
- Migration idempotente dans `DuckDBService._init_schema()` : `ALTER TABLE ... ADD COLUMN` si absent
- v2 : `qc_metrics.mvaf_v1_10m/20m`, `retd_suivis.frag_mode1/2`, `bam_metadata.bam_horaire`, `metadata.{gene1_detailed_variant,active_cancer_clinical,stage,commentaire_global}`
- v3 : `metadata.grade` — source "Grade" gsheet metadata_CGFL VAF, HCL reste NULL
- v4 : `metadata.speedvac` — `SpeedVac` (CGFL) + `SpeedVAc` (HCL, casse), harmonisé `Yes/No`
- v4 (fix bonus) : `"Stage" → stage` ajouté (CGFL stage était 100% NULL avant)
- v5 (mai 2026) : `metadata.cohort` — source col `Cohorte` (col 48 dans les 2 gsheets), mapping unique `"Cohorte" → cohort`. Valeurs : Validation tech, AlCapone, Bladder, Brenus, MSD, Lung-DI précoce. `HARMONIZATION_RULES["cohort"]` défensif (casse/accent). Coverage liquid : CGFL 479/644 (165 manquants = Lung_Alc absents DB), HCL 445/449 (4 vides en gsheet). Rempli uniquement via `import-metadata` (workflow `check` → `import-metadata`).

## Mapping Collision Fix (`upsert_metadata`, avril 2026)
- Plusieurs `tsv_col` peuvent pointer vers le même `db_col` (ex: `"Stage"` et `"Stage (I, II...)"` → `stage` ; `"SpeedVac"` et `"SpeedVAc"` → `speedvac`)
- Avant : 2e itération écrasait la valeur précédente même avec `None` (col absente côté un labo)
- Après : `if new is not None or db_col not in data: data[db_col] = new` — préserve la 1re valeur non-None
- Sans ce fix, ajouter un mapping casse silencieusement les imports précédents

## Export ONT Sample (avril 2026)
- Commande `export-ont-samples` : DuckDB.metadata fusionnée (CGFL+HCL liquid) → onglet `'ONT Sample'` de la gsheet trace-prod (`1gm_vB7vTzAq38dgkJFNpgA3Cy_XRlUqunMgoBvKnh6M`)
- Filtre : `sample_type='liquid'`, rebasecalled exclus par défaut (flag `--include-rebasecalled` pour les inclure)
- Méthode DB : `DuckDBService.get_metadata_unified(exclude_rebasecalled=True)` — JOIN metadata + samples, ORDER BY labo, sample_name
- Méthode export : `GSheetsService.export_ont_samples(rows)` — 51 cols (3 tech + 44 metadata dédupliquées + 2 calculées)
- Headers metadata : déduplication par `db_col` en gardant la 1re entrée de `TSV_TO_DB_METADATA` (gère les collisions `"SpeedVac"/"SpeedVAc"` et `"Stage"/"Stage (I, II, III...)"`)
- Config : entrée `ont_samples` dans `gsheets_config.json`
- Coverage : 687 lignes (357 CGFL + 330 HCL), SpeedVac 687/687, Stage 365/687

## bam_horaire Column (avril 2026)
- Col `bam_metadata.bam_horaire` VARCHAR DEFAULT 'KO'. Tracks présence BAM raw horaires S3.
- Update dédié : `update-column bam_horaire {type} {labo}` — UPDATE chirurgical de la seule colonne via `_update_bam_horaire()`, ne touche JAMAIS nb_bam/taille_bam/bam_completude
- Logique : liste `s3://aima-bam-data/data/{labo}/{type}/{sample}/` via `aws s3 ls --recursive --profile scw`. `OK` si ≥1 `.bam`, `clean` si listing OK et 0 `.bam`, inchangé si erreur S3
- `update-column taille_bam` side-effect : tag aussi `bam_horaire='OK'` quand il observe des BAM raw

## mVAF Rarefied 10M/20M (avril 2026)
- Cols `qc_metrics.mvaf_v1_10m`, `mvaf_v1_20m` DECIMAL(10,4)
- Sources : `BETA/{sample}.10M.epic.raima_score.V2.tsv` et `.20M.epic.raima_score.V2.tsv`
- Extraction via `BaseChecker.get_mvaf_rarefied(depth)` — réutilise `TSVExtractor.extract_mvaf()`
- Export headers : "mVAF v1 10M" / "mVAF v1 20M" dans `_LIQUID_QC` et `_SOLID_QC`
- `update-column mvaf_v1_10m|mvaf_v1_20m` supportés

## Frag Modes (avril 2026)
- Cols `retd_suivis.frag_mode1`, `frag_mode2` VARCHAR DEFAULT 'NA' (**PAS dans STATUS_COLUMNS**)
- Source : `Fragmentomics/filtered/{sample}.fragmentomics_modes.tsv`, ligne 2, col 1 (mode1) et col 2 (mode2)
- Format : virgule décimale, "NA" si fichier absent/colonne vide
- Méthodes `BaseChecker.check_frag_mode1/2` + `_check_frag_mode(col_idx)` (S3-first via `_s3_read_text`, fallback NFS)
- Export : "Frag Mode1" / "Frag Mode2" entre "IchorCNA" et "BAM" dans `_LIQUID_QC` et `_SOLID_QC`

## gene1_vaf Raima Logic (avril 2026, BREAKING)
- Avant : `gene1_vaf = gene1_freq` si gene1_vaf absent (toujours rempli)
- Après : `gene1_vaf = max(gene1_freq.split(" / "))` **uniquement si `gene1_mutation_status == "Tumoral"`**, sinon NULL
- Raison : les freq Non-tumoral/Unknown ne doivent pas alimenter la VAF raima
- Impact : réimporter les metadata peut vider des gene1_vaf qui étaient précédemment remplis

## Metadata Rebasecalled Propagation (avril 2026, updated)
- `import-metadata` : après l'import principal, re-propage les metadata depuis le sample original vers **TOUTES** les variantes `{sample}_rebasecalled*` (pas seulement celles sans metadata)
- Raison : les rebasecalled ne sont jamais dans la gsheet → seule la propagation les touche. Sans re-propagation systématique, leur metadata se fige au moment de la 1re propagation et diverge de l'original dès qu'une valeur ou colonne change
- Exemple constaté : `Lung_10` original avec `stage="IV"`, rebasecalled figé à `"stade IV"` (ancien format) ; `Colon_32` original avec `stage="III"`, rebasecalled à NULL (colonne ajoutée après propagation)
- Résultat à chaque import : 113 CGFL + 71 HCL = 184 rebasecalled re-propagés
- Regex `_rebasecalled.*$` → `base_name`, lookup `get_sample(base_name, type, labo)`, copie complète avec `sample_id` remplacé via `_upsert_table("metadata", ...)`

## Metadata Import Lookup Fallback (avril 2026)
- Si lookup via "Old sample name" échoue → retente avec "Sample name" (était : seulement si Old était vide)
- Nécessaire pour les `*bis` : gsheet a `Old sample name = "Breast_1_bis"` (legacy avec underscore), DB stocke `"Breast_1bis"` (format court)
- Fix : +4 samples `*bis` récupérés (Breast_1bis, Lung_9bis, Lung_10bis, Lung_11bis), +4 rebasecalled propagés

## NFS-First Priority (avril 2026, BREAKING)
- `TSVExtractor._read_lines()` lit NFS d'abord, S3 en fallback (avant : S3 d'abord)
- Raison : sur ce serveur, NFS est plus rapide que S3 pour les petits TSV quand le mount est dispo
- `_s3_read_text()` reste utilisé ailleurs (checkers comme `check_ichorcna`, `check_mvaf_v12`) avec priorité S3
