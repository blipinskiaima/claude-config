# Context — trace-prod — 2026-05-26T12:43:40+00:00

**Branche** : main
**Dernier commit** : 3ff5373 — feat: export-short-read-like — gsheet fusionnée CGFL+HCL liquid (13 cols)
**Status** : 14 fichiers untracked (artifacts dev/backup DB/rapports HTML, non-pertinents)

## Où j'en suis
Schema v8 trace-prod complètement livré + son export gsheet associé. Table `short_read_metrics` (28 colonnes) + commande `check-short-read` (commit `9af554b`) puis nouvel export `export-short-read-like` (commit `3ff5373`) qui fusionne CGFL+HCL liquid (1199 samples) vers l'onglet 'Short Read Like' de la gsheet trace-prod, avec mVAF v1 initial côte à côte avec mVAF v1 short read pour comparaison directe.

## Ce qui marche / ce qui foire
- ✓ Backfill complet : 426/728 CGFL + 384/471 HCL avec mvaf_v1 short read extraite. Reste 302 CGFL + 87 HCL à compléter quand le pipeline short read aura tourné.
- ✓ Export gsheet 'Short Read Like' validé (1199 lignes), pattern strictement aligné sur export-ont-samples
- ✓ mVAF v1 initial vs short read côte à côte (ex: sample 26BM01841 → 1,3870 vs 1,3110 — proches mais différents, comparaison pertinente)
- ✓ ShortReadChecker hérite de BaseChecker, override seulement 4 méthodes (prefix "merged" → "minLen75_maxLen200")
- ⚠️ Précision ichorcna_short_read tronquée à 4 décimales par DECIMAL(10,4). Acceptable, documenté. Bumper en DECIMAL(10,6) si tumor fractions très faibles deviennent critiques.

## Prochaine étape
Décision Boris : (a) relancer `check-short-read liquid CGFL` + `liquid HCL` quand le pipeline short read aura progressé (UPSERT idempotent remplit les NULLs), (b) analyser les corrélations mvaf_v1 initial vs short read sur la gsheet 'Short Read Like' (régression linéaire, biais systématique), (c) commencer une nouvelle feature, (d) bump précision ichorcna en DECIMAL(10,6).
