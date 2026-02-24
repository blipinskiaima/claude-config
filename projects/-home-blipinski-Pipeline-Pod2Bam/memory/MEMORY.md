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
- AWS CLI installé en local : `/home/blipinski/.local/bin/aws` (pas dans PATH par défaut de Claude)
- S3 upload path : `s3://aima-bam-data/data/HCL/liquid/{sample}_rebasecalled_{VERSION}/`

## Serveur GPU
- 2x NVIDIA L4 (23 GB VRAM chacune)
- Images buildées : `pod2bam:0.9.6` (Dorado 0.9.6) et `pod2bam:1.4.0` (Dorado 1.4.0)
- `/scratch/` en root, user blipinski peut écrire (groupe docker/1007)
- Batch sizes L4 : Dorado 0.9.6 = 256/GPU, Dorado 1.4.0 = 1152-2304/GPU

## Structure données
- BAM originaux du séquenceur rangés dans `data/{sample}/bam/` (pas dans compare/)
- Résultats multi-version dans `result/GRCh38/{version}/{sample}/`
- Logs dans `/scratch/basecall/dorado/logs/`

## Observations clés
- **V5.2.0 perd ~24% des reads** : Healthy_11 flagstat = 25M primary vs 33M (V4.2.0-V5.0.0). Dorado 1.4.0 filtre plus strict.
- **Dorado stdout = SAM texte** (pas BAM compressé), unsorted.bam ~2.4x plus gros que sorted BAM
- **Bug bash `((var++))`** : avec `set -e`, `((0++))` retourne exit code 1. Utiliser `VAR=$((VAR + 1))`

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
