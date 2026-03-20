---
name: S3 volumetry
description: Tailles des buckets S3 aima-bam-data et aima-pod-data par categorie - mesure du 2026-03-13
type: project
---

Mesure du 2026-03-13.

## aima-bam-data (SCW)

| Repertoire | CGFL liquid (To) | HCL liquid (To) | CGFL solid (To) | Total (To) |
|-----------|:----------------:|:---------------:|:---------------:|:----------:|
| data/ (BAM horaires) | 14.17 | 11.34 | 4.30 | **30.67** |
| RetD/ (resultats complets) | 10.65 | 8.96 | 5.24 | **24.86** |
| RetD/ *.merged.bam seuls | 8.07 | 6.92 | 3.62 | **18.62** |

## aima-pod-data (SCW + AWS)

| Categorie | SCW (To) | AWS (To) | Doublons (To) | Unique (To) |
|-----------|:--------:|:--------:|:-------------:|:-----------:|
| CGFL liquid | 16.58 | 51.98 | 11.81 | 56.75 |
| HCL liquid | 47.44 | 0 | 0 | 47.44 |
| CGFL solid | 11.10 | 14.79 | ~0 | 25.89 |
| **Total** | **75.12** | **66.76** | **~11.81** | **~130.07** |

## Resume global

| Bucket | Taille (To) |
|--------|:-----------:|
| BAM horaires (redondants) | 30.67 |
| BAM merges | 18.62 |
| Resultats pipeline (hors BAM) | 6.24 |
| POD5 unique | ~130.07 |
| **Total stockage S3** | **~186** |

**Why:** Quantifier le stockage S3 pour evaluer les economies possibles (suppression BAM horaires, deduplication POD5).

**How to apply:** 30.67 To de BAM horaires supprimables (redondants avec merges). 11.81 To de POD5 CGFL liquid en double entre SCW et AWS.
