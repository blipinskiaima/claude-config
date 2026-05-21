# Étape A — Schema bump (lib/duckdb.py)

## Fichier impacté
`~/Pipeline/trace-prod/lib/duckdb.py` UNIQUEMENT (4-5 edits)

## Edits à appliquer

### Edit 1 — Bump SCHEMA_VERSION

Ligne 13 (chercher exactement) :
```python
SCHEMA_VERSION = N
```
Remplacer par `SCHEMA_VERSION = N+1`.

Pour récupérer la version actuelle :
```bash
grep -n "^SCHEMA_VERSION" lib/duckdb.py
```

### Edit 2 — Ajout colonne dans le DDL canonique

Selon Q1, identifier la bonne table CREATE_*_TABLE :

| Table cible | Variable Python | Localisation |
|---|---|---|
| `retd_suivis` | `CREATE_RETD_SUIVIS_TABLE` | ~ligne 52-82 |
| `qc_metrics` | `CREATE_QC_METRICS_TABLE` | ~ligne 31-49 |
| `bam_metadata` | `CREATE_BAM_METADATA_TABLE` | ~ligne 85-106 |
| `metadata` | `CREATE_METADATA_TABLE` | ~ligne 166-220 |

Insérer la colonne juste avant `updated_at` (ou à une position logique entre colonnes existantes du même thème).

**Exemple `retd_suivis`** :
```sql
read_start_time VARCHAR DEFAULT 'KO',
<col> <TYPE> [DEFAULT '<val>'],          -- nouvelle colonne
date_done DATE,
```

### Edit 3 — Migration idempotente `ALTER TABLE`

Dans `DuckDBService._init_schema()` (~ligne 442-487), ajouter un nouveau bloc à la suite des migrations existantes (juste avant le bloc `INSERT INTO _schema_version`) :

```python
# Migration vN+1: ajout colonne <col> (<table>)
if '<col>' not in <table_cols_var>:
    self.conn.execute("ALTER TABLE <table> ADD COLUMN <col> <TYPE> [DEFAULT '<val>']")
```

Variables existantes à réutiliser :
- `retd_col_names` (set des colonnes `retd_suivis`)
- `meta_col_names` (set des colonnes `metadata`)
- Pour `qc_metrics` ou `bam_metadata` : créer le set au début si pas déjà présent

Bumper aussi la description du `_schema_version` :
```python
[SCHEMA_VERSION, f"Add <col> to <table> (v{SCHEMA_VERSION})"],
```

### Edit 4 — Mapping TSV_TO_DB_*

Selon Q1, ajouter dans le bon mapping :

| Table | Mapping | Localisation |
|---|---|---|
| retd_suivis | `TSV_TO_DB_RETD` | ~ligne 270-314 |
| qc_metrics | `TSV_TO_DB_QC` | ~ligne 270-287 |
| bam_metadata | `TSV_TO_DB_BAM` | ~ligne 317-334 |
| metadata | `TSV_TO_DB_METADATA` | ~ligne 337-388 |

```python
"<Header Gsheet>": "<col>",
```

⚠ Collision check : si une autre `tsv_col` pointe déjà vers `<col>`, le code `upsert_metadata` gère via `if new is not None or db_col not in data`. Mais éviter sauf nécessité (casse différente entre labos par exemple : `"SpeedVac"` + `"SpeedVAc"`).

### Edit 5 (conditionnel) — STATUS_COLUMNS

Si Q6 = `OK/KO/WARNING` strict (rare), ajouter `'<col>'` dans le set `STATUS_COLUMNS` (~ligne 412-428). 

**Si VARCHAR libre (recommandé)** : NE PAS ajouter — la valeur sera traitée comme texte brut.

⚠ STATUS_COLUMNS rend la colonne rigide : `_parse_status()` rejette tout sauf OK/KO/WARNING. Préférer VARCHAR libre.

## Vérification (3 commandes)

```bash
# 1. La colonne existe avec le bon default
python3 database/check_samples.py columns <table> | grep <col>

# 2. La migration s'est appliquée (version bumpée + description)
python3 database/check_samples.py query "SELECT version, description FROM _schema_version ORDER BY version DESC LIMIT 3"

# 3. Les samples existants ont le default (0 valeur autre que le default)
python3 database/check_samples.py query "SELECT <col>, COUNT(*) FROM <table> GROUP BY <col>"
```

Résultats attendus :
- Ligne 1 : `<col>  <TYPE>  NULL DEFAULT '<val>'`
- Ligne 2 : nouvelle ligne `vN+1 | Add <col> to <table> (vN+1) | <timestamp>`
- Ligne 3 : `<default> | <count_total>` (uniquement le default, pas de valeur calculée)

## Cas particulier : colonne metadata (Q4=gsheet)

Si la colonne vient d'une gsheet (pas de check S3) :
- Édits 1, 2, 3 dans `CREATE_METADATA_TABLE` + migration
- Édit 4 dans `TSV_TO_DB_METADATA` UNIQUEMENT (pas RETD/QC/BAM)
- **Skip étape B + C** — la donnée arrive via `import-metadata` (gspread)
- Étape D : header dans `_LIQUID_QC`/`_SOLID_QC` si à exporter, ou onglet `ONT Sample` via `export_ont_samples`
- Coverage post-import : `tp query "SELECT COUNT(*) FROM metadata WHERE <col> IS NOT NULL"`

## STOP — Validation Boris

Après les 5 edits + 3 vérifications, présenter le récap :
```
✅ Étape A — Schema vN+1 terminée
- SCHEMA_VERSION bumpé (N → N+1)
- DDL canonique : colonne <col> ajoutée à <table>
- Migration ALTER TABLE appliquée sur la DB existante
- Mapping TSV_TO_DB_<TABLE>["<Header>"] = "<col>"
- Defaults pour <N> samples existants : tous à <default>

OK pour Étape B (check_*()) ?
```
