---
name: reference-infra-pod5-bam-export
description: "Référence infra trace-prod — extraction BAM/barcode, système POD5 storage (6 colonnes), structure S3 AWS/SCW, split dorado model, config gsheet, BETA_28M, ordre des colonnes export, IchorCNA, date_done. Détail extrait de MEMORY.md (index trop long)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7b24b20e-1621-43d4-95c5-a9f36fdc4499
---

# Infra trace-prod — POD5 / BAM / export

Détail extrait de `MEMORY.md` (index devenu trop long). Recoupe partiellement `~/Pipeline/trace-prod/CLAUDE.md` — ici on garde ce qui **n'y est pas** ou qui a une valeur de diagnostic.

## BAM Metadata Extraction
- `BAMExtractor._extract_with_samtools()` : timeout 10s → 30s, 1 retry sur timeout.
- Extrait par `check` : dorado_model, dorado_model_version, run_id, barcode, taille_bam. **PAS** par `check` : reads_per_flowcell, samples_per_run (agrégats, via `update-column`).
- Barcode extrait du **nom de fichier BAM** (regex `barcode\d+`), PAS du header RG.
- **Rebasecalled** (et certains non-rebasecalled, ex `Colon_NN_rep` merged BAM) n'ont de barcode ni dans le nom ni dans RG → barcode reste NA.
  - Workaround : logs Pod2Bam `/mnt/aima-bam-data/processed/Pod2Bam/RetD/{run}/{version}/align_trimmed/{sample}.log` (sous-dossier **align_trimmed**, pas `align` ; version ex `V0.9.6_V5.0.0` ; le `{run}` embarque le préfixe run_id, ex `..._962143e5_pod5_rep1`).
  - Ligne `command: dorado aligner ... {run_id}_barcode{N}.bam` (log sans zero-pad, DB stocke `barcodeNN` zero-paddé).
  - **Aucun fallback automatisé** — récupération = UPDATE SQL manuel sur `bam_metadata.barcode`.
  - 36 barcodes rebasecalled récupérés ainsi (CGFL liquid, mars 2026) ; 8 Colon_17-20_rep1/rep2 en juin 2026 (barcode19/28/30/32, rep1+rep2 partagent le barcode par numéro de Colon). **82 anciens rebasecalled (V4.3.0/V4.2.0) n'ont pas de logs Pod2Bam → barcode NA définitif.**

## POD5 Storage System (bam_metadata)
- 6 colonnes mises à jour **ensemble** via `update-column stockage_pod5` : `stockage_pod5`, `sample_type_pod5`, `taille_pod5`, `pod5_adresse`, `nb_pod5`, `pod5_completude`. Dispatch `COLUMN_CHECKERS` type='storage' → `_update_pod5_storage()`.
- `check` ne lance **plus** `_update_pod5_storage()` — uniquement via `update-column`.
- `taille_pod5` via `aws s3 ls --summarize` (entier GiB, cache `_s3_size_gib()`). `taille_bam` idem `--profile=scw` sur le merged BAM.
- `pod5_completude` = `round(nb_pod5 / (max_index + 1) × 100)` — détecte les POD5 manquants. **> 100% = multi-run mixing** (indices de flowcells différentes dans le même dossier).
- `bam_completude` = `nb_bam / (max_index + 1) × 100` ; cas spécial : 1 BAM = 100%. Fallback via `{sample}_bam_list.txt` quand plus de BAM sur S3 (cas Bladder_Blood).
- "Nb POD5" / "Nb BAM" = colonnes **internes**, retirées de l'export. "Complétude BAM"/"Complétude POD5" exportées.
- ⚠ Rebasecalled → laisser NULL, ne pas propager. Voir [[feedback-rebasecalled-pod5]].

### Structure S3
- Bucket `aima-pod-data`, 2 providers : AWS (profil `aws`) `s3://aima-pod-data/CGFL/liquid/{run}/` ; SCW (profil `scw`) `s3://aima-pod-data/data/CGFL/liquid/{run}/` (même chemin + préfixe `data/`).
- Formats CGFL : `pod5_pass/{sample}/`, `pod5/` flat, `pod5_repN/`, racine `.pod5`. Matching : `run_id[:8]` → hash S3, fallback `sample_name` dans `pod5_pass/`.
- HCL : dossiers `{sample_name}/` avec POD5 directement dedans. Raw NANO : `/mnt/aima-bam-data/data/HCL/raw/NANO{NN}_{YY}_N{X}/no_sample_id/{run_id}/`.
- Dedup (`_dedup_cgfl_folders()`) : `=OK` > original > `=moche`.

### Vérification POD5 (mars 2026)
- CGFL liquid : 462 détectés / 112 non (104 Lung_Alc + 8 Colon rep sans adresse POD5).
- AWS vs SCW : tailles identiques 148/148 ; nombre diff de 1 (fichier metadata extra côté AWS).
- Concordance gsheet CGFL : 285/293 ; 8 non (Colon_17-20_rep sans adresse DB).
- Contiguïté : AWS 89/93 runs à 100%, SCW 33/36. 3 runs ~74% (mars 2025, anciens), 1 à 98,6%.
- Comptes CGFL liquid (mars 2026) : 628 en DB ; 285 AWS / 148 AWS+SCW / 37 SCW / 104 NULL. 93 adresses AWS uniques, 36 SCW.

### Dorado Model Split
- `dorado_model` + `dorado_model_version` — split sur `@` dans `BAMExtractor._parse_rg_line`.
- ⚠ gsheet "dorado version" = version **logiciel** (ex 7.6.7) ; DB = version **modèle** (ex v4.3.0). Ne pas confondre.

## BETA_28M Check (avril 2026, BREAKING)
- `check_beta_28m()` exige **44 fichiers réels** (size > 0) **+ ≤ 1 ghost** (size = 0). Avant : tolérait 44 ou 45 sans distinguer → faux-positif « 44 total = 43 réels + 1 ghost ».
- Les 2 flags `--combine-mods` + `--combine-strands` dans le log chr22 restent obligatoires.
- `_has_single_ghost()` supprimée → comptage direct via `_s3_ls_lines()`.
- Audit : 1 faux-positif = `Healthy_26_rebasecalled_V4.3.0` (HCL), `chr18.bedMethyl.gz` manquant.

## Export GSheet — ordre & logique
- 6 colonnes rarefaction individuelles (20M..1M) remplacées par une seule "Rarefaction" **calculée à l'export** (display-only, jamais en DB). `_RAREFACTION_THRESHOLDS = {20M:20, 15M:15, 10M:10, 5M:5, 2M:2, 1M:1}`, implémenté **en double** dans `GSheetsService._consolidated_rarefaction()` **et** `DuckDBService._consolidated_rarefaction()` (toute modif = les 2).
  - Logique : OK si tous les seuils ≤ `nb_reads_total` sont OK ; KO si l'un ne l'est pas ; OK si aucun seuil applicable (< 1M reads).
  - ⚠ Retirée de `_LIQUID_QC` au nettoyage de juin 2026 (subsiste en solid).
- "QC" supprimée des 2 exports. "BEDMETH EPICS" juste après "BAM". "Dorado Model" avant "Version Dorado Model".

## IchorCNA (mars 2026)
- `retd_suivis.ichorcna_score` VARCHAR, **PAS** dans STATUS_COLUMNS (sinon `_parse_status()` écrase tout en KO — voir [[feedback_status_columns]]).
- Valeur = tumor fraction virgule (ex `0,01271`) ou "KO". Source `{sample_dir}/ichorCNA/{sample}.params.txt` ligne 2 col 2 (tab). Lecture S3 via `_s3_read_text()`, fallback NFS.

## Date Done Bug Fix (update-column)
- Le checker renvoie DD-MM-YYYY, la colonne DuckDB DATE attend YYYY-MM-DD. `_parse_date()` n'existait que dans `upsert_sample()`, pas dans le chemin `update-column` → conversion ajoutée dans `update_column()` (`check_samples.py`) pour `column == 'date_done'`.

## GSheet Config
- `database/gsheets_config.json`. metadata_CGFL : `1v1KUuCoMQV4Qk5jfbHLxhrUK6q_FETLiH8TuCQMdNxA`, worksheet "VAF". metadata_HCL : `1XcWPn3_PT1atR-i5DmOM1t0ldgb5_PnxhQUwNUxWpQg`, worksheet "VAF". Spreadsheet trace-prod : `1gm_vB7vTzAq38dgkJFNpgA3Cy_XRlUqunMgoBvKnh6M`.
- Fetch : `fetch-gsheet metadata_CGFL` / `metadata_HCL`.
- ⚠ `APIError 503` gspread transient récurrent → casse les chaînes `&&` en tmux. Pas de helper retry à ce jour (todo optionnel).

## Scripts utilitaires (dev/)
- `dev/pod5_verification_gen.py` → `pod5_verification.tsv` (croisé POD5 AWS/SCW CGFL, filtre rebasecalled). Voir [[pod5_verification script]].
- `dev/hcl_verification_gen.py` → `hcl_verification.tsv` (raw NANO ↔ S3 POD5/BAM). Voir [[project_hcl_verification]].
- `dev/hcl_correspondance_rapports.tsv` — 66 runs NANO Dir / Run Number / Adresse Rapport. `rapport/` — rapports HTML Dorado copiés depuis SCW.

## CLI Defaults
- Jobs par défaut : **4** (`check`, `update-column`, `probs`) — revert du 12→4, 12 saturait S3.
- `update-column --sample` accepte **plusieurs** `-s` ; `probs --sample` est **mono-sample** (click garde le dernier) → boucler.
- `_update_pod5_storage()` / `_update_bam_sizes()` supportent `sample_filter`.
