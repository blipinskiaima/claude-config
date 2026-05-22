# Context — trace-prod — 2026-05-22T12:12:50+00:00

**Branche** : main
**Dernier commit** : 9af554b — feat: schema v8 — table short_read_metrics + CLI check-short-read
**Status** : 14 fichiers untracked (artifacts dev/backup DB/rapports HTML, non-pertinents)

## Où j'en suis
Feature schema v8 terminée, committée et pushée. Nouvelle table `short_read_metrics` (28 colonnes : 10 DECIMAL + 16 probs v1 + sample_id + updated_at) alimentée par la commande CLI dédiée `check-short-read {liquid} {CGFL|HCL}`, indépendante du `check` standard. Backfill complet déjà lancé sur les 2 labos (CGFL 426/728 avec mvaf_v1 extraite, HCL 384/471).

## Ce qui marche / ce qui foire
- ✓ Schema v8 + migration idempotente (CREATE TABLE IF NOT EXISTS dans ALL_TABLES)
- ✓ ShortReadChecker hérite de BaseChecker, override seulement 4 méthodes (get_cramino_reads, get_epic_reads, get_depth, get_coverage) avec `self._PREFIX = "minLen75_maxLen200"` au lieu de `"merged"` — copie 1:1 du pattern initial
- ✓ Smoke tests 2 samples (Bladder_Blood_01_001 CGFL + Colon_1 HCL) — valeurs cohérentes
- ✓ Sync delete_sample + compact() pour inclure la nouvelle table
- ✓ Doc CLAUDE.md + README.md + MEMORY.md + topic file project_schema_v8 à jour
- ⚠️ Précision ichorcna tronquée à 4 décimales par DECIMAL(10,4) (ex: 0.008966 → 0.0090). Acceptable mais documenté. Bumper en DECIMAL(10,6) si tumor fractions très faibles deviennent critiques.

## Prochaine étape
Décision Boris : (a) bump précision ichorcna_short_read en DECIMAL(10,6), (b) commencer une nouvelle feature, ou (c) creuser l'analyse des données short read backfillées (corrélations mvaf v1 initial vs short read, distribution par cohorte).
