---
name: project-schema-v28-rarefaction-horaire
description: "Schema v28 — table rarefaction_horaire AUTONOME (65 col, PK composite dès l'origine), pseudo-samples {base}_{12h|24h|48h}, 1453 lignes. Calque rarefaction MAIS probs epic = moyenne bootstrap et Loyfer NON bootstrapable. Export vers une gsheet dédiée (onglets mVAF + Prop)"
metadata:
  node_type: memory
  type: project
---

# Schema v28 — rarefaction_horaire (août 2026)

Table **autonome** (aucune FK vers `samples`), calque de [[project-schema-v16-rarefaction]] :
pseudo-samples `{base}_{12h|24h|48h}`, **3 points de temps seulement**, 2 dossiers miroirs
`s3://…/liquid/{CGFL,HCL}_rarefaction_horaire/`. Trace les métriques des BAM horaires
(sortie séquenceur à 12/24/48 h) pour les comparer aux valeurs du run complet.

**65 colonnes** = 4 identité (`sample_name`, `sample_base`, `time_point`, `labo`)
+ 3 statuts + 10 métriques + 47 probs (suffixe **`_horaire`**) + `updated_at`.
**PK composite `(sample_name, labo)` dès le DDL** — pas de migration de rattrapage à la v17 :
**93 collisions inter-labo réelles** constatées avant de coder (`Colon_1_12h` existe des 2 côtés).

## Ce qui diffère de `rarefaction` (et pourquoi)

- **`bam_status_horaire` en plus** (demande Boris) — mais il vaut **OK sur 1453/1453** : chaque
  dossier contient son `.merged.bam`. Le vrai discriminant « pipeline passé ou non » est
  **`prod_status_horaire` (610 OK / 843 KO)**. Dit avant de coder, pas découvert après.
- **`mvaf_v15` en plus** ; **pas** de `mvaf_v13` / `ichorcna` / `frag_mode*_sc` / `frag_score_v2_sc` :
  `raima_score.V1.3.tsv` absent **0/1453**, et les dossiers `ichorCNA/`, `Fragmentomics/`, `IV/`,
  `REPORT/`, `MITO/`, `THEMELIO/`, `TOO/` n'existent pas ici. 7 sous-dossiers seulement :
  `BAM, BETA, BETA_28M, BOOTSTRAP, CNV, EXTRACT_FULL_28M, QC`.
- ⚠⚠ **Les proportions Loyfer NE SONT PAS bootstrapables.** Vérifié sur fichier réel :
  `BOOTSTRAP/{s}.merged.all.bootstrap_v1.props.tsv` = 201 lignes × **16 colonnes epic**
  (200 réplicats) ; `EXTRACT_FULL_28M/{s}.merged.all.props_loyfer.tsv` = 2 lignes × 31 colonnes
  (**valeur unique**). Il n'existe aucun fichier bootstrap Loyfer. Donc : **epic = moyenne des
  200 réplicats** (calque `extract_bootstrap_means`), **Loyfer = la valeur unique**. Une demande
  formulée « les proportions Loyfer et epic bootstrapées » n'est réalisable qu'à moitié — le
  dire au lieu de laisser croire que les 47 sont bootstrapées.
- **Correction assumée du `0,00` fantôme** : `format_millions(None)` renvoie `'0,00'`, d'où le
  piège connu de `nb_reads_total_rarefaction` (export `0,00` au lieu de `NA`). Ici les 3
  comptages de reads gardent le **brut comme témoin de présence** :
  `nb_total if nb_total_raw else "NA"`. Un vrai zéro (`raw == '0'`, truthy) reste `0,00`.
  `rarefaction` n'a **pas** été corrigée (hors scope).

## Gotchas

- ⚠ **Le dossier contient un `LOG/`** (logs `{base}.rarefaction_horaire.log`) en plus des
  pseudo-samples. Sans filtre, `_s3_ls_dirs` crée une ligne `sample_name='LOG'` avec
  `time_point` NULL. Filtre : `[s for s in dirs if split_time_point(s)[1]]` (589→588, 866→865).
- ⚠ **`update-column-rarefaction-horaire <col> <labo> -s <pseudo>` sur un pseudo-sample absent
  de ce labo CRÉE une ligne fantôme** (c'est un `UPSERT`, pas un `UPDATE … WHERE`). Hérité tel
  quel de `update-column-rarefaction`. Sans `-s` aucun risque : le listing S3 ne renvoie que les
  vrais dossiers du labo. Pire que le gotcha « N mis à jour sans rien toucher » de
  [[project-schema-v20-mito]] — ici ça écrit.
- ⚠ **Relecture gsheet après `USER_ENTERED`** : la feuille interprète `19,60` comme un nombre et
  le réaffiche `19,6` ; `3,4900` devient `3,49`. Une comparaison de **chaînes** annonçait
  **1392 faux écarts sur 1453**. Normaliser (virgule→point puis `float`) avant de conclure —
  même piège que [[project-schema-v26-mvaf-v15]] et [[cohort-export]].
- **Les probs partent en gsheet avec le POINT décimal**, pas la virgule : c'est ce que fait
  `export_probs` pour les onglets Prop existants. Les autres exports du projet convertissent en
  virgule — ne pas « harmoniser » sans y penser.
- **Le pipeline produit encore** : 605 PROD OK au listing S3 de 13:00, **610** à la fin du check
  lancé à 13:17 (5 nouveaux, 0 perdu). Relance idempotente, cibler
  `WHERE prod_status_horaire='KO'`.

## Câblage (6 fichiers)

`lib/duckdb.py` (DDL, `ALL_TABLES`, 5 constantes `*_HORAIRE*`, `upsert_rarefaction_horaire`,
`get_rarefaction_horaire_all` / `_mvaf` / `_prop`, `compact()` table_names, bump v28) ·
`lib/utils.py` (`PathConfig.rarefaction_horaire_dir`) ·
**`lib/checkers_rarefaction_horaire.py`** (nouveau : `RarefactionHoraireChecker`,
`split_time_point`, `_bootstrap_means`) · `database/check_samples.py` (4 commandes +
`RAREFACTION_HORAIRE_COLUMN_CHECKERS`) · `lib/gsheets.py` (2 constantes de headers +
2 exports + helper `_export_rarefaction_horaire`) · `database/gsheets_config.json` (2 entrées).

CLI : `check-rarefaction-horaire {CGFL|HCL}` · `update-column-rarefaction-horaire {col} {labo}`
(15 clés) · `export-rarefaction-horaire-mvaf` · `export-rarefaction-horaire-prop` (les deux
acceptent `-o fichier.tsv`).

## Export — gsheet DÉDIÉE

`1Cnzzu-W6-vIoVJoGBu9cv6KqZSAuD8m09zC3DeqKszE` (« Trace Rarefaction horaire »), **distincte** de
la gsheet trace-prod et de la famille `exis_*`. Onglet **`Prop`** avec une majuscule (pas `prop`).

| Onglet | Colonnes | Contenu |
|---|---|---|
| `mVAF` | 15 | `ID`/`Labo`/`XH` + 6 valeurs **initiales du sample parent** + les 6 mêmes en horaire |
| `Prop` | 50 | `ID`/`Labo`/`XH` + 47 probs (16 epic bootstrapées + 31 Loyfer) |

Les valeurs initiales viennent d'une jointure `(sample_base, labo)` → `samples` → `qc_metrics`
(nb reads, depth, coverage) + `retd_suivis` (mvaf_v14/v15). **507/507 bases matchent** un
`sample_name` liquid du bon labo → aucune colonne « initiale » à NA.

## Chiffres (31/08/2026)

**1453 lignes** = 588 CGFL (207/207/174 par point de temps) + 865 HCL (300/300/265), **507 bases**.
Backfill 65 min à `-j 4`, **0 erreur**. BAM 1453 OK · PROD 610 OK / 843 KO ·
métriques renseignées 611 · mVAF v1.4/v1.5 et probs epic 607 · probs Loyfer 610.
Les écarts entre ces compteurs sont tous des dossiers **en cours de production**, pas des bugs.

**Vérifié** : migration idempotente ×3 sur copie, `compact()` préserve table + PK composite ;
collision `Colon_1_12h` CGFL≠HCL → 2 lignes ; moyenne bootstrap identique à un `awk` indépendant
(`blood_0 = 0.9409205`, n=200) ; contrôle croisé base↔fichier source sur 3 samples, **0 écart** ;
relecture gsheet↔base **0 écart sur 21 795 cellules (mVAF) et 72 650 (Prop)**.
Backup `samples_status.backup-pre-rarefaction-horaire-20260831_131018.duckdb`,
checkpoint `checkpoint-pre-rarefaction-horaire` (sur `63418c0`).

Liens : [[project-schema-v16-rarefaction]] (calque principal),
[[project-schema-v9-dilution]] (le `bam_status` + `prod_status` vient de là),
[[project-probs-bootstrap-mode]] (le calcul de moyenne), [[project_columns_index]].
