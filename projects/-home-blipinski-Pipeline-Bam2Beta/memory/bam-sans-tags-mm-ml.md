---
name: bam-sans-tags-mm-ml
description: "Erreur `semi_join x$chrom <logical>` dans Raima_score_mVAF = BAM d'entrée sans tags MM/ML (réaligné minimap2 sans -y) — cas IRCCS RC24 du 2026-09-28"
metadata:
  node_type: memory
  type: project
  originSessionId: eafbe6cc-dcd0-4e1b-90d7-e22c63c4b4c1
  modified: 2026-09-28T17:21:25.417Z
---

Signature : `Raima_score_mVAF` exit 1 avec `Error in semi_join(): Can't join x$chrom with y$chr … x$chrom is a <logical>`
(+ `Raima_process_loyfer` exit 1). Ce n'est PAS un bug raima : les 22 `extract_full_table.bgzf` font 195 octets
(en-tête seul) → `fread` type les colonnes vides en logical. Logs modkit : `MM-tag-missing` sur 100 % des reads.

Cas du 2026-09-28 : client IRCCS (`bccf3cf4-…`), 6 samples RC24_* (flowcell PBI70633, run 20260923_1345),
1 BAM `*.aligned.bam` par sample, sans .bai. En-tête : aucun `@RG`, aucun `@PG` dorado/minknow, seulement
`minimap2 -ax map-ont -t 16 GRCh38_no_alt.fna -` puis `samtools sort` (chemin `.../demux/.../bam_pass/barcodeXX/`).
0/2000 reads avec MM/ML/RG/st sur les 6 BAM. Le même client avait envoyé pt107 (mai) réaligné avec
`minimap2 -y -R @RG…` → MM/ML conservés.

**Why:** ré-alignement côté client via FASTQ sans `-y` (ou FASTQ sans tags) → perte de toute info dorado
(MM/ML/MN, st:Z, RG, qs, mv). Conséquences en chaîne : dorado_model/run_id NULL dans trace-platform,
`read_start_time.tsv` vide, `sequencing_time` KO, mVAF/Loyfer/TOO/THEMELIO/metadata.json absents ;
CNV/FRAG/IV/MITO passent (n'utilisent pas la méthylation).

**How to apply:** face à cette erreur, vérifier d'abord `samtools view -H` (présence @RG / @PG dorado) et les
tags MM/ML des premiers reads avant de soupçonner le code. Piste non implémentée : contrôle MM/ML dans
`Check_Input` pour un échec précoce explicite ([[check-input-qc]]).
