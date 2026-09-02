# Pipeline Cartographer Memory

## Index des mémoires

- [Bam2Beta — architecture et conventions](bam2beta_architecture.md) — structure workflow, profiles, S3, outputs, seuils ; chaîne de calcul complète EPIC/28M/CNV/rarefaction horaire (process+outil+file:line), défs epic/merged/28M, limites traçabilité version
- [trace-prod — schéma et architecture](trace-prod-schema.md) — schéma courant v24 (08/2026), 11 tables, cascade lecture A/B/C/D (`qc`), conventions matrice/statut/clés, angle mort EQC
- [Consommateurs metadata.json / raima_score.V2.json](bam2beta-report-json-consumers.md) — personne ne json.load() ces fichiers hors Bam2Beta (qualif par nom de champ) ; reste = existence/valeur seulement
