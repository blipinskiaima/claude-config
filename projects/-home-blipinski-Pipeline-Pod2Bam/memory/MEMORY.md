# Pod2Bam Memory

## Priorités utilisateur
- **GRCh38 en premier** : se concentrer uniquement sur GRCh38 no_alt pour les tests. hg38 plus tard.
- **Exécution séquentielle GPU** : ne JAMAIS lancer 2 basecalls en parallèle (batch size réduit + résultats tronqués)
- **tmux pour les longs jobs** : l'utilisateur veut lancer lui-même dans tmux, donner la commande

## Décisions pipeline
- `--kit-name SQK-NBD114-24 --trim all` : nécessaire pour obtenir les mêmes longueurs de reads que MinKNOW (delta=0 vérifié sur 10 reads)
- `--trim adapters` seul ne suffit pas (delta ~90 bases)
- Docker nécessite `sg docker -c "..."` sur ce serveur (user dans groupe docker mais session Claude hérite pas)
- `nohup` obligatoire pour les longs jobs lancés par Claude (sinon tué au changement de session)
- AWS CLI : `/usr/local/bin/aws` (dans PATH), profil `--profile scw`
- S3 upload path : `s3://aima-bam-data/data/HCL/liquid/{sample}_rebasecalled_{VERSION}/`
- S3 processed path : `s3://aima-bam-data/processed/MRD/RetD/liquid/HCL/{sample}/` (bedMethyl, RAIMA scores, props)

## Serveur GPU
- 2x NVIDIA L4 (23 GB VRAM chacune)
- Images buildées : `pod2bam:0.9.6` (Dorado 0.9.6) et `pod2bam:1.4.0` (Dorado 1.4.0)
- `/scratch/` en root, user blipinski peut écrire (groupe docker/1007)
- Batch sizes L4 : Dorado 0.9.6 = 256/GPU, Dorado 1.4.0 = 1152-2304/GPU

## Structure données
- BAM originaux du séquenceur rangés dans `data/{sample}/bam/` (pas dans compare/)
- Résultats multi-version dans `result/GRCh38/{version}/{sample}/`
- Logs dans `/scratch/basecall/dorado/logs/`

## Pipeline Nextflow DSL2 (2026-02-25)
- **Converti** de bash vers Nextflow DSL2, style identique à Bam2Beta
- **Fichiers clés** : `main.nf`, `nextflow.config`, `conf/base.config`, `workflow/basecall.nf`
- **Multi-version** : `--version "V4.2.0,V5.0.0,V5.2.0"` → channel tuple avec VERSION, container dynamique `"${IMAGE}"`
- **GPU séquentiel** : `maxForks 1` sur `Dorado_basecall`, sort/index parallèle
- **Profiles** : docker (GPU + /scratch), tower, scw (Scaleway S3), test, debug
- **Réorganisation** : scripts bash → `bash/`, Dockerfiles → `docker/`, figures → `figure/`
- **publishDir** : `${output}/${VERSION}/${ID}/` (ex: `.../V5.0.0/Healthy_4/`)
- **Anciens scripts bash** conservés dans `bash/` pour référence

## Observations clés
- **V5.2.0 perd ~24% des reads** : Healthy_11 flagstat = 25M primary vs 33M (V4.2.0-V5.0.0). Dorado 1.4.0 filtre plus strict.
- **Dorado stdout = SAM texte** (pas BAM compressé), unsorted.bam ~2.4x plus gros que sorted BAM
- **Bug bash `((var++))`** : avec `set -e`, `((0++))` retourne exit code 1. Utiliser `VAR=$((VAR + 1))`

## Investigation faux positifs RAIMA V5.x (2026-02-24)
- **Problème** : V5.0.0/V5.2.0 → mVAF>0 (faux positif) sur healthy, V4.x → mVAF=0 (correct)
- **Cause racine** : seuil adaptatif `modkit pileup` chute de ~0.96 (V4.x) à ~0.78 (V5.x). Les modèles V5.x ont une distribution de probabilités de modification plus étalée.
- **Seuils par version** : V4.2.0=0.967, V4.3.0=0.963, V5.0.0=0.783, V5.2.0=0.823 (invariant à la profondeur)
- **Correction validée** : `--filter-threshold C:0.965` dans `modkit pileup` (beta.nf ligne 143). Testé Healthy_4 + Healthy_11 : tous mVAF=0 avec seuil fixe.
- **Attention model v2** : le seuil fixe corrige RAIMA v1 (clinique) mais dégrade v2 (scores explosent). Le pipeline utilise v1 pour le rapport.
- **Détails** : voir `/scratch/healthy4_investigation/` (bedMethyl, logs, scores)

## Analyse thresholds modkit large cohorte (2026-02-24)
- **292 samples** avec threshold merged pileup (197 HCL, 95 CGFL) — 425 CGFL sans log merged
- **Versions basecaller** (depuis trace-prod DuckDB `bam_metadata.dorado_model`) : v3.3 (10), v4.3.0 (8), v5.0.0 (244)
- **Thresholds par version** : v3.3 ~0.75, v4.3.0 ~0.95, v5.0.0 ~0.79
- Pas de différence cancer vs non-cancer au sein d'une même version
- Outliers v4.3.0 CGFL : 8 Lung_Alc avec threshold ~0.96 (même observation que investigation FP)
- Fichiers : `figure/modkit_thresholds.csv`, `figure/sample_dorado_model.csv`, `figure/plot_modkit_thresholds.R`
- Lecture S3 sans téléchargement : `aws s3 cp "s3://...log" - --profile scw | grep`

## Pipeline Bam2Beta
- Container modkit : `blipinskiaima/bam2beta:latest` (modkit **0.5.1**, pas 0.6.0 du host)
- Container RAIMA : `blipinskiaima/raima:latest` (RAIMA **0.4.3**)
- Perms Docker `/scratch/dependencies/` : fichiers root:aima 770, containers doivent tourner avec `--user $(id -u):1007`
- Workflow : BAM → samtools view -L epic.bed → modkit adjust --convert h m → modkit pileup → RAIMA scoring

## Plan de test (10 samples)
### False Positive (non cancers, mVAF > 0)
- Healthy_4, Healthy_11, Healthy_12, Healthy_25, Healthy_34

### True Negative (non cancers, mVAF = 0)
- Healthy_14, Healthy_3, Healthy_8, Healthy_23, Healthy_26

### Avancement multi-version
- **Healthy_4** : DONE — 4/4 versions (V4.2.0-V5.2.0), uploadées S3
- **Healthy_11** : DONE — 4/4 versions, uploadées S3
- **Healthy_8** : DONE — single version GRCh38 (V5.0.0), uploadé S3
- **8 restants** : batch en cours via run-batch.sh (V4.3.0, V5.0.0, V5.2.0)
