---
name: cross-project-tower-integration
description: Aima-Tower consumes R&D pipeline outputs (e.g. Feature/) via read-only bind mount on flat files, no DB/cache layer
metadata:
  type: project
---

Recurring integration pattern between Boris's R&D pipelines (e.g. `~/Pipeline/Feature/`) and
`~/Pipeline/Aima-Tower/`: the R&D project writes flat CSV outputs to a **gitignored `result/`
directory** (regenerable, not committed) ; Aima-Tower reads them **directly from disk** via a
read-only bind mount (`/pipeline:ro`), no intermediate DuckDB/cache — a page refresh in Tower is
enough to see new results after re-running the R&D script, no rebuild/redeploy needed.

**Why:** avoids duplicating a results-DB layer per R&D project ; keeps Tower as a pure read-only
viewer over whatever the pipeline scientist regenerates locally.
**How to apply:** when connecting a new analysis/pipeline project to Aima-Tower, prefer this
pattern (flat files in a gitignored `result/`, bind-mounted read-only) over building a dedicated
results database, unless Tower needs to query/filter at a scale flat CSVs can't handle.

Confirmed example: `~/Pipeline/Feature/result/speedvac_{no,yes}/{scores,eval_kpis}.csv` ←
consumed by Aima-Tower `/exploration-beta` (`src/feature_service.py`), replacing an earlier
`feature_runs.duckdb` design.
