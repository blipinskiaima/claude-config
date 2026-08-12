---
name: n50-ratio-qc
description: "QC N50/N75 avant-apres filtre 1 kb — detecteur de contamination gDNA du plasma, dans Extract_read (frag.nf), sortie QC/Samtools/{ID}.n50_ratio.tsv"
metadata: 
  node_type: memory
  type: project
  originSessionId: ccc47027-333b-40a9-a728-dd1f326dc446
  modified: 2026-08-12T15:27:49.879Z
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
- ~~Aucun seuil de rendu n'est fixe~~ → **SEUILS DETERMINES le 2026-08-12, voir ci-dessous.**
  Reste vrai : le sens **haut uniquement** — la sur-fragmentation est sans objet (plancher
  biologique du nucleosome a ~147 pb, le plasma le plus court fait 136 pb, soit x0,82 de la
  mediane).

## Seuils (2026-08-12) — sur `ratio_n50_n75_filtered`, reads <= 1 kb

Determines **sans aucun label de matrice**, par la seule geometrie de la distribution : elle est
multimodale, et chaque seuil est place **au milieu d'un intervalle ou aucun echantillon n'existe**
(1,2463-1,2752 et 1,3976-1,4530). Deplacer un seuil de +/-0,013 (bas) ou +/-0,023 (haut) ne
reclasse donc **personne** — c'est ce qui manque aux seuils 5M/0,25x, qui coupent en pleine densite.

| zone | condition | n | % |
|---|---|---:|---:|
| A — analysable | ratio <= **1,26** | 1 227 | 92,7 |
| B — zone grise | 1,26 < ratio <= **1,43** | 32 | 2,4 |
| C — non interpretable | ratio > **1,43** | 65 | 4,9 |

Distribution plasma : mediane **1,10** · p95 1,19 · p99 1,89. Le seuil unique (1,26 seul) reste
possible ; le double est prefere car la zone grise est une population **reellement ambigue**.

**Validation a posteriori** (labels utilises seulement APRES) : plasmas 98,1 % en A · urines
71,6 % en C et 19,8 % en B · les 22 controles synthetiques **Twist 100 % en A**.

⚠ **Angle mort** : le ratio filtre ne voit pas la contamination qu'il a filtree. `Breast_6`
(57 % de masse > 1 kb) et `TNE_2` (81 %) sont classes en **zone A**. Toujours l'accompagner de
`pct_mass_removed` (~2 % chez un plasma normal, examiner au-dela de 25 %).

## Les 12 controles qualite externes forment un mode a part

Les 12 EQC de CGFL (`Breast_17/32/47/49/50/52`, `Prostate_2/3/23/37/38/39`) tombent **tous les 12
en zone grise**, entre **1,3289 et 1,3649** — 0,036 d'amplitude, le groupe le plus resserre de
toute la cohorte — avec une masse > 1 kb de **0,00 a 0,19 %** (les plus propres du jeu).

Materiel de reference industriel : distribution plus etalee qu'un cfDNA natif, mais identique
d'un flacon a l'autre. **Leur position en zone grise est attendue, ce n'est pas une alerte.**

Consequence : la zone grise se decompose en **16 urines + 12 EQC + 3 plasmas** reellement
inexpliques (et non 16 plasmas « de cause inconnue » comme ecrit avant cette identification).
A l'inverse les controles **Twist**, concus pour mimer un profil de cfDNA, sont tous en zone A —
l'indicateur distingue les deux types de controle.

## Les 3 plasmas de la zone grise — mecanismes tranches par la mesure

Une fois urines et EQC retires, il reste **3 plasmas** (et non 4 : le 4e etait
`Breast_17_rebasecalled`, donc un EQC). **Causes distinctes, pas de mecanisme commun.**

Critere discriminant = sur les reads **>= 1 kb**, part **splittee** et part de sequence
**alignee en continu** (le meme test qui avait etabli que `Breast_6` portait du vrai gDNA) :

| sample | ratio | masse >1kb | align/read | reads >=1kb splittees | continu | len max |
|---|---:|---:|---:|---:|---:|---:|
| `Lung_Alc_93_av` CGFL | 1,3976 | 6,4 % | **1,453** (rang 3/1229) | **91,5 %** | **48 %** | 5 201 |
| `Lung_124` HCL | 1,3081 | **17,4 %** | 1,008 (rang 1159) | **2,7 %** | **99,3 %** | **29 255** |
| `Lung_Alc_15_av` CGFL | 1,3014 | 1,9 % | 1,115 (rang 28) | 62,5 % | 71,9 % | 4 026 |
| *(ref)* `Breast_6` | — | 57,3 % | — | 1,8 % | 98,8 % | 65 204 |

- **`Lung_Alc_93_av` = chimeres.** 31,6 % de reads chimeriques, et 91,5 % de ses molecules
  longues sont **decoupees** avec moins de la moitie de sequence alignee d'un tenant : ce sont
  des assemblages, pas des molecules.
- **`Lung_124` = vraie contamination par ADN long.** Meme signature que `Breast_6` (99,3 %
  continu, jusqu'a 29 kb) mais plus modeste : 2 379 pb de moyenne contre 8 926 pb. D'ou une
  traine qui s'eteint vers 3 kb sur la figure.
- **`Lung_Alc_15_av` : indecidable** — seulement **16 reads >= 1 kb**, effectif trop faible.
  Son ratio vient plutot de ses 14,7 % de chimeres. Il est de toute facon **deja rejete** par
  les seuils actuels (0,11x, 2,19 M reads).

⚠ Ne pas conclure sur le seul `align/read` : c'est un proxy. Le test direct (splittees + continu)
est ce qui separe un artefact d'alignement d'une vraie molecule longue.

## Application en aveugle — 10 patients Imagenome Labosud (s3://aima-platform)

Hors des 1 324 ayant servi aux seuils, nature inconnue a l'avance. **Les 10 en zone A**, ratio
1,0764 a 1,1481 (tous sous le p95 de 1,19), masse > 1 kb de 0,22 a 9,95 %. Premiere application
reelle de l'indicateur.

Voir [[softclip-fragmentomics-length]] pour la convention de longueur, et
[[covdepth-qc-valorization]] pour le chantier QC dont ce travail est issu.
