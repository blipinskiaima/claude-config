---
name: Trace-prod fixes for raima alignment
description: Bugs corrigés dans trace-prod lib/duckdb.py et database/check_samples.py pour aligner metadata avec raima
type: project
originSessionId: f0058d0f-dc1a-4ad8-a6eb-05800d23ea89
---
3 fixes appliqués dans trace-prod (repo séparé ~/Pipeline/trace-prod/) pour aligner DuckDB avec ce que raima::compile_vaf_data() produit.

**Fix 1 — active_cancer écrasé à vide (lib/duckdb.py:347)**
- Bug: TSV_TO_DB_METADATA avait 2 clés mappant vers `active_cancer`, la deprecated écrasait la bonne valeur
- Fix: suppression de la ligne deprecated `"..., according mutations detected on ctDNA"`

**Fix 2 — gene1_vaf sans logique raima (lib/duckdb.py:699)**
- Bug: gene1_vaf stockait la valeur brute du GSheet, raima applique `VAF = max(Freq) si Tumoral, sinon NA`
- Fix: upsert_metadata applique maintenant la même logique + max(split(" / ")) pour multi-gène

**Fix 3 — rebasecalled sans metadata (database/check_samples.py:1204)**
- Bug: import-metadata match par nom exact, les _rebasecalled ne matchent pas
- Fix: après l'import, propagation automatique de la metadata du sample de base vers ses variantes rebasecalled

**How to apply:** Après chaque `import-metadata`, ces fixes s'appliquent automatiquement. Vérifier avec `./run_all.sh` que les résultats sont cohérents.
