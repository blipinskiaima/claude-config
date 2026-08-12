---
name: n50-ratio-qc
description: "QC N50/N75 avant-apres filtre 1 kb — detecteur de contamination gDNA du plasma, dans Extract_read (frag.nf), sortie QC/Samtools/{ID}.n50_ratio.tsv"
metadata: 
  node_type: memory
  type: project
  originSessionId: ccc47027-333b-40a9-a728-dd1f326dc446
  modified: 2026-08-12T10:36:28.117Z
---

# QC N50/N75 — detecteur de contamination gDNA (2026-08-12)

Ajoute dans le process **`Extract_read`** ([workflow/frag.nf]) au commit `a95a36b`.
Sortie : `QC/Samtools/{ID}.n50_ratio.tsv`, **12 colonnes**, une ligne par sample.

## Ce que ca detecte, et pourquoi les seuils actuels ne le voient pas

La paire de seuils de rendu (5 M reads OU 0,25x) compte la **quantite**. La contamination
du plasma par de l'ADN genomique leucocytaire est un defaut de **forme** — les deux sont
independants, donc le QC actuel trie au hasard vis-a-vis de ce defaut.

**Le N50 pondere par la MASSE d'ADN** (somme longueur x effectif), pas par le nombre de
reads. C'est ce qui le rend sensible la ou la mediane est aveugle : sur les 8 plasmas
contamines identifies, `median_length` vaut 163-176 pb (parfaitement normal) pendant que
le n50 monte a 1 608 et 3 647.

## Valeurs de reference (1 324 samples liquid, mesure 2026-08-11)

| | mediane | p95 | p99 | max |
|---|---:|---:|---:|---:|
| **plasma** (n=1 243) | **1,10** | 1,19 | 1,89 | 24,4 |
| **urine** (n=81) | 1,78 | 2,75 | 3,59 | 3,6 |

Distribution plasma extremement serree : 95 % entre 1,10 et 1,19. Les urines forment un
**mode separe** (matrice differente, cellules urotheliales desquamees) -> un seuil unique
serait faux pour l'une des deux.

Part de masse portee par les reads > 1 kb : plasma mediane **2,3 %** · **9 plasmas > 50 %**,
dont **5 sont rendus** aujourd'hui sans signalement.

## Les 2 gotchas a ne jamais perdre

1. **Les DEUX jeux (avant/apres filtre) sont indispensables.** L'ecart fait le diagnostic,
   pas l'une des deux valeurs. `Breast_6` : ratio **24,44** avant, **1,11** apres -> son
   cfDNA est sain, la contamination s'est ajoutee par-dessus. Ne garder que l'apres-filtre
   le rendrait indistinguable d'un plasma normal.
   Le `ratio_f` separe meme deux profils : `Breast_6`/`TNE_2` retombent a 1,11 (contamination
   pure) alors que la serie `Colon_22` reste a 1,86-2,09 (cfDNA lui-meme altere).

2. **NOS N50 NE SONT PAS COMPARABLES A CEUX DE CRAMINO.** Sur `Breast_6` : cramino 3 808,
   nous 4 643 (**+22 %**). Le n75 concorde (185 vs 190) car il tombe dans le pic
   nucleosomal ; le n50 non car il est dans la queue. Cause : cramino voit 9,41 M reads
   contre 7,86 M pour FRAG — perimetre BED chr1-22, `-F 3840` et soft-clips retires
   diffèrent. Ne jamais melanger les deux sources dans une analyse ou un seuil.

## Implementation

Lit `${ID}.read_lengths.csv` **que le process vient d'ecrire** (pas de relecture du BAM).
awk + sort, aucune dependance nouvelle, container `bam2beta:latest` (awk 5.1.0, sort 8.32).

Algorithme : histogramme `cnt[longueur]++` -> `sort -k1,1rn` sur les **~50 000 valeurs
distinctes** (pas les 8 M lignes) -> double cumul de masse. Le filtre n'agit qu'au cumul,
avec un **denominateur reduit** (`totf`) — sans quoi le cumul filtre n'atteindrait jamais
50 % du total complet. Seuil `L <= 1000` (une read de 1 000 pb est **conservee**), en dur,
recopie dans la colonne `length_threshold`.

Optimisation : un tri par insertion en awk etait quadratique sur 50 k valeurs -> 65 s/sample.
Le passage a `sort` externe donne **2,7 s**, resultat identique.

## Retrospectif deja en place

**1 324 TSV uploades sur S3** (811 CGFL + 513 HCL) dans `QC/Samtools/`, verifies par scan
recursif. Le pipeline produit un fichier **identique octet par octet** (verifie sur
`Healthy_826` et `Breast_6`). Aucun recalcul retrospectif necessaire.

## Non traite

- `conformity/check-run-output.sh` ne verifie **aucun** fichier de `QC/Samtools/`. Ajouter
  `n50_ratio.tsv` au contrat verifie le ferait entrer dans la qualification ISO — decision
  non prise.
- Aucun seuil de rendu n'est fixe : la valeur devra etre calibree sur nos donnees, **par
  matrice** (plasma / urine), et **dans le sens haut uniquement** — la sur-fragmentation est
  sans objet (plancher biologique du nucleosome a ~147 pb, le plasma le plus court fait
  136 pb, soit x0,82 de la mediane).

Voir [[softclip-fragmentomics-length]] pour la convention de longueur, et
[[covdepth-qc-valorization]] pour le chantier QC dont ce travail est issu.
