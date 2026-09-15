---
name: nano28-arrival
description: Run NANO28_26_N1 reçu sur S3 raw le 2026-09-11 — premier run 96-plex (SQK-NBD114-96, PromethION FLO-PRO114M), 5 vrais samples (barcode09-13), noms inconnus, absent de la gsheet au 2026-09-14
metadata:
  type: project
---

# NANO28_26_N1 — reçu le 2026-09-11 (constat du 2026-09-14)

- Run dir : `20260907_1313_1G_PBK88534_f6bff194`, séquençage 07/09 → 10/09/2026, upload 11/09 21:00 → 23:38 (log 2.6 Go + `done_26-09-11_23-39-29.done`). Pas de `upload.done` dans le dossier raw → **pas encore audité/purgé**.
- **Rupture de format** : kit `SQK-NBD114-96` sur flowcell PromethION `FLO-PRO114M` (les NANO01→27 étaient en NBD114.24/96 avec 4 barcodes par run). 983 Go au total.
- **5 vrais samples** : barcode09 → 13 (BAM 17-25 Go, POD5 83-122 Go chacun). Les ~80 autres barcodes présents dans `bam_pass/`/`pod5_pass/` sont du bleed (quelques Ko, 2-700 fichiers vides) — à ignorer.
- `unclassified` = 13.6 Go BAM / 52 Go POD5 ; `mixed` = 5 Go POD5.
- **Noms de samples inconnus** : gsheet metadata_HCL (fetch 2026-09-14, 422 lignes) ne contient ni NANO28 ni f6bff194. Dernier sample connu en liquid : Healthy_182, Colon_60, Lung_144, Nuclear_16, TNE_10, Pancreas_10.
- Nouveau type vu en liquid : **Pancreas** (Pancreas_1-10), absent de la mémoire précédente.

**How to apply :** dès que Romain remplit la gsheet pour f6bff194, créer `ss11.tsv` avec 5 lignes (barcode09→13) puis `./SampleSheetChecker.sh ss11.tsv` (bam) et `--type=pod5`. La regex barcode `^barcode[0-9]+$` accepte barcode09-13 sans changement. Ensuite audit puis purge raw selon [[audit-purge-workflow]].
