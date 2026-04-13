---
name: Profil scientifique Boris
description: Contexte scientifique AIMA Diagnostics — méthylation ADN, liquid biopsy, ctDNA, pipeline intégré
type: user
originSessionId: 129fb3f7-7613-4550-adf0-9392306d8a85
---
## Domaine

Diagnostic cancer par méthylation ADN via séquençage Oxford Nanopore (basse couverture ~1x) et Illumina (short-read TAPS+).
Objectif : détecter la présence de ctDNA (ADN tumoral circulant) dans le sang des patients.
Norme visée : ISO 15189 (qualité laboratoire clinique).

## Pipeline intégré

```
POD5 → Pod2Bam → BAM → Bam2Beta → bedMethyl → raima → score → trace-prod
       (Dorado)        (34 proc NF)             (Florian)       (DuckDB)
                                                                    │
                                                          ┌─────────┴──────────┐
                                                          │                    │
                                                   exploratory-analysis    IA-for-IA
                                                          │                (Fred+Boris)
                                                     Aima-Tower
                                                     (dashboard)
```

Silos actuels : trace-prod, exploratory-analysis et IA-for-IA ne s'alimentent pas mutuellement.

## Modèle IA ctDNA — état avril 2026

- Meilleur modèle : combined_binom nometh (IA-for-IA Phase 3)
- 97.4% sensibilité VAF>5%, 53.8% VAF 0-5% (vs 85.1% EPIC v1 Illumina)
- Problème n°1 : batch effect CGFL vs HCL (CGFL 100% vs HCL 83% sur MutHigh)
- IA-for-IA piloté par Fred, Boris contribue stratégiquement

## Collaboration

- raima (scoring R) : maintenu par Florian Privé, boîte noire pour Boris
- Mise à jour raima → qualification non-régression Bam2Beta
- ichorCNA : brique exploratoire intégrée dans Bam2Beta, peu concluante pour l'instant

## Priorités scientifiques

1. Correction batch effect CGFL vs HCL (LE facteur limitant)
2. Aima-Tower comme outil interactif pour biologistes (seuils, IGV.js, stats sous-ensembles)
3. Veille scientifique automatisée (liquid biopsy, méthylation, ctDNA)
