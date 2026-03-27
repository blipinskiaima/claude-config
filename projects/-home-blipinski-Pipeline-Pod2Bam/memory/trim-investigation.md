---
name: trim-investigation
description: Resultats complets du test trim gate — trim barcodes au demux reduit mapping rate de ~5pts, retenu pour V0.2.0
type: project
---

## Investigation Trim — TERMINEE (2026-03-25)

### Resultats trim gate test

Test compare demux `--no-trim` vs trim (defaut) sur run 3b1c780b_sub, V4.3.0, Lung_10 + Breast_1.

| Metrique | Lung_10 NOTRIM | Lung_10 TRIM | Delta |
|----------|---------------|-------------|-------|
| Primary | 14,550,693 | 14,550,693 | **0** |
| Secondary | 2,497,134 | 2,367,424 | -5.2% |
| Supplementary | 207,681 | 194,509 | -6.3% |
| Primary mapped | 93.20% | 88.60% | **-4.6pts** |

| Metrique | Breast_1 NOTRIM | Breast_1 TRIM | Delta |
|----------|----------------|--------------|-------|
| Primary | 16,542,263 | 16,542,263 | **0** |
| Secondary | 2,830,823 | 2,658,732 | -6.1% |
| Supplementary | 234,575 | 213,729 | -8.9% |
| Primary mapped | 92.48% | 86.92% | **-5.6pts** |

### Conclusions
1. **Primary reads identiques** — trim ne perd aucun read
2. **Mapping rate chute ~5pts** — les ~92bp de barcode aident minimap2 a ancrer certains reads
3. **Secondary/supplementary en baisse 5-9%** — attendu (reads plus courts)

### Decision V0.2.0
- **Trim active par defaut** (retrait `--no-trim` du demux)
- publishDir `demux_trimmed/` et `align_trimmed/` pour ne pas ecraser les resultats V0.1.0
- Scripts de test deplaces dans `dev/`
