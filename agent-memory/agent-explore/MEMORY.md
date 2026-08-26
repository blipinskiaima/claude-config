# Agent-explore — index mémoire (cross-projet ~/Pipeline/)

- [Tower integration pattern](cross-project-tower-integration.md) — R&D pipelines exposent des CSV plats dans `result/` gitignoré, Tower lit en bind-mount ro, pas de DB/cache
- [trace-prod consumers](cross-project-trace-prod-consumers.md) — DuckDB central (features+metadata+truth), toujours `read_only=True` depuis les projets consommateurs
- [TOO input contract](cross-project-too-input-contract.md) — Bam2Beta produit mvaf/sex/proportions mais noms/format diffèrent du template CSV TOO (rename + mapping requis)
- [Claude CLI auth pattern](cross-project-claude-cli-auth-pattern.md) — subprocess `claude -p` + CLAUDE_CODE_OAUTH_TOKEN réutilisé Aima-Tower→Aima-Survey pour router sur abonnement Pro/Max
- [Pod2Bam→Bam2Beta bridge](cross-project-pod2bam-bam2beta-bridge.md) — chemins S3 incompatibles (`processed/Pod2Bam/RetD/` vs `data/{LABO}/{TYPE}/`), pont manuel uniquement, pas d'automatisation
- [GPU-server git drift](gotcha-pod2bam-gpu-server-git-drift.md) — Pod2Bam GPU server = clone séparé, config (ex V6.0.0/Dorado 2.0.0) peut tourner en prod sans jamais être pushée sur origin/main
- [raima mVAF short-read gap](cross-project-raima-mvaf-shortread-gap.md) — raima convertit DRAGEN/rastair en bedMethyl (model_v1/prop_loyfer OK), mais bootstrap_model_v1 (mVAF v1.4/v1.5) exige des tables par-read modkit-only
- [Bam2Beta "short_read" naming trap](gotcha-bam2beta-shortread-naming-trap.md) — avant 06/2026 "short_read" = filtre longueur fragment (75-200bp), renommé SMALL_FRAGMENTS ; pas du séquençage court-lu
