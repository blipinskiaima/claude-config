# Phase 0 — Questions upfront

8 questions à poser via `AskUserQuestion` AVANT toute édition. Les réponses pilotent les branches du workflow.

**Important** : poser les questions par groupes de 1-4 max (limite AskUserQuestion). Recommandation : 2 batches de 4 questions.

---

## Batch 1 — Nature de la colonne

### Q1 — Table cible

| Option | Quand l'utiliser | Mapping TSV_TO_DB |
|---|---|---|
| `retd_suivis` | Status check d'un fichier/dossier généré par le pipeline (BAM, BEDMETHYL, ancestry, etc.) | `TSV_TO_DB_RETD` |
| `qc_metrics` | Valeur numérique calculée (DECIMAL) — mVAF, ratios, scores | `TSV_TO_DB_QC` |
| `bam_metadata` | Métadonnée extraite du BAM ou liée à POD5/storage | `TSV_TO_DB_BAM` |
| `metadata` | Donnée clinique importée depuis la gsheet metadata_CGFL/HCL VAF | `TSV_TO_DB_METADATA` |

### Q2 — Type SQL

| Option | DDL exact | Cas d'usage |
|---|---|---|
| VARCHAR | `VARCHAR DEFAULT 'KO'` ou `VARCHAR DEFAULT 'NA'` | Status (OK/KO/WARNING) ou texte libre |
| DECIMAL | `DECIMAL(10,4)` ou `DECIMAL(12,2)` | Score/ratio/comptage avec précision contrôlée |
| INTEGER | `INTEGER` | Compteurs entiers (samples_per_run, nb_pod5) |
| DATE | `DATE` | Dates au format YYYY-MM-DD |

### Q3 — Valeur par défaut

| Option | Quand l'utiliser |
|---|---|
| `'KO'` | Status check qui sera mis à jour par `check_*()` (pattern bam_status, threshold_*) |
| `'NA'` | Info qui peut légitimement être absente (ancestry, frag_mode1, ichorcna_score) |
| `NULL` | Valeur numérique non encore calculée (DECIMAL/INTEGER) |
| Aucun | Pour metadata clinique (rempli uniquement via import-metadata) |

### Q4 — Source des données

| Option | Implication étape B |
|---|---|
| Fichier S3 (chemin connu) | `check_*()` utilise `_s3_read_text` / `_s3_exists` / `_s3_ls_recursive` |
| Gsheet metadata | PAS de check_*() — uniquement mapping TSV_TO_DB_METADATA + import-metadata |
| BAM extraction (samtools) | Méthode dans `BAMExtractor`, dispatch type `'bam'` dans COLUMN_CHECKERS |
| Calcul agrégé (run_id, etc.) | Pas de check_*() — dispatch type `'aggregate'` dans COLUMN_CHECKERS |

---

## Batch 2 — Scope et comportement

### Q5 — Scope sample_type

| Option | Câblage check_sample() |
|---|---|
| liquid uniquement | `LiquidChecker.check_sample()` seulement + fallback dict liquid |
| solid uniquement | `SolidChecker.check_sample()` seulement |
| Les deux | Les deux checkers + les deux fallback dicts |
| metadata-only (Q4=gsheet) | Aucun câblage check_sample() — uniquement TSV_TO_DB_METADATA |

### Q6 — Valeurs possibles

| Option | STATUS_COLUMNS ? | Parsing |
|---|---|---|
| OK/KO strict | NON (recommandé) | VARCHAR libre — _parse_status() inutile |
| OK/KO/WARNING | OUI | Strict via `_parse_status()` — rejette les autres valeurs |
| VARCHAR libre | NON | Texte/nombre brut, `_harmonize()` optionnel |
| Numérique | N/A (DECIMAL/INTEGER) | `_parse_numeric()` — virgule→point, KO/NA→NULL |

⚠ Mettre une colonne dans STATUS_COLUMNS la rend rigide. Préférer VARCHAR libre sauf si OK/KO/WARNING est explicitement requis.

### Q7 — Comportement sur erreur S3 transient

| Option | Pattern étape C |
|---|---|
| KO strict (échec = KO en DB) | Pattern simple : retour `"KO"` direct, COLUMN_CHECKERS type `'checker'` |
| Preserve (échec = ne touche pas DB) | Pattern dédié : retour `None` + fonction `_update_<col>()` (cf bam_horaire, short_read) |

Recommandation Boris : **preserve** quand le check S3 est coûteux ou peut échouer pour raisons transient (network, rate limit).

### Q8 — Position dans l'export gsheet

| Option | Action |
|---|---|
| Liquid uniquement (entre X et Y) | Insérer dans `_LIQUID_QC` (lib/utils.py) entre les 2 headers |
| Solid uniquement (entre X et Y) | Insérer dans `_SOLID_QC` |
| Les deux (positions cohérentes) | Insérer dans les deux listes |
| Pas dans l'export | Aucun edit utils.py (colonne interne uniquement) |

---

## Récap à valider avant Étape A

Après les 8 réponses, présenter un récap textuel sous cette forme :

```
Récap feature <col> (schema vN) :
- Table cible       : <table>
- Type SQL          : <type>
- Default           : <default>
- Source            : <source>
- Scope             : <scope>
- Valeurs           : <valeurs>
- Erreur S3         : <preserve | KO strict>
- Position gsheet   : <entre X et Y dans _LIQUID_QC/_SOLID_QC | pas d'export>

Fichiers à modifier : lib/duckdb.py, lib/checkers.py[, lib/extractors.py], database/check_samples.py[, lib/utils.py]
```

Demander : **"OK pour ce récap ? Je lance l'Étape A ?"**
