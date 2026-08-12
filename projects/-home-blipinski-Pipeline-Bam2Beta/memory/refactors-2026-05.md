---
name: refactors-2026-05
description: "Refactors du 2026-05-27 — QC (BAM_Count/Read_Start_Time dans Beta_epic), Raima (3 process fusionnes), nettoyage code mort"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c6971ef-9e62-46ae-935a-5026efb56aa3
  modified: 2026-08-11T08:48:24.927Z
---

# Refactors 2026-05-27

Detail complet dans git + les commits cites.

## QC Refactor (commits 12c5026, 0eec4c4 · tag `pre-raima-refactor`)

`BAM_Count` + `Read_Start_Time` encapsules dans `workflow Beta_epic` (`beta.nf`), plus invoques
au top-level. Definitions de process locales a `beta.nf`. `Merge` ne fait plus que merger.

- **Semantique changee** : `BAM_Count` / `Read_Start_Time` ne tournent plus si `--BETA false`.
- `params.READ_ST` retire.
- **Regression assumee** (decision Boris) : backfill `Read_Start_Time` standalone via
  `launch_SCW.sh` KO.
- TEST OK, QUALIF bit-a-bit vs V1.1.2.

⚠ Consequence pour la lecture des runs anciens : sur un sample produit avant mai 2026, le trace
Nextflow montre `Bam2Beta:Merge:BAM_Count` et non `Bam2Beta:Beta_epic:BAM_Count`.

## Raima Refactor (commit 591733b)

3 process (`Raima_process` / `_v1_2` / `_probs`) fusionnes en **1 seul `Raima_score_all`**
(`bin/raima_score_all.R`) → **-50 % de containers** sur BETA. Sorties V2 / V1.2 / props_v1 +
`raima_version.txt` **bit-a-bit identiques** vs V1.1.2. Les 3 scripts d'origine sont dans
`bin/archive/`.

⚠ Gotcha container : tout nouveau process raima doit avoir son entree `withName:` dans
`conf/base.config`, sinon il herite du defaut `bam2beta:latest`.

## Dead Code Cleanup

Supprime : params orphelins de `nextflow.config` (`SCORE*`, `windows`, `mike_pct`), log `--cpu`,
rename `withName Read_Start_Time`, 2 `withName` orphelins dans `prod.config`.

Garde volontairement (futures features) : process `Nanoplot_qc` / `Plot_Coverage_By_Chromosome` /
`Samtools_qc`, params CNV/ichorCNA, `mode` / `date_tag` / `sample` / `run`. TEST OK.

⚠ **Mise a jour 2026-08-11** : `Samtools_qc` et `Nanoplot_qc` sont toujours presents dans
`qc.nf` mais **enfermes dans un bloc commentaire Groovy** — code mort confirme. Idem
`Raima_score_v1_3` et `bootstrap_transfo` dans `beta_28M.nf` (plus aucun appelant depuis la
disparition de `params.MVAF1_4`).
