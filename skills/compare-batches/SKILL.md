---
name: compare-batches
description: "Compare deux batchs de samples AIMA sur les métriques de pipeline (scores raima, CNV, fragmentomics, QC). Teste significativité statistique (Wilcoxon, Fisher) et identifie les confounders. Use when the user says \"compare batches\", \"comparer batchs\", \"comparer runs\", \"compare-batches\", \"différence entre batchs\"."
argument-hint: "<batch1_filter> <batch2_filter> [--metric mvaf_v1|mvaf_v2|score_cnv|depth] [--plot]"
allowed-tools: Bash(python3*), Bash(cd*), Bash(duckdb*), Bash(Rscript*), Read, Write
---

# compare-batches

Compare statistiquement 2 batchs de samples AIMA pour identifier batch effect, dérive ou différence biologique.

## Contexte

- **DuckDB** : `~/Pipeline/trace-prod/database/samples_status.duckdb`
- **Filtres courants** :
  - Par centre : `labo='CGFL'` vs `labo='HCL'`
  - Par run : `run_id='xxx'` vs `run_id='yyy'`
  - Par version Dorado : `dorado_model_version='v5.0.0'` vs `v5.2.0`
  - Par période : `date_of_run < '2025-09'` vs `>=`
  - Par kit : `kit LIKE 'NBD114-96%'` vs `kit LIKE 'NBD114.24%'`
- **Métriques disponibles** : depth, nb_reads_total, coverage_percent, mvaf_v1, mvaf_v2, score_cnv
- **Règle stats** (cf. `~/.claude/rules/stats-guide.md`) : Wilcoxon par défaut (méthylation non-normale)

## Procédure

### Etape 1 — Parser les filtres

Les arguments `batch1_filter` et `batch2_filter` sont des conditions SQL (ex: `labo=CGFL`, `run_id=abc123`).

Si l'utilisateur donne des filtres simples (ex: `CGFL HCL`), les traduire automatiquement :
- `CGFL` → `labo='CGFL'`
- `HCL` → `labo='HCL'`
- `v5.0.0` → `b.dorado_model_version='v5.0.0'`

Demander confirmation si ambigu.

### Etape 2 — Compter les samples de chaque batch

```sql
SELECT COUNT(*) FROM samples s
JOIN qc_metrics q ON s.id = q.sample_id
JOIN bam_metadata b ON s.id = b.sample_id
LEFT JOIN metadata m ON s.id = m.sample_id
WHERE s.sample_type = 'liquid'
  AND <batch1_filter>
```

Idem pour batch2. Vérifier que chaque batch a au moins 5 samples (sinon stats non fiables).

### Etape 3 — Extraire les métriques

Par défaut, extraire ces métriques pour les 2 batchs :
- depth, coverage_percent, nb_reads_total
- mvaf_v1, mvaf_v2, score_cnv

Si `--metric` fourni, limiter à celle-là.

```sql
SELECT q.depth, q.coverage_percent, q.nb_reads_total,
       q.mvaf_v1, q.mvaf_v2, q.score_cnv,
       m.class, m.category
FROM samples s
JOIN qc_metrics q ON s.id = q.sample_id
LEFT JOIN metadata m ON s.id = m.sample_id
LEFT JOIN bam_metadata b ON s.id = b.sample_id
WHERE <batch_filter>
```

### Etape 4 — Tests statistiques

Pour chaque métrique continue :

```r
# Wilcoxon rank-sum (Mann-Whitney U) — robuste, non-paramétrique
wilcox.test(batch1_values, batch2_values, alternative="two.sided")
```

Pour les métriques catégorielles (Healthy/Cancer, class, category) :

```r
# Fisher exact test sur tableau de contingence
fisher.test(table(class, batch))
```

Rapporter pour chaque test :
- n1, n2
- median1, median2, IQR
- p-value (formater scientifique si < 0.001)
- Significativité : `***` (p<0.001), `**` (p<0.01), `*` (p<0.05), `ns`

### Etape 5 — Identifier les confounders

Vérifier si les 2 batchs diffèrent sur des variables qui ne sont pas le focus :
- Composition par `class` (Healthy/Cancer)
- Composition par `category` (Cat 1-4)
- `dorado_model_version`
- `kit` / `extraction_protocol`
- `reads_per_flowcell`, `samples_per_run`

Si un confounder est détecté (p < 0.05), avertir : la différence observée peut être due au confounder plutôt qu'au batch.

### Etape 6 — Rapport

Produire un rapport structuré :

```markdown
# Comparaison batchs
**Batch 1** : {filter} (n={n1})
**Batch 2** : {filter} (n={n2})

## Résultats quantitatifs

| Métrique | Batch 1 (med) | Batch 2 (med) | Δ | p-value | Verdict |
|----------|---------------|---------------|---|---------|---------|
| depth | 2.1 | 2.6 | +0.5 | 3.2e-10 | *** |
| mvaf_v1 | 0.0 | 0.2 | +0.2 | 0.003 | ** |
| mvaf_v2 | 0.5 | 1.1 | +0.6 | 1.1e-5 | *** |
| score_cnv | 0.0 | 4.5 | +4.5 | <1e-20 | *** |

## Composition (confounders)

| Variable | Batch 1 | Batch 2 | Fisher p |
|----------|---------|---------|----------|
| % Healthy | 20% | 45% | 0.001 |
| Dorado v5.0.0 | 80% | 100% | 0.04 |

## Interprétation

{1-3 phrases sur la significativité et les confounders potentiels}

## Recommandation

- Si batch effect : ...
- Si confondu avec variable biologique : ...
- Si effectifs insuffisants : ...
```

### Option --plot

Si `--plot` est passé, générer des boxplots avec R :

```r
library(ggplot2)
p <- ggplot(df, aes(x=batch, y=value)) +
     geom_boxplot(outlier.shape=NA) +
     geom_jitter(width=0.2, alpha=0.5) +
     facet_wrap(~metric, scales="free_y") +
     theme_minimal()
ggsave("/tmp/compare_batches.pdf", p)
```

Sauvegarder dans `/tmp/compare_batches.pdf` et informer l'utilisateur.

## Notes

- Pour batch effect réel, voir aussi `/batch-effect` (exploration systématique CGFL vs HCL)
- Pour une analyse de corrélation entre 2 métriques au sein d'un batch, utiliser `/correlation`
- Si on compare 2 runs (batch1=run1, batch2=run2), les confounders à vérifier en priorité sont : samples_per_run, reads_per_flowcell, date_of_run
