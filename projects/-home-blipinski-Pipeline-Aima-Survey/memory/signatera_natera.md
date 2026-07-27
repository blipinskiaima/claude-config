---
name: signatera-natera
description: Fiche fact-checkée Natera Signatera (MRD tumor-informed) et le piège de comparaison vs AIMA
metadata: 
  node_type: memory
  type: reference
  originSessionId: a9e0e82a-c541-48a9-9750-e74fa1c4d1cc
  modified: 2026-07-27T15:17:07.746Z
---

Natera Signatera (`docs/competitors/NATERA-SIGNATERA-PROFIL.md`) = MRD **tumor-informed** : WES
tumeur → 16 SNV clonaux → mPCR bespoke → plasma ultradeep >100 000×, positif si ≥2 variants.
À l'opposé d'AIMA (tumor-naive, nanopore natif ~1x, méthylation+frag+CNV).

Chiffres fact-checkés : le « **94 %/98 %** » est **vessie-spécifique** (Lindskrog 2023), pas
pan-cancer. Perfs MRD réelles : CRC 87,5 % (Reinert 2019, spéc « 98 % » non tracée au primaire),
sein 89 %/100 % (Coombes 2019) ou 88,2 %/95,9 % (Shaw 2024), GALAXY 84,4 % (n=2240, lead 5,91 mo).
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
