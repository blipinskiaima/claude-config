---
name: project-schema-v18-themelio
description: "Schema v18 — colonne themelio_score (retd_suivis, liquid only), score Thémélio du pipeline BAM2BETA, source CSV THEMELIO/{sample}.themelio_predictions.csv ligne 2 col 2, virgule précision complète, calque mvaf_v14"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8d5ec8da-3182-45f1-a22a-243b080db5f3
  modified: 2026-07-22T13:44:35.746Z
---

# Schema v18 — themelio_score (juillet 2026)

Ajout colonne `themelio_score` VARCHAR DEFAULT 'KO' dans `retd_suivis`, **liquid uniquement** (`LiquidChecker` seul, Solid intact — 0 dossier THEMELIO en solid). Hors `STATUS_COLUMNS` et `NUMERIC_COLUMNS` → virgule décimale préservée. Trace le score Thémélio récemment ajouté au pipeline BAM2BETA.

**Why:** Boris veut suivre le `themelio_score` (probabilité 0-1 du classifieur Themelio 1.0.0, XGBoost) produit par BAM2BETA, exporté après le score mVAF v1.4.

**How to apply (calque [[project-schema-v13-mvaf-v14]], 3 différences réelles) :**
- Source : `{sample}/THEMELIO/{sample}.themelio_predictions.csv` — dossier `THEMELIO` **directement sous le sample** (⚠ PAS `OUTPUT/THEMELIO/` comme annoncé initialement — vérifié sur NFS : aucun `OUTPUT/`). Fichier **CSV virgule à champs quotés**, header + 1 ligne données. `themelio_score` = **ligne 2, colonne 2** (index 1), non quotée.
- Parsing : `lines[1].split(",")`, `cols[1].strip().strip('"')`, puis `format_comma()` (point→virgule, précision complète = **0.935531 → 0,935531**, choix Boris vs les 4 déc. de format_mvaf4). NA si fichier/ligne/colonne absent (chaîne défensive triple).
- Checker `check_themelio_score` (BaseChecker, `lib/checkers.py`), câblé dans `LiquidChecker.check_sample()` après `"mVAF v1.4"`. `_s3_read_text` S3-first puis fallback NFS. Pas dans SolidChecker.
- `COLUMN_CHECKERS['themelio_score'] = ('retd_suivis', 'check_themelio_score', 'checker', None)` (pattern simple). Passe par `check` général ET rétroactivement via `update-column themelio_score liquid {CGFL|HCL}`.
- Export (`_LIQUID_QC` only) : header `Thémélio` **après `mVAF v1.4`** (avant `Props Bootstrap`). Mapping `TSV_TO_DB_RETD["Thémélio"] = "themelio_score"`.
- `lib/duckdb.py` : `SCHEMA_VERSION 17→18`, DDL retd_suivis, migration idempotente `ALTER TABLE ... ADD COLUMN`, description schema_version, mapping.

**Scope data (22/07/2026) :** THEMELIO présent 810 CGFL liquid + 512 HCL liquid, 0 solid. Le reste des samples liquid → `NA`.

**Vérifié :** `Bladder_Blood_02_099` → `0,935531` (OK), sample sans dossier → `NA`/NULL en DB. Étape B testée sans DB, C persistée en DB, D export TSV local (header position 13, entre mVAF v1.4 et Props Bootstrap). Checkpoint `checkpoint-pre-themelio` (sur `2513f56`). Backfill CGFL+HCL + export gsheet lancés en tmux avec retry 503.

Liens : [[project-schema-v13-mvaf-v14]] (calque principal), [[project-columns-index]].
