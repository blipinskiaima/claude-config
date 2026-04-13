# Aliases et raccourcis AIMA

Boris utilise ces raccourcis fréquemment. Les utiliser dans les commandes quand approprié.

## Commandes fréquentes

| Raccourci | Commande complète |
|---|---|
| `AWS_PROFILE=scw aws` | Toute opération S3 Scaleway |
| `tp` | `cd ~/Pipeline/trace-prod && python3 database/check_samples.py` |
| `tp check liquid CGFL` | Vérifier les samples liquid CGFL |
| `tp export liquid CGFL --gsheet` | Exporter vers Google Sheets |
| `tp query "SQL"` | Requête DuckDB directe |

## Chemins fréquents

| Alias | Chemin |
|---|---|
| Pipeline | `~/Pipeline/` |
| Run | `~/Run/` ou `~/Run2/` (lancement Nextflow) |
| Scratch | `/scratch/` (données de travail, GPU) |
| Dependencies | `/scratch/dependencies/` (genomes, modèles) |
| trace-prod DB | `~/Pipeline/trace-prod/database/samples_status.duckdb` |
| trace-platform DB | `~/Pipeline/trace-platform/platform.duckdb` |
| trace-workflow DB | `~/Pipeline/trace-workflow/trace_workflow.duckdb` |
