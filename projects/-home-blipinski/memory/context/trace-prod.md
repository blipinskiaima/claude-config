# Context — trace-prod — 2026-06-04 14:40 UTC

**Branche** : main
**Dernier commit** : ebf738b — refactor: export liquid — retrait 8 colonnes + Mode1/Mode2 arrondis 2 déc
**Status** : clean côté code (untracked = backup DB/CSV/rapports, hors scope)

## Où j'en suis
Session de nettoyage de l'export gsheet liquid TERMINÉE et pushée. Deux features
distinctes commitées séparément : (A) schema v10 frag softclipped — code qui était
non commité en début de session, (B) nettoyage export liquid de cette session.

## Ce qui marche / ce qui foire
- ✓ Lot A (59dafcb) : schema v10 frag_sc committé (code + CLAUDE.md + README 3 lignes)
- ✓ Lot B (ebf738b) : export liquid — 8 colonnes retirées (mVAF v1.2/v2, Score CNV, Frag Mode1/2, Sex Proba, Rarefaction, FRAG), Frag Mode1/2 SC → Mode1/Mode2, arrondi 2 décimales
- ✓ Découpage 2 commits via reconstruction d'état intermédiaire (revert Lot B → commit A → restore Lot B → commit B), les 2 lots s'entrecroisaient dans utils.py/duckdb.py
- ✓ Export gsheet poussé en cours de session : CGFL 753 + HCL 472 (onglets liquid à jour)
- ✓ `format_round2_comma()` (lib/utils.py) : arrondi virgule française, KO/NA inchangés
- ✗ Solid volontairement inchangé (décision Boris : nettoyage liquid only)

## Prochaine étape
Rien en attente. Au besoin : étendre le nettoyage/renommage à l'export solid si décidé,
ou peupler frag_sc via `check`/`update-column frag_status_sc liquid {labo}`.
