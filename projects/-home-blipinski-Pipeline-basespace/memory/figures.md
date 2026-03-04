# Figure Generation

## Script
`result/generate_figures.R` — remplace l'ancien `generate_figures.py` (supprimé).
Packages: ggplot2, dplyr, tidyr, scales, ggrepel (0.9.6), patchwork.

## Figures produites

| Figure | Fichier | Description |
|--------|---------|-------------|
| Fig 1 | `fig1_qc_overview.png` | Boxplots QC Watchmaker (mapped reads, depth, coverage) — patchwork 3 panels |
| Fig 2 | `fig2_ont_vs_illumina.png` | Scatter concordance ONT vs Illumina + ggrepel + Pearson r |
| Fig 3 | `fig3_bq40_impact.png` | Dumbbell BQ40 impact + annotations jaunes (Colon13, Healthy637, Healthy769) |
| Fig 4 | `fig4_filter_heatmap.png` | Heatmap mVAF x 9 filtres + category color strip, clamped 0-2 |
| Fig 5 | `fig5_score_by_category.png` | Score par catégorie en facet_wrap (4 panels, free_y) |

## Data Sources

| Donnée | Source | Notes |
|--------|--------|-------|
| Fig 1 QC WM | Hardcodé dans le script | Données BaseSpace via `02-download.sh` → `metrics.json` → `metrics.tsv` |
| Fig 2-4 mVAF | `hg38_mvaf.tsv` | 10 colonnes filtre (Standard, QC20, QC30, BQ30, BQ40, combos) |
| Fig 5 score | `hg38_score.tsv` | Mêmes 10 colonnes filtre |
| Fig 1 QC ONT | `comparison_metrics.tsv` col 26,30,34 | Non utilisé actuellement (fig1 = WM) |

## Catégories (4) et palette

```
Cancer actif (3): Breast18, Colon3, Lung8           → #D32F2F
Suspicion (2): Lung12, Lung13                        → #F57C00
Post-op sans détection (7): Colon12-63, Colon9       → #1976D2
Sain (4): Healthy634, 637, 767, 769                  → #388E3C
```

## QC Data Provenance
- `02-download.sh` télécharge `metrics.json` depuis BaseSpace (DRAGEN)
- Extrait via `jq` : total_reads, mapped_reads, avg_coverage, pct_gte_1x
- `generate_comparison.sh` agrège ONT (DuckDB) + 5b/WM/WMQC (`metrics.tsv`)
- Colonnes WM dans `comparison_metrics.tsv` sont NA (BP_Watchmaker/ supprimé)
- Données WM fig1 fournies manuellement par l'utilisateur (probablement Google Sheet)
