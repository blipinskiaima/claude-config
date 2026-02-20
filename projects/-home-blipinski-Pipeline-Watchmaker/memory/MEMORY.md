# Watchmaker Pipeline - Memory

## Project
- Nextflow DSL2 pipeline for DNA methylation (5mC) calling using TAPS+ chemistry
- Developer: Boris Lipinski @ AIMA Diagnostics
- Infrastructure: Scaleway cloud, S3 storage, Docker containers

## Sequencing & Library Prep
- **Sequencer**: Element Biosciences AVITI (sequencing-by-binding / SBB chemistry)
  - Dual flow cells, >1B read pairs/flow cell
  - Supports 2x75, 2x150, 2x300 read lengths
  - Low PhiX spike-in needed for methylation samples (preserves throughput)
  - >90% Q30 (standard), >90% Q40 / >70% Q50 (Cloudbreak UltraQ)
- **Library prep**: Watchmaker Genomics DNA Library Prep Kit with TAPS+
  - Kit: Twist Universal Adapter System (PN **101307** = 16 samples, PN **101308** = 96 samples Plate A)
  - TruSeq-compatible UDI adapters, T-A overhang ligation
  - Element + Watchmaker kits are validated together (official partnership)

## TAPS+ Chemistry
- **Positive readout**: TET oxidation + pyridine borane reduction converts 5mC/5hmC → T
- Unmethylated cytosines remain as C (unlike bisulfite which converts unmethylated C → T)
- Preserves native 4-base complexity → better alignment, SNV/CNV calling alongside methylation
- >98% 5mC conversion efficiency
- ~6h library prep workflow, automation-friendly
- Single library supports integrated methylation + variant analysis

## Rastair Analysis (from PDF guide WMTN003)
- **nOT/nOB trimming**: 0,0,20,0 (mask 20 bases from R2 start for end-repair bias)
  - R1 generally needs no trimming for high-quality libraries
  - Adjust based on mbias plots
- **min-baseq**: 30
- **min-mapq**: 20 (NOT 50 — pipeline has a bug with hardcoded 50)
- **Coverage**: >5 reads on both strands for confident methylation calls
- **Reversed read orientation**: possible with xGen UDI-UMI Adapters (indicator: low methylation calls)
- **samtools view**: should include `-q ${MAPQ}` filter (pipeline has this commented out)

## Adapter Sequences
- **Full adapters** (from PDF):
  - R1: `AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC`
  - R2: `AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA`
- **Pipeline uses short prefix**: `AGATCGGAAGAGC` (sufficient for cutadapt)

## Current Objective
- Iterate on pipeline launches with reference dataset **Healthy_769** (`s3://aima-bam-data/data/CGFL/Watchmaker`)
- Goal: improve output score by tuning parameters across runs

## Baseline Scores (Healthy_769)
- **run1**: score=0.00131, mvaf=0.3374, model=v1
- **run2**: score=0.0013107, mvaf=0.3375, model=v1

## Key Files
- `main.nf` - workflow orchestration
- `workflow/watchmaker.nf` - all 8 process definitions
- `nextflow.config` - params, profiles, resources
- `launch.sh` - production launch script

## Known Issues
- `workflow/watchmaker.nf:187` - `--min-mapq 50` hardcoded instead of `${min_mapq}`
- `workflow/watchmaker.nf:129` - `val(mapq)` commented out in Samtools_view
- `main.nf:153` - debug `.view()` left in production code
- `nextflow.config:52` - Tower access token in plaintext
- Raima_score process needs `/mnt/temp/florian` mount for `model_v1_data.tsv.gz` (not yet in docker profile)

## Reference
- Watchmaker user guide: [WMTN003 PDF](https://www.watchmakergenomics.com/media/wg/asset/%2Fm%2F4%2Fm417_taps_data_analysis_tn_wmtn003_v1-0-1125.pdf)
- taps-foundry: https://github.com/watchmaker-genomics/taps-foundry
- rastair: https://bitbucket.org/bsblabludwig/rastair/src/v0.8.2/
- Watchmaker TAPS+ product: https://www.watchmakergenomics.com/taps.html
- Element AVITI: https://www.elementbiosciences.com/products/aviti
