---
name: schema-v11-mvaf-v13-frag-score
description: "Schema v11 — colonnes retd_suivis mvaf_v13 + frag_score_v2_sc, liquid only, calque mvaf_v12 / frag_mode_sc"
metadata:
  node_type: memory
  type: project
  originSessionId: explore-projet-add-trace-prod
---

# Schema v11 — mvaf_v13 + frag_score_v2_sc (juin 2026)

2 colonnes VARCHAR dans `retd_suivis` (migration idempotente `ALTER TABLE ... ADD COLUMN`), **liquid uniquement** (câblées dans `LiquidChecker` seul, Solid intact).

- `mvaf_v13 VARCHAR DEFAULT 'KO'` — **calque EXACT de mvaf_v12** : source `BETA/{sample}.merged.epic.raima_score.V1.3.tsv`, ligne 2 col 3 (`cols[2]` = colonne `mvaf`), virgule décimale, NA si absent. Fichier V1.3 structure identique au V1.2 (`name\tscore\tmvaf\tmodel`).
- `frag_score_v2_sc VARCHAR DEFAULT 'NA'` — **nouveau checker** : source `Fragmentomics/filtered_softclipped/{sample}.fragmentomics_score.V2.tsv` (≠ `fragmentomics_modes.tsv`), ligne 2 col 1 (`cols[0]` = colonne `score`), virgule décimale, NA si absent. Format fichier : `score\tmodel` / `<val>\tfragmento v2`.

**Why:** Boris a calculé 2 nouveaux scores (mVAF v1.3 = nouvelle version raima ; Frag score v2 = score fragmentomique softclipped, ≠ des modes). Besoin de les tracer comme les scores existants + pouvoir remplir rétroactivement via update-column.

**How to apply:**
- Ni dans STATUS_COLUMNS ni dans NUMERIC_COLUMNS → VARCHAR libre, virgule préservée (comme mvaf_v12 et frag_mode).
- Checkers (`lib/checkers.py`, BaseChecker) : `check_mvaf_v13` (copie 1:1 de `check_mvaf_v12`, seul le nom de fichier V1.2→V1.3 change) ; `check_frag_score_v2_sc` (nouveau, même squelette _s3_read_text + fallback NFS, lit `cols[0]`).
- Câblage : `LiquidChecker.check_sample()` success path (après `mVAF v1.2`) + fallback NA group (sample inexistant → NA). **Pas dans SolidChecker.**
- `update-column` (`check_samples.py`) : 2 entrées `'checker'` simples dans `COLUMN_CHECKERS` (`mvaf_v13` / `frag_score_v2_sc`). Passe par `check` général ET rétroactivement via `update-column {col} liquid {labo} [-s sample]`.
- Export (`lib/utils.py`, `_LIQUID_QC` only) : header `mVAF v1.3` après `mVAF v2` ; `Frag Score v2` après `Mode2`. Mappings `TSV_TO_DB_RETD["mVAF v1.3"]="mvaf_v13"` et `["Frag Score v2"]="frag_score_v2_sc"`. Aucun edit gsheets.py (mapping auto via `_sample_to_row`).
- Schema bump 10→11 (`SCHEMA_VERSION`, DDL `CREATE_RETD_SUIVIS_TABLE` après `mvaf_v12`, migration v11, description).

**Vérifié** : Healthy_826 (CGFL) → mVAF v1.3=`2,581`, Frag Score v2=`-0,0682464198886691` ; 26BM01841 → Frag Score v2=`0,00755156001789226` (= exemple verbatim de Boris). Sample inexistant → NA/NA.

**Étape E (rétrospectif, PAR BORIS)** : `update-column mvaf_v13 liquid CGFL` / `... HCL` ; idem `frag_score_v2_sc` ; puis `export liquid CGFL --gsheet` / `... HCL --gsheet` (séquentiel, single writer lock).

Liens : [[schema-v10-frag-sc]] (schema précédent, mêmes patterns), [[columns-index]]. mvaf_v12 documenté dans CLAUDE.md.
