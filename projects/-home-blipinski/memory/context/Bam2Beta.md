# Context — Bam2Beta — 2026-08-27T15:23

**Branche** : main
**Dernier commit** : 5693a43 — feat(dev): backfill retrospectif du ratio N50/N75
**Status** : 14 fichiers (module RAREFACTION_HORAIRE d'une session parallèle, non commité par moi)

## Où j'en suis

Deux chantiers, aucun code du pipeline touché (analyse rétrospective seule).

**A. Impact référence/pipeline d'alignement** — question d'un interlocuteur externe qui
aligne avec `epi2me-labs/wf-alignment` sur `Homo_sapiens.GRCh38.dna.primary_assembly.fa`
au lieu de notre `GCA_000001405.15_GRCh38_no_alt_analysis_set`. Étapes 1→5 rendues,
**étape 6 (stratégie de test) proposée et en attente de validation Boris**. Rien lancé.

**B. Temps de séquençage** — LIVRÉ. `/scratch/rarefaction_horaire/result.csv`,
485 samples (185 CGFL + 300 HCL), 4 colonnes : ID, sequencing_time, multi_run, nb_bam.

## Ce qui marche / ce qui foire

- ✓ **Notre référence confirmée sur 4 sources** : `nextflow.config:119` de Pod2Bam, le
  rapport séquenceur MinKNOW, le PDF client, et les 195 @SQ des BAM réels (chrEBV présent)
- ✓ **Le vrai écart est le preset minimap2**, pas la référence : wf-alignment utilise
  `-ax map-ont -y` (k15/w10), notre chaîne `lr:hq` (k19/w19). Notre benchmark Pod2Bam
  mesure +5 pts de mapping rate. Le `-q 20` de `Preprocess_28M` amortit côté mVAF ;
  FRAG et BETA epic n'ont **aucun filtre MAPQ** → plus exposés
- ✓ **Ensembl a démasqué le PAR de chrY** depuis la release 110 (GRCh38.p14, 2023) —
  mesuré des deux côtés. Sans impact chez nous : 0 sonde EPIC dans les PAR, mVAF et CNV
  sur chr1-22 seulement
- ✗ **Le test hg38 vs GRCh38 de février ne prouve PAS ce que CLAUDE.md laisse croire** :
  Bam2Beta n'a aucun aligneur, ce test comparait le FASTA aval (modkit/mosdepth), jamais
  l'alignement. Formulation de `CLAUDE.md` à corriger — Boris n'a pas tranché
- ✗ **2 trous non comblés** : régions masquées hors PAR sur chr5/14/19/21/22 (fichier NCBI
  `unmasked_cognates_of_masked_CEN_PAR.txt` non récupéré, et c'est le seul endroit où la
  référence pourrait toucher chr1-22) ; comportement de `raima::infer_sex` sur X/Y
- ✓ **32 samples multi_run détectés** (2 flow cells) via la fraction de seconde, signature
  du run. Leur `sequencing_time` est une fenêtre calendaire, pas un temps machine —
  `HCL_Lung_26` = 99h35 affiché mais 50h57 + gap 1h50 + 46h49

## Prochaine étape

Trancher le sort des **32 samples multi_run** pour la raréfaction horaire (traiter tels
quels / exclure / traiter par run) — décision à prendre avant que la session parallèle
avance. Puis, si Boris valide, l'étape 6 du chantier A : test du preset `lr:hq` vs
`map-ont` sur un uBAM `demux_trimmed/`, en 2 étages avec porte de sortie.
