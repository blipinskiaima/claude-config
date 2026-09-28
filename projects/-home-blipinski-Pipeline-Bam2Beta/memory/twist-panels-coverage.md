---
name: twist-panels-coverage
description: "Couverture de la whitelist du modele v1 (mVAF 1.4 / Exis 1.1) par les 2 panels methylation Twist (Human Methylome 97 %, Alliance Pan-cancer 3 %) — BED publics, convention de coordonnees, proxy de poids"
metadata:
  node_type: memory
  type: project
  originSessionId: f08237a5-0f3a-442c-9175-605e584e2bcf
  modified: 2026-09-28T11:25:18.896Z
---

# Panels Twist x whitelist modele v1 (2026-09-28)

Question du Google Doc « Collaboration_Twist » (`1snkbgUd40pr7-IRsZkGK2zoFdP8hl5g6bPInGllXTRk`) :
quelle part des CpG du modele EPIC (mVAF 1.4, Exis 1.1) est couverte par chaque panel ?

| panel | strict (CpG dans une cible) | fenetre +-100 pb | top 1 % des poids (+-100) | part du poids |
|---|---:|---:|---:|---:|
| Human Methylome (123 Mb) | 96,6 % | **97,1 %** | 98,9 % | 97,8 % |
| Alliance Pan-cancer (1,5 Mb) | 1,9 % | **3,0 %** | 15,7 % (x5 enrichi) | 5,3 % |

Denominateur : **666 990 CpG** de `model_v1_data_whitelist.tsv.gz`, autosomes seuls.

## A savoir pour refaire le calcul

- **BED publics, en hg38** (le lien du BED Alliance n est PAS sur la page produit, qui renvoie au
  support client). Il est sous `/resources/bed-files/twist-alliance-pan-cancer-methylation-panel-15mb-resource-files`
  (la variante `/data-files/` repond 404). Le BED Alliance « covered_targets » est a 79 % fait de
  **cibles de 1 pb** (positions de sondes 450K/EPIC, cg IDs) : 0,63 Mb de cibles pour 1,5 Mb de
  panel -> le chiffre strict est un **minorant**, le +-100 pb est la bonne lecture.
- **`pos` de la whitelist = C du CpG en 0-based** (2000/2000 donnent `CG` via getfasta sur
  `[pos, pos+2)`). Les cibles 1 pb d Alliance tombent sur `pos+1` (le G) pour 80 % d entre elles.
- Le +-100 pb reproduit la logique raima : `compute_mean_betas(radii = 0:100)` moyenne les CpG
  observes dans +-r autour de chaque ancre ; une ancre sans aucune donnee sort en NA et est
  **retiree** du calcul (`nona`) -> le modele tourne sur le sous-ensemble couvert.
- **Poids = proxy** : `||loadings PC_i|| / scale_i` (derivee de la projection ACP par rapport au
  beta du CpG). Ce n est PAS l importance pour le score cancer (non lineaire via `pc_mixtures2`) —
  la vraie importance est a demander a Florian.

Materiel : `/scratch/boris/twist/` (`hmp_hg38.bed`, `apc_hg38.bed`, `wl.bed`, `run_overlap.sh`).
Voir [[batch-effect-investigation]] pour le biais de technologie EPIC -> ONT, meme nature que
EPIC -> EM-seq/Illumina ici.
