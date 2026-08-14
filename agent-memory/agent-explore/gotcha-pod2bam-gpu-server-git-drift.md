---
name: gotcha-pod2bam-gpu-server-git-drift
description: Pod2Bam's GPU-server clone can run configs (Dorado/model versions) that were never committed to origin/main — git log alone is not sufficient to know what actually ran in production
metadata:
  type: project
---

Pod2Bam basecalls on a dedicated remote GPU server (separate host — `/scratch/basecall/dorado/`
does not exist on the CPU/dev servers) with its own `git clone` of the repo. Found 2026-08-14: a
"V6.0.0" / Dorado 2.0.0 setup is documented in Pod2Bam's own Claude auto-memory
(`~/.claude/projects/-home-blipinski-Pipeline-Pod2Bam/memory/setup-v6.0.0.md`, dated 2026-06-04)
and evidenced by a real S3 output path referenced in
`~/Pipeline/Bam2Beta/dev/archive/bacasable.sh:19` (`processed/Pod2Bam/RetD/$SAMPLE/V6.0.0/...`),
but is **completely absent** from `~/Pipeline/Pod2Bam` git history (`git log --all`, single
`main` branch, no stash, up to date with origin) — `nextflow.config`'s version maps only go up to
V5.2.0 / Dorado 1.4.0 as committed.

**Why:** GPU-server edits (nextflow.config version maps, new Dockerfile) can be made and run
directly on the remote clone without ever being pushed back to `origin/main`.
**How to apply:** for Pod2Bam (and likely other GPU-server pipelines), never trust `git log` alone
to enumerate "what versions/configs exist" — cross-check the project's own Claude auto-memory AND
actual S3 output paths from consumer projects before concluding a version is unsupported or a
config is dead.
