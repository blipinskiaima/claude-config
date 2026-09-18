# Pipeline Cartographer Memory

## Index des mémoires

- [Bam2Beta — architecture et conventions](bam2beta_architecture.md) — structure workflow, profiles, S3, outputs, seuils ; chaîne de calcul complète EPIC/28M/CNV/rarefaction horaire (process+outil+file:line), défs epic/merged/28M, limites traçabilité version
- [trace-prod — schéma et architecture](trace-prod-schema.md) — schéma courant v34 (09/2026), 14 tables, 1384 liquid ; cascade `qc` (A/B/C/D), depth/coverage `qc_metrics`, export gsheet "QC read", chemins S3 non stockés (reconstruits)
- [Consommateurs metadata.json / raima_score.V2.json](bam2beta-report-json-consumers.md) — personne ne json.load() ces fichiers hors Bam2Beta (qualif par nom de champ) ; reste = existence/valeur seulement
- [active_cancer — définitions divergentes](active-cancer-definitions.md) — canonique AIMA (exploratory-analysis/Tower/Feature) vs raima (Suspicion, mais mort en pratique) vs TOO (case-sensitive) ; bucket "suspect" Feature
- [trace-platform — sémantique](trace-platform-semantics.md) — schéma v22 (09/2026) ; PROD/DEV = `case` COALESCE sample/labs_users/'PROD' défaut ; chronologie 6 horodatages JSON S3 ; TOO/versions récents et peu couverts ; ⚠ PAS de rename nb_reads_total→nb_lignes_total (diverge de trace-prod v34)
