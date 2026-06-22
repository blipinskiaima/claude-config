# Context — Bam2Beta — 2026-06-22T17:45:16+00:00

**Branche** : main
**Dernier commit** : f1d75be — feat(dev): figures covdepth depth/coverage (Fig.1 cumulative + Fig.2 multi-échelle)
**Status** : 5 fichiers modifiés pré-existants (conf/base.config, dev/PLT, dev/SCW, workflow/beta.nf, workflow/merge.nf) + bacasable.sh — HORS session covdepth, non touchés

## Où j'en suis
Chantier R&D covdepth — Étape 1 LIVRÉE et commitée. Scripts versionnés (`dev/coverage_analysis/fig1_depth_coverage.R`, `fig2_positional_multiscale.R`), figures dans `test/` (gitignoré), workspace `/scratch/boris/covdepth/`. 2 questions ouvertes restées en suspens avant /end-session.

## Ce qui marche / ce qui foire
- ✓ Fig.1 cumulative depth-vs-breadth comparative merged vs epic (global.dist, dénominateur natif = génome)
- ✓ Fig.2 positionnelle multi-échelle + bandes de déplétion systématique (merged propres ; 073 ~9.5x très net)
- ✓ Concordance parfaite mosdepth ↔ trace-prod (qc_metrics) ; finding 067 pathologique (34M reads alignés, depth=0/cov=0%)
- ✗ epic positionnel : 500kb encore bruité (~0.1x), seul le 5Mb est net — choix 1M/5M/10M non tranché
- ✗ Paradoxe 067 (34M reads → 0 couverture) non élucidé (cause exacte : reads courts/dup/QC-fail ?)
- ✗ Healthy CGFL liquid sans per-base epic (642, 831) — epic impossible pour ces samples

## Prochaine étape
Trancher les 2 questions ouvertes : (1) échelles epic 1M/5M/10M (retirer 500k bruité) ? (2) creuser 067 via flagstat + distribution longueur des reads. Puis définir l'Étape 2 du chantier (cohorte/labo/multi-échelle).
