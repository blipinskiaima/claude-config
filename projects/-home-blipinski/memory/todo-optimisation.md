---
name: Todo optimisation Claude Code & projets
description: Liste des tâches en cours (par priorité) et historique des tâches complétées (par jour).
type: project
originSessionId: 129fb3f7-7613-4550-adf0-9392306d8a85
---
# Todo — Optimisation Claude Code & Projets

**Dernière mise à jour : 2026-04-14**

---

# Partie 1 — À faire (par priorité)

## Haute priorité

- [ ] **Sécurité secrets — étape 1** : migrer `~/Pipeline/export/` vers des fichiers `.env` avec `chmod 600`. Documenter le pattern pour les autres projets (tokens Tower dans nextflow.config).
- [ ] **Harmoniser les protocoles wet-lab CGFL/HCL** — négociation labos sur kit extraction (Apostle vs Maxwell) et kit barcoding (NBD114-96 vs NBD114-24). Long terme, mais seule solution durable.

## Moyenne priorité

### Skills bioinformatiques
- [ ] **Skill /audit-trail** — traçabilité ISO 15189 : changelog formaté, diff avant/après, hash containers, résultats non-régression.
- [ ] **Prompts analyse scientifique** — skills /compare-batches, /qc-report, /correlation pour analyses récurrentes.
- [ ] **Améliorer skills v1 avec /meta-skills-creator** — sample, debug-nf, check-consistency sont fonctionnels mais créés sans le processus rigoureux. Raffiner après usage.

### Projets bioinformatiques
- [ ] **Améliorer Aima-Tower** — dashboard interactif pour biologistes :
  - [ ] Intégrer IGV.js via dash-bio (visualisation bedMethyl)
  - [ ] Graphiques interactifs avec seuils de spécificité ajustables
  - [ ] Statistiques par sous-ensembles (centre, type tumoral, VAF)
  - [ ] Enrichir les agents IA d'Aima-Tower avec features DB
  - [ ] Module exploratory-analysis embarqué
- [ ] **Explorer MethylBERT** — Transformer read-level (Nat Comm 2025) pour améliorer sensibilité basse VAF (<5%). Nécessite GPU. ~2-3 jours.
- [ ] **Documenter le biais technologique EPIC→ONT** dans le dossier qualité ISO — finding clé de l'investigation batch effect. Le modèle raima V1 est calibré sur EPIC, pas ONT.

## Basse priorité

- [ ] **Sécurité secrets — étape 2** : installer `gitleaks` en pre-commit hook sur les projets gittés.
- [ ] **Sécurité secrets — étape 3** : évaluer un gestionnaire de secrets (sops, age, vault).
- [ ] **Skill save-code pour trace-prod** — automatiser la sauvegarde de session.
- [ ] **Projet veille-scientifique : automatisation complète** — remplacer les MCP inexistants (DuckDB, S3, Ensembl, NCBI) par des skills ou scripts, enrichir l'analyse des abstracts par Claude, intégrer les résultats dans un dashboard.
- [ ] **Agent de veille enrichi** — ajouter l'analyse automatique des abstracts par Claude (pertinence AIMA).
- [ ] **Skills Pod2Bam** — créer test/qualif/maj analogues à Bam2Beta. Pas urgent tant que Pod2Bam n'est pas soumis à audit qualité.

---

# Partie 2 — Complété (par jour)

## 2026-04-14 — Investigation batch effect CGFL vs HCL

- [x] **Investigation systématique batch effect CGFL vs HCL** — exploration de 12 pistes via trace-prod + exploratory-analysis + lecture BAM/bedMethyl :
  - composition biologique (Cat 1/2/3/4, VAF panel)
  - kit barcoding (NBD114-96 vs NBD114-24) — confounded
  - kit extraction (Apostle vs Maxwell) — confounded, Maxwell n'a PAS plus de gDNA long (hypothèse inverse)
  - version Dorado / GPU — pas significatif en v5.0.0
  - couverture — FP stables à toutes profondeurs
  - taille des fragments — CGFL a en fait des reads plus longs (mean 260bp vs 222bp)
  - fragmentomics mode1 — artefact des rebasecallés, pas un batch effect
  - modkit auto-threshold — déjà testé, ne change rien
  - score CNV — batch effect confirmé (matrice 100% CGFL dans raima)
  - ichorCNA — OK, corrèle avec charge tumorale
  - déconvolution Loyfer — distributions proches
  - profil cfDNA FP HCL — signal tissulaire subtil (moins de blood_0)
  - Voir `~/.claude/projects/-home-blipinski-Pipeline-Bam2Beta/memory/batch-effect-investigation.md`
- [x] **Création projet `~/Pipeline/ComBat-Met/`** — CLAUDE.md, .claude/rules, Docker (R 4.4 + ComBatMet 0.99.3), 9 scripts R/bash pour extraction, correction, scoring parallèle.
- [x] **Test ComBat-met** — 4 variantes testées (group=H/C, rebalancé, ref.batch=CGFL, Healthy only). **Aucune ne fonctionne**. Finding inattendu : la simplification du bedMethyl seule réduit 17% → 3% FP HCL sans ComBat-met.
- [x] **Identification du vrai problème** : biais technologique EPIC → ONT. Raima V1 entraîné sur 19 références EPIC bisulfite microarray, pas sur ONT. CGFL matche par hasard ces références, HCL s'en éloigne.
- [x] **Conclusion ComBat-met** : **non retenu pour la production**. Documenté dans `~/Pipeline/ComBat-Met/README.md`. Dépendance batch-spécifique incompatible ISO 15189 + simplification technique suffit pour 80% du problème.
- [x] **Mise à jour mémoire Claude** : `batch-effect-investigation.md` + pointeur dans MEMORY.md Bam2Beta.
- [x] **Restructuration todo list** : séparation tâches à faire (par priorité) / tâches complétées (par jour).

## 2026-04-13 — Rétrospective et setup Claude Code

- [x] **Nettoyage config Claude** — skills, plugins, agents dupliqués supprimés.
- [x] **Golden rules globales** — s3-safety, duckdb, nextflow, secrets dans `~/.claude/rules/`.
- [x] **CLAUDE.md global** — profil Boris (bioinfo AIMA, bus factor 1) réécrit.
- [x] **MCP installés** — pubmed, duckdb, memory, ensembl, ncbi, s3.
- [x] **Hooks** — protection S3, notification.
- [x] **Veille scientifique automatisée** — cron + skill `/veille`.
- [x] **Skill `/export-gsheet`** pour trace-prod.
- [x] **Profil utilisateur complet** — technique + scientifique dans `~/.claude/projects/-home-blipinski/memory/`.
- [x] **Skills bioinformatiques v1** — `/sample`, `/debug-nf`, `/check-consistency`, `/batch-effect`.
- [x] **Références techniques** — bedMethyl, troubleshooting, stats-guide, dorado-reference.md.
- [x] **Contexte pipeline AIMA** dans 7 CLAUDE.md projets.
- [x] **Instructions compaction intelligente** — garder fichiers modifiés, commandes testées, décisions, état runs NF, bugs.
- [x] **Aliases et template CLAUDE.md** standardisés.
- [x] **Agent explore bioinfo** avec détection automatique Phase 6.

---

**Why:** Issue de la rétrospective complète Claude Code du 13/04/2026 + investigation batch effect du 14/04/2026. Format 2-parties pour distinguer ce qui reste à faire de ce qui est déjà tracé en historique.
**How to apply:** Consulter la Partie 1 en début de session quand Boris demande "quoi faire" ou "prochaine tâche". Ajouter en tête de Partie 2 à chaque fin de session avec la date.
