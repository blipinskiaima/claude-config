---
name: signatera-natera
description: Fiche fact-checkée Natera Signatera (MRD tumor-informed) et le piège de comparaison vs AIMA
metadata: 
  node_type: memory
  type: reference
  originSessionId: a9e0e82a-c541-48a9-9750-e74fa1c4d1cc
  modified: 2026-07-29T17:52:07.700Z
---

Natera Signatera (`concurency/profils/NATERA-P1-TECHNIQUE.md`, ex-`competitors/NATERA-SIGNATERA-PROFIL.md`)
= MRD **tumor-informed** : WES tumeur → 16 SNV clonaux → mPCR bespoke → plasma ultradeep >100 000×,
positif si ≥2 variants. À l'opposé d'AIMA (tumor-naive, nanopore natif ~1x, méthylation+frag+CNV).

⚠ **Deux chiffres corrigés le 2026-07-29** — cette fiche les portait faux, ils circulent partout :

- « **94 %/98 % vessie sur n=170** » : le n est faux d'un facteur 2,7. Lindskrog 2023
  (PMID 37782315) étudie 68 NAC-traités + 102 NAC-naïfs ; le 94 % ne porte QUE sur les
  NAC-traités, en ctDNA cumulé — verbatim **94 % (15/16) / 98 % (47/48)**, n=64 analysés,
  **16 récidives**, IC95 Clopper-Pearson [69,8 ; 99,8]. Une Se de 94 % sur 16 évènements n'est
  pas la même information qu'une Se de 94 % sur 170 patients.
- « **GALAXY 84,4 % (54/64) · 92,1 %/97,2 %** » : ces nombres **n'existent pas** dans Nakamura
  2024 (PMID 39284954), qui ne publie **aucune Se/Sp clinique** — seulement des HR (11,99 / 33,56),
  des taux de positivité et le lead time médian 5,91 mois. Ce sont les chiffres de **Latitude**
  (PMC12913904, n=195), recopiés sur la mauvaise source. Recalcul explicite depuis GALAXY :
  **~53,0 % (263/496) @ 95,5 %** [ESTIMÉ], limité par les récidives censurées (suivi médian 23 mois).
  Ne jamais opposer ce 53,0 % au 58,5 % de Latitude : aucune comparaison tête-à-tête n'existe.

Perfs MRD restantes : CRC 87,5 % (Reinert 2019, spéc « 98 % » non tracée au primaire),
sein 89 %/100 % (Coombes 2019) ou 88,2 %/95,9 % (Shaw 2024).
Signatera Genome (WGS 64 variants) 94 %/100 % = **communiqué ASCO 2025, pas peer-review**.
PhasED-Seq (Foresight, acquis déc. 2025) = variants **phasés** (PAS méthylation), LOD95 0,7 ppm.

**CDx approuvé FDA le 15/05/2026** (MIBC/atézolizumab, 1er CDx MRD sanguin) ; reste = LDT/CLIA.
Remboursé Medicare échelonné depuis 2020. Verdict Guardant v. Natera 292,5 M$ (nov. 2024, appel).

**Piège de comparaison** : ne jamais aligner le 82 % détection d'AIMA (Exis) sur les 88-94 %
MRD-surveillance de Signatera — régimes de fraction tumorale différents. Le vrai comparateur
tumor-naive/méthylation d'AIMA = **Guardant Reveal** (COSMOS 81 %@98,2 %), mais panel enrichi,
pas genome-wide 1x. Verrou AIMA chiffré : aucune MRD nanopore **native** <100 ppm publiée
(NanoRCS plafonne ~2400 ppm avec amplification). Voir [[aima-positioning-profil]],
[[competitive_landscape]].
