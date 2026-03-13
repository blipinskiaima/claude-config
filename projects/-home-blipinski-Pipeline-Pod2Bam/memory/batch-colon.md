---
name: Batch Colon (4 runs)
description: Production batch for Colon samples (9-24 moche) — completed 2026-03-12, S3 synced and verified
type: project
---

## Batch Colon — complété 2026-03-12

**Script** : `Pod2Bam_colon.sh` (copie de Pod2Bam.sh adaptée avec `S3_POD5_MAP`)
**Version** : V0.9.6_V5.0.0 (Dorado 0.9.6, modèle hac V5.0.0)
**Profils** : `-profile docker,tower,scw`

### 4 runs traités

| Run ID | Samples | POD5 | Durée basecall | Durée totale |
|--------|---------|------|----------------|--------------|
| f181e139 | Colon_9-12 | 877G | ~4h | ~7h |
| b4caa48f | Colon_13-16 | 645G | ~3h | ~5h |
| 05ab4dea_rep1 | Colon_17-20_moche | 382G | ~2h | ~3.5h |
| 05ab4dea_rep2 | Colon_17-20_moche_2 | 277G | ~1.5h | ~2.5h |

- **Début** : 2026-03-12 ~12:00
- **Fin** : 2026-03-12 23:32
- **Durée totale batch** : ~11h 35min

### Spécificités

- POD5 source non-standard : pas de sous-dossier `/pod5/`, chemins custom via `declare -A S3_POD5_MAP`
- Run 05ab4dea splitté en 2 (rep1 = `pod5_moche_rep1/`, rep2 = `pod5_moche_rep2/`)
- Barcode sheets custom : `tables/20250904_1028_..._rep1.tsv` et `_rep2.tsv`
- I/O contention observée au début (GPU 9-50%) quand plusieurs POD5 sur disque + background pipelines concurrents — se résout naturellement

### Résultats

| Run | Fichiers | Taille | S3 sync |
|-----|----------|--------|---------|
| f181e139 | 112 | 208G | OK |
| b4caa48f | 100 | 154G | OK |
| 05ab4dea_rep1 | 89 | 101G | OK |
| 05ab4dea_rep2 | 85 | 80G | OK |

- **S3 output** : `s3://aima-bam-data/processed/Pod2Bam/RetD/{RUN_ID}/V0.9.6_V5.0.0/`
- **S3 global log** : `s3://aima-bam-data/processed/Pod2Bam/RetD/Pod2Bam_colon_Pod2Bam_20260312_115934.log`
- **Résultats locaux** : nettoyés (disk 1%)
- **S3 sync vérifié** : 386 fichiers, counts match local vs S3

### Run manquant

- **877aac92 (Colon_21-24)** : POD5 absents sur S3, non traité. À investiguer.

**Why:** Ces 4 runs étaient les runs "moche" retirés du batch principal (POD5 dans des chemins non-standard sur S3).
**How to apply:** Si re-run nécessaire, utiliser `Pod2Bam_colon.sh` avec les S3_POD5_MAP. Le run 877aac92 reste à résoudre.
