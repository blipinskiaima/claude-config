# Position dans le pipeline AIMA

```
 Seqera Tower API ──▶ ╔════════════════╗
                      ║ trace-workflow ║ ◄── CE PROJET (daemon)
                      ╚═══════╤════════╝
                              │
                              ▼
                         Aima-Tower (dashboard, cross-DB join)
```

**En amont** : API Seqera Tower (workflows Nextflow lancés via Tower)
**En aval** : Aima-Tower consomme la base DuckDB pour le monitoring des workflows

## Dépendances inter-projets

- Daemon robuste qui sync les données Seqera → DuckDB locale
- Fait partie du trio traçabilité : trace-prod + trace-platform + trace-workflow
- Base DuckDB lue par Aima-Tower (page Monitoring)
- Les workflows trackés correspondent aux runs Bam2Beta et Pod2Bam lancés via Tower
