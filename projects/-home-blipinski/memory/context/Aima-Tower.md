# Context — Aima-Tower — 2026-06-09T08:16:09+00:00

**Branche** : main
**Dernier commit** : b18c572 — feat(v4.3.0): page /exploration-beta — connexion pipeline Feature (lecture seule)
**Status** : clean (seul `.claude/worktrees/` untracked, exclu volontairement)

## Où j'en suis
Feature `/exploration-beta` terminée, committée (v4.3.0) et déployée en conteneur (live).
Connexion Tower → pipeline `~/Pipeline/Feature` en **lecture seule** : sélection de features →
affichage CSV (Combined coloré vs baseline mVAF) + PNG + best combos top 5 + état cohorte std_359.
Dev itératif validé par Boris à chaque étape. Session clôturée via /end-session.

## Ce qui marche / ce qui foire
- ✓ 4 endpoints `/api/exploration-beta/{result,png,best-combos,cohort-info}` testés en conteneur
- ✓ Lecture read-only `feature_runs.duckdb` via mount `/pipeline:ro` + réécriture path `/home/blipinski/Pipeline`→`/pipeline`
- ✓ `best_combo` répliqué en SQL read-only (subprocess impossible : `connect()` ouvre en write → KO sur `:ro`)
- ✓ `normalize_features` == benchmark pipeline (ordre de sélection indifférent), prouvé empiriquement
- ✓ typecheck + build verts, conteneur healthy, MAJ DB sans restart (bind-mount live)
- ✗ Rendu visuel non vérifié par moi (pas de navigateur) → à confirmer par Boris (couleurs Combined, tables, PNG)
- ⚠ Exécution réelle du pipeline depuis Tower NON faite (par design : Tower = reader)

## Prochaine étape
Boris valide le rendu visuel de `/exploration-beta`. Évolution possible (écartée cette session) :
daemon hôte pour une vraie exécution one-click du pipeline (Option B).
