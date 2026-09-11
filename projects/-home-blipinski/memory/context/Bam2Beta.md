# Context — Bam2Beta — 2026-09-11

**Branche** : main
**Dernier commit** : bbbc009 — chore(perf): right-sizing des ressources mesuré sur 46 traces, paires dilution en 4 lots
**Status** : clean (1 non suivi : pair_current.tsv, fichier tournant du lanceur dilution)

## Où j'en suis

Chantier « QC après filtre fragmentomique 80 < L < 1 kb » livré de bout en bout, hors pipeline.
1378 BAM merged liquid relus (20,96 To, ~15 h, 0 échec) par une passe streaming
`aws s3 cp - | samtools view -h | mawk` (`/scratch/boris/qc_stat/`). 3 colonnes en base
(trace-prod schema v35, commit fa96cb0) + import one-shot `dev/import_qc_80_1000.py`, export fait
dans l'onglet « QC read », et synthèse en 6 parties insérée dans le Google Doc QC, onglet
Deep Dive > Filtre read entre 80 et 1000Kb. Boris relit le doc.

## Ce qui marche / ce qui foire

- ✓ Conventions validées **bit à bit** sur Lung_9 : molécules = cramino `num_reads` à l'unité,
  bases = mosdepth à l'unité (M/=/X seuls, les délétions ne comptent pas), depth et coverage
  identiques aux valeurs publiées
- ✓ Résultat : le filtre coupe du **court** (écartés 78,5 pb vs 177,2 conservés) → comptages
  −7,4 %, depth −3,2 %, coverage −0,96 %. 50 bascules de statut Exis / 46 Themelio, toujours par
  le seul comptage de molécules (jamais depth ni coverage)
- ✓ La perte de depth suit la masse > 1 kb (facteur 30) → le filtre révèle le gDNA (`TNE_2`
  0,66 → 0,13×)
- ✗ **16 flux = optimum, 32 s'effondre** (96 Go de RAM, débit ÷ 6). Ne pas réessayer
- ✗ `qc_metrics.coverage_percent` n'a qu'**1 point de précision** (entier rond 1378/1378) —
  découvert ici, dépasse ce chantier
- ⚠ **`Read_Start_Time` est commenté dans `workflow/qc.nf:27` et c'est commité (bbbc009)** : ni
  `read_start_time.tsv` ni `sequencing_time.tsv` ne sont plus produits. Volontaire pour alléger
  les runs de dilution, mais à re-basculer avant un run prod nominal
- ⚠ Dilutions de Boris toujours en cours : 115/220 paires, 5 tmux (LUNG, LUNG_D1..D4)

## Prochaine étape

Attendre les retours de Boris sur l'onglet du Google Doc. Puis trancher le sort de
`Read_Start_Time` (réactiver ou documenter la coupure) avant tout run de production.
