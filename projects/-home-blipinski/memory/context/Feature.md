# Context — Feature — 2026-06-18

**Branche** : main (Feature/ @ 1a90cac, poussé) — Aima-Tower main @ 5255ac9, poussé
**Status** : clean (sauf result_old/ untracked dans Feature/, .claude/worktrees/ dans Tower)

## Où j'en suis
Feature **dimension depth** livrée end-to-end sur 2 repos (via code-workflow-feature → brainstorming → plan → subagent-driven). Décline sens/spéc à `depth >= 0.25/0.5/1/2X` à l'éval, en plus de `target_spec`.

## Ce qui marche / ce qui foire
- ✓ Feature/ : `select_cohort_*.py` +depth, `train.R` passthrough, `eval.R --depths`, `main.sh` câblé. `result/speedvac_{no,yes}/` régénérés (1023 combos, 0 échec, eval_kpis 147312 lignes). Scores XGBoost bit-identiques (prouvé golden).
- ✓ Aima-Tower : `/exploration-beta` `<select>` Profondeur ; backend feature_service/feature_curves/router + hooks. Tables filtre depth==, courbes recalc depth>=. typecheck+build OK.
- ✓ WIP "section stades Lung-DI" non-committé dans Tower → committé d'abord (952f7ee) puis depth (5255ac9).
- ⚠ Slider non vérifié visuellement (build seul) — Boris validera après redeploy.
- ⚠ Caveat depth haute : peu de healthy à 2X (no=29) → seuil quantifié.

## Prochaine étape
Au besoin : redeploy Tower (docker-restart) pour voir le slider live ; analyser les KPIs par depth (gain sens à profondeur croissante ?). Détails : [[depth-dimension]].
