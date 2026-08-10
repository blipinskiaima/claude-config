# Context — trace-prod — 2026-08-10T19:18:41+00:00

**Branche** : main
**Dernier commit** : 7b75c16 — docs: n50 — corrige l'interprétation des valeurs liquid élevées
**Status** : clean, synchronisé avec origin/main (9 commits poussés cette session)

## Où j'en suis
Deux chantiers terminés et poussés, rien en cours. (1) L'export cohort a quitté la gsheet
trace-prod pour une gsheet dédiée « Trace COHORT » et s'est décliné en 4 onglets par
indication via `export-cohort --indication`. (2) Schema v21 : colonne `n50` dans
`qc_metrics`, backfill rétrospectif terminé (4 min 54 s, couverture 100 %) et exports
gsheet passés.

## Ce qui marche / ce qui foire
- ✓ Famille `exis_*` : Exis Multi (1325×10), Exis CRC (210×20), Exis Lung (437×20,
  Lung+Lung_Alc), Exis Pancreas (33×20), Exis Healthy (330×20). Ajouter une indication
  = 1 ligne `EXIS_TABS` + 1 entrée JSON. Chaque onglet relu et comparé au TSV local :
  0 divergence sur les valeurs brutes.
- ✓ Schema v21 `n50` : 3 combos (liquid CGFL+HCL, solid CGFL), lu par nom d'en-tête dans
  le TSV cramino. Backfill 1471/1471, médiane liquid 174 bp / solid 3804 bp.
- ✓ Correction de doc importante : j'avais écrit qu'un n50 liquid élevé trahissait une
  confusion de fichier — faux. Les 15 liquides ≥1000 bp sont réels (surtout Bladder_Urine,
  matrice urinaire). Le contrôle valable est la cohérence entre réplicats.
- ✗ `Column 43` demandée dans l'export CRC : introuvable (ni TSV_TO_DB_METADATA, ni onglet
  ONT Sample où la 43e est `Freq (Gene 3)`, ni gsheets sources où c'est `Gene 5 mutated`).
  Non exportée, en attente du vrai nom.
- ✗ Question de Boris laissée sans réponse : « pourquoi Healthy_13 n'est pas dans l'export
  trace-prod ? ». Vérifié qu'il est bien en base (HCL, v5.0.0, inclus dans la cohorte) mais
  l'investigation sur l'onglet trace-prod a été interrompue avant conclusion.

## Prochaine étape
Rien d'engagé. Deux reprises possibles : demander à Boris le vrai nom de `Column 43` pour
compléter les onglets par indication, ou reprendre la question Healthy_13 en comparant la
DB à l'onglet `HCL liquid` de la gsheet trace-prod (l'export a été relancé depuis, il se
peut que ce soit déjà résolu).
