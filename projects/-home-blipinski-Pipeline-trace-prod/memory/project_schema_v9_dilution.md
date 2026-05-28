---
name: project-schema-v9-dilution
description: "Schema v9 — table dilution autonome (480 samples, lot expérience Dilution), CLI check/update-column/export-dilution"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3ab5f7a4-d9f6-47e3-89eb-d5f0bc4b58be
---

**Schema v9** (28 mai 2026) — nouvelle table `dilution`, **lot autonome de 480 samples** sans lien avec la base existante.

Différence clé vs [[project-schema-v8-short-read-metrics]] : `short_read_metrics` est FK `sample_id → samples(id)` (réutilise les samples cliniques). `dilution` est **autonome** : PK = `sample_name`, **AUCUNE FK** — les 480 dilutions (`{Tumor}_{Healthy}_target_{niveau}`, niveaux VAF `0_1`/`0_5`/`1_0`/`5_0`) n'existent pas dans `samples`.

- Source : `s3://aima-bam-data/processed/MRD/RetD/liquid/dilution/{sample}/` (préfixe fichier `.merged` = pipeline INITIAL → `DilutionChecker` réutilise les méthodes `BaseChecker` **SANS override**, contrairement à `ShortReadChecker` qui override pour le préfixe minLen75).
- 64 colonnes : 2 statuts + 13 métriques DECIMAL + 16 probs epic v1 + 31 probs Loyfer (suffixe `_dilution`, Loyfer **quotées** car commencent par un chiffre).
- 2 statuts dérivés d'**1 seul listing S3/sample** (`check_statuses`) : `bam_status_dilution` (OK si `BAM/{s}.merged.bam` size>0 = données générées), `prod_status_dilution` (OK si les **10 dossiers** BAM/BETA/BETA_28M/CNV/EXTRACT_FULL_28M/Fragmentomics/IV/QC/REPORT/ichorCNA non-vides = pipeline complet).

**Gotchas** :
- `upsert_dilution` est **dédié** (`ON CONFLICT (sample_name)`) — ne PEUT PAS réutiliser `_upsert_table` qui est hardcodé sur `ON CONFLICT (sample_id)`.
- CLI **sans args type/labo** (lot unique) : `check-dilution`, `update-column-dilution {column}`, `export-dilution`. Source des 480 = helper `_s3_ls_dirs()` (listing `PRE name/`).
- `update-column-dilution` : dispatch `DILUTION_COLUMN_CHECKERS` → 2 statuts / 13 métriques / `probs_epic` / `probs_loyfer` (groupes ; 47 colonnes probs individuelles en CLI = absurde). Réutilise `upsert_dilution` avec dict partiel → isolation par colonne.
- **Probs stockées en DB mais EXCLUES de l'export** (`export-dilution` = **19 colonnes** : statuts + métriques + 3 dérivées du `sample_name` parsées à l'export : `Sample initial` (tumeur), `Healthy` (Healthy_N), `Target` (`_`→`,`)). Décision Boris : export probs prévu plus tard.
- Classe `DilutionChecker` (`lib/checkers_dilution.py`), 3 sous-méthodes `check_statuses`/`extract_metrics`/`extract_probs`. `_read_props(file, expected)` = réplique paramétrée de `_read_props_v1` short_read.

**État prod (28 mai 2026)** : 480 lignes, `bam=OK` 480/480, `prod=OK` 230 / `prod=KO` 250. Onglet 'Dilution' de la gsheet trace-prod (`1gm_vB7...`) peuplé.

Specs/plan : `docs/superpowers/{specs,plans}/2026-05-28-dilution-tracking*.md`.
