# Context — Bam2Beta — 2026-09-08

**Branche** : main
**Dernier commit** : e988b21 — feat(qc): statut QC Exis/Themelio — process QC_status, 4 champs metadata.json (33), module retro RETRO_REPORT
**Status** : 2 fichiers modifiés, pas de moi (dev/SCW/Bam2Beta.sh, dev/SCW/dilution_lung.sh — lanceurs de Boris)

## Où j'en suis

Feature « statut QC Exis/Thémélio » livrée de bout en bout et poussée sur les 2 dépôts :
Bam2Beta e988b21 (process QC_status → QC/{ID}.qc_status.tsv, 4 champs dans metadata.json = 33,
module temporaire --RETRO_REPORT) et trace-prod 2a114b8 (schema v34, read_qc_status preserve,
_update_qc_status, export gsheet). Rétro exécuté : 1366/1379 JSON liquid générés, 157 anciens
sauvegardés en .pre_qc_status, base backfillée par Boris, gsheet vérifiée (distributions identiques
JSON = base = gsheet). Aussi dans la journée : rapport.nf simplifié (7858fe7), sequencing_time.tsv
dans Read_Start_Time + chemin rapide trace-prod (bb84b5e / 19923c1). Mémoire à jour
(qc-status-exis-themelio.md, project_schema_v34_qc_status.md).

## Ce qui marche / ce qui foire

- ✓ Arbre validé par Boris (5 critères, branche 5–20 M, pire statut gagne, raisons FAILED > WARNING > ordre)
  et prouvé : 19 cas fabriqués, Healthy_826 FAILED, Lung_9 SUCCESS, JSON QUALIF inchangé sur 29 champs
- ✓ Cohorte : CGFL 449 S/S · 223 W/W · 105 W/F · 77 F/F ; HCL 475 · 31 · 6. « Non-human » ne sort
  jamais (arrêté avant par l'arbre), gDNA 6 fois seulement
- ✗ Le glob RetD/liquid/CGFL/* casse côté S3 (ListBucketHandler, 4/4, même bridé) ; HCL passe ; un
  dossier seul passe. Cause non établie (Twist_0% = résidu de lanceur, suspect non confirmé).
  CGFL a été généré par Boris via l'arbre data/CGFL/liquid/*
- ✗ Reste ouvert : v34 vs v35 (le commit 19923c1 dit « migration v34 » sans l'avoir portée) ;
  --RETRO_REPORT à retirer plus tard ; backups .duckdb non ignorés par git ; runs sous Nextflow
  25.10.2 (shell) vs 25.04.8 (tmux/documenté) ; artefacts de test DEV/retro_report_test{,2} sur S3
- ⚠ Runs de Boris toujours en cours (tmux Dilution/lung_hcl : dilution_lung Lung_104_Healthy_51)

## Prochaine étape

Trancher v34/v35 avec Boris, puis planifier le retrait de --RETRO_REPORT une fois le
pipeline nominal (QC_status dans RAPPORT) passé sur quelques samples prod. Qualif V2.4.0
à prévoir (/test_bam2beta : metadata.json 33 champs, check-conformity signalera les 4 nouveaux
champs en WARNING « nouvelle feature »).
