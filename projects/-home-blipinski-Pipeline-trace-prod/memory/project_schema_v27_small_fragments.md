---
name: project-schema-v27-small-fragments
description: "Schema v27 — renommage short_read → small_fragments (colonne, table, 26 col, CLI, chemin S3). Pré-migration AVANT les CREATE ; ALTER RENAME préserve PK/FK"
metadata: 
  node_type: memory
  type: project
  originSessionId: 376f4ffa-41ba-47ba-9101-bc82256d2b3d
  modified: 2026-08-21T14:51:34.012Z
---

# Schema v27 — renommage `short_read` → `small_fragments` (août 2026)

**Aucune colonne ajoutée ni supprimée** : uniquement un renommage, pour aligner trace-prod sur
le bucket S3 dont le miroir `{labo}_short_read/` a été renommé `{labo}_small_fragments/` côté
pipeline.

**Why:** le checker construisait toujours `{labo}_short_read` → listing S3 **vide** → la colonne
serait passée **KO sur 100 % des samples** au prochain `check`, alors que les données existent
(CGFL 782 dossiers, HCL 503). Découvert en répondant à « que regarde la colonne Short Read ? » :
la valeur en base était un héritage du dernier passage fait quand le chemin existait encore.

## Ce qui a été renommé

| Objet | Avant | Après |
|---|---|---|
| chemin S3 | `{labo}_short_read/` | `{labo}_small_fragments/` |
| colonne | `retd_suivis.short_read` | `small_fragments` |
| table | `short_read_metrics` | `small_fragments_metrics` |
| colonnes | 26 × `*_short_read` | 26 × `*_small_fragments` |
| header gsheet | `Short Read` | `Small Fragments` |
| CLI | `check-short-read`, `export-short-read-like` | `check-small-fragments`, `export-small-fragments-like` |
| module / classe | `checkers_short_read.py`, `ShortReadChecker` | `checkers_small_fragments.py`, `SmallFragmentsChecker` |

## Le point d'architecture — PRÉ-migration

`_migrate_small_fragments_rename()` est appelée **en tête de `_init_schema()`, AVANT la boucle
`for sql in ALL_TABLES`**. C'est l'inverse de toutes les migrations précédentes (v2→v26), qui
tournent *après* les CREATE.

Raison : `_init_schema()` exécute `CREATE TABLE IF NOT EXISTS` en premier. Si le DDL porte déjà
le nouveau nom, il **crée une `small_fragments_metrics` vide**, puis le
`ALTER TABLE short_read_metrics RENAME TO small_fragments_metrics` échoue sur un nom déjà pris
→ table fantôme + 1199 lignes devenues invisibles. **Tout futur renommage d'objet doit se placer
là.** Un simple `ADD COLUMN` (le cas de v2→v26) n'a pas ce problème.

## `ALTER RENAME` préserve PK/FK — la règle d'or ne s'applique pas

Vérifié sur une base jetable : `ALTER TABLE ... RENAME COLUMN` et `RENAME TO` conservent
**PRIMARY KEY, FOREIGN KEY et NOT NULL** (contraintes identiques avant/après, et la FK rejette
toujours un insert orphelin). Donc **pas besoin** du pattern DDL + `INSERT INTO SELECT` imposé
par [[duckdb-gotchas]] — celui-ci ne vise que `CREATE TABLE AS SELECT`. Migration testée sur
copie (1199 lignes, 1507 non-NULL, 26 colonnes) puis rejouée 2× pour l'idempotence.

## La migration v7 historique doit créer le nom CIBLE

`if 'small_fragments' not in retd_col_names: ALTER TABLE retd_suivis ADD COLUMN small_fragments`.
Sur une base ancienne (v6), la pré-migration ne trouve rien à renommer ; si v7 ajoutait encore
`short_read`, plus rien ne le renommerait → colonne parasite. Les trois cas sont couverts :
base v26 (pré-migration renomme), base v6 (v7 crée le nom cible), base neuve (DDL).

## Gotchas

- ⚠ **`sed 's/short-read/small fragments/g'` casse les noms de commandes Click** : produit
  `@cli.command('check-small fragments')` — avec un **espace**. Le CLI expose alors une commande
  inappelable. Traiter les formes à tiret (`check-short-read`, `export-short-read-like`)
  **avant** la règle générique, et vérifier avec `--help` après tout renommage de commande.
- ⚠ **L'onglet gsheet cible s'appelle `'Small Fragments'`, PAS `'Small Fragments Like'`.** La
  config pointait sur un `'Short Read Like'` qui **n'a jamais existé** dans le classeur. Toujours
  lister `sh.worksheets()` avant de conclure (cf. [[cohort-export]] : un nom absent fait créer un
  onglet fantôme par le fallback `add_worksheet`).
- ⚠ **L'onglet `'Short read'` (minuscule) est un tableau de travail manuel** — header
  *Basespace 5base*, colonnes `sample` / `Tumor fraction` / `total_reads (in M)`, 146 lignes.
  **Aucun rapport** avec cet export : ne jamais l'écraser ni le renommer.
- Le défaut en dur `config.get("worksheet", ...)` de `export_small_fragments_like` reste un
  piège du même type que celui supprimé dans `export_cohort` — recalé sur le bon nom, pas retiré.
- **Les valeurs en base datent d'avant le renommage du bucket** : 782 dossiers CGFL sur S3 pour
  seulement 728 `OK` en base → un `update-column small_fragments liquid {labo}` fera passer des
  KO en OK. Même mécanique de décalage temporel que [[feedback_probs_loyfer_lag]].
- `docs/superpowers/{specs,plans}/*` gardent l'ancien vocabulaire : ce sont des **archives de
  conception datées**, volontairement non réécrites. Idem sections v7/v8 de CLAUDE.md, annotées
  d'un bandeau de renvoi vers v27.

**Vérifié** : checker sur données réelles (`Breast_2` → OK, `Bladder_Urine_02_128` → KO, sample
inexistant → KO) ; migration sur copie + idempotence 3 ouvertures ; `update-column` persiste ;
export TSV (header `Small Fragments` position 27, `Breast_2` → OK) ; `get_small_fragments_unified()`
1362 lignes × 13 colonnes ; les 11 tables intactes. Backup
`samples_status.backup-pre-small-fragments-20260821_144253.duckdb`, checkpoint
`checkpoint-pre-small-fragments` (sur `91e4d53`).

Liens : [[project_schema_v7_short_read]] et [[project_schema_v8_short_read_metrics]] (les objets
renommés), [[project_cohort_export]] (gotcha onglet fantôme).
