---
name: qc-palier1-candidats-ecartes
description: "Palier 1 du doc QC-seuils — MAD ichorCNA et coverage_percent instruits puis ECARTES, avec les mesures qui les disqualifient (ne pas les reinstruire)"
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-12T10:50:38.245Z
  originSessionId: b56b0f4a-9a7a-4318-bb95-549d981af39e
---

# Palier 1 QC — les deux candidats ECARTES (2026-08-10)

Instruits et mesures sur les **1 471 echantillons de production**. Verdicts portes dans
`docs/QC-seuils-biopsie-liquide.md` au commit `a22974f`. **Ne pas les reinstruire** sans
raison nouvelle : la mesure est faite, elle est reproductible, elle est negative.

Le critere de succes applique aux 5 candidats : *attrape-t-il des echantillons que la paire
5 M reads / 0,25x laisse passer ?* Un critere qui rejette les memes samples n'apporte rien.

## MAD GC-Map (ichorCNA) — ECARTE

Disponible sans recalcul dans `ichorCNA/{ID}.params.txt`, champ `GC-Map correction MAD`
(1 471/1 471 presents). Distribution : mediane **0,0208**, p99 0,134, max 0,408.

| seuil publie | rejetes | dont **nouveaux** |
|---|---:|---:|
| > 0,30 « too noisy » | 5 | **0** |
| > 0,20 « sufficient » | 10 | **0** |
| > 0,15 « haute qualite » | 11 | **0** |
| > 0,12 *(non publie)* | 22 | 4 |

A **tous les seuils publies**, ses rejets sont un sous-ensemble strict de ceux de la paire
actuelle. Il ne redevient discriminant qu'a 0,10-0,12, c'est-a-dire en inventant un seuil.

⚠ **L'argument « independant de la longueur de read » du doc est FAUX** : `corr(MAD, longueur
derivee) = +0,411`, `corr(MAD, reads alignees) = -0,468`, `corr(MAD, coverage) = -0,381`.

**Ce qu'il garde** : les 10 samples a MAD > 0,20 sont tous deja ecartes par la paire actuelle
— une metrique publiee par les auteurs de l'outil, construite independamment, designe les
memes echantillons. C'est une **validation croisee externe** des seuils en vigueur, utile au
dossier ISO (clause 7.3.3.e.3), pas un critere de rendu.

⚠ Dependance : le MAD n'existe que si `ICHORCNA` est actif. Vrai via les lanceurs `dev/SCW/`
(`-profile docker,tower,$TYPE,scw`), **faux** sous `-profile ...,prod` ou `ICHORCNA = false`.

## `coverage_percent` (breadth >= 1x) — ECARTE

**Ce n'est pas une seconde grandeur, c'est `depth` reecrite** : `corr(coverage_percent,
ln(depth)) = 0,968`, ce qui est la loi de Poisson `breadth = 1 - e^(-depth)` (22 % attendus a
0,25x, 63 % a 1x, 86 % a 2x). Les 136 liquides sous 50 % de breadth qui passent le QC sont
simplement ceux entre 0,25x et ~0,7x de profondeur — la ou la loi les attend.

Dans le sens que le doc visait — l'heterogeneite qu'une profondeur moyenne masque — il n'y a
**rien a trouver** : ecart au modele de Poisson median -6,8 pts, pire cas **-19,3 pts**,
**2 echantillons sur 1 322** au-dela de -15 pts, **aucun** au-dela de -20. A comparer au N50
dont le percentile extreme atteint x21 de la mediane.

Le -6,8 pts median n'est pas un defaut : c'est la fraction non mappable du genome, qui recoupe
les ~4-5 % de bins non couvrables mesures independamment par `dev/archive/coverage_analysis`.

**Seule valeur residuelle** : « 73 % du genome couvert » est plus lisible au rapport que
« 1,9x de profondeur ». Argument de presentation, pas de rendu.

## Deux corrections apportees au doc au passage

- Les **41 « fragments trop longs »** de la section 2 sont a **71 % des tissus solides et des
  lignees cellulaires** (HT29, PANC-1, MeWo, T98G…), ou un ADN long est normal. Sur le
  perimetre reel du document — la biopsie liquide — **il reste 12 cas, pas 41**.
- Les **5 « reads sans genome de 1 a 95 pb »** mesurent en realite **127 a 341 pb** (cramino).
  La valeur basse etait un artefact de la derivation `depth x 3,1 Gb / reads` quand `depth`
  arrondi a 2 decimales vaut 0,01-0,06. Le mode de defaillance reel reste **non elucide** :
  beaucoup de reads, de longueur normale, alignees, sans couverture — toutes des
  `Bladder_Urine`, meme famille que `Bladder_Urine_02_067`.

Taux d'avertissement : **7,22 % tous types** (chiffre du doc) mais **5,82 % en liquide seul**,
qui est le perimetre annonce par son titre — c'est ce dernier qu'il faut comparer aux 3,1 %
de Guardant.

Voir [[n50-ratio-qc]] pour le candidat retenu, [[read-counting-cascade]] pour le « taux de
mapping » requalifie, et [[gdoc-qc-ratio-n50]] pour le document de restitution.
