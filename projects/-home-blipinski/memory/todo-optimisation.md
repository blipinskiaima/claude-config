---
name: Todo optimisation Claude Code & projets
description: Liste des tâches d'optimisation restantes après la rétrospective du 13/04/2026. Consulter et mettre à jour régulièrement.
type: project
originSessionId: 129fb3f7-7613-4550-adf0-9392306d8a85
---
# Todo — Optimisation Claude Code & Projets

**Dernière mise à jour : 2026-04-13**

## Haute priorité

- [ ] **Tester ComBat-met sur données CGFL vs HCL** — R package (NAR 2025), correction batch effect méthylation. Directement applicable au problème n°1 du modèle ctDNA. ~1-2 jours.
- [ ] **Sécurité secrets — étape 1** : migrer `~/Pipeline/export/` vers des fichiers `.env` avec `chmod 600`. Documenter le pattern pour les autres projets (tokens Tower dans nextflow.config). Step by step.

## Moyenne priorité

- [ ] **Améliorer Aima-Tower** — dashboard interactif pour biologistes :
  - [ ] Intégrer IGV.js via dash-bio (visualisation bedMethyl)
  - [ ] Graphiques interactifs avec seuils de spécificité ajustables
  - [ ] Statistiques par sous-ensembles (centre, type tumoral, VAF)
  - [ ] Enrichir les agents IA d'Aima-Tower avec features DB
  - [ ] Module exploratory-analysis embarqué
- [ ] **Explorer MethylBERT** — Transformer read-level (Nat Comm 2025) pour améliorer sensibilité basse VAF (<5%). Nécessite GPU. ~2-3 jours.
## Basse priorité

- [ ] **Sécurité secrets — étape 2** : installer `gitleaks` en pre-commit hook sur les projets gittés
- [ ] **Sécurité secrets — étape 3** : évaluer un gestionnaire de secrets (sops, age, vault)
- [ ] **Skill save-code pour trace-prod** — automatiser la sauvegarde de session
- [ ] **Agent de veille enrichi** — ajouter l'analyse automatique des abstracts par Claude (pertinence AIMA)
- [ ] **Skills Pod2Bam** — créer test/qualif/maj analogues à Bam2Beta. Pas urgent tant que Pod2Bam n'est pas soumis à audit qualité.

## Complété

- [x] Nettoyage config Claude (skills, plugins, agents dupliqués) — 2026-04-13
- [x] Golden rules globales (s3-safety, duckdb, nextflow, secrets) — 2026-04-13
- [x] CLAUDE.md global réécrit (profil Boris) — 2026-04-13
- [x] MCP installés (pubmed, duckdb, memory, ensembl, ncbi, s3) — 2026-04-13
- [x] Hooks (protection S3, notification) — 2026-04-13
- [x] Veille scientifique automatisée (cron + skill /veille) — 2026-04-13
- [x] Skill export-gsheet trace-prod — 2026-04-13
- [x] Profil utilisateur complet (technique + scientifique) — 2026-04-13

**Why:** Issue de la rétrospective complète Claude Code du 13/04/2026 (Phases 1-4).
**How to apply:** Consulter cette liste en début de session quand Boris demande "quoi faire" ou "prochaine tâche". Mettre à jour quand une tâche est complétée.
