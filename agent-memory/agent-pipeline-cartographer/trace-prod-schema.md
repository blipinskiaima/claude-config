---
name: trace-prod-schema
description: Schéma DuckDB trace-prod (courant v24, 2026-08), 11 tables, cohorte liquide (1359), conventions matrice/statut/clés, mapping cascade lecture A/B/C/D
metadata:
  type: project
---

## Schéma courant (v24, 2026-08-12) — 11 tables (schéma évolue vite, ~1 migration/semaine)

**samples** (racine, 1506 lignes = 1359 liquid + 147 solid ; liquid = 846 CGFL + 513 HCL) : `id` INTEGER PK auto (`nextval`), `sample_name`/`sample_type`/`labo` NOT NULL VARCHAR, `UNIQUE(sample_name, sample_type, labo)`. ⚠️ `sample_name` seul N'EST PAS unique : 75 sample_name liquides existent en CGFL ET HCL (ex. `Colon_1`, `Lung_9`) — `labo` obligatoire pour identifier un échantillon sans ambiguïté.

**qc** (v23, ajoutée 2026-08-11, 1332/1359 liquides) : cascade de comptage reads publiée par Bam2Beta — 12 comptages INTEGER + 11 % DECIMAL(5,2). Colonnes : `reads_total/mapped/alignments/primary/primary_mapped/frag/28m/unmapped/secondary/supplementary/off_chr1_22/mapq_lt20` (+ `_pct` pour tous sauf `reads_total`). Mappe 1:1 les strates A(non alignées)/B(secondaires)/C(supplémentaires)/D(primaires mappées) documentées dans la mémoire projet Bam2Beta `read-counting-cascade.md` : `reads_total`=A+B+C+D, `reads_alignments`=A+C+D (cramino col4), `reads_primary`=A+D (cramino col6, = "molécules générées"), `reads_primary_mapped`=D, `reads_unmapped`=A (idxstats), `reads_secondary`=B, `reads_supplementary`=C. Vérifié arithmétiquement A+B+C+D=reads_total sur 1324/1324 lignes non-NULL. `reads_28m`/`reads_mapq_lt20` (Preprocess_28M, filtre chr1-22+MAPQ≥20) sont **NULL à 100 % (0/1359)** — jamais publiés par le pipeline, colonnes présentes dans le schéma mais mortes. 27 liquides sans ligne `qc` du tout (tous `Bladder_Urine_02_1xx`, CGFL) ; 8 de plus avec ligne mais sans idxstats (`unmapped`/`primary_mapped`/`mapped`/`off_chr1_22` NULL, aussi tous `Bladder_Urine_02_*`).

**qc_metrics** (1:1 samples via FK, jamais NULL sur `nb_reads_*`) : `nb_reads_total`/`nb_reads_aligned` = mêmes métriques que `qc.reads_total`/`reads_primary` mais en **millions** (DECIMAL(12,2), 2 déc.) — sourcées du `metadata.json` Bam2Beta, cohérence à 1e4 près vérifiée sur 1332/1332 lignes communes. `nb_reads_aligned` = A+D, inclut les reads NON alignées (nom trompeur dans metadata.json, cf mémoire Bam2Beta). Aussi : `mvaf_v1/v2/v1_10m/v1_20m/v1_ft092/v1_ft095`, `score_cnv`, `n50`/`n75`/`n50_n75_ratio` (v21-22), `pct_mass_removed` (v24, toujours en écho avec `qc` : 35 NULL au lieu de 27, mêmes 8 samples sans idxstats).

**metadata** (1:1 samples, absente pour 320/1359 liquides — surtout `Lung_*`/`Bladder_*` non encore importés du GSheet) : `class` porte un statut **mixte**, pas un champ binaire propre : `'Healthy'` (329, 100 % cohérent avec préfixe `Healthy_*`), type de cancer anatomique (`Lung`/`Colon`/`Bladder`/`Breast`/`Prostate`/`Rectum`/`Pancreas`/`Rectosigmoïde`/`Sigmoïde`/`Ovary`/`Oropharynx`/`Lymphoma`), nom de cohorte/essai clinique (`NUCLEAR` 16, `TNE` 10 — probable cancer, aucun champ clinique clair pour confirmer : `stage`/`grade`/`active_cancer` NULL, `gene1_mutated`='Non réalisé'/'WT'), ou catégorie technique (`'Test dilution Twist_0.1pc'` 15, `'Plasma_RB'` 2). `category` = sous-classification VAF clinique (`Cat 1..4`), indépendante du statut cancer/healthy.

**dilution** (v9, 2026-05-28, PK `sample_name` seule, **aucune FK vers samples**, 480 lignes) et **rarefaction** (v16, 2026-07-07, PK composite `(sample_name, labo)`, **aucune FK**, 2962 lignes = pseudo-échantillons `{sample}_{niveau}`) : univers séparés et autonomes — NE PAS les compter dans la cohorte liquide/solide (1506). Corrige mémoire précédente (mai 2026, schéma v8) qui affirmait leur absence — elles ont été ajoutées juste après.

**retd_suivis**, **bam_metadata**, **probs**, **short_read_metrics** : inchangées pour l'essentiel depuis la fiche précédente (statuts fichiers, run/pod5/barcode, probabilités déconvolution, subsampling 75-200bp).

## Convention matrice liquide (plasma / urine / autre) — piège connu confirmé

`metadata.class`/`category` NE distingue PAS plasma/urine (même `class='Bladder'` pour un `Bladder_Urine_*` et un `Bladder_Blood_*`, vérifié). La matrice se lit dans le NOM : `Bladder_Urine_{01,02}_NNN` (116) vs `Bladder_Blood_{01,02}_NNN` (58, dont un `_02_156bis`) — couverture exhaustive, 116+58=174 = tout le préfixe `Bladder_`, zéro fuite hors préfixe. Le reste (1158/1359) = plasma par défaut, non marqué explicitement. Contrôles synthétiques `Twist_*` (22, préfixe explicite, dilutions/réplicats compris). 5 échantillons liquides inclassables sans aucune métadonnée ni préfixe reconnu : `Ma_SAB_12-1958_Run_{1,2,merged}`, `26BM03032`, `ANG-CA-11081963` (à l'inverse `26BM01841` a `class`='Bladder or mesothelioma', classé mais matrice non confirmée par le nom).

⚠️ **Angle mort EQC** : 12 contrôles qualité externes CGFL (`Breast_17/32/47/49/50/52`, `Prostate_2/3/23/37/38/39`, cf mémoire Bam2Beta `n50-ratio-qc.md`) sont enregistrés dans trace-prod EXACTEMENT comme des patients cancer normaux (`class`='Breast'/'Prostate', `category` clinique VAF renseignée) — **aucun champ trace-prod ne les marque comme EQC**, confirmé par lecture directe. Liste à maintenir en dehors de la base. Seul `Breast_17` a une variante `_rebasecalled_V5.0.0_trimmed`.

Aucune lignée cellulaire trouvée dans la cohorte liquide (recherche exhaustive `'cell'`/`'lign'` sur tous les champs texte `metadata` — seuls faux positifs : "cellules tumorales/claires/suspectes" en texte clinique libre français).

## Rebasecalled / réplicats = lignes distinctes, même patient

`_rebasecalled_V{4.2.0,4.3.0,5.0.0,5.0.0_trimmed,5.2.0,6.0.0}` (208 liquides, 6 variantes de version) et `_rep1`/`_rep2`/`_rep_2` (33 liquides, dont certains avec suffixe `_OK` additionnel type `Colon_17_rep1_OK`) sont des `sample_id` DISTINCTS de l'original, mais héritent du même `metadata.patient_id`/`class` (propagation confirmée sur `Breast_17` vs `Breast_17_rebasecalled_V5.0.0_trimmed`, id 14 vs 4740, même patient_id/class/gene1_vaf). Comptent comme échantillons distincts en base (QC/`qc`/`qc_metrics` propres à chaque run), mais PAS comme patients/spécimens cliniques distincts.

## Clé primaire réelle

`samples.id` (surrogate, séquence) est LA clé référencée par FK 1:1 dans qc/qc_metrics/retd_suivis/metadata/probs/bam_metadata/short_read_metrics (`sample_id INTEGER PRIMARY KEY REFERENCES samples(id)`). La clé logique/métier est `UNIQUE(sample_name, sample_type, labo)` — jamais `sample_name` seul (cf doublons inter-labo ci-dessus).

## Où stocker les VAF sources

- `metadata.gene1_vaf` : VAF tumorale mesurée (VARCHAR libre, ex : 28.4%, 73.0%) — source GSheet
- `qc_metrics.mvaf_v1/v2` (+ v10m/v20m/ft092/ft095) : mVAF calculée par raima après Bam2Beta
- Pour les healthys : `metadata.class = 'Healthy'`, `gene1_vaf` = NULL

## Key files

- `/home/blipinski/Pipeline/trace-prod/lib/duckdb.py` — DDL complet, SCHEMA_VERSION = 24 (table `_schema_version` = changelog exact avec dates)
- `/home/blipinski/Pipeline/trace-prod/README.md` — documentation schéma
- `/home/blipinski/Pipeline/trace-prod/database/check_samples.py` — CLI principal
- `/home/blipinski/Pipeline/trace-prod/lib/checkers.py` — BaseChecker, LiquidChecker, get_prod_status()
- `/home/blipinski/Pipeline/trace-prod/database/samples_status.duckdb` — DB courante (135 Mo). Multiples backups horodatés dans le même dossier (`*.backup-pre-*.duckdb`), ne pas confondre avec la DB active.
