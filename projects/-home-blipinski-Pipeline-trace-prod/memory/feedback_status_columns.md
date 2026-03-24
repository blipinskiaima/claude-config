---
name: STATUS_COLUMNS is only for strict OK/KO/WARNING
description: Never add free-value VARCHAR columns (like ichorcna_score) to STATUS_COLUMNS — _parse_status() will overwrite non-status values to KO
type: feedback
---

Do NOT add columns to `STATUS_COLUMNS` (lib/duckdb.py) unless they strictly contain OK/KO/WARNING values.

**Why:** `_parse_status()` maps any value that isn't OK/WARNING to KO. Adding `ichorcna_score` (which stores a numeric string like "0,01271" or "KO") caused all scores to be overwritten to KO.

**How to apply:** When adding a new column to `retd_suivis`, check if it's a strict status (add to `STATUS_COLUMNS`), a numeric (add to `NUMERIC_COLUMNS`), or free-form VARCHAR (add to neither — falls through to the `else` branch in `_prepare_data()`).
