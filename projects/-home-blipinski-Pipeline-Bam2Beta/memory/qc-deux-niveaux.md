---
name: qc-deux-niveaux
description: "Architecture QC primaire / QC contributif — les 2 metriques retenues (nb_reads_primary >= 5 M, reads_primary_mapped >= 4 M), leurs seuils et ce qui les fonde"
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-14T14:33:46.629Z
  originSessionId: c23b78b9-f616-423e-90dd-4fb111a4cd59
---

# QC primaire / QC contributif (2026-08-14)

Architecture a deux niveaux instruite sur les 1 332 liquides de la table `qc` de trace-prod.
**Rien n'est implemente** : ni en base, ni dans le pipeline, ni dans `check-run-output.sh`.
Documente dans le Google Doc QC, onglet « Nb reads mapped », partie 6.

## La regle de partage

> Un run de sequencage supplementaire corrigerait-il le defaut ?

**OUI** -> defaut de QUANTITE, actionnable par le client -> **QC primaire**, arret du workflow.
**NON** -> defaut de NATURE de l'echantillon -> **QC contributif**, resultat rendu avec reserve.

## Les deux metriques

| | QC primaire | QC contributif |
|---|---|---|
| metrique | `nb_reads_aligned` -> a renommer `nb_reads_primary` | `reads_primary_mapped` |
| perimetre | **A + D** — molecules sequencees, alignees ou non | **D** — molecules reellement alignees |
| source | cramino `num_reads`, lue par `cut -f 6` ([rapport.nf:45]) | `num_reads` moins la ligne `*` d'idxstats |
| seuil | **5 M** | **4 M** |
| si KO | ARRET, aucun resultat delivre | resultat rendu, marque NON CONTRIBUTIF |
| action | relancer le sequencage | nouveau prelevement |
| effectif | 72 (5,41 %) | 6 (0,45 %) |

Contributif : 1 246 (93,54 %). Non evaluables (pas d'idxstats) : 8 (0,60 %).

## Ce qui fonde les seuils — la table `rarefaction`

458 echantillons raréfiés aux 5 niveaux (1M/2M/5M/10M/20M), chacun compare a **sa propre
version 20M**. Faux positif induit = negatif a 20M (mVAF v1.4 < 0,32, gate du modele TOO)
devenu positif au niveau raréfié.

| niveau | \|ecart mVAF\| median | faux positifs induits |
|---|---:|---:|
| 10 M | 0,0089 | 5,72 % |
| **5 M** | 0,0373 | **11,14 %** |
| 2 M | 0,1400 | 24,40 % |
| 1 M | 0,2940 | 35,24 % |

Le **score fragmentomique est insensible au volume** (ecart max 0,0021 a 1M, contre 0,03 pour
faire basculer une categorie Themelio) : le risque est porte par la mVAF seule.

Seuil du contributif = **coude de la courbe** : 3->4 M fait tomber le residuel de 7,9 a 5,2 %,
4->7 M ne gagne que 0,08 point. Meme logique que le « milieu d'intervalle vide » des seuils N50,
mais en rendement decroissant.

## Les 5 gotchas

1. ⚠ **Recouvrement de 85,9 %** entre les deux criteres appliques independamment (5 / 67 / 6 sur
   78). Arithmetique : 4/5 = 0,80 est proche du taux median de molecules alignees (0,87). Le QC
   contributif ne vaut pas par le NOMBRE qu'il ajoute mais par la NATURE des 6 : 9 a 70 M de
   molecules pour 0,1 a 2,4 % d'alignement. `Bladder_Urine_02_099` = 70,5 M pour 120 000 alignees.
2. ⚠ **Le seuil de 5 M est mesure sur des LIGNES** (`samtools view -s` echantillonne tous les
   enregistrements) : le palier 5M de la mesure vaut ~**4,2 M molecules**. Retenir 5 M sur
   `reads_primary` est donc plus strict que ce que la mesure impose — dans le bon sens.
3. ⚠ **Le 20M est reference a lui-meme** : son taux d'erreur est nul par construction, les taux
   cites sont des **minorants**. Sans niveau 15M, rien ne discrimine dans la plage 10-20 M.
4. ⚠ **Le contributif est en amont de FRAG et 28M** : hors chr1-22 (mediane **3,27 %**) et
   MAPQ<20 ne sont pas deduits. Un seuil sur D est optimiste pour ces modules. `reads_frag` est
   publie et calculable ; **`reads_28m` est NULL 1332/1332** (Preprocess_28M ne publie rien).
5. ⚠ **La profondeur (0,25x) reste necessaire** : l'architecture gagne 9 echantillons sur les
   criteres actuels mais en perd 1 (`Bladder_Urine_02_097`, rattrape par ses 0,24x seulement).

## Repartition par tissu (Bladder eclate par matrice)

| tissu | n | primaire KO | contributif KO | contributif |
|---|---:|---:|---:|---:|
| **Bladder urine** | 89 | **18** | **6** | 57 |
| **Bladder sang** | 58 | **1** | 0 | 57 |
| Lung | 436 | 15 | 0 | 421 |
| Healthy | 329 | 18 | 0 | 311 |
| Colon | 209 | 17 | 0 | 192 |

L'agregat `Bladder` de la Tour (`extract_tissue`, 1re partie du nom) melange **deux populations
sans rapport** : eclate, l'urine porte 24 defauts sur 89 et **la totalite des 6 echecs de
contributivite**, le sang 1 sur 58. Le QC contributif ne se declenche sur **aucun autre tissu**.

Voir [[read-counting-cascade]] pour la cascade et la table `qc`, [[metadata-json]] pour le champ
`nb_reads_aligned`, [[n50-ratio-qc]] pour l'axe contamination gDNA, distinct de celui-ci.
