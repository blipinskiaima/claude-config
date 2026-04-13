# Position dans le pipeline AIMA

```
 trace-prod (DuckDB) ──▶ ╔═══════════════════════╗
 all_scores (TSV)    ──▶ ║ exploratory-analysis  ║ ◄── CE PROJET
                         ╚═══════════╤═══════════╝
                                     │
                              ┌──────┴──────┐
                              │             │
                          Figures      Aima-Tower
                          (R/ggplot)   (intégration)
```

**En amont** : scores raima via trace-prod (export DuckDB/GSheet), fichier all_scores_methylation.tsv
**En aval** : figures et tables pour publications/présentations, intégration dans Aima-Tower

## Dépendances inter-projets

- Consomme les données de trace-prod (scores, métadonnées, VAF)
- Produit les analyses de performance diagnostique (sensibilité, spécificité, ROC)
- Les résultats alimentent les décisions sur le modèle IA (seuils, features)
- Analyse à différents seuils de spécificité (0.85, 0.90, 0.95)
