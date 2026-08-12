---
name: read-counting-cascade
description: "Cascade des comptages de reads Bam2Beta — 4 strates atomiques A/B/C/D, 6 metriques, ce qui est publie ou non, valide contre flagstat sur 10 samples"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c6971ef-9e62-46ae-935a-5026efb56aa3
  modified: 2026-08-11T12:40:06.669Z
---

# Cascade de comptage des reads (Bam2Beta V2.2.0)

Reference chiffree : **Lung_9**, QUALIF V2.2.0, `-profile docker,tower,prod,scw`.
Etabli le 2026-08-11. Validation : concordance exacte contre `samtools flagstat` sur
**10 samples** couvrant tous les profils (chimeriques, palindromiques, contamine gDNA,
minimum de cohorte, temoins). Zero ecart sur 6 metriques.

```
             BAM merged - Lung_9.merged.bam (18 Go)
                        |
                        v
             44 370 277 * nb_reads_total = A+B+C+D             100,00 %
                        |
                        +-- B = secondaires       6 374 488   - 14,37 %
                        v
             37 995 789 * num_alignments = A+C+D                85,63 %
                        |
                        +-- C = supplementaires     303 320   -  0,68 %
                        v
             37 692 469 * num_reads = A+D                       84,95 %
                        |
                        +-- A = non alignees      4 063 811   -  9,16 %
                        v
             33 628 658 o Primaires mappees = D                 75,79 %
                        |
                        +-- hors chr1-22          1 432 633   -  3,23 %
                        v
             32 196 025 * FRAG                                  72,56 %
                        |
                        +-- MAPQ < 20             2 925 325   -  6,59 %
                        v
             29 270 700 o Preprocess_28M                        65,97 %

             * publie par le pipeline    o jamais publie
```

## Les 4 strates atomiques

| | strate | Lung_9 |
|---|---|---:|
| **A** | reads non alignees | 4 063 811 |
| **B** | alignements secondaires (multi-mapping) | 6 374 488 |
| **C** | alignements supplementaires (reads splittees) | 303 320 |
| **D** | alignements primaires mappes | 33 628 658 |

## Table de verite — quelle metrique contient quelle strate

| metrique | A | B | C | D | commande | publie |
|---|:-:|:-:|:-:|:-:|---|:-:|
| `nb_reads_total` | X | X | X | X | `samtools view -c` (aucun flag) | oui |
| `mapped` | — | X | X | X | `idxstats` — **jamais execute** | non |
| `num_alignments` | X | — | X | X | cramino col 4, `≡ -F 0x100` | oui |
| `num_reads` | X | — | — | X | cramino col 6, `≡ -F 0x900` | oui |
| primaires mappees | — | — | — | X | deduit : `num_reads − A` | non |

⚠ **`mapped` exclut A et garde B ; `num_alignments` fait l'inverse.** Aucune soustraction ne
relie les deux — c'est pourquoi `mapped` ne peut pas s'inserer dans la cascade lineaire.

## Ou lire chaque valeur

| valeur | fichier |
|---|---|
| `nb_reads_total` | `QC/Samtools/{ID}.nb_reads_total.tsv` → `metadata.json` |
| `num_alignments` / `num_reads` | `QC/Cramino/{ID}.merged.cramino.tsv` (col 4 / col 6) |
| FRAG | `QC/Samtools/{ID}.nb_reads_total_filtered_softclipped.tsv` — doublon strict de `wc -l` sur `Fragmentomics/filtered_softclipped/{ID}.read_lengths.csv` |
| `Preprocess_28M` | **nulle part** — 22 executions (1/chromosome), jamais publie. ⚠ Le F du schema (29 270 700 pour Lung_9) a ete **calcule a la main** (`samtools view -c -q 20 -F 3844` sur chr1-22), ce n'est PAS une sortie du pipeline. **TODO** : publier ce comptage (todo-optimisation, basse prio) |
| **A** non alignees | `QC/Samtools/{ID}.idxstats.tsv` — **ajoute le 2026-08-11**, retrospectif sur les 1471 samples + `BAM_Count` modifie pour les runs futurs |

⚠ Ancien nommage sur les runs anciens : `{ID}.cramino.tsv` sans le `.merged`.

## Gotchas

- **`nb_reads_aligned` du `metadata.json` porte un nom faux** : il vaut `num_reads`, qui inclut
  les reads NON alignees (effet `--ubam` de cramino). Sur Lung_9 il annonce 37 692 469 la ou le
  nombre de reads reellement alignees est **33 628 658** — surestimation de 12 %, qui monte a
  **22 % sur `Lung_Alc_79_av`** (18 % de non alignees).
- **`flagstat` n'apporte rien** : `duplicates` et `QC-failed` sont a **0 sur 10/10 samples** (le
  pipeline ne fait aucun `markdup`, dorado/minimap2 ne posent pas le flag 0x200). Toute la
  cascade se reconstitue depuis les fichiers publies + un `idxstats` (lecture de l'index seul).
  Une recommandation de remplacer `view -c` par `flagstat` a ete formulee puis **abandonnee**
  sur cette base.
- **Corollaire** : `-F 3840` (FRAG) est equivalent a `-F 0x900` dans notre pipeline, deux des
  quatre bits n'etant jamais poses. L'ecart D → FRAG est donc entierement du au hors chr1-22.
- **FRAG et Preprocess_28M ne different que par le MAPQ** : `samtools view -c -F 3844` sur
  chr1-22 donne **exactement** la valeur FRAG (verifie sur 2 samples). Le `-q 20` coute 9,1 %.
- Le BAM merged est traverse **~4 fois** par run rien que pour compter (BAM_Count, cramino,
  Extract_read, 22x Preprocess_28M).

## Deux ratios detecteurs, gratuits

Calculables depuis les seuls fichiers publies, sans relire un BAM :

```
nb_reads_total / num_reads   ->  non-mapping + alignements multiples
num_alignments / num_reads   ->  alignements multiples seuls
```

| sample | total/reads | align/read | profil |
|---|---:|---:|---|
| Lung_9 | 1,18 | 1,008 | normal |
| Lung_Alc_79_av | 1,23 | 1,059 | temoin (18 % non alignees) |
| Lung_Alc_79_prog | **2,40** | **2,034** | concatemeres, 43 % de supplementaires |

C'est ce second ratio qui a servi a identifier les concatemeres de ligation et les reads
palindromiques — voir [[covdepth-qc-valorization]] et `docs/QC-seuils-biopsie-liquide.md`.

## Materiel

Comparateur reconstitution vs flagstat : `/scratch/boris/flagstat/compare.sh`, sorties brutes
conservees dans `/scratch/boris/flagstat/raw/` (relancer ne relit plus les BAM).
