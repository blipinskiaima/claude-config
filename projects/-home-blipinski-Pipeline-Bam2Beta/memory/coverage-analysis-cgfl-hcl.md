---
name: coverage-analysis-cgfl-hcl
description: "Analyse couverture mosdepth (dev/coverage_analysis) — couverture autosomale équivalente CGFL vs HCL, trous = régions non-mappables, pas d'effet labo"
metadata: 
  node_type: memory
  type: project
  originSessionId: 06a6a4c7-2f91-42ea-b875-de1b330dee9e
---

Analyse de couverture à partir des per-base mosdepth (2026-06-19).

## Outil — `dev/coverage_analysis/`

Binning du per-base mosdepth (`{sample}.merged.per-base.bed.gz`) en bins 100 kb (moyenne pondérée par longueur), **lecture NFS en streaming** (`/mnt/aima-bam-data/processed/...`, aucune copie des ~145 GB sources, sortie = ~1 MB/sample).

- `bin_one.sh` : binne 1 sample (idempotent, skip si `.bins.tsv` existe). `run_healthy.sh` : orchestrateur xargs parallèle (J procs).
- `01_bin_perbase.sh` : binning séquentiel (merged|epic). `02_plot_coverage.R` : figures A (cumulative) + B (positionnelle normalisée /médiane). `03_plot_healthy_compare.R` : comparaison labo médiane + ruban IQR, filtre depth optionnel (matched).
- Outputs (`out/`, `out_healthy/`) **gitignorés** (volumineux). Figures en **PNG** (VSCode ne lit pas les PDF).

## Finding — couverture autosomale équivalente CGFL vs HCL

Sur 231 Healthy (49 CGFL + 182 HCL), merged WGS, autosomes :
- **Trous systématiques identiques** entre labos (~1200 bins, mêmes positions) = régions **non-mappables hg38** : acrocentriques (chr13/14/15/21/22, bras court rDNA/satellite) + hétérochromatine péricentromérique (chr1/9/16). ~4–5 % des bins autosomes.
- Le **batch effect labo connu sur les *scores* (voir [[batch-effect-investigation]]) ne se manifeste PAS sur la couverture** : profil structurel identique, seule différence = niveau de profondeur (HCL plus profond, med 2.67× vs CGFL 0.79×).
- Plateau cumulative ~93–95 % au seuil bas pour les 2 labos = même fraction couvrable.

## Méthodo / gotchas

- **chrX/Y exclus** : mix de sexes → faux trous (femme = 0 sur chrY, hommes 1 copie chrX).
- **epic non comparable** entre labos : les Healthy CGFL n'ont aucun `merged.epic.per-base` (généré tardivement, jamais reprocessés). HCL complet. L'epic en bins 100 kb dilue de toute façon (sondes éparses → figure code-barres).
- ⚠️ **`Healthy_780.merged.per-base.bed.gz` CORROMPU** (CRC/length error au gunzip, 603 MB, daté 1 déc. 2025) → exclu (231/232). Fichier non touché. Intégrité plus large des per-base non encore vérifiée.
- Trous candidats à confirmer par intersection avec blacklist ENCODE (non fait).
