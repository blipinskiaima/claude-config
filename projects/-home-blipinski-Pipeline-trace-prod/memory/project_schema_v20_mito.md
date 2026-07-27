---
name: project-schema-v20-mito
description: "Schema v20 — 5 colonnes mito (mt_depth, mt_coverage_percent, mt_autosomal_depth_ratio, mt_autosomal_coverage_ratio, mt_mean_length) dans retd_suivis, liquid only, source TSV MITO/{sample}.mito_qc.tsv index 3/4/7/8/9, précision complète en base + arrondi 2 déc à l'export via ROUND2_HEADERS"
metadata: 
  node_type: memory
  type: project
  originSessionId: f4c0cc1e-b20b-4f48-bb7a-87640e0b5b07
  modified: 2026-07-27T14:31:19.883Z
---

# Schema v20 — 5 métriques mito (juillet 2026)

Ajout de **5 colonnes** VARCHAR DEFAULT 'KO' dans `retd_suivis`, **liquid uniquement** (`LiquidChecker` seul, Solid intact — 0 dossier MITO en solid, vérifié). Hors `STATUS_COLUMNS` et `NUMERIC_COLUMNS` → virgule décimale préservée. **Calque de `themelio_score` (v18) / TOO (v19)** avec 3 différences.

**Why:** Boris veut suivre les métriques mitochondriales produites par le pipeline (profondeur mito, couverture, ratios mito/autosomes, longueur moyenne des reads mito), exportées en fin de bloc QC liquid.

## Source

`{sample}/MITO/{sample}.mito_qc.tsv` — dossier `MITO` **directement sous le sample**. TSV tabulé, header 11 colonnes + **exactement 1 ligne** de données. Format **strictement homogène** sur les 1095 fichiers (header identique au md5, 2 lignes partout, 0 valeur vide sur les 5 colonnes retenues).

| Colonne DB | Header gsheet | Index (0-based) |
|---|---|---|
| `mt_depth` | `MT Depth` | 3 |
| `mt_coverage_percent` | `MT Coverage %` | 4 |
| `mt_autosomal_depth_ratio` | `MT/Auto Depth Ratio` | 7 |
| `mt_autosomal_coverage_ratio` | `MT/Auto Coverage Ratio` | 8 |
| `mt_mean_length` | `MT Mean Length` | 9 |

Colonnes du fichier **non retenues** : `sample_id`, `mt_n_reads_total`, `mt_n_reads_aligned`, `autosomal_depth`, `autosomal_coverage_percent`, `mt_median_length`.

## How to apply (3 différences vs le calque v18/v19)

1. **Parsing `split("\t")`, PAS le module `csv`** — contrairement à [[project-schema-v19-too]] dont la col 10 `confidence_stratum` contient une virgule interne. Ici c'est un TSV propre, aucun champ quoté.
2. **Deux helpers** dans `BaseChecker` : `_mito_row(sample_dir, sample) -> Optional[list]` (calque `_too_row`, `_s3_read_text` S3-first + fallback NFS, retourne la ligne 2 ou None) et `_mito_value(sample_dir, sample, idx) -> str` (`format_comma` + `NA` si absent). Les 5 `check_mt_*()` publics font **1 ligne chacun**. À 5 colonnes, factoriser évite 5 copies de la même garde (v19 la répétait dans ses 2 checkers).
3. **Double format** : `format_comma()` en base (**précision complète**, `5.133307299 → 5,133307299`) mais **arrondi 2 décimales à l'export** via `format_round2_comma`. Choix Boris : 2 décimales à l'affichage, sans perte en base.

- Constante **`ROUND2_HEADERS`** créée dans `lib/utils.py` (+ `__all__`) = `("Mode1", "Mode2", "MT Depth", "MT Coverage %", "MT/Auto Depth Ratio", "MT/Auto Coverage Ratio", "MT Mean Length")`. Remplace le tuple littéral `('Mode1','Mode2')` **dupliqué** dans `GSheetsService._sample_to_row` et `DuckDBService.export_tsv` → source unique (évite le piège `_RAREFACTION_THRESHOLDS`, implémenté en double).
- Câblés `LiquidChecker.check_sample()` après `"TOO Final Decision"`. 5 entrées `COLUMN_CHECKERS` (pattern simple `'checker'`). `update-column mt_depth|… liquid {labo}`.
- Export (`_LIQUID_QC` only) : 5 headers **en fin de liste, après `Pipeline Version`** → positions **36-40 sur 52** colonnes. ⚠ Ce n'est **pas** la toute dernière colonne de la gsheet : `HEADERS_ALL = _LIQUID_QC + _BAM_COLS`, donc les 12 colonnes BAM (jusqu'à `BAM Horaire`) restent à droite. Choix assumé de Boris.
- `lib/duckdb.py` : `SCHEMA_VERSION 19→20`, DDL, migration idempotente (**boucle** sur les 5 noms, pas 5 blocs `if` copiés), 5 mappings `TSV_TO_DB_RETD`, description.

**Scope data (27/07/2026) :** 582 CGFL liquid + 513 HCL liquid ont `MITO/`, **0 solid**. Sur 811 samples CGFL en base → ~229 à `NA`, essentiellement la cohorte `Lung_Alc_*`.

## Gotchas

- **Homonyme `Colon_1` CGFL ≠ HCL** : le même nom existe dans les deux labos avec des valeurs mito **différentes** (HCL `18,23` / CGFL `5,16`). Un exemple de fichier fourni sans le labo est ambigu — toujours vérifier les deux avant de conclure à une incohérence de données.
- **`update-column -s <sample>` sur un sample absent du labo ciblé ne dit rien** : l'`UPDATE ... WHERE labo=?` n'affecte 0 ligne, mais le compteur affiche quand même « N samples mis à jour » (il compte les **itérations**, pas les lignes touchées). Un test négatif fait sur le mauvais labo semble donc passer alors qu'il ne prouve rien — vérifier que le sample est bien en base pour ce labo (`SELECT ... FROM samples WHERE sample_name=? AND labo=?`).
- **Fallback dict** : les 5 clés ont été ajoutées au groupe `"NA"` de `LiquidChecker.check_sample()` (sample absent du filesystem). v18/v19 **avaient omis** cette étape pour `Thémélio`/`TOO *` — bénin (clé absente = colonne non mise à jour, pas de KeyError) mais incohérent ; non corrigé, hors scope.
- **`NA` vs `KO`** (identique v10/v18/v19) : via `check` général → `"NA"` littéral ; via `update-column` → converti en `NULL` (export `NA`). Les colonnes jamais backfillées gardent le default `KO`.

**Vérifié :** HCL `Colon_1` → `18,23` / `100` / `5,133307299` / `1,1007` / `150,066` (= exemple de référence) ; CGFL `Colon_1` → `5,16` / `98` / `4,724897052` / `1,58915` / `177,011` ; `Lung_Alc_01_av` (sans MITO) → `NULL` en base, `NA` à l'export ; export TSV local headers en position 36-40, `MT/Auto Depth Ratio` affiché `5,13` avec `5,133307299` conservé en base. Checkpoint `checkpoint-pre-mito` (sur `6b22116`).

Liens : [[project-schema-v19-too]] et [[project-schema-v18-themelio]] (calques directs), [[feedback_status_columns]] (pourquoi hors STATUS_COLUMNS), [[project-columns-index]].
