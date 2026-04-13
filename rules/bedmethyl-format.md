---
paths:
  - "**/Bam2Beta/**"
  - "**/IA/**"
  - "**/IA-for-IA/**"
  - "**/exploratory-analysis*/**"
  - "**/*.bedMethyl*"
  - "**/modkit*"
---

# Format bedMethyl — modkit (ONT)

Référence des colonnes bedMethyl produites par `modkit pileup`.
Source : https://gensoft.pasteur.fr/docs/modkit/0.4.0/intro_bedmethyl.html

## Colonnes 1-9 : BED9 standard

| Col | Nom | Description | Type |
|-----|-----|-------------|------|
| 1 | chrom | Chromosome ou contig | string |
| 2 | chromStart | Position début (0-based) | int |
| 3 | chromEnd | Position fin (exclusive) | int |
| 4 | name | Code de modification (`m` = 5mC, `h` = 5hmC) | string |
| 5 | score | Couverture valide (Nvalid_cov), pour visualisation | int |
| 6 | strand | Brin ADN : `+` ou `-` | char |
| 7 | thickStart | = chromStart (affichage) | int |
| 8 | thickEnd | = chromEnd (affichage) | int |
| 9 | itemRGB | Couleur affichage (ex: `255,0,0`) | string |

## Colonnes 10-18 : champs modkit étendus

| Col | Nom | Description | Type |
|-----|-----|-------------|------|
| 10 | Nvalid_cov | Couverture valide = Nmod + Nother_mod + Ncanonical | int |
| 11 | percent_modified | % d'appels classés comme modifiés (Nmod / Nvalid_cov × 100) | float |
| 12 | Nmod | Nb appels classés comme la modification spécifiée | int |
| 13 | Ncanonical | Nb appels classés comme base canonique (non modifiée) | int |
| 14 | Nother_mod | Nb appels classés comme une autre modification (même base canonique) | int |
| 15 | Ndelete | Nb reads avec une délétion à cette position | int |
| 16 | Nfail | Nb appels sous le seuil de probabilité (exclus de la couverture valide) | int |
| 17 | Ndiff | Nb reads avec une base différente de la base canonique attendue | int |
| 18 | Nnocall | Nb reads alignés avec la bonne base mais sans appel de modification | int |

## Relations clés

```
Nvalid_cov = Nmod + Nother_mod + Ncanonical
percent_modified = (Nmod / Nvalid_cov) × 100

Nfail et Nnocall ne comptent PAS dans Nvalid_cov
Ndelete et Ndiff = reads ne pouvant pas produire d'appel valide
```

## Commande modkit standard AIMA

```bash
modkit pileup --cpg --combine-strands --combine-mods input.bam output.bedMethyl
```

- `--cpg` : uniquement les CpG
- `--combine-strands` : combine les brins + et - pour chaque CpG
- `--combine-mods` : fusionne 5mC et 5hmC en un seul appel

## Colonnes utilisées par le pipeline IA-for-IA

Pour le scoring ctDNA, seules ces colonnes sont utilisées :
- Col 1 (chrom), Col 2 (chromStart) → position du CpG
- Col 10 (Nvalid_cov) → couverture (filtrage : coverage >= 30% des samples)
- Col 11 (percent_modified) → valeur de méthylation [0-100] → convertie en beta [0-1]
