---
name: schema-v34-qc-status
description: "Schema v34 — exis_qc_status/reason + themelio_qc_status/reason dans retd_suivis (liquid), lus dans REPORT/metadata.json de Bam2Beta ; pattern preserve ; + chemin rapide sequencing_time.tsv"
metadata:
  type: project
---

# Schema v34 — statuts QC Exis / Thémélio (2026-09-08)

4 colonnes `VARCHAR` **sans default (NULL = jamais evalue)** dans `retd_suivis`, liquid uniquement :
`exis_qc_status`, `exis_qc_reason`, `themelio_qc_status`, `themelio_qc_reason`. Valeurs SUCCESS /
WARNING / FAILED + raison anglaise (`Limited number of molecules`, `Non-plasma-like sample`…) ou NULL.
**Hors `STATUS_COLUMNS`** (sinon `_parse_status` ecraserait tout en KO).

**Why:** le statut est calcule **cote Bam2Beta** (process `QC_status`, arbre de decision du Google Doc
QC onglet Synthese) et publie dans `REPORT/metadata.json` (33 champs) ; trace-prod ne fait que lire.
Les 1366 JSON liquid ont ete generes par le module retro `--RETRO_REPORT` avant l integration.

**How to apply:**
- Lecture : `BaseChecker.read_qc_status()` (lib/checkers.py, apres `check_multi_run`) — `_s3_read_text`
  puis repli local, `json.loads`. Renvoie **None** (= preserve, rien n est ecrit) si JSON absent, illisible
  ou **anterieur a la feature** (pas de clef `exis_qc_status` : 157 anciens JSON a 10 champs existaient).
  Statut `NA` (metrique manquante) -> None -> NULL en base, la raison `Missing metric: …` est gardee.
- Check de routine : `LiquidChecker.check_sample()` n ajoute les 4 clefs FR (`Exis QC`, `Exis QC raison`,
  `Thémélio QC`, `Thémélio QC raison`) **que si** le JSON est lisible — une clef absente est ignoree par
  `_prepare_data`, une clef a None ecrit NULL (voulu : le JSON fait foi), une clef a 'KO' ecraserait.
- `update-column <n importe laquelle des 4 clefs> liquid {labo}` -> `_update_qc_status()` (type
  discriminant `'qc_status'` dans `COLUMN_CHECKERS`) : une lecture, **un UPDATE des 4 colonnes**, skip
  logge « inchangé » si None. Backfill 2026-09-08 par Boris : CGFL 449 S/S, 223 W/W, 105 W/F, 77 F/F,
  6 NULL ; HCL 475 / 31 / 6, 1 NULL — identique au bilan des JSON.
- Export : en-tetes dans `_LIQUID_QC` juste apres `mVAF v1.5` (Exis) et `Thémélio` (Thémélio) ;
  `HEADERS_ALL` est la liste complete, rien d existant ne saute. Gsheet verifiee : positions 12-13 et
  15-16, distributions identiques a la base, NULL rendu `NA`.
- ⚠ Le commit `19923c1` (renommage nb_lignes_total) s intitule « migration v34 » mais n a bumpe ni le code
  ni `_schema_version` : le v34 reel est celui-ci (base : `34 | Statuts QC Exis/Themelio…`).
- Rollback : tag `pre-qc-status-columns` (19923c1) + `samples_status.backup-pre-qc-status-v34-*.duckdb`.

## Chemin rapide `sequencing_time` (meme journee, commite dans 19923c1)

`scan_read_start_time(sample_dir, sample, allow_scan=True)` lit d abord `QC/Samtools/{ID}.sequencing_time.tsv`
(2 lignes, publie par Bam2Beta `Read_Start_Time` depuis le meme awk que read_start_time.tsv, mktime + offset),
sinon balayage 2,5 Go. `check_sample()` l appelle avec `allow_scan=False` et n ajoute `Temps Séquençage` /
`Multi Run` que si la valeur existe (preserve des 1362 valeurs backfillees). Valide sur Twist_10_6_rep_3
(TSV simule sur S3 -> `check` lit 69h07m) et Prostate_31 (valeur preservee). Le calcul lexicographique
historique donne les memes extremes que mktime sur les 28 runs traversant un changement d heure.

Voir `qc-status-exis-themelio` (memoire Bam2Beta) pour l arbre et le module retro.
