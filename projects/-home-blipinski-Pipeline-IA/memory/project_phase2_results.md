---
name: Phase 2 evaluation results
description: cfDNA liquid biopsy evaluation — model doesn't generalize (median score 0 for cancer), 438 samples scored
type: project
---

Phase 2 evaluation on 438 cfDNA liquid biopsy samples (212 CGFL + 227 HCL, minus 50 training healthy).

RAIMA results at ~95% specificity:
- CGFL: 79% sens (VAF>5%), 25% (VAF 0-5%), 61% total with VAF
- HCL: 37% sens (VAF>5%), 22% (VAF 0-5%), 28% total with VAF
- Combined: 64% (VAF>5%), 28% (VAF 0-5%), 47% total with VAF

Score distribution: Healthy mean=0.001, Cancer/Other mean=0.160, both median=0.000.
Thresholds very low (0.014 CGFL, 0.003 HCL) — scores are low but discriminating.

HCL metadata fix: `Old sample name` column in HCL CSV contains the actual sample names (not `Sample name` which has numeric IDs).

**Why:** Model trained on 80-100% TF solid tumor. Detects high-VAF cfDNA well but misses low-VAF.

**How to apply:** Phase 3 would need in-silico dilution, cfDNA-specific training, or a different approach. CGFL centre performs much better than HCL — investigate why.
