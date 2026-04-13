# Position dans le pipeline AIMA

```
 Données clients (échantillons plateforme)
        │
        ▼
 ╔════════════════╗
 ║ trace-platform ║ ◄── CE PROJET
 ╚═══════╤════════╝
         │
         ▼
    Aima-Tower (dashboard, cross-DB join)
```

**En amont** : données clients, métriques QC, statuts échantillons plateforme
**En aval** : Aima-Tower consomme la base DuckDB pour l'affichage dashboard

## Dépendances inter-projets

- Fait partie du trio traçabilité : trace-prod + trace-platform + trace-workflow
- Base DuckDB lue par Aima-Tower (cross-DB join avec les 2 autres bases)
- Schéma similaire à trace-prod mais pour les échantillons clients (pas R&D)
