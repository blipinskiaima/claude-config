# Context — Feature — 2026-06-03

**Branche** : main
**Dernier commit** : e5d7d1e — refactor: pipeline minimal train.R + eval.R, archive ancien grid
**Status** : clean (poussé origin/main)

## Où j'en suis

Pipeline Feature simplifié en production : `scripts/train.R` (trace-prod preset `lung_valtech_nosv_bladder_blood` + XGBoost OOF) → `scripts/eval.R` (5× Sens_* + PNG). Run de référence `result/combo_sc_test/` (4 features : mvaf_v1, ichor_x100, frag_mode1_sc, frag_mode2_sc). Ancien grid 01–06 sous `archives/`.

## Ce qui marche / ce qui foire

- ✓ Entonnoir cohorte documenté : 1224 liquid → 486 SQL → 475 depth → 335 labellisés eval (50 H, 285 cancer)
- ✓ 192 healthy historique vs 50 = preset études + exclusion SpeedVac (160 HCL Val tech)
- ✓ eval aligné : 5 facettes = 5 colonnes CSV ; définitions Sens_Active / mutés non actifs (15) clarifiées
- ✗ Package R `duckdb` non installé — contournement python3 OK dans train.R
- ✗ `note.txt` / prompts locaux non versionnés (gitignore)

## Prochaine étape

Option A : log effectifs par filtre dans `train.R` ; Option B : réintégrer grid search ou nouvelles features (frag v2 trace-prod) ; Option C : élargir preset cohorte si besoin de ~192 healthy.
