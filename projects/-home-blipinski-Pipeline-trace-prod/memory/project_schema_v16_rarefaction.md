---
name: project-schema-v16-rarefaction
description: "Schema v16 — table rarefaction AUTONOME (pseudo-samples {sample}_{niveau}, PK nom du dossier, pas de FK), lot BAM raréfiés 20M/10M/5M/2M/1M, calque dilution, CLI check-rarefaction {CGFL|HCL} / update-column-rarefaction / export-rarefaction (probs DB-only)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8e8e90f0-c16f-492a-a113-8f8efe10ea84
---

# Schema v16 — rarefaction (juillet 2026)

Nouvelle table `rarefaction` (68 colonnes), **lot autonome de pseudo-samples** `{sample}_{niveau}` (niveaux VAF `20M`/`10M`/`5M`/`2M`/`1M`, **pas de 15M**). Trace les métriques QC des BAM raréfiés (sous-échantillonnés à N reads puis repassés dans le pipeline standard).

**Why:** Boris veut suivre les métriques des BAM raréfiés « de la même manière que small_fragments » (= [[project-schema-v8-short-read-metrics]]), mais avec une granularité tidy (1 ligne par pseudo-sample) et une table dédiée exportée dans l'onglet gsheet `Rarefaction`.

**Structure source (NFS/S3) :** `processed/MRD/RetD/liquid/{CGFL,HCL}_rarefaction/{sample}_{niveau}/` — **2 dossiers miroirs par labo** (comme `{labo}_short_read`), pseudo-samples autonomes, **préfixe fichier `.merged`** (BAM raréfié repassé dans le pipeline). 50 pseudo-samples au 07/07/2026 (25 CGFL + 25 HCL, ~10 bases × 5 niveaux), **early-stage + hétérogène**.

**How to apply (calque [[project-schema-v9-dilution]], pas [[project-schema-v8-short-read-metrics]]) :**
- Table **autonome, PK = `sample_name` = nom du dossier** (`Breast_45_10M`), **AUCUNE FK** vers `samples` (les pseudo-samples n'y existent pas). Colonnes identité stockées : `sample_base` (`Breast_45`), `rarefaction_level` (`10M`), `labo`. Parsing via `_split_level` (regex `^(.*)_(\d+M)$`).
- 68 col = 4 identité + 2 statuts + 14 métriques + **47 probs** (16 epic + 31 Loyfer quotées, suffixe `_rarefaction`) + `updated_at`.
- **PROD** (`prod_status_rarefaction`) = OK si `BAM`+`BETA`+`QC` non vides (`_CORE_DIRS`, 1 listing S3), **pas les 10 dossiers dilution** (Fragmentomics/ichorCNA absents sur la majorité). `bootstrap_props` dérivé du même listing.
- `RarefactionChecker(labo)` (`lib/checkers_rarefaction.py`) hérite `BaseChecker` **sans override** (préfixe `.merged`), calque `DilutionChecker`. Importe `_read_props` de `checkers_dilution`. Diffère de dilution : `mvaf_v13`+`frag_score_v2_sc` en plus, **pas** de `mvaf_v12`/`cnv_score`/`bam_status`/`frag_status_sc`.
- `upsert_rarefaction` dédié (`ON CONFLICT (sample_name)`, update partiel), `get_rarefaction_all` (ORDER BY labo, sample_base, rarefaction_level).
- CLI : `check-rarefaction {CGFL|HCL} [-s][-j]` (**arg labo** car 2 dossiers, source = `_s3_ls_dirs(rarefaction_dir)`), `update-column-rarefaction {column} {CGFL|HCL}` (dispatch `RAREFACTION_COLUMN_CHECKERS` : status/metric/probs_epic/probs_loyfer, préserve sur erreur S3), `export-rarefaction` (onglet `Rarefaction`, **20 col, probs EXCLUES** comme dilution).
- `PathConfig.rarefaction_dir` = `_BASE_PROCESSED / liquid / f"{labo}_rarefaction"` (calque `short_read_dir`). `compact()` `table_names` MAJ (sinon `clean-database` perd la table).

**Gotcha data :** `raima_score.V1.3.tsv` **absent sur 50/50** → `mvaf_v13` toujours `NA` (colonne créée quand même, ré-activable). `ichorCNA/` + `Fragmentomics/` sporadiques (Colon_8/Colon_27/Prostate_45…) → ichorcna/Mode1/Mode2/frag_score souvent NULL, se remplissent au fil du pipeline (UPSERT idempotent).

**Sémantique du niveau (07/07/2026) :** une fois le pipeline de raréfaction Bam2Beta **terminé**, `nb_reads_total_rarefaction` == le niveau (1M→1,00 / 5M→5,00 / 20M→20,00). ⚠ **Piège** : si `check-rarefaction` est lancé pendant que Bam2Beta tourne encore, les dossiers contiennent des sorties **intermédiaires** → totaux incohérents (ex 1M→5M vu le matin, corrigé le soir). trace-prod extrait fidèlement le fichier `QC/Samtools/{s}.nb_reads_total.tsv` (vérifié au read près) — donc si les nombres semblent faux, c'est la donnée upstream en cours, pas l'extraction. Remède : `DELETE FROM rarefaction` + re-`check-rarefaction CGFL/HCL` une fois le pipeline fini.

**Vérifié (07/07/2026) :** `Breast_45_10M` PROD OK / mvaf_v1 0,8018 / v1.3 NA ; `Colon_8_10M` ichor 0,3457 + Mode1 144,82 ; `Prostate_45_1M` PROD KO. Export 20 col, probs absentes. Checkpoint `checkpoint-pre-rarefaction` (sur b9abd0c). Commits `9680010`→`e080252`. Spec/plan : `docs/superpowers/{specs,plans}/2026-07-07-rarefaction-tracking*.md`.

Liens : [[project-schema-v9-dilution]] (pattern calqué), [[project-schema-v8-short-read-metrics]] (« small_fragments »), [[project_columns_index]].
