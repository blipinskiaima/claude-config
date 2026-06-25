# Context — Aima-Tower — 2026-06-25 (clôture session)

**Branche** : main (push OK origin/main)
**Dernier commit** : 9a87362 — feat(combined): ajoute mvaf_v14 au sélecteur Features
**Status** : clean (hors `.claude/worktrees/` untracked, hors scope)

## Où j'en suis
Session courte close : ajout de la feature mVAF 1.4 (`mvaf_v14`) au sélecteur Features de `/combined`.
1 ligne ajoutée à `FEATURE_NAMES` (combined-data.ts) + commentaire obsolète rafraîchi + note CLAUDE.md.
Buildé, déployé (conteneur healthy), commité/pushé. Clôture `/end-session` en cours (reste commit-claude + maj-todo).

## Ce qui marche / ce qui foire
- ✓ `mvaf_v14` visible dans le sélecteur `/combined` (confirmé dans le bundle JS servi)
- ✓ Combos mvaf_v14 déjà calculés côté Feature (scores.csv speedvac_no + speedvac_yes) → lookup OK
- ✓ Build front vert + conteneur redéployé healthy (`Application startup complete`, port 8050)
- ✓ Commit 9a87362 pushé sur origin/main
- ℹ Gotcha gravé : `FEATURE_NAMES` est une liste figée à synchroniser **à la main** avec `Feature/script/main.sh` (pas de lecture dynamique ; `features_disponibles.tsv` supprimé)

## Prochaine étape
Rien en cours. À la prochaine feature ajoutée côté pipeline Feature, penser à l'ajouter manuellement dans combined-data.ts.
