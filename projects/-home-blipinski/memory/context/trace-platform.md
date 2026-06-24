# Context — trace-platform — 2026-06-24T14:35:00+0000

**Branche** : main
**Dernier commit** : 8a5c75d — feat(case): compte non déclaré → PROD par défaut
**Status** : clean (tout commité/poussé ; untracked = logs/backups/copie DB seulement)

## Où j'en suis
Grosse session terminée et déployée. trace-platform : scan migré 100% S3 (plus de
/mnt), nouvelles commandes delete/prune/daemon, colonne creation_date (v12), nouveau
compte → PROD. Aima-Tower aligné (PROD défaut) + rebuild OK. Rien en cours.

## Ce qui marche / ce qui foire
- ✓ Scan 100% S3 : découverte (list_objects_v2) + staging tmpdir (petits TSV, mtime préservé) + BAM via URL présignée (samtools header, pas les 8Go). Testé bout-en-bout (~3s/sample).
- ✓ Schema v12 : creation_date (1er objet S3 LastModified), tri export par creation_date DESC. Backfill S3 fait (252/252).
- ✓ Commandes : delete (unitaire), prune (purge samples absents S3, backup auto), daemon (check --new + re-scan 3j + export). Daemon ARRÊTÉ (Boris teste via cron).
- ✓ Occultation gsheet : 168 Bladder blood/urine figés (data/export_hidden_samples.tsv), futurs visibles.
- ✓ Fix bioit : rapport_pdf plus requis (v11) → faux FAILED corrigés.
- ✓ Nouveau compte non déclaré → PROD (COALESCE ..., 'PROD') dans trace-platform ET Aima-Tower (services.py), tower rebuildé healthy.
- ✓ Cron actif : check (full) + export --gsheet toutes les 30 min.
- ⚠ data/export_hidden_samples.tsv + export_labs_users.tsv gitignorés (*.tsv) → locaux, non versionnés.

## Prochaine étape
Aucune tâche en attente. Surveiller le cron 30 min (cron_check.log / cron_export.log).
Option : déclarer les nouveaux comptes dans data/export_labs_users.tsv au fil de l'eau.
