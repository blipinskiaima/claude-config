# Context — Feature — 2026-06-18

**Branche** : main (Feature/ @ 3a03181, poussé) — Aima-Tower main @ 5255ac9, poussé + déployé
**Status** : clean (result_old/ untracked hors session)

## Où j'en suis
Feature dimension depth livrée end-to-end sur 2 repos (code-workflow-feature → brainstorming → plan → subagent-driven). Décline sens/spéc à depth >= 0.25/0.5/1/2X à l'éval, en plus de target_spec. Tower redéployée (docker), slider live.

## Ce qui marche / ce qui foire
- ✓ Feature/ : select_cohort +depth, train.R passthrough, eval.R --depths, main.sh. result/{no,yes} régénérés (1023 combos, eval_kpis 147312 lignes). Scores XGBoost bit-identiques (golden).
- ✓ Aima-Tower : <select> Profondeur dans /exploration-beta (tables depth==, courbes depth>=). Smoke live API OK (294→247). Stack redéployée, healthy.
- ✓ Docs (README+CLAUDE.md) + mémoire (depth-dimension.md) à jour.
- ⚠ Slider non vérifié à l'œil par Boris ; caveat peu de healthy à 2X (no=29).

## Prochaine étape
Au besoin : analyser le gain de sensibilité à profondeur croissante (active_nomut, lung stades) en lisant eval_kpis.csv par depth. Détails : [[depth-dimension]].
