# Position dans le pipeline AIMA

```
 ┌─────────┐     ┌──────────┐
 │  POD5   │ ──▶ │ Pod2Bam  │
 └─────────┘     └────┬─────┘
                      ▼
                 ┌─────────┐
                 │   BAM   │
                 └────┬────┘
                      ▼
                ╔══════════╗
                ║ Bam2Beta ║ ◄── CE PROJET (34 processus NF)
                ╚════╤═════╝
                     ▼
                ┌──────────┐
                │ bedMethyl│
                └────┬─────┘
                     ▼
                ┌────────┐     ┌────────────┐
                │ raima  │ ──▶ │ trace-prod │
                └────────┘     └─────┬──────┘
                                     ▼
                          ┌──────────┴──────────┐
                          │                     │
                    exploratory-analysis    Aima-Tower
```

**En amont** : BAM alignés, soit directement depuis le séquenceur ONT (cas standard), soit produits par Pod2Bam (cas de re-basecalling)
**En aval** : bedMethyl → raima (scoring) → trace-prod (traçabilité) → exploratory-analysis + Aima-Tower

## Dépendances inter-projets

- Consomme les BAM de Pod2Bam — la version Dorado impacte les résultats
- Produit les bedMethyl consommés par raima (package R de Florian)
- Mise à jour raima → qualification non-régression obligatoire
- trace-prod tracke tous les samples traités et leurs métriques QC
- Les scores alimentent exploratory-analysis (stats/figures) et Aima-Tower (dashboard)
