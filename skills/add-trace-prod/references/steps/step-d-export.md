# Étape D — Export gsheet (lib/utils.py)

## Fichier impacté
`~/Pipeline/trace-prod/lib/utils.py` UNIQUEMENT (1 edit)

⚠ **Aucun edit dans `lib/gsheets.py`** — le mapping `TSV_TO_DB_*` (ajouté en Étape A) est utilisé automatiquement par `GSheetsService._sample_to_row()` qui fait :
```python
mappings = {**TSV_TO_DB_QC, **TSV_TO_DB_RETD, **TSV_TO_DB_BAM, ...}
for header in headers:
    if header in mappings:
        db_col = mappings[header]
        row.append(self._format_value(sample.get(db_col), db_col))
```

Donc tout ce qu'il faut, c'est faire apparaître le `<Header>` dans la liste `HEADERS_ALL`.

## Edit unique — Insertion dans _LIQUID_QC / _SOLID_QC

### Localisation

`lib/utils.py` :
- `_LIQUID_QC` : ~ligne 58-86
- `_SOLID_QC` : ~ligne 89-112

### Position selon Q8

Insérer `"<Header Gsheet>"` entre les 2 headers identifiés à Q8.

**Exemple** (insertion entre `"Read Start Time"` et `"BAM"`) :
```python
_LIQUID_QC = [
    *_BASE_COLS,
    ...
    "Read Start Time",
    "<Header Gsheet>",        # ← nouvelle ligne
    "BAM",
    ...
]
```

### Scope (Q5)

| Q5 | Action |
|---|---|
| liquid uniquement | Insérer dans `_LIQUID_QC` seulement |
| solid uniquement | Insérer dans `_SOLID_QC` seulement |
| Les deux | Insérer dans les deux (position cohérente quand possible) |
| Pas dans l'export | Aucun edit (colonne interne, accessible via `tp query` uniquement) |

### Cas particulier — colonne bam_metadata

Si la colonne est dans `bam_metadata`, vérifier `_BAM_COLS` (~ligne 49-52). Mais attention : les colonnes BAM sont déjà incluses via `HEADERS_ALL["liquid"] = _LIQUID_QC + _BAM_COLS`. La nouvelle col doit aller soit dans `_LIQUID_QC` (position thématique) soit dans `_BAM_COLS` (groupée avec les autres BAM).

## Vérification (3 commandes)

```bash
# 1. Export local TSV (~30s)
python3 database/check_samples.py export liquid CGFL -o /tmp/test_<col>.tsv

# 2. Le header est présent à la bonne position
head -1 /tmp/test_<col>.tsv | tr '\t' '\n' | grep -n -E "<Header avant>|<Header>|<Header après>"

# 3. La valeur d'un sample testé apparaît
awk -F'\t' 'NR==1{for(i=1;i<=NF;i++)if($i=="<Header>"||$i=="Sample")c[$i]=i} $c["Sample"]=="<sample_ok>"{print $c["Sample"]"\t"$c["<Header>"]}' /tmp/test_<col>.tsv
```

Résultats attendus :
- Header présent à la position N+1 où N = position de "<Header avant>"
- Valeur du sample testé = celle persistée en DB (Étape C)

## STOP — Récap final avant Étape E

```
✅ Étape D — Export validée

Récap global des modifications :
| Fichier                       | Edits | Nature                                         |
|-------------------------------|-------|------------------------------------------------|
| lib/duckdb.py                 |   4-5 | SCHEMA_VERSION, DDL, migration, mapping        |
| [lib/extractors.py]           |   1   | (si nouveau helper S3)                         |
| lib/checkers.py               |   4   | Import, méthode, câblage, fallback             |
| database/check_samples.py     |   1-3 | COLUMN_CHECKERS (+ dispatch + _update_<col>)   |
| lib/utils.py                  |   1   | Header dans _LIQUID_QC / _SOLID_QC             |

Tests passants :
✅ Schema vN+1 appliquée + samples au default
✅ check_<col>() : <sample_ok>=OK / <sample_ko>=KO
✅ update-column persist en DB
✅ Header présent dans export TSV à la bonne position
✅ Valeur sample propagée dans l'export

🚀 Étape E à toi (Boris) :
   tp update-column <col> liquid CGFL
   tp update-column <col> liquid HCL    (si scope HCL)
   tp export liquid CGFL --gsheet
   tp export liquid HCL --gsheet

⚠ Ne PAS exécuter CGFL et HCL en parallèle (DuckDB single writer lock).
```

## Post-livraison — Mémoire

Après confirmation Boris, créer le fichier topique dans la mémoire :

```
~/.claude/projects/-home-blipinski-Pipeline-trace-prod/memory/project_schema_v<N>_<col>.md
```

Avec frontmatter :
```markdown
---
name: schema-v<N>-<col>
description: Schema v<N> — colonne <table>.<col> ...
metadata:
  type: project
---
```

Et 1 ligne dans `MEMORY.md` :
```
- [Schema v<N> — <col>](project_schema_v<N>_<col>.md) — <hook 1 phrase>
```

Voir `project_schema_v7_short_read.md` comme modèle exact.
