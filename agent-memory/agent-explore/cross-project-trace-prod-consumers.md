---
name: cross-project-trace-prod-consumers
description: trace-prod DuckDB (samples_status.duckdb) is the shared read-only feature/metadata store consumed by multiple downstream R&D projects
metadata:
  type: project
---

`~/Pipeline/trace-prod/database/samples_status.duckdb` is the central registry (samples +
features computed by raima/Bam2Beta + clinical metadata/truth labels from GSheet). Multiple
downstream projects read it **read-only** (`duckdb.connect(path, read_only=True)`) and must never
write to it from outside trace-prod itself (single-writer DB, a concurrent check/write elsewhere
locks it).

**Why:** trace-prod is fed by Bam2Beta/raima pipeline outputs and is the single source of truth
for cohort selection + truth labels across R&D. Locking rules matter because a stray writer from
an analysis script breaks trace-prod's own ingestion.
**How to apply:** any new analysis project reading sample cohorts/features should connect
read-only to this DB rather than re-deriving cohort logic from S3/GSheet directly. Known consumer:
`~/Pipeline/Feature/` (`select_cohort_train.py` / `select_cohort_eval.py`).
