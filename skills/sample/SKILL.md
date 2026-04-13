---
name: sample
description: "Statut cross-projet d'un sample AIMA. Interroge trace-prod, vérifie S3, rassemble scores/QC/metadata. Use when the user says \"sample\", \"statut sample\", \"où en est\", or gives a sample name like \"Healthy_826\"."
argument-hint: "<sample_id> [--full]"
allowed-tools: Bash(python3*), Bash(cd*), Bash(aws*), Bash(duckdb*), Read
---

# Skill : Sample Status

Vérifie le statut cross-projet d'un sample AIMA en interrogeant trace-prod (DuckDB) et S3.

## Contexte

- **DuckDB** : `~/Pipeline/trace-prod/database/samples_status.duckdb`
- **Tables** : `samples`, `qc_metrics`, `bam_metadata`, `probs`, `metadata`
- **CLI** : `python3 ~/Pipeline/trace-prod/database/check_samples.py`
- **S3 Scaleway** (profil `scw`) :
  - POD5 : `s3://aima-pod-data/data/{labo}/{type}/{sample}/`
  - BAM raw : `s3://aima-bam-data/data/{labo}/{type}/{sample}/`
  - BAM merged : `s3://aima-bam-data/processed/MRD/RetD/{type}/{labo}/{sample}/BAM/`
  - bedMethyl : `s3://aima-bam-data/processed/MRD/RetD/{type}/{labo}/{sample}/BETA/`
- **Combinaisons valides** : `liquid x (CGFL|HCL)`, `solid x CGFL`

## Instructions

Quand l'utilisateur donne un sample_id (ex: `Healthy_826`, `CGFL_123`), exécute les étapes suivantes :

### Etape 1 : Recherche dans trace-prod

Cherche le sample dans la DB DuckDB. Essaie d'abord une correspondance exacte, puis un LIKE si pas de résultat.

```bash
duckdb ~/Pipeline/trace-prod/database/samples_status.duckdb -cmd ".mode line" \
  "SELECT s.sample_id, s.labo, s.type, s.status, s.created_at, s.updated_at
   FROM samples s
   WHERE s.sample_id = '{sample_id}'
   OR s.sample_id LIKE '%{sample_id}%'
   LIMIT 10;"
```

Si plusieurs résultats, demande à l'utilisateur de préciser. Si un seul, continue avec le `sample_id`, `labo` et `type` trouvés.

### Etape 2 : Scores (table probs)

```bash
duckdb ~/Pipeline/trace-prod/database/samples_status.duckdb -cmd ".mode line" \
  "SELECT sample_id, raima_v1, raima_v2, mvaf_v1, mvaf_v2
   FROM probs
   WHERE sample_id = '{sample_id}';"
```

### Etape 3 : Métriques QC (table qc_metrics)

```bash
duckdb ~/Pipeline/trace-prod/database/samples_status.duckdb -cmd ".mode line" \
  "SELECT sample_id, coverage, total_reads, mapped_reads, mapping_rate
   FROM qc_metrics
   WHERE sample_id = '{sample_id}';"
```

### Etape 4 : Metadata et Dorado (tables metadata, bam_metadata)

```bash
duckdb ~/Pipeline/trace-prod/database/samples_status.duckdb -cmd ".mode line" \
  "SELECT m.sample_id, m.run_id, m.barcode, b.dorado_version
   FROM metadata m
   LEFT JOIN bam_metadata b ON m.sample_id = b.sample_id
   WHERE m.sample_id = '{sample_id}';"
```

### Etape 5 : Vérification S3

Utilise les valeurs `{labo}` et `{type}` récupérées à l'étape 1. Exécute les 3 vérifications en parallèle :

```bash
# BAM merged
aws s3 ls s3://aima-bam-data/processed/MRD/RetD/{type}/{labo}/{sample_id}/BAM/ --profile scw 2>/dev/null | head -5

# bedMethyl
aws s3 ls s3://aima-bam-data/processed/MRD/RetD/{type}/{labo}/{sample_id}/BETA/ --profile scw 2>/dev/null | wc -l

# POD5
aws s3 ls s3://aima-pod-data/data/{labo}/{type}/{sample_id}/ --profile scw 2>/dev/null | wc -l
```

### Etape 6 : Rapport

Présente les résultats dans ce format exact :

```
## Sample : {sample_id} — {labo} {type}
### Scores
- mVAF v1 : {score} | mVAF v2 : {score}
- raima v1 : {score} | raima v2 : {score}
### QC
- Couverture : {depth}x | Reads : {total} | Mapping rate : {rate}%
### S3
- BAM merged : ✓/✗
- bedMethyl : ✓/✗ ({n} fichiers)
- POD5 : ✓/✗ ({n} fichiers)
### Metadata
- Dorado : {version}
- Run : {run_id}
- Barcode : {barcode}
```

Remplace les valeurs manquantes par `—` (tiret cadratin).

### Option --full

Si `--full` est passé, ajoute en plus :
- Toutes les colonnes des tables `samples`, `qc_metrics`, `probs`, `metadata`, `bam_metadata`
- Liste complète des fichiers S3 (pas juste le count)
- Historique des statuts si disponible

## Gestion d'erreurs

- Si le sample n'existe pas dans la DB : affiche "Sample non trouvé dans trace-prod" et tente quand même la vérification S3.
- Si S3 est inaccessible : affiche "S3 inaccessible" pour les chemins concernés.
- Si DuckDB n'est pas disponible : tente `python3 ~/Pipeline/trace-prod/database/check_samples.py {sample_id}` en fallback.
