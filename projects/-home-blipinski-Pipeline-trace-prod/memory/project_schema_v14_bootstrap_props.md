---
name: schema-v14-bootstrap-props
description: "Schema v14 — colonne retd_suivis.bootstrap_props (OK/KO), présence S3 du fichier BOOTSTRAP/{sample}.merged.all.bootstrap_v1.props.tsv, liquid only, calque EXACT de bootstrap (v12)"
metadata: 
  node_type: memory
  type: project
  originSessionId: d535c45c-6098-4ead-86fb-0dfa18961e0a
---

# Schema v14 — bootstrap_props (juin 2026)

Colonne `bootstrap_props VARCHAR DEFAULT 'KO'` dans `retd_suivis`, **liquid uniquement** (`LiquidChecker` seul, Solid intact). **Calque EXACT de `bootstrap` (schema v12)** — seule différence : fichier source `bootstrap_v1.tsv` → `bootstrap_v1.props.tsv` (fichier de propriétés/probabilités du bootstrap, généré à côté).

- Source : **présence** S3 `BOOTSTRAP/{sample}.merged.all.bootstrap_v1.props.tsv` (OK si présent, KO si absent). Pas de lecture du contenu.
- Hors STATUS_COLUMNS et NUMERIC_COLUMNS → VARCHAR libre (OK/KO).

**Why:** Bam2Beta produit désormais un `bootstrap_v1.props.tsv` (à côté du `bootstrap_v1.tsv` déjà tracé par la colonne `bootstrap` v12). Boris veut tracer sa présence à l'identique.

**How to apply:**
- Checker `BaseChecker.check_bootstrap_props(sample_dir, sample) -> Optional[str]` : `_s3_exists(... / "BOOTSTRAP" / f"{sample}.merged.all.bootstrap_v1.props.tsv")` → True=OK / False=KO / None (timeout)=preserve. Câblé dans `LiquidChecker.check_sample()` (success après `"Bootstrap"` + fallback `"KO"`). Pas dans SolidChecker.
- **Pattern preserve** (calque [[schema-v12-bootstrap]]) : update-column via `_update_bootstrap_props()` dédié (skip si None, stocke `"KO"` littéral via UPDATE direct), entrée `('retd_suivis', None, 'bootstrap_props', None)` dans COLUMN_CHECKERS + dispatch `if col_type == 'bootstrap_props'`. Passe par `check` général ET rétroactivement via `update-column`.
- Export (`_LIQUID_QC` only) : header `Props Bootstrap` **après `mVAF v1.4`**. Mapping `TSV_TO_DB_RETD["Props Bootstrap"]="bootstrap_props"`. Aucun edit gsheets.py.
- Schema bump 13→14 (`SCHEMA_VERSION`, DDL `CREATE_RETD_SUIVIS_TABLE` après `bootstrap`, migration idempotente v14, description). 4 fichiers : `lib/duckdb.py` (5 edits), `lib/checkers.py` (3), `database/check_samples.py` (3), `lib/utils.py` (1).
- Checkpoint rollback : tag `checkpoint-pre-bootstrap-props` (sur cd72c61).

**Vérifié** : OK = 26BM01841 / Breast_1 / Lung_1 / Bladder_Urine_02_090 / Twist_* / Healthy_151-182 (14 samples) ; KO = `Lung_8` (HCL). update-column persiste (Colon_1=OK, Lung_8=KO), export place `Props Bootstrap` en position 13 (après mVAF v1.4). **Couverture élevée attendue** (le module bootstrap a été re-tourné le 25/06 → la plupart des samples ont le `.props.tsv`, peu de KO).

**Étape E (rétrospectif, PAR BORIS)** : `update-column bootstrap_props liquid CGFL` / `... HCL` ; puis `export liquid CGFL --gsheet` / `... HCL --gsheet` (séquentiel, single writer lock DuckDB).

Liens : [[schema-v12-bootstrap]] (calque, même pattern preserve), [[schema-v13-mvaf-v14]] (schema précédent), [[columns-index]].
