# Context — trace-prod — 2026-09-08T10:03:29+00:00

**Branche** : main
**Dernier commit** : 560622b — refactor: étiquettes d'export Nb reads total/Nb read alignés → Nb lignes total/Nb molécule
**Status** : 5 fichiers modifiés (lots v33 `dilution_lung` + `EXPORT_HIDDEN_SAMPLES` d'autres sessions,
non commités) + `lib/checkers_dilution_lung.py` untracked + backups/CSV/HTML habituels

## Où j'en suis
Session 03→08/09. (1) Probs epic bootstrap + Loyfer 28M : 119 urine chargés, puis audit exhaustif
des 1509 samples (fichiers sources relus) → liquid 100 % conforme (1 seul HCL corrigé,
`Healthy_11_rebasecalled_V5.2.0`), solid : 25 Loyfer comblés, epic solid gardées en v1.3 (0 dossier
BOOTSTRAP en solid, choix Boris). (2) 8 Twist `_rep_3` créés (`check`) + probs + exports.
(3) Renommage d'étiquettes `Nb lignes total` / `Nb molécule`, 6 onglets ré-exportés et relus,
commit 560622b (staging partiel, les lots des autres sessions laissés en place).

## Ce qui marche / ce qui foire
- ✓ `probs` : liquid 857 CGFL + 513 HCL = epic bootstrap + Loyfer, 0 trou ; solid 147 Loyfer, 49 epic NULL (aucune source)
- ✓ 6 onglets relus : nouvelles étiquettes partout, aucune ancienne
- ✗ `raima/R/evaluate-score.R:237,240` (+ `exploratory-analysis` misc/dev) lisent l'export par l'ancien
  en-tête `Nb reads total` → casseront au prochain `download_trace_prod_metadata()`
- ✗ Les 8 Twist `_rep_3` n'ont pas de metadata (`import-metadata` non lancé, hors demande)
- ✗ Lock DuckDB très disputé (3 sessions en parallèle) : toujours un retry sur « Could not set lock » ;
  une connexion `read_only` attend autant qu'un writer

## Prochaine étape
Adapter les lectures par en-tête de `raima` / `exploratory-analysis` avant tout re-téléchargement ;
laisser la session v33 committer son lot (`dilution_lung` + `EXPORT_HIDDEN_SAMPLES`).
