# Context — Aima-Tower — 2026-06-10T18:00:00+02:00

**Branche** : main
**Dernier commit** : 6048729 — feat(exploration-beta): courbes Plotly 6 facettes + CSV legacy reconstruit
**Status** : clean (origin/main synchronisé)

## Où j'en suis
Intégration Feature → Tower `/exploration-beta` **terminée** : courbes Plotly 6 facettes (5 strates train + Alc),
CSV legacy reconstruit, schéma DB `runs`+`eval_kpis`, cohorte `std_335`. UI polie (grille cartes, légende HTML,
sans barre Plotly, axes Y 0–100 % / X 80–100 %). Conteneur rebuild + redéployé.

## Ce qui marche / ce qui foire
- ✓ `feature_curves.py` : parité `eval_v2.r` (quantile type=1, grille spec, 6 strates dont Alc)
- ✓ `feature_service.py` : lit `runs`+`eval_kpis`, fallback `results`, reconstruit CSV + courbes JSON
- ✓ Frontend `FeatureSensitivityChart.tsx` : 6 mini-panneaux, labels hors Plotly, tooltips sens/spec
- ✓ API smoke test OK (mvaf_v1 : 2 csv_rows, 252 points courbe)
- ✓ Tower redéployé (docker compose build + up)
- ⚠ Bench Feature `main_bench.sh` tourne en tmux (BL2) — pas bloquant Tower

## Prochaine étape
Vérifier visuellement `/exploration-beta` sur quelques combos bench (pas seulement mvaf_v1). Commit Aima-Tower poussé.
