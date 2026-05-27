# Context — trace-prod — 2026-05-26T14:00:00+00:00

**Branche** : main
**Dernier commit** : 3ff5373 — feat: export-short-read-like — gsheet fusionnée CGFL+HCL liquid (13 cols)
**Status** : clean (code), 14 untracked (artifacts dev/backup/rapports HTML, non-pertinents)

## Où j'en suis
Session de maintenance DB après livraison schema v8 + export Short Read Like. Suppression de 5 samples Twist test (Twist_0%/0.1%/0.25%/0.5%/1%) demandés par Boris, conservation de `Twist_1pct`. Re-export liquid CGFL → gsheet (737 samples). Aucune modification de code.

## Ce qui marche / ce qui foire
- ✓ 5 samples Twist supprimés (cascade sur toutes les tables liées via `delete_sample()` qui inclut bien `short_read_metrics` depuis le sync v8)
- ✓ `Twist_1pct` confirmé toujours en DB (le bon Twist à garder)
- ✓ Export liquid CGFL pushé sur gsheet : 737 samples (728 initiaux + N nouveaux entre les sessions − 5 Twist supprimés)
- ⚠️ Précision ichorcna_short_read tronquée à 4 décimales (DECIMAL(10,4)) — décision encore en attente si on bumpe à (10,6)

## Prochaine étape
Décision Boris : (a) relancer `check-short-read liquid {labo}` quand le pipeline short read aura progressé (UPSERT idempotent remplit les NULLs), (b) analyser les corrélations mvaf_v1 initial vs short read sur la gsheet 'Short Read Like', (c) commencer une nouvelle feature, (d) bump précision ichorcna en DECIMAL(10,6).
