---
name: signal-mitochondrial-mesure-sur-donnees-aima
description: "Ce que contient réellement le chrM de nos BAM ONT — couverture, fragmentation, méthylation, et le confondant de cohorte qui invalide la feature de DELFI"
metadata: 
  node_type: memory
  type: project
  originSessionId: b25ebc3a-3971-43e9-a55f-036a8c7ff44c
  modified: 2026-07-23T10:38:00.542Z
---

Mesuré le 2026-07-23 sur 15 BAM ONT de sujets **sains** (11 CGFL, 4 HCL), pris dans
`/scratch/florian/tmp-data/tempdir/` faute de BAM de production accessibles.
Concerne **Bam2Beta**, pas Aima-Survey. Aucun cancer mesuré.

## Le chrM est déjà là

Pod2Bam aligne contre `GRCh38_no_alt` qui contient `chrM 16569`, `samtools merge` ne filtre
aucun contig. L'exclusion se fait **six fois indépendamment en aval** (BED `hg38_chr1_22.bed`,
`filtered_bins.bed`, boucle `CHR=1..22` codée en dur dans beta_28M/TOO/THEMELIO…).
→ Ajouter un chemin mitochondrial ne demande **aucun re-basecalling ni réalignement**.

⚠ Fuite existante : le BED EPIC contient **7 régions chrM**. Ce qu'en fait `raima::model_v1/v2`
n'a pas été vérifié.

## Les chiffres

| | chrM | nucléaire |
|---|---|---|
| couverture | **2,2 – 148 x** | 0,37 – 2,7 x |
| médiane de longueur | 180 pb | 167 pb |
| moyenne | 656 pb | 184 pb |
| > 500 pb | 25,3 % | 1,3 % |
| hors fenêtre raima 75-500 | **31,3 %** | 3,3 % |
| CpG méthylés (5mC) | **0,69 %** | **71,1 %** |

Mesures faites à la convention exacte de `frag.nf` (`-F 3840` + longueur soft-clip déduite du
CIGAR). Fraction de reads mito = 0,0079 % (littérature : 0,0032 % médian, van der Pol 2023).
La couverture dépasse la littérature parce que **nos fragments mito sont 3-4x plus longs** que
les nucléaires : même fraction de reads, beaucoup plus de bases.

## Le confondant qui décide de tout

Séparation HCL vs CGFL, **sur des sujets tous sains** :

| feature | AUC cohorte |
|---|---|
| couverture chrM brute | **0,977** |
| ratio chrM/nucléaire | 0,955 |
| fraction > 1 kb | 0,955 |
| fraction > 220 pb | 0,727 |
| ratio court/long | **0,682** |

**Why :** 98,7-99,4 % du mtDNA plasmatique circule en mitochondries entières ou vésicules, pas
en ADN nu — donc gouverné par hémolyse, plaquettes et délai de centrifugation. Varie d'un
facteur 67 entre sains, contre 7 pour le nucléaire.

→ **L'abondance mitochondriale — la feature que DELFI utilise réellement — est la plus
confondue chez nous.** Copier DELFI serait le pire choix. L'abondance va au QC pré-analytique,
jamais au modèle. Seules les features de **forme** (normalisées en interne) sont recevables.

## Méthylation : négatif comme biomarqueur, mais outil anti-NUMT

0,69 % sur chrM contre 71,1 % au nucléaire (contrôle interne validant le basecaller), **en
nanopore natif** — donc hors de portée de la critique « artefact bisulfite ». Colle aux valeurs
publiées (Bicci 2022 : 0,37 ± 0,15 % ; MitSorter 2025 : 0,22 ± 0,03 %).

Basecalling **CpG-only** vérifié (positions listées / CpG attendus = 1,00) → 435 CpG sur chrM,
méthylation non-CpG inaccessible sans re-basecalling toutes-cytosines (GPU).

**Le retournement :** les NUMT portent la méthylation nucléaire (~63 %), le vrai mtDNA non
(0,7 %) → seuil ~15 % pour les trier (méthode MitSorter 2025). Intérêt réel : ça marche sur
les **fragments courts**, là où le MAPQ échoue (≤220 pb : seulement 53,5 % à MAPQ≥30 ; >220 pb :
95,4 %). Or le mtDNA tumoral est plus court que le normal → c'est là qu'on attend le signal.
Impossible en Illumina/bisulfite.

## Fermé par les chiffres — ne pas y revenir

- **Hétéroplasmie / mutations** : 378-810x requis (nanopore), nous sommes à 2-148x et le signal
  tumoral plasmatique est dilué sous le seuil.
- **Méthylation comme biomarqueur** : 0,69 %, il n'y a rien à mesurer.
- **Motifs d'extrémité 4-mer** (le signal de Dang 2024, AUC 0,9845) : 13,7 reads par motif chez
  nous contre 2354-6814x de capture chez eux. Trop mince par échantillon.
- **Analyses positionnelles / D-loop** : la référence est linéaire et le génome circulaire —
  1,5 % des reads démarrent en position 1, 2,9 % butent sur la fin. Le creux de couverture
  observé à la D-loop est indistinguable d'un artefact tant qu'on n'a pas de référence décalée.

## How to apply

Avant de construire quoi que ce soit : tester si la **forme** de la distribution de longueur
mitochondriale sépare cancer et sain **à centres équilibrés**. Sans cet équilibre on retrouvera
l'AUC 0,977 du site en croyant mesurer la tumeur. Rien n'a été mesuré sur cancer à ce jour.
Voir [[delfi_firstlook]] pour ce que DELFI fait de la mitochondrie (AUC 0,72 seule, ablation
montrant que leur modèle complet égale la fragmentomique seule).
