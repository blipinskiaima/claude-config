---
name: S3 data paths
description: S3 bucket paths for cancer and healthy bedMethyl data, requires --profile scw
type: reference
---

- **Cancer samples**: `s3://aima-bam-data/processed/MRD/RetD/solid/CGFL/{BARCODE}/BETA_28M/`
- **Healthy CGFL**: `s3://aima-bam-data/processed/MRD/RetD/liquid/CGFL/Healthy_{ID}/BETA_28M/`
- **Healthy HCL**: `s3://aima-bam-data/processed/MRD/RetD/liquid/HCL/Healthy_{ID}/BETA_28M/`
- **Profile**: `--profile=scw` (Scaleway)
- **Files per sample**: 22 bedMethyl.gz (chr1-chr22) + 22 modkit_pileup.log
- **Naming**: `{SAMPLE_ID}.merged.all.chr{N}.bedMethyl.gz`
