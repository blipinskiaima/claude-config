# Schéma trace-prod (samples_status.duckdb)

Snapshot : 2026-06-08. **1381 samples** dans `samples`.

**9 tables**, **268 colonnes** (255 noms distincts ; `sample_id`, `updated_at`, `sample_name` partagés entre tables).

Liste complète : `trace_prod_columns.txt` (racine Feature/).

## `_schema_version` — 11 lignes, 3 colonnes

| Colonne | Type |
|---|---|
| `version` | INTEGER |
| `applied_at` | TIMESTAMP |
| `description` | VARCHAR |

## `bam_metadata` — 1381 lignes, 18 colonnes

| Colonne | Type |
|---|---|
| `sample_id` | INTEGER |
| `dorado_model` | VARCHAR |
| `dorado_model_version` | VARCHAR |
| `run_id` | VARCHAR |
| `barcode` | VARCHAR |
| `reads_per_flowcell` | DECIMAL(10,2) |
| `samples_per_run` | INTEGER |
| `stockage_pod5` | VARCHAR |
| `sample_type_pod5` | VARCHAR |
| `taille_pod5` | DECIMAL(10,2) |
| `pod5_adresse` | VARCHAR |
| `nb_pod5` | INTEGER |
| `pod5_completude` | INTEGER |
| `taille_bam` | DECIMAL(10,2) |
| `nb_bam` | INTEGER |
| `bam_completude` | INTEGER |
| `bam_horaire` | VARCHAR |
| `updated_at` | TIMESTAMP |

## `dilution` — 480 lignes, 64 colonnes

| Colonne | Type |
|---|---|
| `sample_name` | VARCHAR |
| `bam_status_dilution` | VARCHAR |
| `prod_status_dilution` | VARCHAR |
| `nb_reads_total_dilution` | DECIMAL(12,2) |
| `nb_reads_aligned_dilution` | DECIMAL(12,2) |
| `nb_reads_epic_dilution` | DECIMAL(12,2) |
| `ratio_percent_dilution` | DECIMAL(5,2) |
| `depth_dilution` | DECIMAL(10,2) |
| `coverage_percent_dilution` | DECIMAL(5,2) |
| `mvaf_v1_dilution` | DECIMAL(10,4) |
| `mvaf_v2_dilution` | DECIMAL(10,4) |
| `mvaf_v12_dilution` | DECIMAL(10,4) |
| `ichorcna_dilution` | DECIMAL(10,4) |
| `cnv_score_dilution` | DECIMAL(10,4) |
| `frag_mode1_dilution` | DECIMAL(10,4) |
| `frag_mode2_dilution` | DECIMAL(10,4) |
| `blood_0_dilution` | VARCHAR |
| `breast_0_dilution` | VARCHAR |
| `breast_1_dilution` | VARCHAR |
| `colon_0_dilution` | VARCHAR |
| `colon_1_dilution` | VARCHAR |
| `kidney_1_dilution` | VARCHAR |
| `liver_0_dilution` | VARCHAR |
| `liver_1_dilution` | VARCHAR |
| `lung_0_dilution` | VARCHAR |
| `lung_1_dilution` | VARCHAR |
| `muscle_0_dilution` | VARCHAR |
| `ovary_0_dilution` | VARCHAR |
| `ovary_1_dilution` | VARCHAR |
| `prostate_0_dilution` | VARCHAR |
| `prostate_1_dilution` | VARCHAR |
| `testis_0_dilution` | VARCHAR |
| `1_Fibroblast_Heart_dilution` | VARCHAR |
| `2_Neuron_dilution` | VARCHAR |
| `3_Myeloid_Granulocyte_dilution` | VARCHAR |
| `4_Epithelium_Gastric_dilution` | VARCHAR |
| `5_Epithelium_UpperAirway_dilution` | VARCHAR |
| `6_Tcell_EffectorMemory_dilution` | VARCHAR |
| `7_Epithelium_Colon_Intestinal_dilution` | VARCHAR |
| `8_Glia_Oligodendrocyte_dilution` | VARCHAR |
| `9_Hepatocyte_dilution` | VARCHAR |
| `10_Cardiomyocyte_dilution` | VARCHAR |
| `11_Pancreas_Endocrine_dilution` | VARCHAR |
| `12_Epithelium_Fallopian_dilution` | VARCHAR |
| `13_Breast_Epithelial_dilution` | VARCHAR |
| `14_Epithelium_Bladder_dilution` | VARCHAR |
| `15_Pancreas_Acinar_dilution` | VARCHAR |
| `16_Epithelium_Kidney_dilution` | VARCHAR |
| `17_Endothelium_Hepatic_Pulmonary_dilution` | VARCHAR |
| `18_Epithelium_Thyroid_dilution` | VARCHAR |
| `19_Erythroid_Progenitor_dilution` | VARCHAR |
| `20_Pancreas_Duct_dilution` | VARCHAR |
| `21_Epithelium_Lung_Bronchus_dilution` | VARCHAR |
| `22_Epithelium_Endometrium_dilution` | VARCHAR |
| `23_Epithelium_Prostate_dilution` | VARCHAR |
| `24_Epithelium_Lung_Alveolar_dilution` | VARCHAR |
| `25_Bcell_Memory_dilution` | VARCHAR |
| `26_Endothelium_Kidney_dilution` | VARCHAR |
| `27_Muscle_Smooth_dilution` | VARCHAR |
| `28_Endothelium_Vascular_dilution` | VARCHAR |
| `29_Epithelium_Gallbladder_dilution` | VARCHAR |
| `30_Myeloid_Macrophage_Lung_dilution` | VARCHAR |
| `31_Muscle_Skeletal_dilution` | VARCHAR |
| `updated_at` | TIMESTAMP |

## `metadata` — 950 lignes, 51 colonnes

| Colonne | Type |
|---|---|
| `sample_id` | INTEGER |
| `sample_name_orig` | VARCHAR |
| `class` | VARCHAR |
| `patient_id` | VARCHAR |
| `age` | VARCHAR |
| `sex` | VARCHAR |
| `date_prelevement` | VARCHAR |
| `library_yield` | VARCHAR |
| `library_quantity` | VARCHAR |
| `volume_loaded` | VARCHAR |
| `quantity_loaded` | VARCHAR |
| `run_number` | VARCHAR |
| `date_of_run` | VARCHAR |
| `kit` | VARCHAR |
| `index_id` | VARCHAR |
| `barcode_number` | VARCHAR |
| `extraction_protocol` | VARCHAR |
| `dorado_version` | VARCHAR |
| `gene1_mutated` | VARCHAR |
| `gene1_freq` | VARCHAR |
| `gene1_mutation_status` | VARCHAR |
| `gene1_vaf` | VARCHAR |
| `active_cancer` | VARCHAR |
| `metastatic` | VARCHAR |
| `category` | VARCHAR |
| `pfs_before_progression` | VARCHAR |
| `progression` | VARCHAR |
| `comments` | VARCHAR |
| `gene1_comment` | VARCHAR |
| `gene2_mutated` | VARCHAR |
| `gene2_freq` | VARCHAR |
| `gene2_comment` | VARCHAR |
| `gene3_mutated` | VARCHAR |
| `gene3_freq` | VARCHAR |
| `gene3_comment` | VARCHAR |
| `gene4_mutated` | VARCHAR |
| `gene4_freq` | VARCHAR |
| `gene4_comment` | VARCHAR |
| `gene1_detailed_variant` | VARCHAR |
| `active_cancer_clinical` | VARCHAR |
| `stage` | VARCHAR |
| `grade` | VARCHAR |
| `speedvac` | VARCHAR |
| `cohort` | VARCHAR |
| `commentaire_global` | VARCHAR |
| `gene5_mutated` | VARCHAR |
| `gene5_freq` | VARCHAR |
| `gene5_comment` | VARCHAR |
| `vaf_category` | VARCHAR |
| `vaf_threshold` | VARCHAR |
| `updated_at` | TIMESTAMP |

## `probs` — 1356 lignes, 49 colonnes

| Colonne | Type |
|---|---|
| `sample_id` | INTEGER |
| `blood_0` | VARCHAR |
| `breast_0` | VARCHAR |
| `breast_1` | VARCHAR |
| `colon_0` | VARCHAR |
| `colon_1` | VARCHAR |
| `kidney_1` | VARCHAR |
| `liver_0` | VARCHAR |
| `liver_1` | VARCHAR |
| `lung_0` | VARCHAR |
| `lung_1` | VARCHAR |
| `muscle_0` | VARCHAR |
| `ovary_0` | VARCHAR |
| `ovary_1` | VARCHAR |
| `prostate_0` | VARCHAR |
| `prostate_1` | VARCHAR |
| `testis_0` | VARCHAR |
| `1_Fibroblast_Heart` | VARCHAR |
| `2_Neuron` | VARCHAR |
| `3_Myeloid_Granulocyte` | VARCHAR |
| `4_Epithelium_Gastric` | VARCHAR |
| `5_Epithelium_UpperAirway` | VARCHAR |
| `6_Tcell_EffectorMemory` | VARCHAR |
| `7_Epithelium_Colon_Intestinal` | VARCHAR |
| `8_Glia_Oligodendrocyte` | VARCHAR |
| `9_Hepatocyte` | VARCHAR |
| `10_Cardiomyocyte` | VARCHAR |
| `11_Pancreas_Endocrine` | VARCHAR |
| `12_Epithelium_Fallopian` | VARCHAR |
| `13_Breast_Epithelial` | VARCHAR |
| `14_Epithelium_Bladder` | VARCHAR |
| `15_Pancreas_Acinar` | VARCHAR |
| `16_Epithelium_Kidney` | VARCHAR |
| `17_Endothelium_Hepatic_Pulmonary` | VARCHAR |
| `18_Epithelium_Thyroid` | VARCHAR |
| `19_Erythroid_Progenitor` | VARCHAR |
| `20_Pancreas_Duct` | VARCHAR |
| `21_Epithelium_Lung_Bronchus` | VARCHAR |
| `22_Epithelium_Endometrium` | VARCHAR |
| `23_Epithelium_Prostate` | VARCHAR |
| `24_Epithelium_Lung_Alveolar` | VARCHAR |
| `25_Bcell_Memory` | VARCHAR |
| `26_Endothelium_Kidney` | VARCHAR |
| `27_Muscle_Smooth` | VARCHAR |
| `28_Endothelium_Vascular` | VARCHAR |
| `29_Epithelium_Gallbladder` | VARCHAR |
| `30_Myeloid_Macrophage_Lung` | VARCHAR |
| `31_Muscle_Skeletal` | VARCHAR |
| `updated_at` | TIMESTAMP |

## `qc_metrics` — 1381 lignes, 15 colonnes

| Colonne | Type |
|---|---|
| `sample_id` | INTEGER |
| `nb_reads_total` | DECIMAL(12,2) |
| `nb_reads_aligned` | DECIMAL(12,2) |
| `nb_reads_epic` | DECIMAL(12,2) |
| `ratio_percent` | DECIMAL(5,2) |
| `depth` | DECIMAL(10,2) |
| `coverage_percent` | DECIMAL(5,2) |
| `mvaf_v1` | DECIMAL(10,4) |
| `mvaf_v2` | DECIMAL(10,4) |
| `mvaf_v1_10m` | DECIMAL(10,4) |
| `mvaf_v1_20m` | DECIMAL(10,4) |
| `mvaf_v1_ft092` | DECIMAL(10,4) |
| `mvaf_v1_ft095` | DECIMAL(10,4) |
| `score_cnv` | DECIMAL(10,3) |
| `updated_at` | TIMESTAMP |

## `retd_suivis` — 1381 lignes, 33 colonnes

| Colonne | Type |
|---|---|
| `sample_id` | INTEGER |
| `bam_status` | VARCHAR |
| `bedmethyl_all_status` | VARCHAR |
| `extract_full_all_status` | VARCHAR |
| `props_epic_status` | VARCHAR |
| `props_loyfer_status` | VARCHAR |
| `bedmeth_epics_status` | VARCHAR |
| `threshold_20m` | VARCHAR |
| `threshold_15m` | VARCHAR |
| `threshold_10m` | VARCHAR |
| `threshold_5m` | VARCHAR |
| `threshold_2m` | VARCHAR |
| `threshold_1m` | VARCHAR |
| `frag_status` | VARCHAR |
| `frag_mode1` | VARCHAR |
| `frag_mode2` | VARCHAR |
| `cnv_status` | VARCHAR |
| `ichorcna_score` | VARCHAR |
| `mvaf_v12` | VARCHAR |
| `qc_status` | VARCHAR |
| `ancestry` | VARCHAR |
| `sex_proba` | VARCHAR |
| `sex_predicted` | VARCHAR |
| `read_start_time` | VARCHAR |
| `short_read` | VARCHAR |
| `date_done` | DATE |
| `pipeline_version` | VARCHAR |
| `updated_at` | TIMESTAMP |
| `frag_status_sc` | VARCHAR |
| `frag_mode1_sc` | VARCHAR |
| `frag_mode2_sc` | VARCHAR |
| `mvaf_v13` | VARCHAR |
| `frag_score_v2_sc` | VARCHAR |

## `samples` — 1381 lignes, 7 colonnes

| Colonne | Type |
|---|---|
| `id` | INTEGER |
| `sample_name` | VARCHAR |
| `sample_type` | VARCHAR |
| `labo` | VARCHAR |
| `prod_status` | VARCHAR |
| `created_at` | TIMESTAMP |
| `updated_at` | TIMESTAMP |

## `short_read_metrics` — 1199 lignes, 28 colonnes

| Colonne | Type |
|---|---|
| `sample_id` | INTEGER |
| `nb_reads_total_short_read` | DECIMAL(12,2) |
| `nb_reads_aligned_short_read` | DECIMAL(12,2) |
| `nb_reads_epic_short_read` | DECIMAL(12,2) |
| `ratio_percent_short_read` | DECIMAL(5,2) |
| `depth_short_read` | DECIMAL(10,2) |
| `coverage_percent_short_read` | DECIMAL(5,2) |
| `mvaf_v1_short_read` | DECIMAL(10,4) |
| `mvaf_v2_short_read` | DECIMAL(10,4) |
| `mvaf_v12_short_read` | DECIMAL(10,4) |
| `ichorcna_short_read` | DECIMAL(10,4) |
| `blood_0_short_read` | VARCHAR |
| `breast_0_short_read` | VARCHAR |
| `breast_1_short_read` | VARCHAR |
| `colon_0_short_read` | VARCHAR |
| `colon_1_short_read` | VARCHAR |
| `kidney_1_short_read` | VARCHAR |
| `liver_0_short_read` | VARCHAR |
| `liver_1_short_read` | VARCHAR |
| `lung_0_short_read` | VARCHAR |
| `lung_1_short_read` | VARCHAR |
| `muscle_0_short_read` | VARCHAR |
| `ovary_0_short_read` | VARCHAR |
| `ovary_1_short_read` | VARCHAR |
| `prostate_0_short_read` | VARCHAR |
| `prostate_1_short_read` | VARCHAR |
| `testis_0_short_read` | VARCHAR |
| `updated_at` | TIMESTAMP |
