---
name: unmapped-reads-urines
description: "Origine des reads non alignes des 16 urines de vessie CGFL — 2 populations (proliferation bacterienne / sequencage trop faible), 6 especes, clivage a 9 M de lectures"
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-14T14:17:07.379Z
  originSessionId: 29628a00-4f33-42b4-bd1c-33ece9372659
---

# Reads non alignes des urines de vessie (2026-08-14)

Investigation des **16 echantillons a plus de 30 % de reads non alignes**, tous CGFL,
toutes des urines de vessie (voir [[n50-ratio-qc]] pour le contexte matrice urinaire).
Les 16 ont ete traites. Espace de travail : `/scratch/boris/unmapped` (29 Go).

## LA REFERENCE D'ALIGNEMENT DU PIPELINE — a connaitre au-dela de ce chantier

Etabli en comparant l'en-tete des BAM au `.fai` local : **0 contig d'ecart dans les deux sens**.

| | valeur |
|---|---|
| aligneur | **MinKNOW 6.5.14**, alignement live sur GPU A800 pendant le run |
| reference | **`GCA_000001405.15_GRCh38_no_alt_analysis_set.fa`** — 195 contigs, 3,100 Gb |
| preset | `map-ont` (pas de ligne @PG minimap2 avec ses parametres) |

⚠ **Ce n'est PAS le hg38 UCSC** de `params.fasta` (455 contigs, 3,209 Gb) : celui-la sert aux
modules Bam2Beta, pas a l'alignement, fait en amont par MinKNOW. **Version SANS decoy hs38d1
ni contigs HLA** — des sequences humaines connues hors assemblage principal n'ont aucune cible.

`chrEBV` est present, donc EBV serait capture s'il y en avait.

## Resultat : DEUX populations, clivage sur le VOLUME sequence

Aucun recouvrement — **3,31 M / 9,09 M de lectures**, rien entre les deux.

| groupe | n | BAM | ce que c'est |
|---|---:|---|---|
| A | 8 | 9,1 a 70,6 M | une bacterie occupe **52 a 87 %** du sequencage |
| B | 8 | 0,6 a 3,3 M | **aucun organisme dominant** — sequencage trop faible, pas une contamination |

⚠ **Le taux de non-alignement ne discrimine pas** : `02_054` a 91,5 % de non alignees et reste
non identifiable ; `02_119` en a 34,2 % et livre son *Lactobacillus*. C'est le volume total.

### Groupe A — 6 especes, aucune partagee

| sample | organisme | part attribuee |
|---|---|---:|
| `01_001` | *Proteus mirabilis* | 86,5 % |
| `02_067` | *E. coli* souche uropathogene | 81,1 % |
| `02_014` | *Alcaligenes faecalis* + *Proteus mirabilis* | 76,2 % |
| `02_099` | *Citrobacter freundii* + *Morganella morganii* | 67,5 % |
| `01_003` | *Proteus mirabilis* | 62,8 % |
| `02_119` | *Lactobacillus crispatus* (**flore normale**) | 62,3 % |
| `02_100` | *Citrobacter freundii* | 58,3 % |
| `02_066` | *Providencia rettgeri* | 51,6 % |

**L'argument decisif contre une contamination de laboratoire** : `01_001` et `01_003` portent
tous deux *P. mirabilis*, mais sur le **meme genome de reference** l'un s'aligne a 86,5 % et
l'autre a 62,8 % → **souches distinctes**. Une source commune donnerait la meme souche.

### Groupe B — ce n'est PAS un probleme de longueur

Piste testee et **ecartee** (je l'avais d'abord deduite a tort du seul `02_044`) :

| | groupe B | `02_067` (identifie a 81 %) |
|---|---:|---:|
| longueur mediane | **112-138 pb** (plus long !) | 104 pb |
| bases repetees consecutives | 26,6-27,2 % | 26,4 % |
| classification a `--confidence 0` | **2,9 %** | — |
| **ecart interquartile du GC** | **18 points** | 9 points |

Le GC deux fois plus etale signe un **melange heterogene**, pas une espece non repertoriee.
Seul `02_044` a vraiment des reads courts (72 pb).

## Les 2 limites qui faisaient sous-estimer (question de Boris : « pourquoi un % mineur ? »)

Kraken2 seul n'expliquait que **15 a 35 %**. Deux causes cumulees, pas une seconde origine :

1. **Kraken2 decroche sur les reads courts.** Un read de 90 pb ne porte que ~56 k-mers de 35 nt.
   Test croise : parmi les reads abandonnes par Kraken2, **55,7 % s'alignent sur *E. coli*** contre
   **0,04 %** sur *L. crispatus* — specificite > 1000x. Matrice croisee complete dans
   `test_nonclasses.sh`, diagonale nette sur 5/6.
2. **La souche de reference n'est pas celle du patient.** Sur `02_067` :

   | reference *E. coli* | alignes |
   |---|---:|
   | K-12 MG1655 (labo) | 61,7 % |
   | CFT073 (UPEC pyelonephrite) | 80,2 % |
   | **UTI89 (UPEC cystite)** | **81,1 %** |

   **+19,4 points** en changeant de souche. Signature a reconnaitre : taux bas + residu **long**
   = mauvaise souche ; taux haut + residu **court** = limite de longueur.

## Ce qui n'est PAS determinable (a tenir devant un biologiste)

Quatre situations donnent **le meme profil de sequencage** : infection urinaire · colonisation ·
souillure au recueil · **prolifération avant congelation**. Trancher demande l'ECBU du meme
prelevement, le contexte clinique, les conditions de recueil et le **delai avant congelation**.

- *L. crispatus* (`02_119`) est de la **flore urogenitale saine**, pas un pathogene.
- Seuls *E. coli* et *P. mirabilis* sont etiquetes uropathogenes **sur source verifiee** ;
  *Citrobacter*, *Providencia*, *Morganella*, *Alcaligenes* ne l'ont pas ete.

## Consequence QC

**2 des 16 seulement sont rendus** : `02_119` (2,71x) et `02_066` (0,92x) — les 2 seuls avec
plus de 2,5 % d'ADN humain. Le seuil de profondeur intercepte les 14 autres **sans voir la
cause**, qui n'est pas la meme dans les deux groupes. `reads_unmapped_pct` comme signal direct
reste une piste non instruite.

## Gotchas outils

- **`master` de `DerrickWood/kraken2` NE COMPILE PAS** : `'struct kraken2::Sequence' has no member
  named 'compare_header'` (`classify.cc:570`). Se placer sur une release taguee — `git checkout
  v2.17.1` — avant `install_kraken2.sh`. Compilation OK ensuite, sans root.
- **URLs des index Kraken2** : la convention a change. `k2_standard_16gb_<date>` → **404**. Format
  actuel `k2_standard_16_GB_<date>`. Extraire les liens de <https://benlangmead.github.io/aws-indexes/k2>,
  ne pas les deviner.
- **Sortie `kraken2 --output`** : colonnes `C/U | seqID | taxID | longueur | LCA`. La longueur est
  en **colonne 4**, pas 3 — lire la 3 donne des taxID interpretes comme des longueurs (medianes
  aberrantes de 1833 pb).
- **`samtools view <bam> '*'`** cible la section des reads non places **via l'index** : 7 min sur
  un BAM de 10,7 Gio au lieu d'une passe complete. Debit s3fs ~26 000 reads/s.
- ⚠ **`The index file is older than the data file`** sur **tous** les BAM de `RetD/` : le `.bai`
  est systematiquement anterieur au `.bam`. Les comptages tombent au read pres sur la table `qc`
  (16/16), donc les index sont exploitables — mais l'anomalie est generale.
- **Genomes de reference** : API NCBI datasets v2alpha `/genome/taxon/<espece>/dataset_report?filters.reference_only=true`
  donne accession + `assembly_name`, dont on construit l'URL FTP. Elle fournit aussi le **GC publie**.

## Materiel

`/scratch/boris/unmapped` : `extract.sh` (extraction + histogrammes en une passe) · `run_batch.sh`
(chaine complete par echantillon) · `affinage.sh` / `affinage_auto.py` (realignement + detection
2e espece) · `test_nonclasses.sh` (matrice croisee) · `fig_seize.py` (figure de synthese pour
biologiste, portee au Google Doc). Index Kraken2 Standard-16 dans `db/` (15 Go).

Voir [[read-counting-cascade]] pour la definition des strates et [[n50-ratio-qc]] pour la
matrice urinaire.
