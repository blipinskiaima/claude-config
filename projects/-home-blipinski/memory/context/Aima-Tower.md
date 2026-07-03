# Context — Aima-Tower — 2026-07-03 (clôture session)

**Branche** : main (push OK origin/main)
**Dernier commit** : 107c636 — feat(exploration): toggle Score mVAF v1 / v1.4 sur toute la page
**Status** : clean (hors `.claude/worktrees/` untracked, hors scope)

## Où j'en suis
Feature livrée : toggle **Score mVAF v1 / v1.4** sur `/exploration`, pilotant toute la page
(tables Sens/Spé + graphes) via param `score_source`. 2 commits pushés : fix bug pré-existant
(4 endpoints graphes morts) + feat. Session close via /end-session.

## Ce qui marche / ce qui foire
- ✓ Toggle fonctionnel bout-en-bout (validé live conteneur : v1 78.5%/88.4%, v1.4 81.7%/85.3%)
- ✓ mvaf_v14 lu depuis retd_suivis (VARCHAR virgule FR), KO→exclu cohorte (~8 cancers en moins)
- ✓ 4 endpoints graphes (qc/dotplot/methylation/bladder) réparés (étaient morts sur main)
- ✓ Conteneur healthy redéployé, docker-restart OK
- ℹ Gotcha : `_load_from_duckdb` connecte read_only SANS retry → 500 pendant un job trace-prod
  qui tient le lock write (`check_samples update-column`). Tester sur copie de la DB.

## Prochaine étape
Rien en cours. Feature terminée. Si besoin d'un score_source supplémentaire (mvaf_v13...),
le pattern est en place : ajouter la colonne au parsing + option ScoreSource front.
