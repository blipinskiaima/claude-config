# Context — trace-prod — 2026-06-17T13:53:16+0000

**Branche** : main
**Dernier commit** : ac7f0f5 — feat: schema v12 — colonne bootstrap (retd_suivis)
**Status** : clean côté tracké (untracked préexistants : backups .duckdb, csv dev/, html rapport/, .claude/)

## Où j'en suis
Session terminée, tout committé/poussé. 3 blocs : (1) recalcul probs epic+Loyfer liquid CGFL+HCL, (2) import metadata + export ONT Sample, (3) ajout feature bootstrap (schema v12) via /add-trace-prod + backfill rétrospectif.

## Ce qui marche / ce qui foire
- ✓ Feature bootstrap v12 : `retd_suivis.bootstrap` OK/KO, liquid only, pattern preserve (`_s3_exists`), câblée check + update-column + export (entre Short Read et BAM). Committée ac7f0f5.
- ✓ Backfill bootstrap : CGFL 247 OK / 542 KO, HCL 2 OK / 511 KO. Exports gsheet poussés.
- ✓ Probs epic+Loyfer recalculées : CGFL 771/772, HCL 513/513 → gsheet.
- ✓ Metadata import CGFL+HCL + export ONT Sample (834 lignes). 17 nouveaux samples CGFL intégrés (probs re-run).
- ✗ Trous résiduels : `Bladder_Urine_02_090` (props absents S3), `Twist_10_8` (ni metadata ni probs, blanc probable), `Bladder_Urine_02_091/092/093` (sur S3, pas en base).

## Prochaine étape
Rien d'engagé. Optionnel : `check liquid CGFL --new_samples` pour intégrer `Bladder_Urine_02_091/092/093`. La colonne bootstrap se remplira au fil de Bam2Beta via `update-column bootstrap liquid {labo}`.
