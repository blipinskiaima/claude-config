# Agent-explore — index mémoire (cross-projet ~/Pipeline/)

- [Tower integration pattern](cross-project-tower-integration.md) — R&D pipelines exposent des CSV plats dans `result/` gitignoré, Tower lit en bind-mount ro, pas de DB/cache
- [trace-prod consumers](cross-project-trace-prod-consumers.md) — DuckDB central (features+metadata+truth), toujours `read_only=True` depuis les projets consommateurs
- [TOO input contract](cross-project-too-input-contract.md) — Bam2Beta produit mvaf/sex/proportions mais noms/format diffèrent du template CSV TOO (rename + mapping requis)
