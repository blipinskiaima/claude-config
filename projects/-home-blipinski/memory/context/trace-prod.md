# Context — trace-prod — 2026-07-03T12:56:10+0000

**Branche** : main
**Dernier commit** : b9abd0c — feat: schema v14 (bootstrap_props) + v15 (dilution enrichie) + mode probs --probs_bootstrap
**Status** : clean (tracké)

## Où j'en suis
Session multi-features (3 sessions Claude //), tout committé b9abd0c. Livré : colonne `bootstrap_props` (v14), table `dilution` enrichie (v15, session //), mode `probs --probs_bootstrap` (epic = moyenne 200 réplicats bootstrap). Backfills + exports gsheet faits.

## Ce qui marche / ce qui foire
- ✓ `bootstrap_props` (v14) : OK/KO présence `bootstrap_v1.props.tsv`, liquid, calque `bootstrap` v12. Backfill CGFL 804 + HCL 513 + exports.
- ✓ Mode `probs --probs_bootstrap` : epic = moyenne bootstrap (vérifié == awk), backfill CGFL 791/804 + HCL 502/513, préserve loyfer, réversible via `probs --probs`.
- ✓ Backfill `mvaf_v14` (1305) + v15 dilution (`check-dilution` 480 + `export-dilution`) faits.
- ✗ `APIError 503` gspread transient a cassé une chaîne `&&` de tmux (export-dilution) → rattrapé à la main.
- ⚠ Enrichissement EPIC raté sur des `Bladder_Urine` (epic ~0, mVAF non fiable) — investigation mise de côté.

## Prochaine étape
Rien d'engagé. Optionnel : helper retry(3×) gsheet réutilisable (503 récurrent) ; reprendre l'investigation enrichissement EPIC.
