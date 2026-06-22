# Context — Aima-Tower — 2026-06-22T17:49:04+00:00

**Branche** : main (push OK origin/main)
**Dernier commit** : 80f6330 — feat(combined): onglet Dilution piloté par le combo + retrait page /dilution
**Status** : clean (hors `.claude/worktrees/` untracked, hors scope)

## Où j'en suis
Session terminée sur 2 features livrées + déployées + pushées : (1) refonte page **Combined** (ex-exploration-beta, commit `0fb9357`) et (2) **onglet Dilution** dans Combined piloté par le combo sélectionné (commit `80f6330`). Tower redéployée (docker), smoke-testée OK. En cours de clôture via `/end-session` (reste commit-claude + maj-todo).

## Ce qui marche / ce qui foire
- ✓ `/combined` : 3 onglets Résultat (Initial / Lung-DI / **Dilution**), panneaux Cohorte retirés, défaut SpeedVac, params d'éval à gauche
- ✓ Onglet Dilution : source **unique** `scores.csv` (unité `dilution`, archi α), marche mono ET multi-features (XGBoost) ; smoke prod OK (mvaf_v1 seuil 0.6906 ; mvaf_v1,ichor_x100 seuil 0.7627 proba [0,1])
- ✓ Page `/dilution` autonome supprimée ; `DilutionChart`+`DilutionPoint` conservés
- ✓ Build/tsc/py_compile verts ; endpoints `/api/combined/*` OK, ancien `/api/dilution` → 404
- ⚠ Vérif **visuelle** du rendu de l'onglet Dilution pas encore faite par Boris (data validée, chart non vu)
- ⚠ `Twist_10_8` exclu du scoring → d8 absent de l'axe (vs trou avant) — accepté

## Prochaine étape
Vérif visuelle Boris sur `tower.aima-diagnostics.com/combined` (choisir un combo → onglet Dilution). Sinon, rien en cours : les 2 features sont closes.
