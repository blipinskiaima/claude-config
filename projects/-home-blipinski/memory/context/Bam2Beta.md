# Context — Bam2Beta — 2026-09-03

**Branche** : main
**Dernier commit** : b97fd0b — feat(rarefaction): module RAREFACTION_HORAIRE_THRESHOLD
**Status** : clean sauf `dev/SCW/rarefaction_horaire_threshold.sh` non suivi

## Où j'en suis

Module `RAREFACTION_HORAIRE_THRESHOLD` livré et commité (`workflow/BAM/`, câblé dans
`main.nf` + `nextflow.config` + `conf/{base,prod,liquid}.config` + CLAUDE.md). Produit
4 BAM aux **5/10/15/20 premiers millions de molécules** dans l'ordre `st:Z:`, seulement
si le sample porte **≥ 30 M molécules primaires (A+D)**. Publication dans
`{LABO}_rarefaction_horaire_threshold`. Boris a lancé les runs de production (tmux CGFL
et HCL) pour l'expérience de concordance mVAF. Détail : memory/rarefaction-horaire.md.

## Ce qui marche / ce qui foire

- ✓ Validé sur `Breast_11_rebasecalled_V5.0.0_trimmed` (48 578 468 molécules) : 4 paliers
  exacts au read près, même origine temporelle (MIN_EPOCH identique), 0 orphelin sur les
  3 paires de nesting, et le BAM 5M est le préfixe temporel rigoureux du 20M
- ✓ **100 % des reads primaires portent un `st:Z:`** — vérifié sur 2 samples (Breast_11 ;
  Colon_1 HCL 68 714 795). Aucun read perdu par l'ordonnancement temporel
- ✓ `mktime` + offset corrige à la racine l'ordre lexicographique faux sur un changement
  d'heure (testé : lexico sort B,C,A là où l'ordre réel est C,A,B)
- ✗ Lanceur `dev/SCW/rarefaction_horaire_threshold.sh` **NON corrigé et non commité** :
  `Cd ~/Run` ligne 3 (majuscule → command not found, le cd ne se fait pas) et témoin
  d'idempotence `${ID}_12h` ligne 10 au lieu de `${ID}_20M` → aucune reprise possible,
  chaque sample est relancé même s'il est déjà fait
- ✗ **Temps 2 non écrit** : récapitulatif mVAF v1.4 + v1.5 par palier (run EXIS sur chaque
  `{ID}_5M`… puis agrégation). C'est ce que demande le cahier des charges
- ⚠ Confondant pour l'analyse : à **20 M molécules**, les BAM pèsent **5,9 à 8,1 Gio**
  selon le sample (36 % d'écart — reads plus longs chez HCL + secondaires/supplémentaires
  ramenés par `samtools view -N`). Comparaison palier vs run complet du même sample non
  affectée ; comparaison **entre samples à palier égal** biaisée
- ✗ Hérité V2.3.0, toujours ouvert : trace-prod lit des sorties coupées
  (`checkers.py:91,507` + colonne `score_cnv`), `docker push raima:latest`/`:0.5.6`
  (Hub à 0.5.3), tarball 0.5.6 → `s3://aima-resources/raima-model/`, backfill amplitude
  ~1 500 samples via `--RETRO_FRAG_AMPLITUDE`, casse `trace-platform/check_platform.py`

## Prochaine étape

Corriger le lanceur (2 lignes), laisser les runs finir, puis écrire le **Temps 2** : boucle
`--EXIS true --MERGE false` sur les 4 paliers de chaque sample, puis agrégation des mVAF
v1.4/v1.5 en un récapitulatif par seuil pour l'évaluation de concordance
(classifications +/− et scores continus vs run complet).
