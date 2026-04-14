---
name: qc-report
description: "Génère un rapport QC standardisé pour un ou plusieurs samples AIMA : couverture, reads, scores, conformité seuils. Format markdown exportable. Use when the user says \"qc-report\", \"rapport qc\", \"qualité sample\", \"qc-report Healthy_826\", or wants a QC summary."
argument-hint: "<sample_id|--labo CGFL|--run run_id|--all-recent> [--format md|tsv|html]"
allowed-tools: Bash(python3*), Bash(cd*), Bash(duckdb*), Bash(aws*), Read, Write
---

# qc-report

Génère un rapport QC standardisé pour 1 ou N samples AIMA.

## Contexte

- **DuckDB** : `~/Pipeline/trace-prod/database/samples_status.duckdb`
- **Tables** : `samples`, `qc_metrics`, `bam_metadata`, `metadata`, `retd_suivis`
- **Seuils QC** (valeurs de référence production) :
  - depth_min : 0.5x (acceptable), 1.0x (bon)
  - coverage_percent_min : 40% (acceptable), 70% (bon)
  - nb_reads_total_min : 10M (acceptable), 30M (bon)
  - ratio_percent_min : 3% (acceptable)
- **Statuts Bam2Beta** (retd_suivis) : bam_status, bedmethyl_all_status, cnv_status, frag_status, qc_status, ichorcna_score

## Procédure

### Etape 1 — Identifier les samples

Selon les arguments :

| Argument | Requête |
|----------|---------|
| `<sample_id>` (ex: `Healthy_826`) | 1 sample exact |
| `--labo CGFL` | Tous les CGFL liquid |
| `--labo HCL --type liquid` | HCL liquid |
| `--run <run_id>` | Samples d'un run donné |
| `--all-recent` | 20 derniers samples (sort by updated_at DESC) |
| `--cancer Colon` | Tous les Colon |

Construire la requête SQL adaptée :

```sql
SELECT s.id, s.sample_name, s.labo, s.sample_type, m.class
FROM samples s
LEFT JOIN metadata m ON s.id = m.sample_id
WHERE <filter>
ORDER BY s.sample_name
```

### Etape 2 — Extraire les métriques QC

Pour chaque sample :

```sql
SELECT q.depth, q.coverage_percent, q.nb_reads_total, q.nb_reads_aligned,
       q.nb_reads_epic, q.ratio_percent,
       q.mvaf_v1, q.mvaf_v2, q.score_cnv,
       q.mvaf_v1_10m, q.mvaf_v1_20m
FROM qc_metrics q
WHERE q.sample_id = <id>
```

### Etape 3 — Extraire metadata contextuelles

```sql
SELECT b.dorado_model_version, b.run_id, b.reads_per_flowcell, b.samples_per_run,
       m.kit, m.extraction_protocol, m.date_of_run, m.category, m.gene1_vaf
FROM samples s
LEFT JOIN bam_metadata b ON s.id = b.sample_id
LEFT JOIN metadata m ON s.id = m.sample_id
WHERE s.id = <id>
```

### Etape 4 — Statuts pipeline

```sql
SELECT r.bam_status, r.bedmethyl_all_status, r.cnv_status,
       r.frag_status, r.qc_status, r.ichorcna_score,
       r.date_done, r.pipeline_version
FROM retd_suivis r
WHERE r.sample_id = <id>
```

### Etape 5 — Évaluer conformité aux seuils

Pour chaque sample, marquer les métriques :
- ✓ (vert) : au-dessus du seuil "bon"
- ~ (orange) : entre seuils acceptable et bon
- ✗ (rouge) : en-dessous seuil acceptable
- — : non disponible

### Etape 6 — Rapport

Format par défaut : **markdown**.

Pour 1 seul sample (format détaillé) :

```markdown
# QC Report — {sample_name} ({labo} {type})

**Classe** : {class} | **Catégorie** : {category}
**Date run** : {date_of_run} | **Run ID** : {run_id}
**Pipeline** : {pipeline_version} | **Dorado** : {dorado_version}
**Kit** : {kit} | **Extraction** : {extraction_protocol}

## Couverture
| Métrique | Valeur | Seuil bon | Status |
|----------|--------|-----------|--------|
| Depth | 2.67x | ≥1.0 | ✓ |
| Coverage CpG | 81.7% | ≥70% | ✓ |
| Reads total | 57.9M | ≥30M | ✓ |
| Reads epic | 2.8M | - | - |
| Ratio % | 5.5% | ≥3% | ✓ |

## Scores
| Score | Valeur |
|-------|--------|
| mVAF V1 (merged) | 0.000 |
| mVAF V1 (20M) | 0.000 |
| mVAF V1 (10M) | 0.000 |
| mVAF V2 | 1.15 |
| Score CNV | 4.47 |
| ichorCNA TF | 0.0046 |

## Statuts modules
| Module | Status |
|--------|--------|
| BAM | OK |
| bedMethyl | OK |
| CNV | OK |
| Fragmentomics | OK |
| QC | OK |

## Verdict global
{✓ CONFORME / ⚠ ATTENTION / ✗ ÉCHEC}
{1-2 phrases d'explication}
```

Pour N samples (format tableau synthétique) :

```markdown
# QC Report — {N} samples ({description})

## Tableau synthétique

| Sample | Labo | Class | Depth | Cov% | Reads(M) | mVAF V1 | Status |
|--------|------|-------|-------|------|----------|---------|--------|
| Healthy_13 | HCL | Healthy | 2.01 | 80.0 | 48.0 | 1.383 | ⚠ FP |
| Healthy_34 | HCL | Healthy | 2.67 | 86.0 | 63.8 | 0.000 | ✓ |
| ...

## Statistiques globales
- N = {N}
- Depth median : {med}
- Coverage% median : {med}
- FP Healthy : {n}/{N_healthy} ({pct}%)
- Échecs pipeline : {n}

## Échantillons problématiques
- Healthy_13 : FP mVAF V1 (score={score}, depth={depth})
- ...
```

### Option --format tsv|html

- `tsv` : sortir un TSV brut (pour import dans Excel/R)
- `html` : rendu HTML avec couleurs via pandoc (si disponible)

Sauvegarder dans `/tmp/qc_report_{timestamp}.{ext}` par défaut, proposer à l'utilisateur.

## Notes

- Pour comparer QC entre 2 batchs, utiliser `/compare-batches`
- Pour un seul sample avec toutes les infos, préférer `/sample --full`
- Les seuils sont indicatifs — à ajuster selon le contexte clinique
- Ne pas inclure les samples rebasecallés sauf demande explicite (artefacts fragmentomics)
