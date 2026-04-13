---
paths:
  - "**/exploratory-analysis*/**"
  - "**/IA/**"
  - "**/IA-for-IA/**"
  - "**/batch_effect/**"
  - "**/*.R"
  - "**/figures*/**"
---

# Guide Statistique — Analyse Methylation / ctDNA

Ce guide aide Claude a choisir le bon test statistique et a l'expliquer simplement a Boris (debutant en stats, expert en bioinformatique).

**Regle** : TOUJOURS expliquer POURQUOI on utilise ce test, avec un schema visuel, AVANT d'implementer.

## Comparaison de 2 groupes (ex: CGFL vs HCL)

### Donnees continues (scores, couverture, mVAF)

```
Donnees normales ?
  |-- OUI --> t-test (rarement le cas en methylation)
  +-- NON --> Wilcoxon rank-sum (Mann-Whitney U)
              <-- CHOIX PAR DEFAUT pour donnees de methylation
```

**Pourquoi Wilcoxon ?** Les donnees de methylation (beta values 0-1) et les scores mVAF ne suivent pas une distribution normale. Le test de Wilcoxon compare les rangs, pas les moyennes — il est robuste aux distributions asymetriques.

```r
# R
wilcox.test(score ~ labo, data = df)

# Python
from scipy.stats import mannwhitneyu
stat, pval = mannwhitneyu(cgfl_scores, hcl_scores)
```

### Donnees categorielles (positif/negatif, OK/KO)

```
Tableau de contingence 2x2 ?
  |-- n > 5 dans chaque case --> Chi2 ou Fisher exact
  +-- n <= 5 dans une case  --> Fisher exact (toujours safe)
```

## Evaluation d'un seuil de classification (ex: score ctDNA)

```
Score continu --> seuil --> positif/negatif
                              |
                    +---------+---------+
                    |                   |
              Sensibilite          Specificite
              (vrais +)            (vrais -)
                    |                   |
                    +---------+---------+
                              |
                        Courbe ROC
                        AUC = aire sous la courbe
                              |
                        +-----+-----+
                        |           |
                     AUC = 0.5   AUC = 1.0
                     (hasard)    (parfait)
```

**Sensibilite** = vrais positifs / (vrais positifs + faux negatifs) = "parmi les malades, combien sont detectes ?"
**Specificite** = vrais negatifs / (vrais negatifs + faux positifs) = "parmi les sains, combien sont correctement identifies ?"

AIMA utilise 95% de specificite comme cible --> le seuil est choisi pour que <=5% des sains soient faussement positifs.

```r
# R (avec raima)
raima::evaluate_score(scores, labels, target_spec = 0.95)
```

## Correlation (ex: 2 scores, 2 methodes)

```
Relation lineaire ?
  |-- OUI (rare) --> Pearson (r)
  +-- NON / pas sur --> Spearman (rho)
                        <-- CHOIX PAR DEFAUT
```

**Pourquoi Spearman ?** Il mesure la relation monotone (pas forcement lineaire). Plus robuste aux outliers. Valeurs de methylation souvent non-lineaires.

```r
cor.test(x, y, method = "spearman")
```

## Correction pour tests multiples

Si on teste > 1 hypothese (ex: 1000 CpGs differentiels) :

```
p-values brutes --> correction --> p-values ajustees
                        |
                 +------+------+
                 |             |
            Bonferroni     Benjamini-Hochberg (FDR)
            (tres strict)  (moins strict, plus puissant)
                 |             |
            p x N tests    controle le taux de
                           faux positifs global
```

**Defaut** : Benjamini-Hochberg (FDR) — bon compromis entre puissance et controle des faux positifs.

```r
p.adjust(pvalues, method = "BH")
```

## Correction de batch effect

```
Donnees de methylation (beta values 0-1)
          |
    +-----+-----+
    |           |
 ComBat     ComBat-met (NAR 2025)
 (classique) (specifique methylation)
    |           |
 Suppose      Respecte la borne [0,1]
 donnees      des beta values
 non bornees  <-- CHOIX POUR AIMA
```

**Pourquoi ComBat-met ?** ComBat classique peut produire des valeurs < 0 ou > 1 (impossible pour de la methylation). ComBat-met utilise une regression beta qui respecte la nature bornee des donnees.

```r
library(ComBatMet)
corrected <- combat_met(beta_matrix, batch = labo_vector)
```

## Visualisation recommandee

| Question | Graphique | R function |
|---|---|---|
| Distribution d'un score | Violin plot ou density | `ggplot + geom_violin()` |
| Comparaison 2 groupes | Boxplot + points | `ggplot + geom_boxplot() + geom_jitter()` |
| Performance classification | Courbe ROC | `pROC::plot.roc()` |
| Relation 2 variables | Scatter + Spearman | `ggplot + geom_point() + stat_cor()` |
| Heatmap methylation | Heatmap clusterisee | `pheatmap::pheatmap()` |
