# Context — trace-prod — 2026-08-14T14:26:35+00:00

**Branche** : main
**Dernier commit** : e7ff4e6 — docs: rarefaction — reconnaître un lot en cours de production
**Status** : propre, synchronisé avec origin/main (20 untracked : backups .duckdb, CSV dev/, rapports HTML)

## Où j'en suis
Session d'exploitation, pas de développement. Lot **Bladder_Blood CGFL** intégré à la table
`rarefaction` : 269 pseudo-samples insérés (2 passages de `check-rarefaction`), onglet
`Rarefaction` réexporté à chaque fois. **En attente de la 2ᵉ vague Bam2Beta** — le pipeline
écrivait encore à 12h16.

## Ce qui marche / ce qui foire
- ✓ 279 lignes Bladder_Blood en base = 58 bases × niveaux applicables (0 manquant vérifié
  sample par sample). Export **2962 lignes × 20 col** relu depuis la gsheet en valeurs brutes.
- ✓ 2ᵉ passage (12h26) : **84 valeurs gagnées** — `mVAF v1.4` et `Props Bootstrap` désormais
  **279/279**, exclusivement sur 10M (23) et 20M (19). Boris avait raison sur l'avancement.
- ✗ `PROD` reste **KO sur 269** : aucun dossier `QC/CNV/Fragmentomics/IV/ichorCNA` produit,
  10M et 20M compris. Donc `Depth`, `Coverage`, `Ratio %`, `IchorCNA`, `Mode1/2`,
  `Frag Score v2`, `mVAF v1/v2/v1.3` à `NA`.
- ⚠ `Nb reads total` affiche **`0,00`** (pas `NA`) sur ces 269 — faux zéro à ne pas lire
  comme un comptage.
- ⚠ Piège de contrôle : `COUNT(colonne)` ne détecte pas les changements sur les VARCHAR où
  `'NA'`/`'KO'` comptent comme valeurs. Le bon contrôle est le **diff contre le backup**
  (`ATTACH ... AS old (READ_ONLY)`), qui seul a révélé les 84 modifications.
- ⚠ Les 41 `mVAF v1.4 = 0,0000` sont **légitimes** (vrais négatifs + convergence) : sur les 21
  pseudo-samples à parent nul, 2/21 sont à zéro à 1M contre 11/19 à 20M. Une mVAF non nulle
  à 1M/2M ne prouve pas une détection.
- ○ Ouvert, non traité : **12 `Bladder_Urine` sur 95** sans `mvaf_v14` dans `retd_suivis`
  (proposé à Boris, pas de réponse).

## Prochaine étape
Attendre que `QC/` apparaisse — repère :
`aws s3 ls s3://aima-bam-data/processed/MRD/RetD/liquid/CGFL_rarefaction/Bladder_Blood_02_094_20M/ --profile scw`
Dès que `QC/`, `CNV/`, `Fragmentomics/`, `IV/`, `ichorCNA/` s'y ajoutent : relancer
`check-rarefaction CGFL` ciblé sur `WHERE prod_status_rarefaction='KO'` (269, ~20 min, tmux)
puis `export-rarefaction`. C'est le passage qui bascule les 269 en `PROD OK`.
