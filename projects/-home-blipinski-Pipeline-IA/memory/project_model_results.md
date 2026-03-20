---
name: Model training results
description: Baseline ML results — LR with 1000 variance features achieves AUC=1.0, sens=0.988 on 5-fold CV
type: project
---

Best model: Logistic Regression, 1000 CpGs selected by variance.

5-fold CV results: AUC=1.000, sensitivity=0.988, specificity=1.000, PR-AUC=1.000.

Grid search over n_features=[500,1K,2K,5K,10K,20K]: performance plateaus at 1000. LR consistently best on sensitivity.

Transformer skipped — baseline near-perfect.

**Why:** Near-perfect results expected because training data is 80-100% TF (solid tumor) vs 0% TF (healthy). The real challenge is Phase 2: cfDNA with low tumor fractions (0.1-5%).

**How to apply:** For Phase 2, consider in-silico dilution to simulate low TF, or retrain with real cfDNA samples. Current model will likely score low TF samples as healthy.
