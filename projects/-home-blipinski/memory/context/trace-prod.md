# Context — trace-prod — 2026-08-12T11:22:10+00:00

**Branche** : main
**Dernier commit** : dce1d45 — feat: métriques de longueur de reads filtrées (v24) + table qc (v23)
**Status** : propre, synchronisé avec origin/main (untracked préexistants only : backups
.duckdb, CSV dev/, rapports HTML)

## Où j'en suis
Session close, tout est commité et poussé. Chantiers livrés de bout en bout : export-cohort
redirigé vers la gsheet « Trace COHORT » avec 5 onglets par indication ; schemas v21 (n50),
v22 (n75 + ratio) ; bascule de la source liquid vers le bloc filtré (reads ≤ 1 kb) ;
schema v24 (pct_mass_removed). Rien n'est en cours.

## Ce qui marche / ce qui foire
- ✓ Backfills complets et vérifiés : n50/n75/ratio 1471/1471, pct_mass_removed 1324/1332.
  Exports gsheet systématiquement relus (valeurs brutes) plutôt que crus sur parole.
- ✓ Contrôle d'intégrité SQL sur le ratio : 0 incohérence sur 1324, 0 cas de n75 > n50.
- ✓ **Question Healthy_13 résolue** (elle était restée ouverte dans le snapshot du 10/08) :
  il est bien présent dans l'onglet `HCL liquid`, relu trois fois pendant les vérifications
  d'export (N50=170, Ratio=1,1039, % Masse > 1kb=1,46). Les exports relancés depuis ont réglé
  le problème — c'était vraisemblablement un décalage d'export, pas une absence en base.
- ⚠ 8 `Bladder_Urine_02_*` arrivés pendant la session (CGFL 811 → 819) n'ont ni n50, ni n75,
  ni ratio, ni pct : leur pipeline n'a pas encore produit les fichiers. Ils partent en gsheet
  avec NA sur ces colonnes.
- ⚠ `N50` a désormais **deux définitions** : samtools filtré ≤ 1 kb en liquid, cramino non
  filtré en solid. Le solid a été laissé de côté sur décision explicite.
- ⚠ Le chantier `check-qc` d'une session parallèle (table `qc`, v23) a été commité avec le
  mien — code que je n'ai ni écrit ni testé, volontairement non documenté dans README/CLAUDE.md.
- ✗ `Column 43` demandée pour l'export cohort reste introuvable (absente de TSV_TO_DB_METADATA,
  de l'onglet ONT Sample où la 43ᵉ est `Freq (Gene 3)`, et des gsheets sources où c'est
  `Gene 5 mutated`) — jamais exportée, en attente du vrai nom.

## Prochaine étape
Quand le pipeline aura produit les fichiers des 8 nouveaux Bladder_Urine :
`update-column n50|n75|n50_n75_ratio|pct_mass_removed liquid CGFL` puis
`export liquid CGFL --gsheet`. Sinon, trancher le sort du solid (rester sur cramino
ou basculer quand n50_ratio.tsv y sera disponible).
