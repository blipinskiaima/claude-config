# Context — trace-prod — 2026-07-22T14:50:00+0000

**Branche** : main
**Dernier commit** : 6b22116 — feat: schema v19 — too_predicted_class + too_final_decision
**Status** : clean (synchro origin/main, 15 commits pushés cette session dont rattrapage rarefaction v16/v17)

## Où j'en suis
Deux features ajoutées via /add-trace-prod (calque themelio → too), développées pas-à-pas (A→D validées une par une), documentées, committées, pushées, backfillées et exportées gsheet. Session terminée, rien d'engagé.

## Ce qui marche / ce qui foire
- ✓ Schema v18 `themelio_score` : CSV THEMELIO/{s}.themelio_predictions.csv L2C2, format_comma précision complète, liquid only. Backfill 1322 liquid + export OK (1re tentative).
- ✓ Schema v19 `too_predicted_class` (col 9) + `too_final_decision` (col 20) : parsing module csv OBLIGATOIRE (virgule interne dans confidence_stratum col 10). Backfill 1323 liquid + export OK. Éventail : Lung 549, Bladder+Pancreas 370, Colon 256, Breast 95, Prostate 53.
- ✓ Chemins réels : dossier direct sous le sample (THEMELIO/ et TOO/, PAS OUTPUT/). Fichier too `.too5_predictions.csv` un seul point.
- ⚠ 147 lignes solid à 'KO' sur les colonnes liquid-only = normal (jamais exportées, défaut DDL non écrasé).

## Prochaine étape
Rien d'engagé. Si demande future : les colonnes too/themelio passent aussi par le `check` général (câblées LiquidChecker), donc remplies automatiquement pour les nouveaux samples.
