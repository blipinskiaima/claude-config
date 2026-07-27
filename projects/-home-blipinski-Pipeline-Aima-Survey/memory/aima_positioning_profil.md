---
name: aima-positioning-profil
description: "Profil AIMA canonique (docs/AIMA-POSITIONING.md), perfs Exis 1.1 mVAF v1.4, nuance détection vs MRD"
metadata: 
  node_type: memory
  type: reference
  originSessionId: a9e0e82a-c541-48a9-9750-e74fa1c4d1cc
  modified: 2026-07-27T15:16:55.766Z
---

`~/Pipeline/Aima-Survey/docs/AIMA-POSITIONING.md` = **profil AIMA canonique**, base de comparaison
de tout `/deep-dive-concurency` (Partie 1). Source de vérité des perfs = **rapport Exis 1.1
(doc SD-02)**, reproduit par la page `/exploration` d'Aima Tower. Mis à jour au fil de l'eau.

Deux référentiels de perf à **NE JAMAIS mélanger** : mVAF v1.4 seul (Exis 1.1) = **82,0 % @
95,1 %, n=261 cancers / 224 sains**, seuil 0,0042 % de fraction tumorale ; vs combo THEMELIO
(eval `Feature/`) = 90,5 % @ 96,2 %, n=190/53. Scores et cohortes différents — jamais opposés
comme un progrès.

Correspondance nette : ligne **MRD** = mVAF v1.4 = rapport Exis 1.1 ; ligne **MCED** = THEMELIO.
⚠ Le mVAF v1.4 est la ligne MRD, mais Exis l'évalue en **détection cas/témoin** (cancers avérés
vs sains), pas en MRD longitudinale post-op. Ne jamais opposer ce 82 % à un chiffre de
MRD-surveillance concurrent (piège bloqué au fact-check du deep-dive Signatera). Vrai
différenciateur AIMA à revendiquer : genome-wide, résolution par base, 5hmC natif, CNV inclus.
Voir [[signatera-natera]], [[competitive_landscape]], [[delfi_firstlook]].
