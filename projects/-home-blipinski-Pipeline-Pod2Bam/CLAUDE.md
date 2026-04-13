# Position dans le pipeline AIMA

```
 ┌─────────┐
 │  POD5   │ (S3 aima-pod-data)
 └────┬────┘
      ▼
╔═══════════╗
║  Pod2Bam  ║ ◄── CE PROJET
╚═════╤═════╝
      ▼
 ┌─────────┐
 │   BAM   │ (S3 aima-bam-data)
 └────┬────┘
      ▼
 ┌──────────┐     ┌───────┐     ┌────────────┐
 │ Bam2Beta │ ──▶ │ raima │ ──▶ │ trace-prod │
 └──────────┘     └───────┘     └────────────┘
```

**En amont** : 
- Cas standard : POD5 brutes directement depuis le séquenceur ONT
- Cas particulier : POD5 issus du pipeline Pod2Bam lui-même (re-basecalling)

**En aval** : BAM alignés consommés par Bam2Beta

## Dépendances inter-projets

- Les BAM produits par Pod2Bam alimentent directement Bam2Beta
- La version Dorado et le modèle de basecalling impactent les résultats de méthylation en aval
- trace-prod tracke les samples traités par Pod2Bam (colonnes basecalling)
