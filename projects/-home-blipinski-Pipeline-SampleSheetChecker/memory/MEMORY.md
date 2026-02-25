# SampleSheetChecker - Project Memory

## Project Overview
- Single Bash script (`SampleSheetChecker.sh`, 305 lines) — no dependencies, no build system
- Validates TSV sample sheets then syncs BAM data from `raw/` to `liquid/` on S3 (Scaleway, `AWS_PROFILE=scw`)
- 3 modes: normal sync, `--dry-run`, `--size`

## Architecture (single file, 5 logical sections)
1. **Input Validation** (L9-93): CLI args, header check, per-row regex validation
2. **Path Resolution** (L114-149): glob on `/mnt/aima-bam-data/data/HCL/raw/*/no_sample_id/{run}/bam_pass/{barcode}/`
3. **Sync Orchestration** (L151-190): S3 destination check, skip if exists, parallel `aws s3 sync`
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

## Data Files
- `samplesheet.tsv`: 32 samples (Colon_21-36, Healthy_11-26)
- `samplesheet2.tsv`: 4 samples (Colon_37-40)
- `samplesheet3.tsv`: 32 samples (Healthy_27-58)
