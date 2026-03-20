---
name: Data processing statistics
description: Sparse matrix dimensions, sparsity, and CpG coverage stats for the ctDNA pipeline
type: project
---

Sparse matrices: 133 samples × 27.4M CpGs. Sparsity 81% (19% observed per sample, ~5.1M CpGs avg). Higher coverage than the ~1x/~5% initially estimated.

Download: 33 GB on /scratch/ia_ctdna/raw/ (symlinked from data/raw).

**Why:** Sparsity impacts feature selection thresholds. With 19% observation rate, coverage_filter at 30% is reasonable (not too aggressive).

**How to apply:** If feature selection is too slow or noisy, coverage_filter threshold can be raised (e.g., 50%) since data is denser than expected.
