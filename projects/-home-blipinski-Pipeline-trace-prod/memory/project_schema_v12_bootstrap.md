---
name: schema-v12-bootstrap
description: "Schema v12 — colonne retd_suivis.bootstrap (OK/KO), présence S3 du fichier BOOTSTRAP/{sample}.merged.all.bootstrap_v1.tsv, liquid only, pattern preserve via _s3_exists"
metadata: 
  node_type: memory
  type: project
  originSessionId: d535c45c-6098-4ead-86fb-0dfa18961e0a
---

# Schema v12 — bootstrap (juin 2026)

Colonne `bootstrap VARCHAR DEFAULT 'KO'` dans `retd_suivis`, **liquid uniquement** (câblée dans `LiquidChecker` seul, Solid intact). Trace en rétrospectif l'ajout de la feature Bootstrap dans le pipeline Bam2Beta.

- Source : **présence** du fichier S3 `processed/MRD/RetD/{type}/{labo}/{sample}/BOOTSTRAP/{sample}.merged.all.bootstrap_v1.tsv` (OK si présent, KO si absent). Pas de lecture du contenu.
- Ni dans `STATUS_COLUMNS` ni dans `NUMERIC_COLUMNS` → VARCHAR libre (OK/KO).

**Why:** Boris a ajouté un module Bootstrap dans Bam2Beta et veut suivre, comme les autres statuts, quels samples ont déjà le fichier généré, avec remplissage rétroactif via update-column.

**How to apply:**
- Checker `BaseChecker.check_bootstrap(sample_dir, sample) -> Optional[str]` : `_s3_exists(... / "BOOTSTRAP" / f"{sample}.merged.all.bootstrap_v1.tsv")` → True=OK, False=KO, **None (timeout S3) → None = preserve**. Câblé dans `LiquidChecker.check_sample()` (success après `"Short Read"` + fallback `"KO"`). Pas dans SolidChecker.
- **Pattern preserve** (calque [[schema-v7-short-read]]) : update-column via `_update_bootstrap()` dédié (skip UPDATE si None), entrée `('retd_suivis', None, 'bootstrap', None)` dans `COLUMN_CHECKERS` + dispatch `if col_type == 'bootstrap'` dans `update_column()`.
- **Choix `_s3_exists` (head-object) et NON `_s3_ls_lines`** : `_s3_ls_lines` a le bug "préfixe vide → None" (non corrigé, contrairement à `_s3_ls_recursive` au commit 8c16ae3), donc un dossier `BOOTSTRAP/` absent donnerait None (preserve) au lieu de KO. `_s3_exists` distingue proprement présent (True→OK) / absent (404→False→KO) / timeout (None→preserve). **Limite connue** : le preserve via `_s3_exists` ne couvre que le timeout subprocess (5s), pas les erreurs réseau non-timeout (head-object renvoie returncode != 0 → False → KO). Acceptable car aws CLI retry les 503/rate-limit avant timeout.
- Export (`_LIQUID_QC` only) : header `Bootstrap` entre `Short Read` et `BAM`. Mapping `TSV_TO_DB_RETD["Bootstrap"]="bootstrap"`. Aucun edit gsheets.py (mapping auto via `_sample_to_row`).
- Schema bump 11→12 (`SCHEMA_VERSION`, DDL `CREATE_RETD_SUIVIS_TABLE` après `short_read`, migration idempotente v12, description). 4 fichiers modifiés : `lib/duckdb.py` (5 edits), `lib/checkers.py` (3), `database/check_samples.py` (3), `lib/utils.py` (1).

**Vérifié** : OK = 26BM01841 / Breast_1 / Lung_1 / Bladder_Blood_01_001 / Lung_Alc_01_av ; KO = Healthy_826 / Colon_1 / Prostate_1 / Pancreas_1 / Ovary_1. update-column persiste (26BM01841=OK, Healthy_826=KO), export place `Bootstrap` en position 20 (entre Short Read 19 et BAM 21).

**Étape E (rétrospectif, PAR BORIS)** : `update-column bootstrap liquid CGFL` / `... HCL` ; puis `export liquid CGFL --gsheet` / `... HCL --gsheet` (séquentiel, single writer lock DuckDB).

Liens : [[schema-v11-mvaf-v13-frag-score]] (schema précédent, mêmes patterns), [[schema-v7-short-read]] (même pattern preserve / VARCHAR libre / default 'KO'), [[columns-index]].
