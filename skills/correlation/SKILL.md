---
name: correlation
description: "Analyse la corrélation entre 2 métriques sur un ensemble de samples AIMA (Spearman par défaut, Pearson optionnel). Détecte outliers, identifie confounders. Use when the user says \"correlation\", \"correler\", \"corrélation\", \"correlation mvaf_v1 depth\", \"is X correlated with Y\"."
argument-hint: "<metric_x> <metric_y> [--filter \"labo=CGFL\"] [--method spearman|pearson] [--plot]"
allowed-tools: Bash(python3*), Bash(cd*), Bash(duckdb*), Bash(Rscript*), Read, Write
---

# correlation

Analyse la corrélation entre 2 métriques sur un ensemble de samples AIMA.

## Contexte

- **DuckDB** : `~/Pipeline/trace-prod/database/samples_status.duckdb`
- **Métriques courantes** :
  - QC : `depth`, `coverage_percent`, `nb_reads_total`, `ratio_percent`, `reads_per_flowcell`
  - Scores : `mvaf_v1`, `mvaf_v2`, `score_cnv`, `mvaf_v1_10m`, `mvaf_v1_20m`
  - Biologie : `gene1_vaf` (VAF panel), `age`
  - ichorCNA/frag : via table `retd_suivis` (`ichorcna_score`, `frag_mode1`, `frag_mode2` — virgule décimale à convertir)
- **Règle stats** (cf. `~/.claude/rules/stats-guide.md`) : Spearman par défaut (non-linéaire, robuste)

## Procédure

### Etape 1 — Identifier les métriques

Parser `<metric_x>` et `<metric_y>`. Vérifier qu'elles existent dans les tables. Si ambiguë, demander confirmation.

Si une métrique est dans `retd_suivis` et utilise une virgule décimale (ex: frag_mode1), prévoir la conversion :

```sql
CAST(REPLACE(r.frag_mode1, ',', '.') AS DOUBLE)
```

### Etape 2 — Construire la requête

```sql
SELECT s.sample_name, s.labo, s.sample_type, m.class,
       <metric_x>, <metric_y>
FROM samples s
JOIN qc_metrics q ON s.id = q.sample_id
LEFT JOIN metadata m ON s.id = m.sample_id
LEFT JOIN bam_metadata b ON s.id = b.sample_id
LEFT JOIN retd_suivis r ON s.id = r.sample_id
WHERE s.sample_type = 'liquid'
  AND <metric_x> IS NOT NULL
  AND <metric_y> IS NOT NULL
  [AND <filter>]
```

Si `--filter` fourni, l'ajouter à la clause WHERE.

### Etape 3 — Charger les données dans R

```r
library(data.table)
dt <- fread("/tmp/correlation_data.tsv")
cat(sprintf("N samples : %d\n", nrow(dt)))
```

Vérifier N ≥ 10 (sinon corrélation non fiable).

### Etape 4 — Test de corrélation

```r
# Spearman par défaut (rangs, non-linéaire, robuste)
test <- cor.test(dt$metric_x, dt$metric_y, method = "spearman")

# Pearson si --method pearson
test <- cor.test(dt$metric_x, dt$metric_y, method = "pearson")
```

Extraire :
- `rho` (Spearman) ou `r` (Pearson)
- p-value
- N

Interprétation :
- |r| < 0.1 : très faible / inexistante
- 0.1-0.3 : faible
- 0.3-0.5 : modérée
- 0.5-0.7 : forte
- > 0.7 : très forte

### Etape 5 — Corrélation par centre (si applicable)

Si le dataset contient CGFL et HCL, faire la corrélation **séparément par centre** pour détecter un paradoxe de Simpson :

```r
for (lab in unique(dt$labo)) {
    sub <- dt[labo == lab]
    t <- cor.test(sub$metric_x, sub$metric_y, method = "spearman")
    cat(sprintf("%s: rho=%.3f, p=%.3g, n=%d\n", lab, t$estimate, t$p.value, nrow(sub)))
}
```

Si la corrélation globale est forte mais nulle dans chaque centre → paradoxe de Simpson (confondant centre).

### Etape 6 — Détecter les outliers

Identifier les samples aux extrêmes :

```r
# Résidus de la régression linéaire
model <- lm(metric_y ~ metric_x, data = dt)
dt$residual <- residuals(model)
dt$outlier <- abs(dt$residual) > 3 * sd(dt$residual)
```

Lister les samples outliers.

### Etape 7 — Rapport

```markdown
# Corrélation {metric_x} ↔ {metric_y}

**Filtre** : {filter or "aucun"}
**N samples** : {N}
**Méthode** : {Spearman|Pearson}

## Résultat global
- **rho** = {value}
- **p-value** = {value}
- **Interprétation** : {très faible|faible|modérée|forte|très forte}
- **Direction** : {positive|négative}

## Par centre (Simpson check)
| Centre | n | rho | p-value |
|--------|---|-----|---------|
| CGFL | 49 | 0.12 | 0.42 (ns) |
| HCL | 98 | -0.09 | 0.38 (ns) |
| Global | 147 | 0.52 | 1e-10 *** |

**Paradoxe de Simpson** : {OUI / NON}
{explication si Simpson détecté}

## Outliers (|residual| > 3σ)
| Sample | {metric_x} | {metric_y} | Résidu |
|--------|------------|------------|--------|

## Interprétation
{1-3 phrases sur le sens biologique/technique de la corrélation}
```

### Option --plot

Générer un scatter plot avec R :

```r
library(ggplot2)
p <- ggplot(dt, aes(x = metric_x, y = metric_y, color = labo)) +
     geom_point(alpha = 0.6) +
     geom_smooth(method = "loess", se = TRUE) +
     labs(title = sprintf("%s vs %s (rho=%.2f, p=%.1e)", mx, my, rho, pval)) +
     theme_minimal()
ggsave("/tmp/correlation_plot.pdf", p, width = 8, height = 6)
```

## Notes

- Spearman préféré pour données de méthylation (distributions asymétriques, non-linéaire)
- Vérifier toujours le scatter plot visuellement — une corrélation peut être significative mais biologiquement non pertinente
- Pour une comparaison de 2 groupes (pas une corrélation), utiliser `/compare-batches`
- Si l'une des métriques a beaucoup de zéros (ex: mvaf sur Healthy), la corrélation Spearman peut être dominée par les ties
