---
name: cross-project-too-input-contract
description: Bam2Beta output naming does not match the TOO (tumor-of-origin) CSV input contract 1:1 — rename/format mapping needed when bridging the two
metadata:
  type: project
---

TOO reference input template lives at
`~/Pipeline/exploratory-analysis-CGFL-HCL/tumor_of_origin/releases/too5_v0_4_1/input_features_template.csv`
(columns: sample_id, sex, mvaf_v1_4, 16 EPIC proportions, 31 numbered Loyfer proportions).
Bam2Beta (`~/Pipeline/Bam2Beta`) produces the raw ingredients but under different names/formats:

- `mvaf_v1_4`: Bam2Beta's TSV column is called `mvaf` (not `mvaf_v1_4`), file
  `${ID}.merged.epic.raima_score.V1.4.tsv` in `BETA/`. Value is already on the **percentage
  scale** (`mean(sqrt(scores))^2 * 100`, e.g. 45.53) — matches TOO template scale, only the column
  name needs remapping.
- `sex`: Bam2Beta's IV module (`raima::infer_sex`) outputs a **numeric probability** (`IV/*.sex.tsv`),
  not the `"M"`/`"F"` string TOO expects — needs a threshold/mapping step, not just a rename.
- 47 proportions: come from two separate Bam2Beta outputs (`BETA/*.props_v1.tsv` for EPIC classes,
  `EXTRACT_FULL_28M/*.props_loyfer.tsv` for Loyfer classes) — column names/order vs the TOO
  template's 16+31 naming convention not yet verified.

**Why:** any future "TOO module" bridging Bam2Beta -> TOO needs an explicit rename/threshold
layer, it's not a straight column concat of existing Bam2Beta TSVs.
**How to apply:** when building a Bam2Beta->TOO CSV assembly step, budget time to verify/rename
each of the 3 groups above (mvaf, sex, proportions) rather than assuming Bam2Beta's native TSV
headers already match the TOO contract.
