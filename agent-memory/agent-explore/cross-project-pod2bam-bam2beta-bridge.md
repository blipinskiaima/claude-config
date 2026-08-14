---
name: cross-project-pod2bam-bam2beta-bridge
description: Pod2Bam's production S3 output tree does not match Bam2Beta's expected input path — bridging is manual, not automated
metadata:
  type: project
---

Pod2Bam (GRCh38 no_alt aligned BAM) writes production output to
`s3://aima-bam-data/processed/Pod2Bam/RetD/{RUN_ID}/{VERSION}/align_trimmed/{SAMPLE}/{SAMPLE}.bam`.
Bam2Beta expects its `--input` under `s3://aima-bam-data/data/{LABO}/{liquid,solid}/{SAMPLE_ID}/`.
As of 2026-08, the only bridge seen is a manual `aws s3 cp` (renaming into
`{SAMPLE}_rebasecalled_{VERSION}/`) in `~/Pipeline/Bam2Beta/dev/archive/bacasable.sh` — no cron/
sentinel automation exists yet. `~/Pipeline/Pod2Bam/PLAN_ACTION_PROD.md` still lists
"standardiser le chemin S3 de sortie Pod2Bam" and a `Pod2Bam.done` sentinel as open TODOs.

**Why:** Pod2Bam and Bam2Beta were built independently (GPU re-basecalling pipeline vs CPU
methylation/QC pipeline) and were only wired together ad hoc for FP-investigation batches, not as
a production hand-off.
**How to apply:** when asked whether a Pod2Bam-produced BAM is "ready for Bam2Beta", check
whether it has been manually copied/renamed into the `data/{LABO}/{TYPE}/` convention first — the
native `processed/Pod2Bam/RetD/` path is not a valid Bam2Beta `--input` as-is.
