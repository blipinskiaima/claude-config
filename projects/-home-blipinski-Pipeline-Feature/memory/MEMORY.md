# Feature — index mémoire Claude (auto memory)

> Pas de dossier `~/Pipeline/Feature/memory/` dans le repo (archivé dans `archives/memory/`). Contexte opérationnel : `CLAUDE.md` + `.claude/rules/` + fichiers ci-dessous.

- [Truth labels](label-definitions.md) — **canon** positif/négatif/NA ; suspects exclus du train, via l'eval (select_cohort_train/eval.py)
- [Feedback design pipeline](feedback-feature-pipeline-design.md) — scripts sélection = très simples ; args explicites, pas d'état caché
- [Feedback vérifier avant redesign](feedback-verifier-avant-redesign.md) — prouver ce que le code fait (subset sample_id) avant de proposer une refonte / question multi-options
- [Pipeline select_cohort→train→eval](pipeline-3-etapes.md) — **source de vérité** architecture juin 2026 (post-extraction)
- [Dimension depth](depth-dimension.md) — depth 0.25/0.5/1/2X live à l'éval (Feature + Tower) ; sémantique Option-1 + gotchas (scores.csv par-sample, result/ gitignoré)
- [Dilution eval unit](dilution-eval-unit.md) — mécanisme `unit` pour empiler cohortes éval hors-train (Twist) dans cohort_eval/scores.csv
- [Suspect eval unit](suspect-eval-unit.md) — unité `suspect` (imageries suspectes) : flag `--include-suspicious` (Feature) + onglet dotplot (Tower), juin 2026
- [Bladder exclu du KPI](bladder-kpi-exclusion.md) — flag `--exclude-bladder` (active/active_nomut) ; contre-intuitif : +2 à +6 pts (bladder = cas difficiles), reste dans le train, juillet 2026
- [Livrables et décisions pool](livrables-actuels.md) — v2_probs / v4_short_read ; livrables sous `result/`, DB `feature_runs.duckdb`
- [Convergence exploratory-analysis](convergence-exploratory-analysis.md) — scripts Michael (référence)
- [Target specificity](target-specificity.md) — Sens@95% KPI standard, Sens@90% complément
- [Cascade filtres cohorte](cohort-filters-cascade.md) — historique 1309→454 (pré-pipeline scripts)
- [trace-prod schema](trace-prod-schema.md) — colonnes tables (complète rule 03)
- [Tableau final KPI](tableau-final-kpi.md) — archive 7 mai 2026 (pré-tri)

**Doc longue archivée** : `~/Pipeline/Feature/archives/memory/projects-knowledge-base.md` (trace-prod, Bam2Beta, exploratory — à lire si besoin cross-projet).
