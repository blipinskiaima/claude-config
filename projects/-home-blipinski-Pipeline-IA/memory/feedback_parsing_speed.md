---
name: bedMethyl parsing optimization
description: Use pandas.read_csv with usecols instead of line-by-line Python parsing — 16x speedup
type: feedback
---

Always use `pd.read_csv(filepath, sep='\t', header=None, usecols=[0,1,9,10])` for bedMethyl files.

**Why:** Line-by-line Python parsing took ~15 min/sample. pandas.read_csv: ~1 min. For 600 samples = 150h vs 9h.

**How to apply:** Also avoid `df.iterrows()` for lookups — use dict lookups on numpy arrays instead.
