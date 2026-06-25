---
name: project_schema_v13_mvaf_v14
description: "Schema v13 — colonne retd_suivis.mvaf_v14 VARCHAR DEFAULT 'KO', liquid only, calque de mvaf_v13 SAUF extraction cols[1] (colonne mvaf, fichier V1.4 à 3 colonnes name·mvaf·model), export après mVAF v1.3"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9b50bb93-854b-4ab6-bd15-bba0563cc6dc
---

# Schema v13 (juin 2026) — colonne `mvaf_v14` (retd_suivis)

Ajout colonne `mvaf_v14` VARCHAR DEFAULT 'KO' dans `retd_suivis` (migration idempotente `ALTER TABLE retd_suivis ADD COLUMN`), **liquid uniquement** (`LiquidChecker` seul, Solid intact). Hors STATUS_COLUMNS et NUMERIC_COLUMNS → virgule décimale préservée.

**Why:** suivre le mVAF du modèle raima V1.4 (nouvelle version), en parallèle de mvaf_v12/mvaf_v13.

**How to apply:** calque de [[project_schema_v11_mvaf_v13_frag_score]] (`check_mvaf_v13`) avec **UNE seule différence** = l'extraction de colonne.

- **Source** : `BETA/{sample}.merged.epic.raima_score.V1.4.tsv`
- **Structure fichier** (≠ V1.3) : **3 colonnes** `name · mvaf · model` (V1.3 en avait 4 : name·score·mvaf·model).
- **Extraction** : ligne 2, colonne 2 = **`cols[1]`** (colonne `mvaf`), `len(cols) >= 2`, `NA` si absent.
- **Formatage** (≠ v1.3 qui fait un simple `.replace(".",",")`) : via `format_mvaf4()` (lib/utils.py) — **4 décimales** si `|v| >= 1e-4` (ex `0,0121`), sinon **4 chiffres significatifs** (ex `1,56e-05 → 0,00001561` ; `5,07e-05 → 0,00005074`). **Jamais de notation scientifique** dans la DB ni l'export. KO/NA/non numérique inchangés. Demandé par Boris (juin 2026). Helper importé dans checkers.py et appelé dans `check_mvaf_v14`.
  - ⚠ Piège de nommage : V1.3 lit `cols[2]` (3ᵉ col), V1.4 lit `cols[1]` (2ᵉ col) — dans les deux cas c'est bien la **colonne mvaf**, mais sa position a changé car V1.4 a perdu la colonne `score`. (Boris avait d'abord parlé de "score" puis corrigé : c'est la colonne mvaf.)
- Exemple réel `26BM01841` : `name\tmvaf\tmodel` / `26BM01841\t0.0121269944369721\tv1.4` → DB `0,0121269944369721`.

## Câblage (5 fichiers)

1. `lib/duckdb.py` : `SCHEMA_VERSION = 13` ; DDL `mvaf_v14 VARCHAR DEFAULT 'KO'` après `mvaf_v13` ; migration v13 `if 'mvaf_v14' not in retd_col_names` ; mapping `TSV_TO_DB_RETD["mVAF v1.4"] = "mvaf_v14"` ; description schema_version.
2. `lib/checkers.py` : `check_mvaf_v14()` (BaseChecker) ; câblé `LiquidChecker.check_sample()` success dict (`"mVAF v1.4"`) après mVAF v1.3 + fallback dict (liste NA). Pas dans SolidChecker.
3. `database/check_samples.py` : `COLUMN_CHECKERS['mvaf_v14'] = ('retd_suivis', 'check_mvaf_v14', 'checker', None)` (pattern simple).
4. `lib/utils.py` : `"mVAF v1.4"` dans `_LIQUID_QC` après `"mVAF v1.3"` (avant `IchorCNA`).

Passe par le `check` général (nouveaux samples) ET rétroactivement via `update-column mvaf_v14 liquid {labo} [-s sample]`.

## Vérifs (juin 2026)
- Checker : `26BM01841` → `0,0121269944369721` ; fichier absent (`Lung_Alc_01_av`, sample bidon) → `NA`/NULL.
- Export liquid CGFL : header `mVAF v1.4` en position 12 (entre v1.3 et IchorCNA).
- Checkpoint git de rollback : tag `checkpoint-pre-mvaf-v14` sur `ac7f0f5`.

## Rétrospectif (PAR BORIS, non lancé par Claude)
```bash
python3 database/check_samples.py update-column mvaf_v14 liquid CGFL
python3 database/check_samples.py update-column mvaf_v14 liquid HCL
python3 database/check_samples.py export liquid CGFL --gsheet
python3 database/check_samples.py export liquid HCL --gsheet
```
⚠ DuckDB single writer lock : ne PAS lancer CGFL et HCL en parallèle.
