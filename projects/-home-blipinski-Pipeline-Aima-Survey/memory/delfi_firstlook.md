---
name: delfi-firstlook-lung-analyse-concurrentielle
description: "Mécanique du produit fragmentomique de DELFI, ses vraies performances, et ce qui est vérifié ou non"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2cf74f69-f6e5-4e35-926d-561f28925c84
  modified: 2026-07-22T16:10:49.538Z
---

Rapports complets : `Aima-Survey/DELFI-FIRSTLOOK-P1-TECHNIQUE.md` (bioinfo) et
`-P2-MARCHE.md` (direction). PDF combiné regénérable, gitignoré. Analyse du 2026-07-22.

## Ce qu'il faut retenir

**Le produit** : test sanguin de **triage** vers le scanner faible dose, pas de détection.
Fragmentomique **pure** — ni méthylation, ni mutations. WGS Illumina **~3x**, ratio
court/long (100-150 vs 151-220 pb) sur **504 fenêtres de 5 Mb**, + Z-scores de 39 bras +
fraction mitochondriale, PCA puis **régression logistique bayésienne**, seuil verrouillé à 0,22.

**Les vraies performances** (piège classique — trois jeux de chiffres circulent) :
- **Observé** en validation (n=382) : sensibilité **84 %**, spécificité **53 %**, stade I **71 %**
- **Repondéré** population de dépistage : 80 % / 58 %, VPN 99,8 %, **VPP 1,3 %**, NNS 76
- **Brochure** : VPN 99,8 %, NNS **79**, RR **5,2** → tous renvoient à « Unpublished data on file »

⚠ Ne jamais citer 80 %/58 % comme mesure observée. Ne jamais citer les chiffres de
cross-validation (75/90/96/97 par stade) comme performance du test.

**Ce que la brochure ne contient pas** : les mots *fragmentomics*, *machine learning*,
*genome*, *methylation*, *sensitivity*, *specificity*, *positive predictive value*. Aucun
papier de fragmentomique dans sa bibliographie.

## Pour AIMA

- Le pont scientifique est **Noë 2024, PMID 39107309** : la méthylation *détermine* la
  fragmentation. DELFI mesure une ombre du signal qu'AIMA mesure directement.
- ⚠ **Guardant Shield MCD combine déjà méthylation + fragmentomique** (Breakthrough Device
  FDA juin 2025). L'espace n'est pas vierge — notre angle est la mesure **native simultanée
  en nanopore**, pas la combinaison en soi.
- ⚠ **La méthylation n'est pas une garantie de performance précoce** : Galleri (méthylation
  ciblée) plafonne à **18 % au stade I**, contre 71 % pour la fragmentomique seule de DELFI.
- Verrou critique non résolu : **aucun classifieur de méthylation genome-wide résolu en
  régions n'a été validé à ~1x**. Hypothèse à tester : agréger en larges fenêtres comme DELFI
  le fait pour la fragmentation.
- Les bornes 100-150/151-220 pb **ne sont pas transposables telles quelles en ONT** (aucune
  publication ne les recalibre).
- Enseignements de méthode à copier : **verrouiller classifieur et seuil avant validation**,
  randomiser par batch et travailler en insu.
- DELFI n'a **toujours aucun remboursement large** 3 ans après lancement → dimensionne tout
  business case.

**How to apply :** avant de citer un chiffre de ce dossier, vérifier son niveau de preuve
(les rapports les marquent explicitement). Voir aussi [[competitive_landscape]].
