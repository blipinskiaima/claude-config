# Context — Aima-Tower — 2026-06-10T08:56:21+00:00

**Branche** : main
**Dernier commit** : 3de8681 — feat(exploration-beta): top N configurable + filtres présence/absence des best combos
**Status** : README.md modifié (v4.4.0, working tree) ; sinon main == origin/main

## Où j'en suis
Page `/exploration-beta` complète et en prod. Tout poussé sur main :
- Base v4.3.0 (b18c572) : features → CSV (Combined coloré vs mVAF) + PNG + best combos top 5 + état cohorte std_359, lecture seule de `feature_runs.duckdb`
- Fix cache refetch (eac709f, cette session) : reclic Exécuter sur même sélection force un `refetch()`
- Raffinements (session parallèle) : diagramme Venn composition cohorte, top-N configurable (5/10/20/50) + filtres présence/absence des best combos, clic sur un combo coche ses features + charge son résultat, colonnes nb_healthy/nb_cancer masquées du CSV

## Ce qui marche / ce qui foire
- ✓ Lecture read-only `feature_runs.duckdb` via mount `/pipeline:ro`, MAJ DB sans restart
- ✓ Fix refetch validé (combo `mvaf_v1,frag_score_v2_sc` trouvé après recalcul)
- ✓ `best_combo` répliqué read-only, `normalize_features` == benchmark pipeline
- ✓ README bumpé **v4.4.0** documentant les 4 raffinements (modif working tree à committer)
- ⚠ CLAUDE.md table Pages décrit la version de base de `/exploration-beta` (raffinements pas encore reflétés — optionnel)
- ⚠ Exécution réelle du pipeline depuis Tower NON faite (par design : Tower = reader)

## Prochaine étape
Committer la modif README v4.4.0. Évolution possible : daemon hôte pour vraie exécution one-click (Option B, écartée).
