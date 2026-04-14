# Batch Effect Project — Memory

## Project Overview

**Centralisation de tous les travaux batch effect CGFL vs HCL** pour le pipeline AIMA Diagnostics.
- **Répertoire** : `~/Pipeline/batch_effect/` — point d'entrée unique
- **Sous-projets** : `~/Pipeline/batch_effect/ComBat-Met/` (test ComBat-met, non retenu)
- **Données Claude** : ce dossier (+ topic files)
- **Données de travail** : `/scratch/boris/combat-met/` (matrices ComBat-met), `/scratch/batch_effect/` (supprimé, investigation 2026-02 archivée dans le README)

## Problème

- **CGFL Healthy** : 2% FP (mVAF V1 > 0)
- **HCL Healthy** : 17% FP (ratio ×8.5)
- Impact : CGFL sur-spécifique (97.6%), HCL sous-spécifique (83.6%)
- Comparaisons inter-centres invalides sans harmonisation

## Les 2 batch effects racines identifiés (2026-04-14)

### 1. EPIC → ONT (MAJEUR, jamais corrigé)
- `raima::model_v1` entraîné sur 19 références EPIC bisulfite microarray
- Appliqué en production sur ONT modkit pileup
- Biais technologique : bisulfite ≠ nanopore direct

### 2. Apostle vs Maxwell (AMPLIFICATEUR)
- CGFL : Apostle MiniMax (nanoparticules, cfDNA court)
- HCL : Maxwell RSC Rapid ccfDNA (billes magnétiques Promega)
- Chimies de surface différentes → biais de capture CpG différent
- **Apostle matche mieux les refs EPIC par hasard** → CGFL sous-performance "artificielle" = HCL

Les 2 sont liés et confounded avec le centre. Seule une expérience wet-lab contrôlée (même plasma, 2 kits) peut trancher.

## Investigations par date

### 2026-02-19/20 — BAM headers (707 samples)
- 188 HCL + 519 CGFL analysés
- Matrice 31 colonnes (BAM + trace-prod metadata)
- Scripts : generate_reports.sh, build_matrix.sh, enrich_matrix.py
- Confounding majeur identifié : GPU, kit (barcoding + extraction), reads_per_flowcell

### 2026-04-13 — Investigation systématique (12 pistes)
- 8 pistes REJETÉES (couverture, Dorado, GPU, taille fragments, modkit, fragmentomics, Loyfer, ichorCNA)
- 1 ARTEFACT (fragmentomics mode1 +14bp = rebasecallés)
- 1 CONFONDANT (composition biologique Cat 1-4)
- 2 BATCH EFFECTS RACINES (EPIC→ONT + kit extraction)

### 2026-04-14 — Test ComBat-met (non retenu)
- Container Docker : `blipinskiaima/combat-met:latest` (R 4.4 + ComBatMet 0.99.3)
- 574 samples Healthy + Cancer v5.0.0 extraits
- 4 variantes testées (group=H/C, rebalancé, ref.batch=CGFL, Healthy only)
- **Aucune ne fonctionne** : pire ou équivalent au BEFORE
- **Finding inattendu** : la reconstruction du bedMethyl (coverage fixé, filtre CpGs, imputation NAs) réduit 17% → 3% FP HCL **sans ComBat-met**
- **Conclusion** : ComBat-met crée une dépendance batch-spécifique (incompatible ISO 15189), simplification technique suffit pour 80% du problème

## Findings techniques détaillés

### CGFL : 3 générations techniques (2022 → 2026)
| Période | Basecaller | MinKNOW | Modèle | Flowcell | Samples |
|---|---|---|---|---|---|
| sept 2022 | Guppy | non tracé | hac@v3.3 | R9.4.1 | 10 |
| nov 2024 → mars 2025 | Guppy | non tracé | hac@v4.1.0/v5.0.0 | R10.4.1 | 52 |
| mars → sept 2025 | Dorado | v6.2.6 | hac@v4.3.0 | R10.4.1 | 153 |
| sept 2025 → fév 2026 | Dorado | v6.5.14 | hac@v5.0.0 | R10.4.1 | 304 |

### HCL : config unique
- Dorado / MinKNOW v6.5.14 / hac@v5.0.0 / PromethION / A100 / R10.4.1

### Variables confounded avec centre
| Variable | CGFL | HCL |
|----------|------|-----|
| GPU | A800/Quadro | A100 |
| Kit barcoding | NBD114-96 (multiplex) | SQK-NBD114.24 (simplex) |
| Kit extraction | Apostle/Apostole | Maxwell RSC |
| Reads/flowcell | 149M median | 239M median (×1.6, p=1.1e-40) |

### Scores raima V1 par centre (v5.0.0 propre)
- CGFL Healthy rebasecallés : 0/49 FP
- HCL Healthy originaux : 17/98 FP = 17%
- FP HCL stable en rarefaction (merged → 1M) → pas un effet couverture

### Signal cfDNA FP HCL (vs TN HCL)
- blood_0 Loyfer : -2.5% (84.96% vs 87.47%)
- T-cell : +1.6%
- Erythroid : +1.2%
- Hepatocyte : +0.8%
- → Profil cfDNA légèrement non-hématopoïétique, raima V1 le capte comme positif

### Distribution longueur reads (hypothèse gDNA leucocytaire rejetée)
- CGFL TN Apostle : mean 260bp, 7.22% > 500bp
- HCL FP Maxwell : mean 227bp, 4.29% > 500bp
- → CGFL a reads **plus longs**, inverse de l'hypothèse

### Score CNV — batch effect séparé
- `regions_CNV` raima : matrice 50 Healthy **100% CGFL**
- HCL Healthy : médiane score_cnv = 4.54 (FP systématique)
- CGFL Healthy : médiane = 0.0
- Fix : reconstruire regions_CNV avec mix CGFL+HCL

## Recommandations (par priorité)

### P0 — Fix les 2 batch effects
- Ré-entraîner `raima::model_v1` avec références ONT mixtes (CGFL + HCL) → résout EPIC→ONT et Apostle/Maxwell ensemble
- Reconstruire `regions_CNV` raima avec Healthy mixtes CGFL+HCL

### P1 — Quick wins
- Normaliser couverture + filtrer CpGs bien couverts en pré-scoring (17% → 3% FP sans re-entraînement)
- Expérience wet-lab contrôlée Apostle vs Maxwell (même plasma → 2 kits) pour trancher définitivement
- Exclure les 46 rebasecallés HCL des analyses

### P2 — Long terme
- Harmoniser protocoles wet-lab CGFL/HCL (kit extraction + barcoding)
- Documenter les 2 batch effects dans le dossier qualité ISO 15189

## Références

- README central : `~/Pipeline/batch_effect/README.md`
- Détails techniques 2026-02 : [batch-effect-details.md](batch-effect-details.md)
- Mémoire Bam2Beta (pointeur) : `~/.claude/projects/-home-blipinski-Pipeline-Bam2Beta/memory/batch-effect-investigation.md`
- Pub ComBat-met : Wang 2025, NAR Genomics and Bioinformatics, DOI: 10.1093/nargab/lqaf062

## Bash Gotcha

- awk dans heredoc `cat << 'SCRIPT'` : ne pas utiliser `!=` directement dans les commandes bash inline, utiliser heredoc avec quotes simples autour de SCRIPT pour éviter l'échappement du `!`
