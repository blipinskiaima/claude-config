# Position dans le pipeline AIMA

```
 Pod2Bam ──▶ Bam2Beta ──▶ raima ──▶ scores
                                       │
                                       ▼
                                ╔════════════╗
                                ║ trace-prod ║ ◄── CE PROJET
                                ╚══════╤═════╝
                                       │
                            ┌──────────┴──────────┐
                            │                     │
                      exploratory-analysis    Aima-Tower
                            │                     │
                         (stats)            (dashboard)
```

**En amont** : scores raima, métriques QC Bam2Beta, métadonnées BAM/POD5
**En aval** : données consommées par exploratory-analysis et Aima-Tower, export Google Sheets

## Dépendances inter-projets

- Centralise les données de tous les projets pipeline (samples, QC, scores, métadonnées)
- Export GSheet pour les biologistes (skill /export-gsheet)
- Base DuckDB interrogeable par Aima-Tower (cross-DB join)
- Source de données pour l'investigation batch effect CGFL vs HCL
