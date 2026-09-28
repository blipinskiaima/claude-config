---
name: run-5base-healthy767
description: Premier run methylseq --taps sur FASTQ 5base (Healthy_767, 18/09/2026) — 98 % d'alignement, nOT/nOB mesurés très différents du Watchmaker
metadata:
  type: project
---

Premier passage de nf-core/methylseq (HEAD `64121ef`, v4.2.0) sur des FASTQ **5base**,
jusque-là traités uniquement par DRAGEN (couloir BP_5base). Lancé le 2026-09-18,
succès en **8 h 35**, 120,6 h CPU, 16/16 tâches.

- Script : `/scratch/boris/5base_methylseq/run_5base_methylseq.sh` — calque de l'étape 1 de
  `short-read/NF_Watchmaker_Methylseq/nf_watchmaker_methylseq.sh` :
  `--taps --aligner bwamem --genome hg38 -profile local_docker`
- Sorties : `/scratch/boris/5base_methylseq/Healthy_767/` (BAM 26 Go, `rastair_call` 2,8 Go,
  55,3 M lignes). FASTQ dans `/scratch/boris/5base_methylseq/data/Healthy_767/`.
- Lancé depuis **`~/Run2`** avec `-name ms-5base-healthy767` : `~/Run` était verrouillé par le
  run Bam2Beta `b2b_test_v232`, et `-resume` nu y aurait repris la session d'un autre run.
  Nextflow refuse un `-name` qui commence par un chiffre ou contient des majuscules.

## Pourquoi --taps + bwamem est valide sur le 5base

Composition des bases sur 50 000 reads R1 de Healthy_767 :
5base C = **20,56 %**, Watchmaker C = 20,39 %. Un bisulfite classique tomberait à 2-5 %.
Le 5base **préserve l'alphabet à 4 lettres**, comme TAPS → l'alignement 4 lettres (bwamem)
convient, pas besoin de bwameth/bismark. Confirmé à l'usage : **98,03 % mappés**,
91,22 % en paires propres, 26,8 % de duplication (546 M reads).
Les README short-read disent « bisulfite short-read » pour les deux chimies : étiquette
générique, pas la chimie réelle.

## nOT / nOB — non transposables d'un kit à l'autre

Format rastair : `[r1_start, r1_end, r2_start, r2_end]` = bases exclues depuis les
extrémités 5'/3' **de la read** (soft-clips compris).

| | 5base (mesuré, reads 101 bp) | Watchmaker (codé en dur, reads 110 bp) |
|---|---|---|
| nOT | `5,10,19,0` | `2,0,21,1` |
| nOB | `14,5,19,0` | `1,5,21,1` |

Commun aux deux kits : ~20 bases exclues au 5' de R2. Propre au 5base : R1 bien plus biaisé
(OB 14 au 5', OT 10 au 3').

**Why:** le pipeline chaîne `RASTAIR_MBIAS → MBIASPARSER → RASTAIR_CALL` et applique tout seul
les valeurs mesurées sur le BAM du run — aucune relance nécessaire pour le call par défaut.
La table codée en dur de `nf_watchmaker_methylseq.sh` ne sert qu'aux 9 calls MAPQ×BQ lancés
hors pipeline.

**How to apply:** pour décliner la matrice MAPQ×BQ ou d'autres samples 5base, relancer
`rastair call` sur le BAM avec les nOT/nOB lus dans
`rastair/mbiasparser/{ID}.rastair_mbias_processed.csv` (ligne 1 = OT, ligne 2 = OB) de
**chaque** sample — jamais ceux du Watchmaker.

Lien short-read : répond en partie au point « 5base non tranché » de
[[../-home-blipinski/memory/context/short-read]] ; le score raima de ce run n'est pas
encore calculé. Pipeline : [[version-pipeline-nf-core]].

## Validation du call (2026-09-21)

- **Sens du signal correct** : sur 517 k CpG (couverture ≥ 10, hors SNP, chr1→chr3),
  bêta moyen **0,768**, 57,9 % > 0,8, 6,7 % < 0,2 — profil d'un ADNcf sain d'origine sanguine.
  Un sens inversé (logique bisulfite lue en TAPS) aurait donné ~0,23 et une majorité < 0,2.
- **Call équivalent à la colonne « Standard » du Watchmaker** : même conteneur
  `rastair:0.8.2--bf70eeab4121509c`, mêmes options (`--threads --nOT --nOB --fasta-file`,
  aucun `--min-mapq`/`--min-baseq`), nOT/nOB mesurés par sample dans les deux cas.
  → la mVAF de ce call est directement comparable à Watchmaker Standard (0,00) et à BP_5base.
