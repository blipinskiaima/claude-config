# Context — Feature — 2026-07-03T13:10:30+0000

**Branche** : main
**Dernier commit** : 1086238 — docs(eval): documente --exclude-bladder (README + CLAUDE.md)
**Status** : clean (untracked : "result backup/" pré-existant)

## Où j'en suis
Ajout du flag `--exclude-bladder` à eval.R terminé et livré : retire le Bladder sang
(52 samples, cohort=='Bladder') des unités KPI `active`/`active_nomut`. `eval_kpis.csv`
des 2 variantes speedvac régénérés, Tower sert la vue sans-bladder après refresh.
Code + doc committés et poussés (867e4f2..1086238).

## Ce qui marche / ce qui foire
- ✓ Flag `--exclude-bladder` (défaut OFF rétro-compat, activé dans main.sh)
- ✓ Delta vérifié : Sens_Active_NoMut +2 à +6 pts (bladder = cas difficiles, PAS gonflage)
- ✓ Tower relit live (bind mount /pipeline:ro, pas de cache, pas de rebuild)
- ✓ Backups avec-bladder conservés (eval_kpis_withbladder_*.csv)
- ⚠ Bladder restent dans le TRAIN (modèle inchangé) — retirés du KPI seulement (cas 1)

## Prochaine étape
Comparer avec/sans bladder sur les autres targets (0.90, 0.98) et depths si besoin ;
ou évaluer le « cas 2 » (modèle entraîné sans bladder) si l'écart justifie un retrain.
