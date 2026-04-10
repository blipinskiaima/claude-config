---
name: Data sourcing chain
description: Chaine complete des données depuis le séquençage jusqu'aux résultats du pipeline exploratory-analysis
type: reference
originSessionId: f0058d0f-dc1a-4ad8-a6eb-05800d23ea89
---
## Chaine de données

```
Séquençage ONT → POD5 → Fastq2Bam → BAM
  → Bam2Beta (Nextflow, Docker blipinskiaima/bam2beta)
    → raima::model_v1() → mVAF v1 (score principal)
    → outputs sur S3 (Scaleway)
  → trace-prod (Python/DuckDB)
    → check: inspecte S3/NFS, extrait métriques → tables qc_metrics, retd_suivis, bam_metadata
    → import-metadata: lit GSheet ONT samples → table metadata
    → export: DuckDB → GSheet Trace PROD
  → exploratory-analysis (R)
    → 00: export DuckDB → TSV
    → 01: prepare datasets (.rds)
    → 02: sensibilité/spécificité (CSV)
    → 03: comptage cohorte (CSV)
```

## 3 Google Sheets sources

| Sheet | ID | Usage |
|---|---|---|
| Trace PROD | 1gm_vB7vTzAq38dgkJFNpgA3Cy_XRlUqunMgoBvKnh6M | Scores production (exporté depuis DuckDB) |
| ONT samples CGFL | 1v1KUuCoMQV4Qk5jfbHLxhrUK6q_FETLiH8TuCQMdNxA | Annotations cliniques CGFL |
| ONT samples HCL | 1XcWPn3_PT1atR-i5DmOM1t0ldgb5_PnxhQUwNUxWpQg | Annotations cliniques HCL |

## Docker raima

Image: `blipinskiaima/raima:latest` — raima v0.4.13 (construite 2026-03-24)
Local: raima v0.4.5 (cassée sur Freq Gene 3 type mismatch)
Source: `/home/blipinski/Pipeline/raima/` (v0.4.14 dev)
