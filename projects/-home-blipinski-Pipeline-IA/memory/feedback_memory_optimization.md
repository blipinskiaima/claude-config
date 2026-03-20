---
name: Memory optimization pattern
description: Never hstack full genome sparse matrices — process per chromosome, prefilter, then hstack only filtered columns
type: feedback
---

Never build a single 27.4M-column sparse matrix (36 GB per matrix). Always process per chromosome.

**Why:** First attempt hstacked all 22 chr into one matrix → 36 GB × 2 = unusable. Even loading it for prefiltering OOMs.

**How to apply:** Save per-chr matrices (44 files, ~1 GB peak). Prefilter (coverage + variance) one chr at a time, collect scores in a list, then hstack only filtered columns. Final reduced matrix is small (107 MB for 50K cols).
