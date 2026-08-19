---
name: reads-28m-cpg-counting
description: "Comptage retrospectif de la population Preprocess_28M et de la population CpG — methode uniq+skipped, impasses ecartees, backfill 1506 samples, distribution"
metadata:
  node_type: memory
  type: project
  originSessionId: 7e91f1a9-0ac8-479a-8cc5-bfa7aa8b3b7c
  modified: 2026-08-19T00:00:00.000Z
---

# Comptage 28M et CpG (2026-08-19)

Ferme le trou de la cascade : `Preprocess_28M` ne publie toujours rien, mais son comptage se
reconstitue **entierement depuis des sorties deja sur S3**. Voir [[read-counting-cascade]].

## La formule

```
reads_28m  =  read_id uniques (EXTRACT_FULL_28M/*.bgzf)  +  skipped (*.modkit_extract_full.log)
```

Modkit lit le BAM produit par `Preprocess_28M` et range chaque read dans l'une de deux
categories : celles portant >= 1 CpG (ecrites dans la table) et celles qui n'en portent aucune
(comptees en `skipped`). La somme reconstitue son entree.

**Precision +-0,002 %**, verifiee contre `samtools view -c -q 20 -F 3844` sur 2 samples :

| sample | cible samtools | estime | ecart |
|---|---:|---:|---:|
| Healthy_826 | 81 117 | 81 122 | +5 (+0,0062 %) |
| Lung_9 (QUALIF V2.2.0) | **29 270 700** | 29 270 051 | -649 (-0,0022 %) |

Le residuel vient du tilde que modkit ecrit lui-meme (`skipped ~581`). Signe variable.
La valeur 29 270 700 de la cascade, calculee a la main, est ainsi reproduite.

## Les trois pieges

1. ⚠ **Compter les LIGNES ne marche pas** : une read produit une ligne par CpG *et par mod_code*
   (`h` + `m`). Surcompte mesure de **x3,7 a x6,4**, et le facteur varie avec la densite CpG du
   chromosome — aucun coefficient correctif possible.
2. ⚠ **Dedupliquer sur `read_id` seul ne marche pas non plus** : une read sans aucun CpG n'a
   **aucune ligne**. Sous-compte de 20 a 34 %. Il faut ajouter le `skipped`.
3. ⚠ **Ne pas utiliser le `processed` du log** : il vaut 1 565 sur chr20 de Healthy_826 la ou
   seuls 1 459 read_id apparaissent. C'est `uniq(read_id) + skipped`, pas `processed + skipped`.

## Performance

- **`uniq` sans `sort` suffit** : les lignes d'un meme read sont contigues. Verifie `uniq ==
  sort -u` sur **22/22 chromosomes de Lung_9** (chr2 : 1,68 M reads). Le backfill est donc un
  streaming O(n), sans memoire ni fichier temporaire.
- **`bgzip -@ 4 -dc` est 31 % plus rapide que `zcat`** (4,0 s contre 5,8 s sur 189 Mo) : les
  fichiers sont en BGZF, pas en gzip simple. Au-dela de 4 threads, plus de gain.
- ⚠ **`awk` en une passe est PIRE** (9,0 s) : il parse tous les champs. Garder le pipe
  `tail -n +2 | cut -f1 | uniq | wc -l`.
- ⚠ **`AWS_PROFILE=scw` n'apporte rien** (6,5 s contre 7,4 s en s3fs) : le goulot est la
  decompression, pas le reseau.

## Deux impasses ECARTEES — ne pas les reinstruire

**Dossier `BETA_28M`** (1,4 Mo/sample contre 3,3 Go) : aucune de ses deux valeurs ne convient.
`sampling total N reads` du `modkit_pileup.log` est un **plafond d'echantillonnage constant**
(10 042 sur les 22 chromosomes de Lung_9) ; il coincidait sur Healthy_826 chr20 uniquement parce
que ce BAM ne contient que 2 040 reads. Et `Processed + skipped` du pileup **sous-compte de 26 a
32 %** — `pileup` applique un filtre de qualite de modification que `extract full` n'applique pas.

**Index `.bai` et dossier `QC`** : aucun ne porte le filtre **MAPQ >= 20**, qui est precisement
ce qui separe FRAG (32 196 025 sur Lung_9) de 28M (29 270 700), soit 9,1 %. Les BAM de
`Preprocess_28M` — les seuls dont l'index porterait le bon filtre — n'ont pas de `publishDir`.

## Le backfill

`/scratch/boris/nb_read_28M/` : `one_sample.sh` (un sample), `run_backfill2.sh` (file prioritaire
+ reprise), `count_28M.sh` (validation contre samtools), `result_Lung_9.txt`.

**Sortie : `nb_reads_28M.tsv`, 1 506 samples, 100 % `OK`** — 846 CGFL liquid, 513 HCL liquid,
147 CGFL solid. Colonnes : `type labo sample_id n_chr reads_with_cpg reads_skipped reads_28m status`.

⚠ **Cle TYPE+LABO+ID obligatoire** : `Lung_9` existe en **CGFL (13 264 379)** ET en **HCL
(29 270 051)**, deux samples distincts. Le QUALIF V2.2.0 est la copie du HCL.

Cout : 4,4 To lus en s3fs, ~4 h a 16 process. Debit ~37 s/sample.

## La population CpG

`reads_with_cpg` + `reads_with_cpg_pct` ajoutees a la table `qc` de trace-prod en **schema v25**
(2026-08-19), 1332/1332 remplies, perimetre liquid. Les `_pct` sont rapportes a `reads_total`,
comme les 11 autres.

**~35 % des reads du module 28M ne portent aucun CpG** et le traversent sans rien apporter a la
mVAF : 68,1 % en moyenne sur les 1 506 du TSV, mediane **64,63 %** sur les 1 332 en base.
Sur Lung_9 : 29 270 700 reads 28M dont 19 151 267 porteuses (65,4 %), soit **43,2 % du BAM
d'origine** la ou la cascade s'arretait a 65,97 %.

## Distribution (publiee dans le Google Doc, partie 3)

| decoupe | n | 28M % | 28M reads | CpG % | CpG/28M % |
|---|---:|---:|---:|---:|---:|
| cohorte | 1332 | **62,59** | 26,0 M | **40,53** | **64,63** |
| plasma | 1243 | 62,79 | 26,9 M | 40,64 | 64,49 |
| **urine** | 89 | **52,74** | 10,2 M | 36,51 | **71,20** |
| cancer | 1003 | 62,57 | 25,5 M | 40,38 | 64,58 |
| healthy | 329 | 62,66 | 27,2 M | 41,07 | 64,81 |
| CGFL | 819 | 61,80 | **18,9 M** | 40,26 | 64,96 |
| HCL | 513 | 63,58 | **36,8 M** | 41,02 | 64,37 |

- **Meme signature que le Primary mapped %** : coeur etroit (IQR 3,4 et 3,0 pt) + longue trainee
  basse (asymetrie -5,5 et -4,4). Plafond **70,10 %**, structurel (28M est un sous-ensemble du
  Primary mapped qui plafonne vers 80 %).
- **La matrice est le seul axe discriminant** : -10 pt entre plasma et urine.
- ⚠ **Le ratio CpG/28M s'INVERSE chez l'urine** (71,20 contre 64,49) : moins de reads survivent,
  mais celles qui survivent portent plus de CpG. Piste coherente = fragments plus longs
  ([[n50-ratio-qc]], urine N50 median 1,78 contre 1,10) — **non mesuree**.
- **Cancer vs healthy ne separe rien** (62,57 / 62,66). Resultat negatif net.
- ⚠ **Le labo separe les VOLUMES mais pas les proportions** : 1,8 pt d'ecart en %, mais x1,9 en
  nombre de reads. Toujours lire les deux.
- **16 urines sur 89 sous 40 % de 28M** contre 2 plasmas sur 1 243 ; **14 sont les memes** que les
  16 urines a > 30 % de non-alignement ([[unmapped-reads-urines]]). Les 2 ecarts sont
  interpretables : `Bladder_Urine_02_066` et `_119`, les seules jugees rendables, restent
  au-dessus de 40 % — le 28M les recupere la ou le taux de non-alignement les condamnait.
- Extremes : min `Bladder_Urine_02_067` (34 871 reads), max `Colon_51` (100,9 M, un des 4 plasmas
  HCL aux alignements dedoubles).

## Ou vit le filtre MAPQ

**Seul `Preprocess_28M` filtre sur MAPQ** (`-q 20 -F 3844`). EPIC (`-L bed_epic -F 3840`) et FRAG
(`-L bed_fragmentomics -F 3840`) **n'ont aucun `-q`**. C'est la raison de fond pour laquelle
aucune sortie QC publiee ne permet de deduire le 28M.

## Comptage EPIC (au passage)

`QC/Cramino/{ID}.merged.epic.cramino.tsv` colonne 6. Sur le BAM EPIC, `num_alignments == num_reads`
et `percent_from_total = 100` : le `-L` elimine les non alignees (sans position, elles ne
chevauchent rien) et `-F 3840` le reste, donc **la strate D seule** — le gotcha du merged
(`num_reads` inclut les non alignees) **ne s'applique pas ici**.
⚠ `nb_reads_epics` et `percentage_epics` sont calcules par `rapport.nf` mais **jamais publies** :
ils n'alimentaient que le rapport PDF, mort depuis juin 2026. `nb_reads_m` du JSON est le merged
en millions, pas l'EPIC.
