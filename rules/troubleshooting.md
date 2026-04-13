# Troubleshooting — Problemes recurrents AIMA

**Regle** : Claude DOIT consulter ce fichier AVANT de proposer des solutions aux erreurs connues. Ne pas reinventer la roue.

## DuckDB

| Probleme | Cause | Solution |
|---|---|---|
| "database is locked" | Autre processus (session Claude, daemon trace-workflow, script) a un verrou | Fermer les autres sessions ou attendre. `fuser database.duckdb` pour identifier le process. |
| CREATE TABLE AS SELECT perd les PK/FK | Comportement DuckDB par design | Utiliser DDL original + INSERT INTO ... SELECT |
| Base grossit apres UPSERT | Blocs morts copy-on-write | `python3 check_samples.py clean-database` pour compacter |

## S3 Scaleway

| Probleme | Cause | Solution |
|---|---|---|
| `aws s3 sync` skip des fichiers (3-5 sur 23-90, aleatoire) | Bug Scaleway S3 | Retry en boucle jusqu'a `local_count == s3_count`. TOUJOURS verifier le nombre de fichiers apres sync. |
| "An error occurred (SlowDown)" | Rate limiting Scaleway | Attendre 30s et retry. Reduire le parallelisme. |
| Upload timeout | Fichiers > 5GB | Chunk size 100MB configure dans nextflow.config. Verifier connexion. |

## Nextflow

| Probleme | Cause | Solution |
|---|---|---|
| OOM killed (exit code 137) | Memoire insuffisante pour le process | Ajouter `memory { X.GB * task.attempt }` avec `maxRetries 3` |
| "No such file" dans publishDir | S3 path incorrect ou bucket inexistant | Verifier le chemin S3 et le profil scw |
| Process ne demarre pas | Image Docker non trouvee | `docker pull blipinskiaima/{image}:{tag}` |
| "Cannot acquire lock" | 2 Nextflow lances dans le meme workdir | Utiliser ~/Run et ~/Run2 pour separer. Ou `nextflow clean -f` si le lock est stale. |
| Resultats tronques / batch size reduit | 2 basecalls GPU en parallele | NEVER paralleliser les GPU. Execution sequentielle obligatoire. |

## Docker

| Probleme | Cause | Solution |
|---|---|---|
| "permission denied" sur /scratch | Container n'a pas le groupe 1007 | `--group-add 1007` dans docker run |
| "no space left on device" | Disque plein (images Docker ~10-12GB chacune) | `docker system prune` pour nettoyer les images/containers inutilises |
| GPU non accessible | NVIDIA Container Toolkit pas installe | Verifier `docker run --rm --gpus all nvidia-smi` |

## Pod2Bam specifique

| Probleme | Cause | Solution |
|---|---|---|
| Migration POD5 v3 vers v4 (.tmp files) | Dorado >= 1.0 tente de migrer | Utiliser Dorado 0.9.6 (pod2bam:0.9.6) qui lit v3 directement |
| Reads ~90 bases plus longs que MinKNOW | Trimming different standalone vs integre | Utiliser `--kit-name SQK-NBD114-24 --trim all` pour delta=0 |
| `((COMPLETED++))` crash avec set -e | Bash: 0++ evalue a false | Utiliser `COMPLETED=$((COMPLETED + 1))` |
