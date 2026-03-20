# SampleSheetChecker - Project Memory

## Project Overview
- Single Bash script (`SampleSheetChecker.sh`, ~317 lines) — no dependencies, no build system
- Validates TSV sample sheets then syncs BAM/POD5 data from `raw/` to `liquid/` on S3 (Scaleway, `AWS_PROFILE=scw`)
- 4 modes: normal sync, `--dry-run`, `--size`, `--type=pod5`
- POD5 destination: `s3://aima-pod-data/data/HCL/liquid/` (vs `s3://aima-bam-data` for bam)

## Architecture (single file, 5 logical sections)
1. **Input Validation** (L9-93): CLI args, header check, per-row regex validation
2. **Path Resolution** (L127-162): glob on `/mnt/aima-bam-data/data/HCL/raw/*/no_sample_id/{run}/{type}_pass/{barcode}/`
3. **Sync Orchestration** (L164-202): S3 destination check, skip if identical, resync if size differs, parallel `aws s3 sync`
4. **Progress Monitoring** (L193-278): polling loop, progress bar, size verification
5. **Summary** (L280-304): recap of synced/skipped/failed

## Key Patterns
- Variables: `UPPER_SNAKE_CASE`, associative arrays for per-sample tracking
- Error handling: `set -euo pipefail` + `|| true` for non-fatal commands
- Parallel sync: background subshells with PID tracking in `NAME_PIDS`
- French comments, mixed FR/EN user output

## Known Issues
- `SIZE_INFO` (L107): declared but never used — dead code
- Logs in `/tmp/SampleSheetChecker_*/` accumulate without cleanup
- `AWS_PROFILE=scw` hard-coded in multiple places (not configurable)
- Glob expansion (L119) unquoted — fragile if paths have spaces (safe with current name regex)

## Rules
- NEVER delete anything from S3 buckets (rule d'or)

## Upload Monitoring
- Upload logs in `s3://aima-bam-data/data/HCL/LOG/`
- Pattern: `upload_YY-MM-DD_HH-MM-SS.log` (large = real upload) + `done_*.done` (completion marker) + 62-byte stubs ("Already uploaded")
- Recurring error on all uploads: `sequencing_summary_*.txt` fails with "Part number must be an integer between 1 and 1000" (file too large for default multipart)
- Some NANOs upload without dedicated log entries (e.g. NANO14_26_N1, NANO15_26_N2)

## trace-prod Integration
- Project at `/home/blipinski/Pipeline/trace-prod/` — DuckDB database
- `bam_metadata.run_id` (UUID) maps to last 8 chars of S3 run folder name
- Google Sheet metadata_HCL: key `1XcWPn3_PT1atR-i5DmOM1t0ldgb5_PnxhQUwNUxWpQg`, worksheet "VAF"
- fetch via: `python3 database/check_samples.py fetch-gsheet metadata_HCL`
- import metadata: `python3 database/check_samples.py import-metadata liquid HCL`
- **Last sync (2026-03-07):** 282 lignes gsheet, 281 samples en DB, 196 metadata importées, 86 non trouvés en base

## Analyse croisée S3/gsheet/DB (2026-03-07)
- 67 runs sur S3 raw, 63 runs dans gsheet
- NANO01-NANO12: complets (raw + liquid + DB)
- NANO13_26_N3-N4, NANO14_26_N3: complets
- **9 runs gsheet absents de S3** (~40 samples)

### Cas 1 — Healthy_59-66 : NANO13 manquants
| Sample | Name | Barcode | Run | Run ID | NANO |
|--------|------|---------|-----|--------|------|
| Healthy_59 | H60-S | barcode25 | 20260216_1053_1C_PBI54259_aa33c7e7 | aa33c7e7 | NANO13_26_N1 |
| Healthy_60 | H61-S | barcode26 | (même run) | aa33c7e7 | NANO13_26_N1 |
| Healthy_61 | H62-S | barcode27 | (même run) | aa33c7e7 | NANO13_26_N1 |
| Healthy_62 | H63-S | barcode28 | (même run) | aa33c7e7 | NANO13_26_N1 |
| Healthy_63 | H64-S | barcode29 | 20260216_1054_1E_PBI51449_99962cf0 | 99962cf0 | NANO13_26_N2 |
| Healthy_64 | H65-S | barcode30 | (même run) | 99962cf0 | NANO13_26_N2 |
| Healthy_65 | H66-S | barcode31 | (même run) | 99962cf0 | NANO13_26_N2 |
| Healthy_66 | H67-S | barcode32 | (même run) | 99962cf0 | NANO13_26_N2 |
→ Données jamais uploadées, à localiser sur machine source

### Cas 2 — Samples sur S3 raw mais pas en DB (à sync liquid)
- NANO13_26_N4 (`bc4b0d55`): Healthy_71-74
- NANO14_26_N1 (`8927831e`): Healthy_75-78
- NANO14_26_N2 (`f8c47674`): Healthy_79-82
- NANO14_26_N4 (`da634bcf`): Healthy_87-90
- NANO15_26_N1 (`0c3c2bf1`): TNE_1-10
- NANO15_26_N2 (`f8591d83`): Healthy_91-94
- NANO15_26_N3 (`ec230a7d`): Healthy_95-98
- NANO16_26_N1 (`00d00a6a`): Healthy_99-102

### Cas 3 — Runs gsheet absents de S3 (NANO16/17 incomplets)
- `4c110756`: Healthy_103-106 | `3072ab39`: Healthy_107-110
- `f7f94bec`: Nuclear_1-4 | `b91aeb6d`: Nuclear_5-8 (sur S3) | `db2a4605`: Nuclear_9-12
- `90484f97`: Colon_41-44 (sur S3) | `332f0d71`: Colon_45-48 (sur S3)
- `5b2d333d`: Colon_49-52 | `af90a5f8`: Colon_53-56 | `edc2b04b`: Colon_57-60

### Nouveaux types d'échantillons
- **TNE** (TNE_1-10): nouveau type, run `0c3c2bf1` sur NANO15_26_N1
- **Nuclear** (Nuclear_1-12): nouveau type, runs sur NANO17

## Data Files
- `samplesheet.tsv`: 32 samples (Colon_21-36, Healthy_11-26)
- `samplesheet2.tsv`: 4 samples (Colon_37-40)
- `samplesheet3.tsv`: 32 samples (Healthy_27-58)
- `samplesheet_test_basecall.tsv`: 7 samples (Healthy_11/12/14/23/25/26/34) — test pod5
- `ss4.tsv`: sample sheet supplementaire

## Upload Speed Monitoring
- R/ggplot2 graph: `upload_speed.png`, data in `/tmp/upload_speed_week.csv`
- Performance categories: CRITIQUE(<50)/DEGRADE/MOYEN/BON/OPTIMAL/EXCELLENT(>300 Go/h)
- Feb 22-28: ~38 Go/h avg (degraded) → Mar 5: ~330 Go/h (excellent)
- Tmux monitoring: `tmux attach -t monitor` — checks every 30 min, logs to `/tmp/monitor_overnight_*.log`
