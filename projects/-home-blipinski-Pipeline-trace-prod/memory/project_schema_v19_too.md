---
name: project-schema-v19-too
description: "Schema v19 — 2 colonnes too_predicted_class (col 9) + too_final_decision (col 20) dans retd_suivis, liquid only, source CSV TOO/{sample}.too5_predictions.csv, parsing module csv OBLIGATOIRE (virgules internes dans confidence_stratum), texte brut (indications, pas scores)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8d5ec8da-3182-45f1-a22a-243b080db5f3
  modified: 2026-07-22T14:12:50.478Z
---

# Schema v19 — too_predicted_class + too_final_decision (juillet 2026)

Ajout de **2 colonnes** VARCHAR DEFAULT 'KO' dans `retd_suivis`, **liquid uniquement** (`LiquidChecker` seul, 0 dossier TOO en solid). Hors `STATUS_COLUMNS` et `NUMERIC_COLUMNS` (ce sont des **indications texte**, pas des scores → toute inclusion dans STATUS_COLUMNS écraserait `Bladder+Pancreas` en KO, cf [[feedback_status_columns]]). Suit le classifieur TOO (Tissue-Of-Origin) du pipeline BAM2BETA.

**Why:** Boris veut suivre la prédiction TOO : le type de cancer prédit (`predicted_class`) ET la décision finale (`final_decision`) exportés après `Thémélio`.

**How to apply (calque [[project-schema-v18-themelio]], 2 différences majeures) :**
- Source : `{sample}/TOO/{sample}.too5_predictions.csv` (dossier `TOO` directement sous le sample, ⚠ nom de fichier `.too5_predictions.csv` **un seul point** — le `..` de la demande initiale était une coquille). CSV virgule à champs quotés, header (23 col) + 1 ligne données.
- `too_predicted_class` = **colonne 9 / index 8** (`predicted_class`), valeurs : `Lung`, `Colon`, `Prostate`, `Bladder+Pancreas`, `Breast`.
- `too_final_decision` = **colonne 20 / index 19** (`final_decision`), ex `Unresolved: gate not reached`, `Unresolved: uncertain tumor class`.
- **⚠ Parsing module `csv` OBLIGATOIRE** (≠ le `split(",")` des calques précédents) : la colonne 10 `confidence_stratum` contient une **virgule interne** (`"(iii) Gate reached, low confidence"`) sur ~18 % des samples → un split naïf décalerait `final_decision`. `csv.reader(content.splitlines())` gère les guillemets. `predicted_class` (col 9) resterait OK au split (virgule après lui) mais `final_decision` NON. `import csv` ajouté en tête de `lib/checkers.py`.
- Helper `_too_row(sample_dir, sample) -> Optional[list]` factorise le parsing (retourne la ligne 2 ou None). `check_too_predicted_class` → `row[8]`, `check_too_final_decision` → `row[19]`, texte brut `.strip()` (csv dé-quote déjà), NA si absent. Chaque colonne reste independamment updatable (1 lecture par méthode).
- Câblés `LiquidChecker.check_sample()` après `"Thémélio"`. 2 entrées `COLUMN_CHECKERS` (pattern simple). `update-column too_predicted_class|too_final_decision liquid {labo}`.
- Export (`_LIQUID_QC` only) : headers `TOO Predicted` + `TOO Final Decision` après `Thémélio` (avant `Props Bootstrap`). Mappings `TSV_TO_DB_RETD`.
- `lib/duckdb.py` : `SCHEMA_VERSION 18→19`, DDL 2 col, migration idempotente (2 ALTER), description.

**Scope data (22/07/2026) :** TOO présent 810 CGFL + 513 HCL liquid, 0 solid.

**Vérifié :** `Bladder_Blood_02_099` (23 champs) → `Bladder+Pancreas` / `Unresolved: gate not reached` ; `26BM01841` (24 champs, virgule interne) → `Lung` / `Unresolved: uncertain tumor class` (split naïf aurait échoué) ; sample sans TOO → `NA`/NULL. Étape C : valeurs texte persistées sans corruption (hors STATUS/NUMERIC confirmé). Checkpoint `checkpoint-pre-too` (sur `37762f3`). Backfill CGFL+HCL + export gsheet en tmux avec retry 503.

Liens : [[project-schema-v18-themelio]] (calque, session juste avant), [[feedback_status_columns]] (gotcha texte vs STATUS), [[project-columns-index]].
