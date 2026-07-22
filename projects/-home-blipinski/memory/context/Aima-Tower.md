# Context — Aima-Tower — 2026-07-22 (clôture session)

**Branche** : main (push OK origin/main)
**Dernier commit** : 486e043 — docs: page /reproductibilite + onglet Suspects manquant
**Status** : clean (hors `.claude/worktrees/` untracked, hors scope)

## Où j'en suis
Page **/reproductibilite** livrée et déployée en prod (2 commits : feat 8088a4e + docs
486e043). Dispersion de plusieurs mesures d'un même prélèvement, 2 onglets (réplicats
purs / kits d'extraction), 3 modèles dont themelio, métriques CV + accord des verdicts.
Session close via /end-session.

## Ce qui marche / ce qui foire
- ✓ 61 tests verts, typecheck 0, conteneur healthy, 3 routes 200
- ✓ themelio branché : `retd_suivis.themelio_score` renseigné pendant la session
  (job `update-column themelio_score liquid CGFL`), 56/56 en pure, 28/28 en extraction
- ✓ Archéologie des suffixes trace-prod résolue → mémoire `reproducibilite_page.md`
  (« moche » = rangement POD5 hors chemins S3 standards, **pas** un défaut qualité)
- ℹ Résultat marquant : le **kit d'extraction pèse bien plus lourd que le run** —
  CV médian 26,2 % / accord 19/30 en extraction, contre 1,2 % / 44/48 en pure
- ℹ Divergence assumée avec le R : `05_replicate_concordance_98pct.R` inclut les `_OK`
  dans `REPLICATE_SUFFIXES`, Tower les exclut des stats (même run_id → effet de
  profondeur). À trancher côté R si on veut aligner un jour.
- ℹ Gotcha : les jobs `check_samples.py update-column` tiennent le lock DuckDB plusieurs
  minutes → fixture `svc` dans les tests bascule sur une copie. Le code de prod n'a pas
  ce filet (`DuckDBMixin` retry 5×/7,5 s seulement).

## Prochaine étape
Rien en cours. Pistes d'approfondissement discutées et **non implémentées** :
reproductibilité **inter-centre** CGFL vs HCL (les Colon_17..24 existent aussi en HCL,
corpus déjà disponible) et lien **dispersion ↔ profondeur** (table `rarefaction` de
trace-prod, 1355 lignes × 5 niveaux, déjà remplie). Bland-Altman/ICC écartés pour
l'instant : 2 à 6 réplicats par famille, puissance statistique trop faible.
