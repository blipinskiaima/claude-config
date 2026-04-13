# Position dans le pipeline AIMA

```
 trace-prod ────────┐
 trace-platform ────┼──▶ ╔════════════╗
 trace-workflow ────┘    ║ Aima-Tower ║ ◄── CE PROJET
                         ╚════════════╝
                              │
                         Dashboard web
                         (biologistes)
```

**En amont** : 3 bases DuckDB (trace-prod, trace-platform, trace-workflow)
**En aval** : interface utilisateur pour biologistes et équipe

## Dépendances inter-projets

- Lit les 3 bases DuckDB via cross-DB join (ATTACH in-memory)
- trace-workflow est un daemon qui sync les données Seqera → DuckDB
- Les données affichées dépendent de la fraîcheur des 3 bases
- Ne modifie JAMAIS les bases sources — lecture seule
