---
name: batch-effect
description: Analyser les sources de batch effect inter-centres (CGFL vs HCL). Tracking systematique de toutes les variables confondantes, identification des biais, recommandations de correction. Use when the user says "batch effect", "effet batch", "CGFL vs HCL", "biais inter-centres", or wants to investigate performance differences between centers.
argument-hint: "[--track sample_id] [--compare CGFL HCL] [--report] [--sources]"
allowed-tools: Bash(python3*), Bash(cd*), Bash(aws*), Bash(samtools*), Bash(duckdb*), Read, Glob, Grep, WebSearch, WebFetch
---

# Analyse Batch Effect Inter-Centres — AIMA Diagnostics

## Contexte

Le modèle ctDNA (combined_binom nometh) montre un écart de performance significatif entre les deux centres hospitaliers :
- **CGFL** : 100% sensibilité MutHigh (29/29)
- **HCL** : 83.3% sensibilité MutHigh (25/30)

L'objectif est d'identifier **toutes les sources de variabilité** qui pourraient expliquer cette différence, pas seulement le basecalling.

## Sources de batch effect à tracker

```
Batch Effect CGFL vs HCL
│
├── PRÉ-ANALYTIQUE
│   ├── Kit d'extraction ADN (méthode, fournisseur)
│   ├── Kit de barcoding
│   │   ├── CGFL : SQK-NBD114-96 (multiplex, 96 barcodes)
│   │   └── HCL  : SQK-NBD114-24 (simplex, 24 barcodes)
│   ├── Volume/concentration cfDNA en entrée
│   ├── Protocole de préparation librairie
│   └── Conditions de stockage échantillons
│
├── SÉQUENÇAGE
│   ├── Type de flowcell (R10.4.1 — identique ?)
│   ├── Version MinKNOW (6.5.14 HCL — quid CGFL ?)
│   ├── Durée de run (heures)
│   ├── Nombre de pores actifs
│   ├── Opérateur / site
│   └── Machine (PromethION — même modèle ?)
│
├── BASECALLING
│   ├── Version Dorado
│   │   ├── Software : 0.9.6 (pod2bam) vs MinKNOW intégré
│   │   └── Modèle : V4.2.0 / V4.3.0 / V5.0.0 / V5.2.0
│   ├── Mode : MinKNOW intégré (live) vs standalone (Pod2Bam)
│   ├── Paramètres de trimming (--kit-name, --trim)
│   └── Paramètres de demux (--min-qscore, barcode_sheet)
│
├── PIPELINE BIOINFORMATIQUE
│   ├── Version Bam2Beta (V1.0.x)
│   ├── Version raima (v0.4.x)
│   ├── Genome de référence (hg38 vs GRCh38)
│   ├── Paramètres modkit (--cpg --combine-strands --combine-mods)
│   └── Filtres appliqués (MAPQ, BQ, coverage min)
│
├── MÉTRIQUES QC (quantifiables depuis trace-prod)
│   ├── Couverture moyenne (depth)
│   ├── Nombre de reads total / primary / supplementary
│   ├── Read length distribution (N50, mean, median)
│   ├── Q-score distribution (mean, Q20, Q30)
│   ├── Mapping rate (%)
│   ├── Ratio reads primaires / secondaires / supplémentaires
│   ├── Taux de duplication
│   └── Nombre de CpG couverts (coverage >= X)
│
└── DONNÉES BIOLOGIQUES
    ├── Type d'échantillon (liquid vs solid)
    ├── Type tumoral (Colon, Breast, Lung, Prostate, ...)
    ├── Stade cancer
    ├── VAF (variant allele frequency)
    ├── Fraction tumorale estimée (ichorCNA)
    └── Profil de méthylation global (mean beta)
```

## Commandes

### --track sample_id : profiler un sample

Collecter toutes les variables ci-dessus pour un sample donné.

```bash
cd ~/Pipeline/trace-prod

# Métriques QC depuis DuckDB
python3 database/check_samples.py query \
  "SELECT * FROM samples LEFT JOIN qc_metrics USING(sample_id) WHERE sample_id = '{sample_id}'"

# Metadata BAM
python3 database/check_samples.py query \
  "SELECT * FROM bam_metadata WHERE sample_id = '{sample_id}'"

# Version Dorado depuis le BAM header
samtools view -H /mnt/aima-bam-data/processed/MRD/RetD/{type}/{labo}/{sample_id}/BAM/{sample_id}.merged.bam \
  | grep '@PG.*dorado'

# Scores raima
python3 database/check_samples.py query \
  "SELECT sample_id, raima_score_v1, raima_score_v2, mvaf_v1, mvaf_v2 FROM samples WHERE sample_id = '{sample_id}'"
```

Produire un rapport structuré :
```
## Profil sample : {sample_id}
### Pré-analytique
- Centre : {CGFL|HCL}
- Kit barcoding : {SQK-NBD114-24|SQK-NBD114-96}
- Barcode : {barcodeXX}
### Séquençage
- Run : {run_id}
- MinKNOW : {version}
### Basecalling
- Dorado : {version software} / modèle {version modèle}
- Mode : {intégré|standalone}
### QC
- Couverture : {depth}x
- Reads : {total} (primary: {n}, supp: {n})
- Q-score moyen : {q}
- Mapping rate : {rate}%
### Scores
- mVAF v1 : {score}
- raima v1 : {score}
```

### --compare CGFL HCL : comparaison statistique

Requêter trace-prod pour comparer les distributions CGFL vs HCL :

```sql
-- Distribution couverture par centre
SELECT labo,
  AVG(depth) as mean_depth,
  MEDIAN(depth) as median_depth,
  STDDEV(depth) as std_depth,
  COUNT(*) as n
FROM samples JOIN qc_metrics USING(sample_id)
WHERE sample_type = 'liquid'
GROUP BY labo;

-- Distribution scores par centre
SELECT labo,
  AVG(raima_score_v1) as mean_score,
  MEDIAN(raima_score_v1) as median_score,
  COUNT(CASE WHEN mvaf_v1 > 0 THEN 1 END) as n_positive,
  COUNT(*) as n_total
FROM samples
WHERE sample_type = 'liquid'
GROUP BY labo;
```

Produire des schémas ASCII comparatifs (distributions, boxplots).

### --sources : lister les variables confondantes identifiées

Afficher la liste complète des variables avec leur statut :
- **Confirmé différent** : variables connues comme différentes entre CGFL et HCL
- **À vérifier** : variables non encore comparées
- **Identique** : variables confirmées identiques

### --report : rapport complet

Combiner --compare et --sources en un rapport structuré avec :
1. Variables confondantes identifiées
2. Distributions comparatives (ASCII)
3. Recommandations de correction (ComBat-met, normalisation, etc.)
4. Prochaines étapes d'investigation

## Variables confondantes CONNUES (état avril 2026)

| Variable | CGFL | HCL | Impact estimé |
|----------|------|-----|--------------|
| Kit barcoding | SQK-NBD114-96 (multiplex) | SQK-NBD114-24 (simplex) | **CONFOUNDED** — impossible de séparer l'effet kit de l'effet centre |
| Nombre samples | 519 | 188 | Déséquilibre dataset |
| Mode basecalling | MinKNOW intégré | MinKNOW intégré | Identique (à confirmer) |

## Outils de correction disponibles

- **ComBat-met** (NAR 2025, R) : correction batch effect spécifique méthylation [0,1]. Package R `ComBatMet`.
- **iComBat** (BIB 2025) : correction incrémentale (nouveau centre = nouveau batch).
- **SVA** (R) : surrogate variable analysis pour effets confondants inconnus.

## Références

- batch_effect project : `~/Pipeline/batch_effect/` (investigation initiale, notes de session)
- Investigation multi-version Dorado : `~/Pipeline/Pod2Bam/docs/` + mémoire Pod2Bam
- Données : trace-prod DuckDB `~/Pipeline/trace-prod/database/samples_status.duckdb`
