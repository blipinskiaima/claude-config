---
name: fano-couverture-qc
description: "Indice de dispersion (Fano) comme critere QC — genomique brut ECARTE, EPIC retenu (48 outliers dont 47 nouveaux sur 1344 samples), confondants CNV et longueur ecartes"
metadata:
  node_type: memory
  type: project
  modified: 2026-08-19T14:40:00.000Z
---

# Fano — homogeneite de couverture comme critere QC (2026-08-17/19)

Instruit sur **Lung_9** (QUALIF, propre) et **Bladder_Urine_02_117** (le plus aberrant de la
cohorte), puis mesure sur **1 344 des 1 346 liquides**. Materiel : `/scratch/boris/depth_fano/`.

Fano = variance / moyenne de la profondeur. Poisson pur = 1. > 1 = couverture en paquets.

## Ce qui ne marche pas

**Le Fano genomique BRUT est inutilisable.** Calcule sur la distribution complete par base
(MAPQ 20, autosomes), il donne **22,30 pour Lung_9** contre **7,41 pour l'urine** — il classe
le sample propre 3x pire que l'aberrant. Cause : la variance est ecrasee par les satellites
peri-centromeriques, qui montent a **23 130x** sur quelques bases et entrent au carre.

**Le Fano de cohorte ne marchait que par accident** : il etait calcule depuis `global.dist`,
qui est **tronque** (~38 niveaux). Les extremes n'y figuraient pas. Garde-fou fortuit, pas un
choix de conception — a ne pas reproduire sans le savoir.

**`--use-median` est inutilisable a notre profondeur** : la mediane de profondeurs entieres est
un entier. A 2,3x elle ne produit que **7 valeurs distinctes** sur 28 760 bins, dont 90 % a
exactement 2. Elle ecrase bien les pics (max 3,0x med au lieu de 29,6x) mais detruit toute la
resolution. Conviendrait a du 30x, pas a du 2x.

## Ce qui marche — le binning

**A l'echelle du bin de 100 kb, le bruit d'echantillonnage disparait** : CV observe entre bins
**305x** le bruit de Poisson attendu (62,21 % contre 0,204 %). C'est ce qui leve la limite de
fond de l'approche base-par-base — a basse profondeur chaque base est un tirage a pile ou face
(*thinning* de Poisson), mais 100 000 bases agregees donnent une moyenne precise a 0,2 %.

Le `per-base` ne sauverait donc rien en base-par-base : ce n'etait pas un probleme de precision
d'arrondi, mais de physique de l'echantillonnage.

## Ce qui marche — le perimetre EPIC

Le BED `epic850K.extended.100.clean.bed` ne contient **aucun satellite** (max 90x contre
23 130x genome-wide), donc rien ne pollue la variance.

| | Lung_9 | Urine_117 |
|---|---:|---:|
| Fano genomique brut (MAPQ 20) | 22,30 | 7,41 | **inverse** |
| Fano BED EPIC | 1,12 | 3,90 | x3,5 |
| Fano whitelist CpG v1 | 1,12 | 3,74 | x3,3 |
| Fano cohorte (`global.dist` tronque) | 1,32 | 3,94 | x3,0 |

BED EPIC et whitelist donnent la meme chose — la whitelist est un sous-ensemble des memes
regions. Le **BED EPIC suffit** : deja dans le pipeline (`params.bed_epic`), 75 Mb au lieu de
0,67 Mb (moins de bruit), et independant de la version du modele raima.

## Mesure sur la cohorte (1 344 liquides)

```
p05 1,062 · mediane 1,152 · p95 1,290 · p99 1,523 · max 4,053
Tukey (Q1 1,117 / Q3 1,197 / IQR 0,080) -> seuil 1,320
   48 outliers (3,6 %), dont 47 INVISIBLES aux seuils 5 M reads / 0,25x
   plasma 35/1183 (3,0 %) · urine 13/98 (13,3 %) · sang 0/58
```

C'est la **premiere metrique du palier 1 a passer le critere de succes** — le MAD et
`coverage_percent` ne rejetaient aucun sample nouveau (voir [[qc-palier1-candidats-ecartes]]).

Les outliers sont confortables sur les criteres actuels : 1,7x a 8,5x de profondeur, 40 a
134 M de reads. Exemple hors urine : **`Breast_51`** (Fano 1,817, depth 3,70x, 62,9 M reads,
N50 178 pb — taille de fragment normale).

## Confondants testes

| confondant | resultat |
|---|---|
| **CNV reel** | `corr(Fano, score_cnv) = -0,020`. Outliers : score_cnv median **0,00** contre 4,28. **Ecarte** |
| **Longueur de fragment** | `corr(z, N50) = +0,050`, `pct_mass_removed` +0,008. Les flagges ont des fragments **plus courts** (166 vs 174 pb). **Ecarte** |
| **Nombre de reads** | +0,065 sur le residu. **Ecarte** |
| **Profondeur** | `corr(EPIC, depth) = +0,445` — **subsiste**, il faut travailler sur un residu |
| **Matrice** | urines **13,3 %** vs plasma 3,0 %. Reel, mais 35 plasmas flagges : ce n'est pas qu'un detecteur d'urine |

⚠ `corr(Fano EPIC, Fano genomique) = +0,811` — les deux designent largement les memes samples.
Le proxy genomique est **gratuit et deja calcule** ; comparer les deux listes d'outliers avant
de payer l'EPIC en routine.

## Piste ouverte — lien avec le module CNV

**55,9 % des outliers Fano ont `score_cnv` = 0** contre 26,9 % dans la cohorte —
**enrichissement x2,1**. Hypothese : la couverture inegale empeche le module CNV de produire un
resultat. ⚠ Sens de la fleche **non etabli**, et 34 outliers c'est peu. A tester : les samples
a CNV nul ont-ils un Fano superieur a profondeur comparable ?

## Reference — Lung_9 vs Urine_117 (MAPQ 20, autosomes)

| | Lung_9 | Urine_117 |
|---|---:|---:|
| profondeur | 2,16x | 3,59x |
| bases a 0x (attendu Poisson) | 18,3 % (11,6) | 20,4 % (2,7) |
| chromosomes hors +/-5 % | 1 (chr19) | 10 |
| CpG du modele jamais vus | 11,5 % | 4,05 % |
| CpG a >= 10 reads | **0,0 %** | 23,9 % |

⚠ **chr19 est systematiquement le plus bas** (-6,9 % genome, -8 % EPIC, -8,6 % CpG modele) —
c'est le chromosome le plus riche en GC. Signature de biais GC, presente aussi chez le sample
propre.

⚠ **Aucun CpG de Lung_9 n'atteint 10 observations** (repere Loyfer). A 2,3x, chaque CpG repose
sur 2 reads. raima agrege des milliers de CpG, donc ce n'est pas disqualifiant — mais ca situe.

Voir [[qc-palier1-candidats-ecartes]] · [[read-counting-cascade]] · [[n50-ratio-qc]]
