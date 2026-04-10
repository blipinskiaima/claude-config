---
name: Pipeline DuckDB migration
description: Migration de l'input GSheet vers DuckDB trace-prod — validations, comparaisons, scripts créés
type: project
originSessionId: f0058d0f-dc1a-4ad8-a6eb-05800d23ea89
---
Migration de l'input du pipeline exploratory-analysis de GSheet (via raima::compile_vaf_data) vers DuckDB trace-prod directement.

**Why:** Eliminer la dépendance aux GSheets (auth Google, caches stales, format européen), avoir une source unique de vérité, et meilleure complétude (+9 samples CGFL grâce au join par sample_id vs join par nom).

**How to apply:**
- Le pipeline s'exécute maintenant via `./run_all.sh <target_specificity>` (ex: `./run_all.sh 0.85`)
- Scripts créés: `00_export_from_duckdb.py` (export DuckDB → TSV), `run_pipeline.R` (01+02+03 unifié), `run_all.sh` (orchestrateur)
- Les anciens scripts 01/02/03 sont toujours présents et fonctionnels avec l'input GSheet via raima
- Résultats validés: 11/11 summary CSV identiques entre les deux paths, 3 misclassified CSV identiques (sauf labels colonnes)
- DuckDB produit 9 samples CGFL de plus (Breast_18, Colon_62, Colon_63, Lung_10, Lung_12, Lung_13, Pancreas_10, Pancreas_12, Pancreas_4) car le join par nom dans le path GSheet perd ces samples (slice(1) prend la variante bis/ter au lieu du base)
- Output: 17 CSV dans `figures_and_tables/`
