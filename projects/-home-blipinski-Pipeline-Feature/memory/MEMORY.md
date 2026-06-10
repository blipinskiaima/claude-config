# Feature — index mémoire Claude (auto memory)

> Pas de dossier `~/Pipeline/Feature/memory/` dans le repo (archivé dans `archives/memory/`). Contexte opérationnel : `CLAUDE.md` + `.claude/rules/` + fichiers ci-dessous.

- [Truth labels](label-definitions.md) — **canon** positif/négatif/NA + imagerie suspecte (select_cohort.py)
- [Feedback design pipeline](feedback-feature-pipeline-design.md) — scripts sélection = très simples ; args explicites, pas d'état caché
- [Pipeline select_cohort→train→eval](pipeline-3-etapes.md) — **source de vérité** architecture juin 2026 (post-extraction)
- [Livrables et décisions pool](livrables-actuels.md) — v2_probs / v4_short_read ; livrables sous `result/`, DB `feature_runs.duckdb`
- [Convergence exploratory-analysis](convergence-exploratory-analysis.md) — scripts Michael (référence)
- [Target specificity](target-specificity.md) — Sens@95% KPI standard, Sens@90% complément
- [Cascade filtres cohorte](cohort-filters-cascade.md) — historique 1309→454 (pré-pipeline scripts)
- [trace-prod schema](trace-prod-schema.md) — colonnes tables (complète rule 03)
- [Tableau final KPI](tableau-final-kpi.md) — archive 7 mai 2026 (pré-tri)

**Doc longue archivée** : `~/Pipeline/Feature/archives/memory/projects-knowledge-base.md` (trace-prod, Bam2Beta, exploratory — à lire si besoin cross-projet).
