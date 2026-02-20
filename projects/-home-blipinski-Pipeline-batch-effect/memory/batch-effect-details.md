# Batch Effect — Détails techniques

## Colonnes de batch_matrix.tsv (21 colonnes originales)

centre, sample, cancer_type, nb_bam, taille_gb, device_type, device_serial, flowcell, run_date, gpu, minknow, basecall_model, basecall_version, basecaller, methyl_detected, methyl_tags, aligner, sort_order, genome_ref, n_chroms, batch_group

## Colonnes ajoutées dans batch_matrix_enriched.tsv (+10 = 31 total)

kit, extraction_protocol, library_yield, library_quantity, volume_loaded, quantity_loaded, barcode_number, dorado_version_gsheet, samples_per_run, reads_per_flowcell

Source : DuckDB trace-prod (tables samples + metadata + bam_metadata), jointure sur (centre, sample)

## Normalisations appliquées

### device_type (depuis champ Appareil)
- `P2 Solo` ou serial `PBE*` → P2_Solo
- `P2i` ou serial `PAW*` → P2i
- `PromethION` ou serial `PBI*` → PromethION
- `GridION` ou serial `FAU*` → GridION
- Serial `PBA/PBC/PBG` → Flongle
- Reste (dont `PAY*`) → unknown

### Valeurs uniques par champ
- **gpu** : A100_80GB (188 HCL), A800_80GB (372 CGFL), Quadro_GV100 (147 CGFL)
- **basecaller** : Dorado (645), Guppy (62 CGFL-only)
- **basecall_version** : 5.0.0 (520), 4.3.0 (153), 4.1.0 (24), 3.3 (10)
- **flowcell** : R10.4.1 (697), R9.4.1 (10)
- **minknow** : v6.5.14 (492), v6.2.6 (153), non_disponible (62)
- **methyl_tags** : MM_ML_MN_mv (527), aucun (120), MM_ML_MN (60)
- **aligner** : minimap2_integrated (645), minimap2_v2.28 (38), minimap2_v2.27 (24)
- **genome_ref** : hg38 (707) — identique partout (GCA_000001405.15_GRCh38_no_alt_analysis_set, 195 contigs)
- **sort_order** : coordinate (554), unknown (153)

## Modèles de modification (modbase)
- hac@v5.0.0 → 5mCG_5hmCG@v3 (déduit, 28 Guppy le confirment)
- hac@v4.3.0 → 5mCG_5hmCG@v2 (déduit, même génération que v4.1.0)
- hac@v4.1.0 → 5mCG_5hmCG@v2 (tracé dans BAM Guppy)
- hac@v3.3 → 5mCG_5hmCG@v0 (tracé, 1 sample avec 5mCG@v0.1 seulement)

## Versions Guppy (ont_basecall_client)
- v7.9.8 : 38 samples (10 R9.4.1 + 28 R10.4.1)
- v7.6.7 : 24 samples (R10.4.1, hac@v4.1.0)
