# Context — trace-prod — 2026-07-30T21:20:02+00:00

**Branche** : main
**Dernier commit** : 1a8e05e — feat: export-cohort — audit d'inclusion cohorte Sens/Spé
**Status** : clean (untracked préexistants only : backups .duckdb, CSV dev/, rapports HTML)

## Où j'en suis
Deux chantiers terminés, rien en cours. (1) Backfill du schema v20 (5 métriques mito)
clos et vérifié. (2) Nouvelle feature `export-cohort` livrée de bout en bout : audit
d'inclusion dans la cohorte Sens/Spé de la Tower, onglet 'Cohort' de la gsheet
trace-prod peuplé, code commité et poussé.

## Ce qui marche / ce qui foire
- ✓ Backfill mito v20 : 10/10 update-column, 0 erreur, CGFL 582/811 + HCL 513/513,
  les 2 exports gsheet passés dès la 1re tentative.
- ✓ `export-cohort` : 1324 lignes liquid × 17 colonnes, 485 inclus (261 cancers +
  224 sains). Vérifié **nominativement** contre `compute_cohort_samples()` — 485
  communs, 0 manquant, 0 en trop, 0 label divergent — et les 7 deltas de la cascade
  reproduits exactement (242/254/25/30/134/63/91).
- ✓ Audit adversarial (workflow 12 agents, 7 lots de prédicats) : **0 divergence
  confirmée**. Il a tout de même fait remonter 2 vrais défauts, corrigés : 6 mVAF
  ~1e-7 écrasés en `0` par un `.6f` naïf, et 2 imports morts.
- ✓ Aucune règle métier dupliquée : le script importe les prédicats d'Aima-Tower.
- ⚠ Décision laissée ouverte par Boris : les 229 Alcapone portent un motif
  « indication hors-cible (Lung_Alc) » redondant avec « cohorte Alcapone ». Fidèle
  à la Tower (car `get_indications()` n'expose pas `Lung_Alc`), mais trompeur à la
  lecture. Laissé tel quel.

## Prochaine étape
Rien d'engagé. Si Boris veut nettoyer le libellé : restreindre le motif
« indication hors-cible » aux 4 vraies indications exclues (TNE, Nuclear,
Bladder_Blood, Bladder_Urine) dans `dev/cohort_extraction.py`, puis relancer
`python3 database/check_samples.py export-cohort`. Ne change aucun effectif.
