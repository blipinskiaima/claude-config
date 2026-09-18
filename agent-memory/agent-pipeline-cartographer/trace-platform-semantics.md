---
name: trace-platform-semantics
description: Sémantique trace-platform (platform.duckdb) — horodatages, statuts, PROD/DEV, versions, TOO — pour bâtir des pages/indicateurs sans rescanner le projet
metadata:
  type: project
---

Base `~/Pipeline/trace-platform/platform.duckdb`, table unique `samples` (schéma v22 au 2026-09-18, `lib/platform_db.py:12`). CLI `check_platform.py`. Alimentée par scan S3 (`s3://aima-platform/`), écrite uniquement par le daemon/`check` (jamais par le pipeline Bam2Beta lui-même) — voir [[bam2beta_architecture]].

**PROD/DEV = point le plus piégeux** : `case` effectif = `COALESCE(samples.case, labs_users.case, 'PROD')` (`lib/platform_db.py:810`). `labs_users.case` vient du TSV `data/export_labs_users.tsv` (déclaratif, par compte/lab) ; `samples.case` est un override par échantillon (v10) ; **un compte non déclaré dans labs_users est PROD par défaut** (commit `8a5c75d`, 2026-06-24) — donc l'absence de flag ne signifie PAS dev/test. `PROD_CUTOFFS` (`check_platform.py:683`) ne couvre qu'un seul client à ce jour (CGFL/Romain Boidot, PROD depuis 2026-06-15). Ce `case` sert avant tout à la politique d'archivage DEV (`archive` → `run_status=ARCHIVED` si DEV + >2 mois, sticky), pas à un vrai flag environnement pipeline. Un segment `PROD` existe aussi en dur dans les chemins S3 (`processed/{analysis}/PROD/{client}/...`, `utils.py:35`) mais c'est un **littéral de chemin fixe**, sans équivalent DEV — à ne pas confondre avec le `case`.

**Chronologie (v15, commit `43089a3` 2026-09-17)** : 6 horodatages `session_start/stop`, `transfer_start/stop`, `copy_start/stop` lus dans les flags JSON S3 (`completedAt`/`createdAt`), PAS le `LastModified` (corrigeait 150 valeurs faussées par fuseau s3fs) + 3 dates pipeline `pipeline_start/failed/done_date` (`Bam2Beta.start` JSON depuis le 2026-09-09, `.done/.failed` vides → LastModified only). `bulk/` (upload réel) n'est conservé que depuis le 2026-09-14.

**Statuts** : cascade `upload_status → bioit_status → rapport_status` (NA/OK/KO/WARNING) puis `run_status` calculé = WAITING/RUNNING/SUCCESSED/WARNING/FAILED, + `ARCHIVED` posé hors-calcul (sticky). Pas de table d'historique des statuts (seule `annotations_history` existe, pour `commentaire`/`cancer_type` manuels uniquement, pas pour les statuts).

**Versions/TOO très récents et peu couverts** : `version_bam2beta/raima/themelio/too` (v18, 2026-09-17) = 29/373 samples ; `too_predicted_class/final_decision` (v17, 2026-09-17) = 28/373 ; `exis_qc_*/themelio_qc_*` (v21) = 10/373. Schéma en pleine réécriture la semaine du 2026-09-14 au 2026-09-18 (v17→v22 en 5 jours).

⚠ **Divergence de nommage avec trace-prod (piège Sept 2026)** : trace-platform garde encore `nb_reads_total`/`nb_reads_filtered` (`lib/platform_db.py:56-58`) — **PAS** renommé en `nb_lignes_total` comme trace-prod v34 (voir [[trace-prod-schema]]). Ne pas supposer un alignement de noms entre les deux bases.
