# Context — trace-prod — 2026-05-27 (fin de session)

**Branche** : main
**Dernier commit** : 36748ac — fix: sex_predicted — inversion labels M/F (logique p<0.5 → M, p≥0.5 → F)
**Status** : clean (tracked) — 13 untracked préexistants (.claude workspace, backups, dev CSV, rapports)

## Où j'en suis
Session terminée avec succès. 3 batchs `update-column` IV/QC livrés + fix bug `sex_predicted` (labels F/M inversés) appliqué partout (code, doc, mémoire, DB, 3 gsheets régénérées). Tout commité et pushé.

## Ce qui marche / ce qui foire
- ✓ Fix `check_sex_predicted` propagé sur les 3 entry points (LiquidChecker, SolidChecker, update-column dispatch) — automatique pour futurs samples
- ✓ DB swap atomique F↔M via UPDATE SQL : 732↔567 (NULL=60 préservés)
- ✓ Exports gsheet : liquid CGFL 741, liquid HCL 471, solid CGFL 147 (= 1359 samples corrigés)
- ✓ Spot-check 5 samples post-swap cohérent (p=0,997→F, p=0,194→M, etc.)
- ✗ Pipeline IV/QC non lancé pour 29 samples HCL liquid récents (Lung_104-120 + Lung_133-144) — à vérifier côté Bam2Beta upstream
- ✗ `read_start_time` quasi vide sur HCL (5/109 OK seulement) vs 20/56 OK sur CGFL — pipeline Samtools moins avancé côté HCL

## Prochaine étape
Si besoin de relancer une maj IV/QC : workflow validé est `update-column ancestry|sex_proba|sex_predicted|read_start_time liquid {labo} -s sample1 -s sample2 ...` (séquentiel, single writer lock DuckDB) puis `export {type} {labo} --gsheet`. Sinon, à investiguer : pourquoi le pipeline IV n'a pas tourné sur Lung_104-120 + Lung_133-144 HCL (upstream Bam2Beta).
