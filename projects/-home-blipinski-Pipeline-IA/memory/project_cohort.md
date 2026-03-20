---
name: Cohort composition
description: ctDNA pipeline cohort — 83 cancer + 50 healthy samples, all validated on S3 with 22 bedMethyl.gz each
type: project
---

Cohort: 133 samples (83 cancer, 50 healthy).

**Cancer**: All 83 from `s3://aima-bam-data/processed/MRD/RetD/solid/CGFL/` (excluded LOG dir). 4 without Colon_ prefix (0002A83, 0002A89, 0002DP5, 0002EEN). Google Sheet filter (column P==TRUE) not applied — CSV export was not available. All 83 may include some that should be excluded.

**Healthy**: 25 CGFL + 25 HCL, random seed=42. From 50 CGFL and 103 HCL available (excluding rebasecalled).

**Why:** Started without Google Sheet export to avoid blocking. May need refinement when CSV available.

**How to apply:** If user provides raw_data_export.csv, re-run cancer selection to filter by column P == TRUE.
