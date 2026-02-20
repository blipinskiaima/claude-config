# Test Results History

## 2026-02-20: GRCh38 vs hg38 Comparison

**Objectif**: Verifier si le changement de genome de reference impacte les resultats

**Config**:
- Sample: Healthy_826 (liquid)
- hg38: `/scratch/dependencies/genomes/hg38/hg38.fa` (QUALIF V1.0.0)
- GRCh38: `/scratch/dependencies/genomes/GRCh38/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa`
- Output GRCh38: `s3://aima-bam-data/processed/MRD/DEV/V1.0.0-GRCh38/run_2026-02-20_14-10-34`
- Pipeline duration: 2m45s, 24/24 tasks OK

**Resultats**:

| Metrique | hg38 | GRCh38 | Diff |
|----------|------|--------|------|
| Raima Score v1 | 0 | 0 | = |
| Raima Score v2 | -0.2868 | -0.2868 | = |
| CNV Score | 0.001436 | 0.001436 | = |
| Fragmentomics Score | -158.904 | -158.904 | = |
| CNV Depths (all bins) | identical | identical | = |
| Cramino (alignments) | 116435 | 116435 | = |
| Mosdepth merged total | 18,182,071 | 18,182,071 | = |
| Mosdepth EPIC total | 1,425,825 | 1,425,825 | = |

**Conclusion**: Changement de genome safe. Seule difference: champ JSON `mvaf` -> `tf` (changement de code, pas de genome).

## 2026-02-20: V1.0.1 Test avec raima 0.4.3 (hg38)

**Objectif**: Valider V1.0.1 apres fix du container raima (0.3.2 -> 0.4.3)

**Probleme rencontre**:
- Premier run KO: `raima:latest` contenait raima 0.3.2 (pas rebuild)
- Rebuild avec raima 0.4.5 -> KO: `'depth_per_region' is not an exported object from 'namespace:raima'`
- Fix: Dockerfile.raima passe de 0.4.5 a 0.4.3, rebuild + push

**Config**:
- Sample: Healthy_826 (liquid)
- Genome: hg38 (defaut)
- Container: raima 0.4.3
- Output: `s3://aima-bam-data/processed/MRD/DEV/V1.0.1/run_2026-02-20_15-35-00`
- Pipeline duration: 4m08s, 24/24 tasks OK

**Resultats**: 3/3 etapes OK
- Etape 1: Pipeline OK (24/24)
- Etape 2: RUN CONFORME (17/17 fichiers)
- Etape 3: QUALIFICATION CONFORME vs QUALIF V1.0.0
  - raima_score.V2.tsv: IDENTIQUE
  - fragmentomics_score.tsv: IDENTIQUE
  - bedMethyl: IDENTIQUE (14289 lignes)
  - score_cnv.tsv: IDENTIQUE

**Conclusion**: V1.0.1 conforme a QUALIF V1.0.0 avec raima 0.4.3.
