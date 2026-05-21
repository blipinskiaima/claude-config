---
name: add-trace-prod
description: Workflow guidé pour ajouter une nouvelle colonne/feature à la base de données trace-prod (~/Pipeline/trace-prod). Reproduit le processus rigoureux validé sur schema v7 (short_read) — 5 étapes avec validation utilisateur entre chaque, arrêt avant l'exécution rétrospective qui reste sous contrôle de Boris. Use when the user wants to add a new column to retd_suivis/qc_metrics/bam_metadata/metadata, bump schema version, says "add-trace-prod", "nouvelle colonne trace-prod", "schema vN", "nouvelle feature DB trace-prod", "ajoute une colonne dans trace-prod", or any variation of extending the trace-prod database schema.
---

<objective>
Ajouter une nouvelle colonne/feature à la base trace-prod en suivant le pattern éprouvé (schema v2→v7). Le skill garantit la cohérence entre DDL, migration idempotente, checker, dispatch update-column, export gsheet, et mise à jour mémoire.
</objective>

<rules>
- Demander confirmation utilisateur entre CHAQUE étape (A → B → C → D)
- S'ARRÊTER avant l'étape E — Boris exécute lui-même le rétrospectif (update-column + export)
- Karpathy Guidelines obligatoires (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution)
- Read-before-Edit absolu — lire les fichiers cibles AVANT toute modification
- Aucun edit speculatif — ne pas anticiper des besoins non exprimés
- Test fonctionnel obligatoire à chaque étape (1 sample OK + 1 sample KO réels)
- Toutes commandes utilisent `python3 database/check_samples.py ...` depuis ~/Pipeline/trace-prod (alias `tp`)
</rules>

<workflow>

## Overview

```
Phase 0  → 8 décisions clés via AskUserQuestion  (verify: récap validé par Boris)
Étape A  → Schema bump (lib/duckdb.py)           (verify: `tp columns <table>` + version DB)
Étape B  → Méthode check_*() (lib/checkers.py)   (verify: 1 sample OK + 1 sample KO testés)
Étape C  → update-column (check_samples.py)      (verify: `tp update-column -s` persiste DB)
Étape D  → Export gsheet (lib/utils.py)          (verify: TSV local + grep header + valeur sample)
Étape E  → Exécution rétrospective                ⚠ PAR BORIS — Claude s'arrête ici
```

**Confirmation utilisateur requise entre chaque étape. Aucune cascade automatique.**

---

## Phase 0 — Décisions upfront

Avant tout code, clarifier la nature de la feature via 8 questions structurées.

Voir [references/decisions/upfront-questions.md](references/decisions/upfront-questions.md) pour les questions exactes à poser via `AskUserQuestion`, les arbres de décision, et l'impact de chaque réponse sur les étapes A→D.

**Output** : un récap textuel (table cible, type, default, source, scope, valeurs, comportement erreur S3, position gsheet) validé par Boris avant d'attaquer l'étape A.

---

## Étape A — Schema bump

**Fichier impacté** : `lib/duckdb.py`

4-5 edits chirurgicaux (ordre exact) :
1. `SCHEMA_VERSION = N → N+1` (ligne 13)
2. Ajout colonne dans le DDL canonique (`CREATE_RETD_SUIVIS_TABLE` / `CREATE_QC_METRICS_TABLE` / `CREATE_BAM_METADATA_TABLE` / `CREATE_METADATA_TABLE` selon réponse Q1)
3. Migration idempotente `ALTER TABLE ... ADD COLUMN` dans `DuckDBService._init_schema()` (test via `information_schema.columns`)
4. Mapping `TSV_TO_DB_*[<header gsheet>] = <db_col>` (RETD/QC/BAM/METADATA selon Q1)
5. Bump description schema_version

**Vérification obligatoire** :
```bash
python3 database/check_samples.py columns <table> | grep <col>
python3 database/check_samples.py query "SELECT MAX(version), description FROM _schema_version"
python3 database/check_samples.py query "SELECT <col>, COUNT(*) FROM <table> GROUP BY <col>"
```

Voir [references/steps/step-a-schema.md](references/steps/step-a-schema.md) pour le diff exact, les 4 tables possibles, et le pattern STATUS_COLUMNS vs VARCHAR libre.

**⏸ STOP — Demander validation Boris avant Étape B.**

---

## Étape B — Méthode `check_*()`

**Fichiers impactés** : `lib/extractors.py` (si nouveau helper S3 nécessaire) + `lib/checkers.py`

1. (Optionnel) Ajouter helper S3 dans `extractors.py` si aucun existant ne convient
2. Importer le helper dans `checkers.py` (ligne 10)
3. Implémenter `check_<col>(self, sample_dir: Path, sample: str) -> Optional[str]` dans `BaseChecker`
4. Câbler dans `LiquidChecker.check_sample()` ET/OU `SolidChecker.check_sample()` (selon Q5 scope)
5. Ajouter au fallback dict (cas sample n'existe pas, ~ligne 480-520)

**Vérification obligatoire** (test direct sans toucher la DB) :
```python
from lib.utils import get_config
from lib.checkers import LiquidChecker
cfg = get_config('liquid', 'CGFL')
ck = LiquidChecker(cfg)
print('OK:', ck.check_<col>(cfg.base_dir / '<sample_ok>', '<sample_ok>'))
print('KO:', ck.check_<col>(cfg.base_dir / '<sample_ko>', '<sample_ko>'))
```

Voir [references/steps/step-b-checker.md](references/steps/step-b-checker.md) pour les 4 helpers S3 disponibles, signatures de référence, et templates de méthodes.

**⏸ STOP — Demander validation Boris avant Étape C.**

---

## Étape C — Dispatch update-column

**Fichier impacté** : `database/check_samples.py`

Deux patterns possibles selon Q7 (comportement erreur S3) :

**Pattern simple** (KO strict sur erreur, suffit dans 80% des cas) :
```python
# 1 seul edit dans COLUMN_CHECKERS (ligne ~337)
'<col>': ('<table>', 'check_<col>', 'checker', None),
```

**Pattern preserve** (skip UPDATE si None — pour les checks S3 coûteux) :
```python
# 3 edits : déclaration + dispatch + nouvelle fonction _update_<col>()
```

**Vérification obligatoire** :
```bash
python3 database/check_samples.py update-column <col> liquid CGFL -s <sample_ok> -s <sample_ko>
python3 database/check_samples.py query "SELECT s.sample_name, r.<col> FROM samples s JOIN <table> r ON s.id=r.sample_id WHERE s.sample_name IN ('<sample_ok>','<sample_ko>')"
```

Voir [references/steps/step-c-update-column.md](references/steps/step-c-update-column.md) pour le template `_update_<col>()` et l'arbre de décision pattern simple vs preserve.

**⏸ STOP — Demander validation Boris avant Étape D.**

---

## Étape D — Export gsheet

**Fichier impacté** : `lib/utils.py` UNIQUEMENT

1 seul edit : ajouter `"<header gsheet>"` dans `_LIQUID_QC` ET/OU `_SOLID_QC` à la position validée en Q8.

**Aucun edit dans `lib/gsheets.py`** — le mapping `TSV_TO_DB_*` (déjà ajouté en étape A) est utilisé automatiquement par `_sample_to_row()`.

**Vérification obligatoire** :
```bash
python3 database/check_samples.py export liquid CGFL -o /tmp/test.tsv
head -1 /tmp/test.tsv | tr '\t' '\n' | grep -n "<header>"
awk -F'\t' 'NR==1{for(i=1;i<=NF;i++)if($i=="<header>"||$i=="Sample")c[$i]=i} $c["Sample"]=="<sample_ok>"{print $c["<header>"]}' /tmp/test.tsv
```

Voir [references/steps/step-d-export.md](references/steps/step-d-export.md) pour les positions standard et la logique `_sample_to_row()`.

**⏸ STOP — Récapituler à Boris + proposer Étape E.**

---

## Étape E — Exécution rétrospective (PAR BORIS)

⚠ **Claude NE LANCE PAS ces commandes** — Boris les exécute lui-même.

```bash
python3 database/check_samples.py update-column <col> liquid CGFL
python3 database/check_samples.py update-column <col> liquid HCL   # si scope inclut HCL
python3 database/check_samples.py export liquid CGFL --gsheet
python3 database/check_samples.py export liquid HCL --gsheet
```

⚠ **DuckDB single writer lock** : ne PAS exécuter CGFL et HCL en parallèle.

---

## Post-workflow — Mémoire

Après validation Étape D, créer/mettre à jour la mémoire trace-prod :

1. **Fichier topique** : `~/.claude/projects/-home-blipinski-Pipeline-trace-prod/memory/project_schema_v<N>_<col>.md`
   - Frontmatter `type: project`
   - Sections : **Why:** (motivation) + **How to apply:** (sources, méthode, patterns)
   - Liens `[[schema-v<N-1>-...]]` vers schemas antérieurs

2. **MEMORY.md** : ajouter 1 ligne `- [Schema vN — <col>](project_schema_vN_<col>.md) — <hook 1 phrase>`

Voir `project_schema_v7_short_read.md` existant comme modèle.

</workflow>

## Navigation

| Besoin | Référence |
|---|---|
| Questions upfront + arbres de décision | [decisions/upfront-questions.md](references/decisions/upfront-questions.md) |
| Diff exact lib/duckdb.py (4 tables possibles) | [steps/step-a-schema.md](references/steps/step-a-schema.md) |
| Helpers S3 + signatures check_*() | [steps/step-b-checker.md](references/steps/step-b-checker.md) |
| Pattern simple vs preserve (update-column) | [steps/step-c-update-column.md](references/steps/step-c-update-column.md) |
| Positions _LIQUID_QC / _SOLID_QC | [steps/step-d-export.md](references/steps/step-d-export.md) |
| Quel helper S3 utiliser quand | [patterns/s3-helpers.md](references/patterns/s3-helpers.md) |
| Pattern preserve sur erreur S3 (None → skip) | [patterns/preserve-vs-overwrite.md](references/patterns/preserve-vs-overwrite.md) |
| Colonnes modèles (ancestry, bam_horaire, etc.) | [patterns/reference-columns.md](references/patterns/reference-columns.md) |
| Pièges critiques à éviter | [gotchas/critical-pitfalls.md](references/gotchas/critical-pitfalls.md) |

## Karpathy Guidelines

**Think Before Coding** — chaque décision Phase 0 doit avoir une réponse explicite avant d'écrire la moindre ligne.

**Simplicity First** — code minimal. Une méthode `check_*` ~15-25 lignes. Aucune classe nouvelle. Aucun helper spéculatif.

**Surgical Changes** — entre 4 et 6 fichiers modifiés au total. Aucun edit hors des points d'extension prévus.

**Goal-Driven Execution** — chaque étape se termine par une vérification commande qui prouve le succès (pas "should work").
