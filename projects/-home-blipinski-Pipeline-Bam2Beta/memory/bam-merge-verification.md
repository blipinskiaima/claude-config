---
name: BAM merge verification
description: Verification exhaustive que le merge des BAM horaires ne perd aucune donnee ni metadonnee - 3/3 PASS confirme + volumetrie S3
type: project
---

## Verification merge BAM (2026-03-13) — 3/3 PASS

Le merge BAM (samtools cat + sort) a ete verifie sur 3 configurations :

- **Breast_1** (CGFL liquid, 44 BAM) : PASS reads + PASS metadonnees
- **Nuclear_4** (HCL liquid, 433 BAM) : PASS reads + PASS metadonnees
- **Colon_0001N8M** (CGFL solid, 129 BAM) : PASS reads + PASS metadonnees

**100% des infos des BAM horaires sont retrouvables dans le BAM merge** (preuve directe) :
- Reads : flagstat Σ horaires = merged, Δ=0 sur toutes les metriques (3/3 samples)
- Tags optionnels reads (RG, NM, MD, MM, ML) : comparaison read-par-read identique
- @SQ : diff direct horaire vs merged = strictement identiques (3/3)
- @RG : `comm -23` = 0 RG horaire absent du merged (merged = union de tous les horaires)
- @PG : idem, 0 PG absent
- @HD : seul changement `SO:unknown → SO:coordinate` (attendu apres samtools sort)
- Headers intra-horaires : verification exhaustive 44/44 identiques sur Breast_1

Les BAM horaires sont **100% redondants** avec le BAM merge.

## Volumetrie S3 (2026-03-13)

### BAM horaires (aima-bam-data/data/)

| Categorie | Taille (To) | Nb samples | Nb BAM |
|-----------|:-----------:|:----------:|:------:|
| CGFL liquid | 14.17 | 653 | 421,889 |
| HCL liquid | 11.34 | 357 | 36,149 |
| CGFL solid | 4.30 | 82 | 35,032 |
| **Total** | **30.67** | **1,092** | **493,070** |

### BAM merges (aima-bam-data/processed/MRD/RetD/)

| Categorie | merged.bam (To) | RetD complet (To) |
|-----------|:---------------:|:-----------------:|
| CGFL liquid | 8.07 | 10.65 |
| HCL liquid | 6.92 | 8.96 |
| CGFL solid | 3.62 | 5.24 |
| **Total** | **18.62** | **24.86** |

### POD5 (aima-pod-data)

| Categorie | SCW (To) | AWS (To) | Doublons (To) |
|-----------|:--------:|:--------:|:-------------:|
| CGFL liquid | 16.58 | 51.98 | 11.81 |
| HCL liquid | 47.44 | 0 | 0 |
| CGFL solid | 11.10 | 14.79 | 0 |
| **Total** | **75.12** | **66.76** | **11.81** |

Total POD5 unique : ~130 To. Total stockage S3 tous buckets : ~186 To.

**Why:** Confirmer qu'aucun read/metadonnee n'est perdu avant suppression eventuelle des BAM horaires (~30.7 To).

**How to apply:** Le BAM merge est la source de verite unique. Les BAM horaires sont redondants et supprimables. Les POD5 ont ~11.81 To de doublons CGFL liquid entre SCW et AWS.

Script sauvegarde headers : `dev/save_bam_headers.sh`
Doc complete : `BAM_MERGE_VERIFICATION.md`
