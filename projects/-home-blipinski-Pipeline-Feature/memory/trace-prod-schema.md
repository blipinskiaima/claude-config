# Schéma trace-prod (samples_status.duckdb)

Snapshot : 2026-05-07. **1309 samples** total dans `samples`.


## `samples` — 1309 lignes, 7 colonnes

| Colonne | Type | Couverture | Description / valeurs |
|---|---|---|---|
| `id` | INTEGER | 1309/1309 | min=2 max=5378 avg=1975.684 |
| `sample_name` | VARCHAR | 1309/1309 | `Colon_13` (2), `Colon_50` (2), `Colon_2` (2), `Pancreas_7` (2), `Colon_32` (2) |
| `sample_type` | VARCHAR | 1309/1309 | `liquid` (1165), `solid` (144) |
| `labo` | VARCHAR | 1309/1309 | `CGFL` (860), `HCL` (449) |
| `prod_status` | VARCHAR | 1309/1309 | `OK` (1295), `KO` (14) |
| `created_at` | TIMESTAMP | 1309/1309 | min=2026-01-19 15:37:11 max=2026-05-06 06:36:43 |
| `updated_at` | TIMESTAMP | 1309/1309 | min=2026-03-04 13:04:37 max=2026-05-06 07:49:43 |

## `qc_metrics` — 1309 lignes, 15 colonnes

| Colonne | Type | Couverture | Description / valeurs |
|---|---|---|---|
| `sample_id` | INTEGER | 1309/1309 | min=2 max=5378 avg=1975.684 |
| `nb_reads_total` | DECIMAL(12,2) | 1309/1309 | min=0.00 max=158.57 avg=39.560 |
| `nb_reads_aligned` | DECIMAL(12,2) | 1309/1309 | min=0.00 max=133.54 avg=33.132 |
| `nb_reads_epic` | DECIMAL(12,2) | 1165/1309 | min=0.00 max=7.40 avg=1.973 |
| `ratio_percent` | DECIMAL(5,2) | 1165/1309 | min=0.00 max=11.00 avg=5.571 |
| `depth` | DECIMAL(10,2) | 1303/1309 | min=0.00 max=17.62 avg=2.561 |
| `coverage_percent` | DECIMAL(5,2) | 1303/1309 | min=0.00 max=94.00 avg=71.186 |
| `mvaf_v1` | DECIMAL(10,4) | 1299/1309 | min=0.0000 max=100.0000 avg=6.505 |
| `mvaf_v2` | DECIMAL(10,4) | 1299/1309 | min=0.0000 max=86.6300 avg=7.819 |
| `mvaf_v1_ft092` | DECIMAL(10,4) | 488/1309 | min=0.0000 max=84.1700 avg=2.333 |
| `mvaf_v1_ft095` | DECIMAL(10,4) | 488/1309 | min=0.0000 max=85.6200 avg=1.887 |
| `score_cnv` | DECIMAL(10,3) | 1295/1309 | min=0.000 max=87.950 avg=6.778 |
| `updated_at` | TIMESTAMP | 1309/1309 | min=2026-03-04 13:04:37 max=2026-05-06 07:49:43 |
| `mvaf_v1_10m` | DECIMAL(10,4) | 1035/1309 | min=0.0000 max=87.5200 avg=2.670 |
| `mvaf_v1_20m` | DECIMAL(10,4) | 751/1309 | min=0.0000 max=87.0300 avg=2.480 |

## `retd_suivis` — 1309 lignes, 23 colonnes

| Colonne | Type | Couverture | Description / valeurs |
|---|---|---|---|
| `sample_id` | INTEGER | 1309/1309 | min=2 max=5378 avg=1975.684 |
| `bam_status` | VARCHAR | 1309/1309 | `OK` (1303), `KO` (6) |
| `bedmethyl_all_status` | VARCHAR | 1308/1309 | `OK` (1302), `KO` (6) |
| `extract_full_all_status` | VARCHAR | 1309/1309 | `OK` (1303), `KO` (6) |
| `props_epic_status` | VARCHAR | 1309/1309 | `OK` (1299), `KO` (10) |
| `props_loyfer_status` | VARCHAR | 1309/1309 | `OK` (1303), `KO` (6) |
| `bedmeth_epics_status` | VARCHAR | 1309/1309 | `OK` (1165), `KO` (144) |
| `threshold_20m` | VARCHAR | 1309/1309 | `OK` (897), `KO` (412) |
| `threshold_15m` | VARCHAR | 1309/1309 | `OK` (968), `KO` (341) |
| `threshold_10m` | VARCHAR | 1309/1309 | `OK` (1035), `KO` (274) |
| `threshold_5m` | VARCHAR | 1309/1309 | `OK` (1091), `KO` (218) |
| `threshold_2m` | VARCHAR | 1309/1309 | `OK` (1124), `KO` (185) |
| `threshold_1m` | VARCHAR | 1309/1309 | `OK` (1139), `KO` (170) |
| `frag_status` | VARCHAR | 1309/1309 | `OK` (1165), `KO` (144) |
| `cnv_status` | VARCHAR | 1309/1309 | `OK` (1303), `KO` (6) |
| `ichorcna_score` | VARCHAR | 1303/1309 | `0` (18), `0,01078` (3), `0,01482` (3), `0,01014` (2), `0,01465` (2) |
| `mvaf_v12` | VARCHAR | 1299/1309 | `0` (679), `2,549` (11), `100` (10), `2,551` (6), `2,547` (4) |
| `qc_status` | VARCHAR | 1309/1309 | `OK` (1303), `KO` (6) |
| `date_done` | DATE | 1305/1309 | min=2025-09-26 max=2026-05-06 |
| `pipeline_version` | VARCHAR | 1305/1309 | `1.0.1` (323), `1.1.2` (206), `0.0.1` (182), `0.0.10` (121), `1.1.1` (118) |
| `updated_at` | TIMESTAMP | 1309/1309 | min=2026-03-04 13:04:37 max=2026-05-06 07:49:43 |
| `frag_mode1` | VARCHAR | 1263/1309 | `167,573302897716` (1), `167,059789794977` (1), `167,054690521612` (1), `166,908651029417` (1), `165,860542003704` (1) |
| `frag_mode2` | VARCHAR | 1263/1309 | `334,799670111699` (1), `328,352483650663` (1), `323,407959182065` (1), `314,791280728573` (1), `324,978257603243` (1) |

## `bam_metadata` — 1309 lignes, 18 colonnes

| Colonne | Type | Couverture | Description / valeurs |
|---|---|---|---|
| `sample_id` | INTEGER | 1309/1309 | min=2 max=5378 avg=1975.684 |
| `dorado_model` | VARCHAR | 1291/1309 | `dna_r10.4.1_e8.2_400bps_hac` (1281), `dna_r9.4.1_e8_hac` (10) |
| `dorado_model_version` | VARCHAR | 1291/1309 | `v5.0.0` (879), `v4.3.0` (225), `v5.2.0` (151), `v4.1.0` (24), `v3.3` (10) |
| `run_id` | VARCHAR | 1291/1309 | `499f0d1f-5533-4265-b278-f28cf0…` (15), `67466d85-b548-4067-87b0-dd9b21…` (13), `9fc13cc1-f3c6-4000-9ce2-877982…` (10), `0c3c2bf1-a1af-4edd-8b0e-50044b…` (10), `6bead390-73af-475a-ae9b-a76b95…` (10) |
| `barcode` | VARCHAR | 1208/1309 | `barcode22` (20), `barcode23` (19), `barcode27` (18), `barcode28` (18), `barcode18` (18) |
| `reads_per_flowcell` | DECIMAL(10,2) | 1291/1309 | min=0.23 max=587.12 avg=200.303 |
| `samples_per_run` | INTEGER | 1291/1309 | min=1 max=15 avg=5.240 |
| `stockage_pod5` | VARCHAR | 1076/1309 | `SCW` (841), `AWS` (207), `AWS+SCW` (28) |
| `sample_type_pod5` | VARCHAR | 1285/1309 | `multiplex` (978), `simplex` (307) |
| `taille_pod5` | DECIMAL(10,2) | 1182/1309 | min=0.00 max=1283.00 avg=224.762 |
| `pod5_adresse` | VARCHAR | 1067/1309 | `s3://aima-pod-data/data/CGFL/l…` (16), `s3://aima-pod-data/CGFL/liquid…` (16), `s3://aima-pod-data/data/CGFL/l…` (10), `s3://aima-pod-data/data/CGFL/l…` (8), `s3://aima-pod-data/data/CGFL/l…` (8) |
| `nb_pod5` | INTEGER | 1180/1309 | min=10 max=389 avg=109.037 |
| `pod5_completude` | INTEGER | 1182/1309 | min=35 max=194 avg=101.459 |
| `taille_bam` | DECIMAL(10,2) | 1293/1309 | min=0.00 max=107.00 avg=18.258 |
| `nb_bam` | INTEGER | 1292/1309 | min=1 max=31585 avg=419.615 |
| `bam_completude` | INTEGER | 1292/1309 | min=67 max=286700 avg=2456.233 |
| `updated_at` | TIMESTAMP | 1309/1309 | min=2026-03-04 13:04:37 max=2026-05-06 07:49:43 |
| `bam_horaire` | VARCHAR | 1309/1309 | `clean` (892), `OK` (232), `KO` (185) |

## `metadata` — 928 lignes, 50 colonnes

| Colonne | Type | Couverture | Description / valeurs |
|---|---|---|---|
| `sample_id` | INTEGER | 928/928 | min=2 max=5378 avg=2216.037 |
| `sample_name_orig` | VARCHAR | 928/928 | `H11-S` (5), `H4-S` (4), `H8-S` (3), `H23-S` (3), `H12-S` (3) |
| `class` | VARCHAR | 928/928 | `Healthy` (279), `Lung` (189), `Colon` (128), `Breast` (75), `Bladder` (71) |
| `patient_id` | VARCHAR | 588/928 | `Colon_5` (10), `Colon_3` (7), `Colon_20` (7), `Colon_19` (6), `Colon_21` (6) |
| `age` | VARCHAR | 847/928 | `65` (32), `66` (30), `60` (30), `61` (29), `62` (28) |
| `sex` | VARCHAR | 847/928 | `M` (451), `F` (396) |
| `date_prelevement` | VARCHAR | 757/928 | `24/11/2025` (17), `26/11/2025` (16), `01/12/2025` (16), `29/12/2025` (14), `22/12/2025` (13) |
| `library_yield` | VARCHAR | 479/928 | `1.35` (8), `1.62` (8), `1.41` (7), `7.21` (7), `9.61` (6) |
| `library_quantity` | VARCHAR | 479/928 | `24.3` (8), `20.25` (8), `21.15` (7), `108.15` (7), `28.95` (6) |
| `volume_loaded` | VARCHAR | 479/928 | `8` (219), `10` (67), `7` (35), `6` (35), `5` (21) |
| `quantity_loaded` | VARCHAR | 479/928 | `10.8` (8), `12.96` (8), `15.44` (6), `11.28` (6), `31.7` (6) |
| `run_number` | VARCHAR | 928/928 | `20250904_1028_P2S-01677-A_PBE7…` (16), `20250908_1347_P2I-00117-B_PBG4…` (16), `20251219_1518_2H_PBI50743_499f…` (15), `20260202_1135_1E_PBI54916_6746…` (13), `20260202_1136_1H_PBI51599_9fc1…` (10) |
| `date_of_run` | VARCHAR | 928/928 | `19/12/2025` (74), `27/04/2026` (56), `02/02/2026` (53), `01/12/2025` (45), `02/03/2026` (44) |
| `kit` | VARCHAR | 928/928 | `NBD114-96` (479), `SQK-NBD114.24` (266), `SQK-NBD114.90` (125), `SQK-NBD114.49` (2), `SQK-NBD114.50` (2) |
| `index_id` | VARCHAR | 928/928 | `D04` (10), `C04` (10), `F03` (10), `C03` (10), `G03` (10) |
| `barcode_number` | VARCHAR | 928/928 | `22` (17), `28` (16), `41` (16), `23` (16), `27` (15) |
| `extraction_protocol` | VARCHAR | 449/928 | `Maxwell` (385), `Qiagen` (55), `Maxwell® RSC ccfDNA LV Plasma …` (9) |
| `dorado_version` | VARCHAR | 928/928 | `7.9.8` (560), `7.6.7` (228), `7.11.2` (140) |
| `gene1_mutated` | VARCHAR | 756/928 | `Non réalisé` (183), `None` (139), `WT` (125), `TP53` (78), `APC` (39) |
| `gene1_freq` | VARCHAR | 280/928 | `9` (8), `1` (8), `3.6` (8), `1.7` (7), `0.7` (7) |
| `gene1_mutation_status` | VARCHAR | 529/928 | `Non-tumoral` (253), `Tumoral` (252), `Unknown` (23), `Tumoral or germline` (1) |
| `gene1_vaf` | VARCHAR | 252/928 | `1.0` (11), `3.6` (8), `9.0` (8), `1.3` (7), `0.7` (7) |
| `active_cancer` | VARCHAR | 591/928 | `Yes` (419), `No` (106), `Suspicion` (22), `imagerie suspecte` (20), `External quality control sampl…` (13) |
| `metastatic` | VARCHAR | 306/928 | `Yes` (238), `No` (56), `External quality control sampl…` (12) |
| `category` | VARCHAR | 531/928 | `Cat 1: Active/No panel detecti…` (256), `Cat 4: Tumoral VAF >5%` (122), `Cat 3: Tumoral VAF ≤5%` (105), `Cat 2: Post-op no detection` (48) |
| `pfs_before_progression` | VARCHAR | 38/928 | `440` (6), `339` (6), `357` (3), `493` (2), `406` (2) |
| `progression` | VARCHAR | 38/928 | `No` (26), `Yes` (12) |
| `comments` | VARCHAR | 140/928 | `pTa` (36), `pT1` (12), `pT2` (7), `T3N2b` (6), `Repasse pour avoir + de reads` (5) |
| `gene1_comment` | VARCHAR | 6/928 | `Digital PCR` (4), `Seen on raw data only` (2) |
| `gene2_mutated` | VARCHAR | 131/928 | `TP53` (53), `APC` (14), `PIK3CA` (10), `KRAS` (7), `CTNNB1` (7) |
| `gene2_freq` | VARCHAR | 131/928 | `10.9` (6), `5.1` (6), `23` (6), `1.10` (5), `6.2` (4) |
| `gene2_comment` | VARCHAR | 101/928 | `Tumoral` (42), `Unknown` (6), `p.(Ser37Phe)` (3), `p.(Arg248Trp)` (2), `p.(Gly719Ala)` (2) |
| `gene3_mutated` | VARCHAR | 58/928 | `TP53` (36), `KRAS` (5), `KEAP1` (3), `EGFR` (2), `ALK` (2) |
| `gene3_freq` | VARCHAR | 58/928 | `23.8` (6), `15.9` (6), `47` (3), `1.20` (2), `2.30` (2) |
| `gene3_comment` | VARCHAR | 45/928 | `Tumoral` (20), `p.(Gly379Cys)` (2), `p.(Asp281His)` (2), `p.(Arg1275Gln)` (2), `p.(Ser419Phe)` (1) |
| `gene4_mutated` | VARCHAR | 14/928 | `KEAP1` (3), `PIK3CA` (2), `PTEN` (1), `TP53` (1), `GNAS` (1) |
| `gene4_freq` | VARCHAR | 14/928 | `12.4` (2), `38.91` (1), `0.70` (1), `9.95` (1), `1.30` (1) |
| `gene4_comment` | VARCHAR | 12/928 | `Tumoral` (2), `p.(Gln402*)` (1), `p.Arg844Cys` (1), `p.(Phe220Ser)` (1), `p.(Gly417Val)` (1) |
| `gene5_mutated` | VARCHAR | 5/928 | `TP53` (2), `SMAD4` (2), `NRAS` (1) |
| `gene5_freq` | VARCHAR | 5/928 | `68.2` (2), `5.3` (1), `15.07` (1), `4.45` (1) |
| `gene5_comment` | VARCHAR | 3/928 | `p.(Arg167Gln)` (1), `p.Glu108*` (1), `p.Asn151fs` (1) |
| `vaf_category` | VARCHAR | 928/928 | `Non renseigne` (397), `Cat 1 (Active/No detection)` (256), `Cat 4 (VAF >5%)` (122), `Cat 3 (VAF ≤5%)` (105), `Cat 2 (Post-op)` (48) |
| `vaf_threshold` | VARCHAR | 928/928 | `Non renseigne` (397), `No VAF` (307), `VAF >=5%` (121), `VAF <5%` (103) |
| `updated_at` | TIMESTAMP | 928/928 | min=2026-05-05 15:56:59 max=2026-05-06 22:02:46 |
| `gene1_detailed_variant` | VARCHAR | 115/928 | `p.(Glu746_Ala750del)` (10), `p.(Leu858Arg)` (9), `p.(?)` (7), `p.(Gly12Asp)` (6), `p.(Ser752_Ile759del)` (4) |
| `active_cancer_clinical` | VARCHAR | 0/928 |  |
| `stage` | VARCHAR | 491/928 | `IV` (364), `III` (54), `I` (36), `II` (21), `NR` (13) |
| `commentaire_global` | VARCHAR | 61/928 | `preuve histo 1 mois après` (4), `sous surveillance annuelle` (3), `C'est une erreur, corrigée ce …` (3), `sous surveillance` (3), `radiothérapie sans preuve` (3) |
| `grade` | VARCHAR | 69/928 | `haut grade` (32), `bas grade` (28), `Pas de cancer` (5), `bénin` (4) |
| `speedvac` | VARCHAR | 872/928 | `No` (613), `Yes` (259) |

## `probs` — 1231 lignes, 49 colonnes

| Colonne | Type | Couverture | Description / valeurs |
|---|---|---|---|
| `sample_id` | INTEGER | 1231/1231 | min=2 max=5258 avg=1763.193 |
| `blood_0` | VARCHAR | 1156/1231 | `0` (53), `1` (2), `0.7257074` (1), `0.8675612` (1), `0.7222989` (1) |
| `breast_0` | VARCHAR | 1156/1231 | `0` (1132), `0.0539125` (1), `0.0209271` (1), `0.009045` (1), `0.0021704` (1) |
| `breast_1` | VARCHAR | 1156/1231 | `0` (779), `0.1431944` (1), `0.0570032` (1), `0.4083055` (1), `0.2182784` (1) |
| `colon_0` | VARCHAR | 1156/1231 | `0` (1020), `0.3904896` (1), `0.0765561` (1), `0.0257426` (1), `0.7459322` (1) |
| `colon_1` | VARCHAR | 1156/1231 | `0` (483), `1` (5), `0.0360146` (1), `0.8230325` (1), `0.0804521` (1) |
| `kidney_1` | VARCHAR | 1156/1231 | `0` (321), `0.0303304` (1), `0.0213523` (1), `0.0040416` (1), `0.006753` (1) |
| `liver_0` | VARCHAR | 1156/1231 | `0` (580), `0.0013867` (2), `0.0942638` (1), `0.0491204` (1), `0.0427711` (1) |
| `liver_1` | VARCHAR | 1156/1231 | `0` (173), `0.0425662` (1), `0.0284965` (1), `0.0312639` (1), `0.0825207` (1) |
| `lung_0` | VARCHAR | 1156/1231 | `0` (314), `0.0026227` (1), `0.038132` (1), `0.0784206` (1), `0.0466987` (1) |
| `lung_1` | VARCHAR | 1156/1231 | `0` (1070), `0.0729629` (1), `0.0155656` (1), `0.0043001` (1), `0.38294` (1) |
| `muscle_0` | VARCHAR | 1156/1231 | `0` (824), `0.0015405` (1), `0.0030094` (1), `0.0027542` (1), `0.0147125` (1) |
| `ovary_0` | VARCHAR | 1156/1231 | `0` (442), `0.0180767` (2), `0.009642` (1), `0.0071225` (1), `0.0051481` (1) |
| `ovary_1` | VARCHAR | 1156/1231 | `0` (1074), `0.0474256` (1), `0.0536186` (1), `0.0082883` (1), `0.003693` (1) |
| `prostate_0` | VARCHAR | 1156/1231 | `0` (1072), `0.0036131` (1), `0.0053535` (1), `0.0133514` (1), `0.0604014` (1) |
| `prostate_1` | VARCHAR | 1156/1231 | `0` (1036), `0.0013619` (1), `0.0198811` (1), `0.2576102` (1), `0.0083738` (1) |
| `testis_0` | VARCHAR | 1156/1231 | `0` (772), `0.0316596` (1), `0.0248357` (1), `0.0058272` (1), `0.1305418` (1) |
| `1_Fibroblast_Heart` | VARCHAR | 1231/1231 | `0` (877), `0.2218291` (1), `0.0299224` (1), `0.2061607` (1), `0.2341867` (1) |
| `2_Neuron` | VARCHAR | 1231/1231 | `0` (135), `0.0429257` (1), `0.0739026` (1), `0.0475517` (1), `0.0104956` (1) |
| `3_Myeloid_Granulocyte` | VARCHAR | 1231/1231 | `0` (141), `0.6793981` (1), `0.6542928` (1), `0.6982215` (1), `0.6161802` (1) |
| `4_Epithelium_Gastric` | VARCHAR | 1231/1231 | `0` (760), `0.0062411` (1), `0.0027375` (1), `0.0020801` (1), `0.0126237` (1) |
| `5_Epithelium_UpperAirway` | VARCHAR | 1231/1231 | `0` (1200), `0.2978028` (1), `0.0536591` (1), `0.0736229` (1), `0.1218916` (1) |
| `6_Tcell_EffectorMemory` | VARCHAR | 1231/1231 | `0` (52), `0.0372531` (2), `0.0870392` (1), `0.0524802` (1), `0.0571529` (1) |
| `7_Epithelium_Colon_Intestinal` | VARCHAR | 1231/1231 | `0` (556), `0.005341` (2), `0.0023164` (2), `0.0108679` (1), `0.0103915` (1) |
| `8_Glia_Oligodendrocyte` | VARCHAR | 1231/1231 | `0` (1170), `0.0257293` (1), `0.0111523` (1), `0.0048455` (1), `0.0041662` (1) |
| `9_Hepatocyte` | VARCHAR | 1231/1231 | `0` (199), `0.0488489` (1), `0.0488508` (1), `0.0210447` (1), `0.0210047` (1) |
| `10_Cardiomyocyte` | VARCHAR | 1231/1231 | `0` (519), `0.0160488` (2), `0.015017` (1), `0.0084559` (1), `0.0200051` (1) |
| `11_Pancreas_Endocrine` | VARCHAR | 1231/1231 | `0` (415), `0.0025079` (2), `0.0040599` (2), `0.0103114` (2), `0.0040613` (2) |
| `12_Epithelium_Fallopian` | VARCHAR | 1231/1231 | `0` (1220), `0.0067305` (1), `0.0277771` (1), `0.0067397` (1), `0.0406072` (1) |
| `13_Breast_Epithelial` | VARCHAR | 1231/1231 | `0` (1147), `0.0322501` (1), `0.0510348` (1), `0.0169436` (1), `0.0939332` (1) |
| `14_Epithelium_Bladder` | VARCHAR | 1231/1231 | `0` (1052), `0.0020879` (1), `0.0142383` (1), `0.0244436` (1), `0.0030272` (1) |
| `15_Pancreas_Acinar` | VARCHAR | 1231/1231 | `0` (800), `0.005563` (1), `0.006693` (1), `0.01047` (1), `0.0073634` (1) |
| `16_Epithelium_Kidney` | VARCHAR | 1231/1231 | `0` (1226), `0.0006196` (1), `0.0144574` (1), `0.0792819` (1), `0.2381629` (1) |
| `17_Endothelium_Hepatic_Pulmonary` | VARCHAR | 1231/1231 | `0` (1184), `0.1701718` (1), `0.204397` (1), `0.0172359` (1), `0.1600122` (1) |
| `18_Epithelium_Thyroid` | VARCHAR | 1231/1231 | `0` (1191), `0.022023` (1), `0.0045334` (1), `0.0255262` (1), `0.0053239` (1) |
| `19_Erythroid_Progenitor` | VARCHAR | 1231/1231 | `0` (117), `0.0754713` (1), `0.048319` (1), `0.0924556` (1), `0.2707474` (1) |
| `20_Pancreas_Duct` | VARCHAR | 1231/1231 | `0` (958), `0.0005326` (2), `0.0028803` (1), `0.0047117` (1), `0.003866` (1) |
| `21_Epithelium_Lung_Bronchus` | VARCHAR | 1231/1231 | `0` (1226), `0.0482397` (1), `0.0226742` (1), `0.0198735` (1), `0.0395442` (1) |
| `22_Epithelium_Endometrium` | VARCHAR | 1231/1231 | `0` (960), `0.0134484` (1), `0.0046088` (1), `0.0152495` (1), `0.0167848` (1) |
| `23_Epithelium_Prostate` | VARCHAR | 1231/1231 | `0` (729), `8.24e-05` (2), `0.0011181` (2), `0.0038375` (1), `0.0088327` (1) |
| `24_Epithelium_Lung_Alveolar` | VARCHAR | 1231/1231 | `0` (1177), `0.1006525` (1), `0.056902` (1), `0.0974923` (1), `0.0421595` (1) |
| `25_Bcell_Memory` | VARCHAR | 1231/1231 | `0` (1028), `0.101317` (1), `0.0589428` (1), `0.0940255` (1), `0.1290676` (1) |
| `26_Endothelium_Kidney` | VARCHAR | 1231/1231 | `0` (234), `0.0447649` (1), `0.1054027` (1), `0.025107` (1), `0.0233337` (1) |
| `27_Muscle_Smooth` | VARCHAR | 1231/1231 | `0` (1188), `0.0430288` (1), `0.0133438` (1), `0.0062568` (1), `0.0064003` (1) |
| `28_Endothelium_Vascular` | VARCHAR | 1231/1231 | `0` (404), `0.0507417` (1), `0.0296368` (1), `0.0506877` (1), `0.0392263` (1) |
| `29_Epithelium_Gallbladder` | VARCHAR | 1231/1231 | `0` (1141), `0.0067792` (2), `0.0040792` (1), `0.0065343` (1), `0.0008306` (1) |
| `30_Myeloid_Macrophage_Lung` | VARCHAR | 1231/1231 | `0` (1152), `0.0350135` (1), `0.285259` (1), `0.1054046` (1), `0.3101908` (1) |
| `31_Muscle_Skeletal` | VARCHAR | 1231/1231 | `0` (1207), `0.0022563` (1), `0.0078543` (1), `0.0061132` (1), `0.1821709` (1) |
| `updated_at` | TIMESTAMP | 1231/1231 | min=2026-04-27 08:24:53 max=2026-04-29 08:50:29 |

## `_schema_version` — 4 lignes, 3 colonnes

| Colonne | Type | Couverture | Description / valeurs |
|---|---|---|---|
| `version` | INTEGER | 4/4 | min=1 max=4 avg=2.500 |
| `applied_at` | TIMESTAMP | 4/4 | min=2026-01-19 15:34:33 max=2026-04-29 10:04:31 |
| `description` | VARCHAR | 4/4 | `Add bam_horaire column (v2)` (1), `Add grade column to metadata (…` (1), `Add speedvac column to metadat…` (1), `Initial schema v1` (1) |
