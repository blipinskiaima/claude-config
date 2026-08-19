---
name: project-schema-v25-qc-28m-cpg
description: "Schema v25 — qc.reads_with_cpg + reads_with_cpg_pct (nouvelles colonnes), alimentation PONCTUELLE des 4 champs 28M/CpG depuis un TSV rétrospectif (backfill S3), pas de checker permanent"
metadata: 
  node_type: memory
  type: project
  originSessionId: 944cb86a-c04e-4105-8a23-04b1ab426260
  modified: 2026-08-19T08:43:08.487Z
---

# Schema v25 (août 2026) — reads_with_cpg + alimentation ponctuelle 28M/CpG (table `qc`)

Contexte : la table `qc` (schema v23, distincte de `qc_metrics`) trace la cascade de comptage
des reads (12 comptages bruts + % sur `reads_total`, calculés par `QCChecker` depuis 4 TSV déjà
publiés par Bam2Beta — voir lib/checkers_qc.py). Deux comptages y sont codés en dur à `NULL`
depuis l'origine : `reads_28m` et `reads_mapq_lt20`, car « le pipeline ne publie pas le comptage
de Preprocess_28M ».

Boris a reconstruit ce comptage manquant **rétrospectivement**, hors pipeline : outillage ad-hoc
dans `/scratch/boris/nb_read_28M/` (`one_sample.sh` + `run_backfill.sh`/`run_backfill2.sh`) qui
relit les sorties déjà publiées `EXTRACT_FULL_28M/{id}.merged.all.chr{1..22}.extract_full_table.bgzf`
(read_id uniques) + `.modkit_extract_full.log` (skipped) sur tout RetD/{liquid,solid}/{CGFL,HCL}
— validé contre `samtools view -c -q20 -F3844` (écart -0,0022 % sur Lung_9). Sortie :
`/scratch/boris/nb_read_28M/nb_reads_28M.tsv` (1506 lignes, colonnes `reads_28m` ET
`reads_with_cpg` = read_id uniques SANS les skipped).

**Why:** Boris voulait profiter de ce backfill pour peupler les 2 champs existants
(`reads_28m`/`reads_28m_pct`, vides depuis v23) ET tracer `reads_with_cpg` (jusque-là absent),
mais **sans construire de mécanisme permanent** — le pipeline Bam2Beta ne publie pas encore ces
comptages nativement, donc un vrai checker S3 n'a pas de source stable à lire aujourd'hui.

**How to apply:**
- 2 colonnes ajoutées à `qc` : `reads_with_cpg` INTEGER + `reads_with_cpg_pct` DECIMAL(5,2),
  juste après `reads_28m`/`reads_28m_pct` (DDL + `QC_COLUMNS`, lib/duckdb.py). Migration
  idempotente v25 — ⚠ variables nommées `qc_table_cols`/`qc_table_col_names` pour NE PAS
  collisionner avec `qc_cols`/`qc_col_names` déjà utilisées pour `qc_metrics` (nom de table
  proche, migrations v21/v22/v24) dans `_init_schema()`.
- **`COLUMN_CHECKERS` n'a nécessité AUCUN edit** : `{c: ('qc', None, 'qc', None) for c in QC_COLUMNS}`
  dérive automatiquement de `QC_COLUMNS` (database/check_samples.py:763). Pareil pour
  `get_qc_unified()` (lib/duckdb.py) qui fait `", ".join(f"q.{c}" for c in QC_COLUMNS)` — ajouter
  une colonne à `QC_COLUMNS` suffit à la propager partout. Seul edit gsheet : `_QC_READ_HEADERS`
  (lib/gsheets.py) +`("CpG %", "reads_with_cpg_pct")` après `"28M %"` — le brut n'est pas exporté
  (pattern « resserré » existant : seul `Total` sort en brut, tout le reste en %).
- **Alimentation = script jetable, PAS `check-qc`/`update-column`** (demande explicite de Boris :
  pas de procédure automatisée pour l'instant) : `/scratch/boris/nb_read_28M/populate_qc.py`
  (hors repo git, non versionné). Lit le TSV, jointure `samples.sample_name = TSV.sample_id AND
  samples.labo = TSV.labo AND samples.sample_type = TSV.type` (⚠ le `sample_id` du TSV est en
  réalité le sample_name texte, pas le PK entier), calcule les % via `qc.reads_total` déjà en
  base (= nb reads BAM d'origine, même formule que `_pct()` dans checkers_qc.py : `round(100 *
  valeur / reads_total, 2)`), puis `upsert_qc(sample_id, {...})`.
- **`checkers_qc.py`/`QCChecker.check_sample()` volontairement PAS touché** — continue de
  renvoyer `reads_28m: None` et n'inclut pas `reads_with_cpg`. `check-qc`/`update-column` restent
  inertes sur ces 2 champs. Câblage réel = tâche future, quand Bam2Beta publiera nativement ces
  comptages (source S3 stable à identifier alors).
- **Scope réel alimenté : 1332/1506 lignes du TSV** (819 CGFL + 513 HCL) — exactement les
  samples liquid qui avaient déjà une ligne `qc` avec `reads_total` connu (= déjà passés par
  `check-qc` avant ce jour). Exclus, volontairement, sans écriture : **147 solid CGFL** (la table
  `qc` est structurellement liquid-only, `check-qc` restreint `sample_type` à liquid en dur dans
  le CLI) et **27 liquid CGFL `Bladder_Urine_02_*`** (jamais passés par `check-qc` → pas de
  `reads_total` → % incalculable). Backup DB pris avant écriture :
  `database/samples_status.backup-pre-reads-with-cpg-20260819_083902.duckdb`.
- Export : `export-qc` (commande déjà existante, inchangée) → 1362 lignes (tous les liquid
  CGFL+HCL en DB, LEFT JOIN — pas seulement les 1332 alimentés), 16 colonnes (15 + `CpG %`). Les
  30 lignes sans ligne `qc` du tout (dont les 27 ci-dessus) restent `NA` sur toute la cascade —
  comportement standard préexistant de `get_qc_unified()`, pas introduit par ce travail.

Checkpoint git : tag `checkpoint-pre-reads-with-cpg`.
