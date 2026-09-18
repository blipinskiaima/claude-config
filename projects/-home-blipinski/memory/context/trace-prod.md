# Context — trace-prod — 2026-09-18T10:12:34+00:00

**Branche** : main
**Dernier commit** : f653ac0 — docs: rattrapage retrospectif des statuts QC v34 (gotchas RETRO_REPORT)
**Status** : clean (untracked inchangés : backups .duckdb, CSV dev/, rapports HTML)

## Où j'en suis
Rattrapage rétrospectif des statuts QC Exis/Thémélio (schema v34) terminé côté R&D,
et portage de la même information sur le bucket plateforme. Deux prompts livrés pour
la session parallèle trace-platform (statuts QC + sequencing_time). Rien en cours.

## Ce qui marche / ce qui foire
- ✓ **R&D : 44 NULL → 10.** 34 samples comblés (24 CGFL, 10 HCL) via `--RETRO_REPORT`
  puis `update-column exis_qc_status`. Les 10 restants sont irrécupérables : 6 dossiers
  RetD vidés (samples traités sur la plateforme), 3 `Bam2Beta.failed`, 1 sans THEMELIO
- ✓ **Plateforme : 10 `qc_status.tsv` + 10 `sequencing_time.tsv` créés**, diff S3 vérifié
  par sample (`164 → 165`, 1 ajout, 0 modifié). Aucun `metadata.json` touché
- ✓ Patch `RETRO_QC_ONLY` dans Bam2Beta (saute `Raima_report`) — **non commité**
- ✗ **Le run RetD a réécrit les 34 `metadata.json`** et y a perdu `version_raima` → `null`.
  Repéré seulement après coup, sur question de Boris. Sans impact en base (trace-prod ne lit
  pas ce champ) mais non restaurable (versioning S3 `Suspended`)
- ✗ **38 trous `sequencing_time` restent en R&D** (28 CGFL + 10 HCL), comblables par
  `update-column sequencing_time liquid {labo}` — ~95 Go, ~10 min. Non lancé
- ⚠ Bug repéré dans trace-platform : `.tsv` générique dans `_STAGE_CONTENT_SUFFIXES` fait
  télécharger `read_start_time.tsv` (1,6 Go) à chaque `check`

## Prochaine étape
Lancer `update-column sequencing_time liquid CGFL` puis `HCL` (tmux, séquentiel) pour les
38 trous. Et décider du sort du patch `RETRO_QC_ONLY` : le commiter dans Bam2Beta, ou le
laisser en working tree.
