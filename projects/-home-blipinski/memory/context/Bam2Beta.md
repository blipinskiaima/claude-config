# Context — Bam2Beta — 2026-07-07T21:17:04+0000

**Branche** : main
**Dernier commit** : b2648b5 — feat(rarefaction): module Rarefaction cascade (subsample BAM 20M->1M nested)
**Status** : WIP dev/ perso laissée (Bam2Beta.sh, launch_SCW.sh, bacasable.sh untracked)

## Où j'en suis
Feature raréfaction en cascade développée, validée et commitée. `Rarefaction_Cascade`
(workflow/rarefaction.nf) produit des BAM rarifiés NESTÉS 20M→10M→5M→2M→1M via
`samtools -s`, 2 temps façon small_fragment. Prêt à re-lancer Temps 1 en prod.

## Ce qui marche / ce qui foire
- ✓ Cascade corrigée validée : comptes ±0,13 %, nesting 0 orphelin (1M⊂2M⊂5M⊂10M⊂20M)
- ✓ Bug racine trouvé : `samtools -s` = hash absolu du read-name ; même seed en cascade →
  seuils composés en MIN → comptes faux (frac×N_merged). Fix = seed INCRÉMENTÉ par niveau
- ✓ Bug reproduit bit-à-bit sur donnée réelle (buggy 10M→15M = ta table prod)
- ✓ Commit b2648b5 (rarefaction.nf + conf/base.config + main.nf + nextflow.config + CLAUDE.md)
- ✗ Sorties S3 prod actuelles (`CGFL_rarefaction`/`HCL_rarefaction`) FAUSSES (bug) → à re-run
- ✗ KO=0 sur Lung_121 / Prostate_45 / Lung_13 = échecs Temps 2 SÉPARÉS (crash), non investigués

## Prochaine étape
Re-lancer Temps 1 (code corrigé) sur les 10 samples puis Temps 2. Décider écrasement S3
vs nouveau dossier. Toggle = `--RAREFACTIONS` (pluriel !), depths = `--rarefaction '20M,10M,5M,2M,1M'`.
Artefacts de test conservés : /scratch/boris/rare_test/
