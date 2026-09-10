# Pipeline Cartographer Memory

## Index des mémoires

- [Bam2Beta — architecture et conventions](bam2beta_architecture.md) — structure workflow, profiles, S3, outputs, seuils ; chaîne de calcul complète EPIC/28M/CNV/rarefaction horaire (process+outil+file:line), défs epic/merged/28M, limites traçabilité version
- [trace-prod — schéma et architecture](trace-prod-schema.md) — schéma courant v34 (09/2026), 14 tables, 1384 liquid ; cascade `qc` (A/B/C/D), depth/coverage `qc_metrics`, export gsheet "QC read", chemins S3 non stockés (reconstruits)
- [Consommateurs metadata.json / raima_score.V2.json](bam2beta-report-json-consumers.md) — personne ne json.load() ces fichiers hors Bam2Beta (qualif par nom de champ) ; reste = existence/valeur seulement
