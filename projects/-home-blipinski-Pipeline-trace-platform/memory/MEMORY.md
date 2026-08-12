# Memory — trace-platform

## Architecture

- CLI Python (Click) pour le tracking des échantillons clients sur la plateforme AIMA
- Base DuckDB : `platform.duckdb` — schema v14 (14 migrations successives)
- Export vers Google Sheets via gspread
- **Scan 100% S3 (boto3, profil scw), plus de mount /mnt** : découverte (list_objects_v2) + staging tmpdir pour le contenu (petits TSV, mtime S3 préservé) + BAM via URL présignée (samtools view -H, header seul, pas les 8Go). Le mount s3fs est non fiable (dossiers fantômes, mtimes incohérents) — abandonné.

## Points clés

- Projet en production, utilisé pour le suivi des échantillons clients
- Fait partie du trio traçabilité : trace-prod + trace-platform + trace-workflow → Aima-Tower
- Schema DB v14 : v10 = override `samples.case` (PROD/DEV niveau sample), v11 = drop `report_date` (plus de PDF), v12 = `creation_date` (date du 1er objet S3 uploadé via LastModified ; tri export récents en haut), v13 = `commentaire`/`cancer_type` (annotations manuelles du gsheet, désormais persistées en base), v14 = `themelio_score`
- **Themelio** (v14, 2026-08-10) : score du module THEMELIO de Bam2Beta >= V2.2.0, lu dans `THEMELIO/{sample}.themelio_predictions.csv` (colonne `themelio_score`). Probabilité XGBoost dans **[0,1]**, PAS un %. Seuils Bam2Beta : >0,921 Detection / 0,725-0,921 Suspicious / ≤0,725 Negative. Module conditionnel (`params.THEMELIO` : ON liquid/prod, OFF solid) → 12 samples sur 327 en ont un, le reste est NA. Export gsheet colonne #20 après mVAF, 6 décimales virgule via `SCORE_6_DECIMALS_COLS` (surtout pas `NUMERIC_COLS` qui arrondit à 2). Staging S3 : suffixe **complet** `.themelio_predictions.csv` déclaré, jamais `.csv` — les `read_lengths.csv` pèsent 5,7 Go sur le bucket
- Annotations manuelles (Commentaire / Cancer type) : saisies dans le gsheet, sauvegardées en base à chaque export. Le sheet gagne si la cellule est non vide, sinon la base restaure. Avant v13 elles n'existaient que dans le sheet → 15 annotations perdues entre le 2026-06-30 et le 2026-07-27, récupérées via l'historique de versions Google Sheets (l'API Drive n'expose PAS les anciennes révisions d'un fichier Sheets natif : `revisions.list` ne renvoie que la révision courante — seule l'UI permet la récupération)
- run_status : WAITING (état 0, pas de .dl-complete) → RUNNING → SUCCESSED/WARNING/FAILED ; ARCHIVED (rétention) posé hors-calcul par `check_platform.py archive` (DEV >2 mois, sticky). bioit ne requiert PLUS rapport_pdf (aligné v11)
- PROD granulaire : `PROD_CUTOFFS` dans check_platform.py (un compte passe prod à partir d'une date d'upload). **case effectif = COALESCE(samples.case, labs_users.case, 'PROD')** — compte détecté mais NON déclaré dans labs_users (TSV) = PROD par défaut (non archivé). Aligné aussi dans Aima-Tower services.py
- Commandes : `check --new` (incrémental, ajoute seulement) vs `check` (full = nouveaux + re-scan WAITING/RUNNING, pas les terminaux) ; `delete` (unitaire), `prune` (purge samples absents de S3, backup auto), `daemon` (check --new + re-scan récents Nj + export, en boucle/tmux). En prod : cron check+export toutes les 30 min
- Occultation export gsheet : snapshot figé `data/export_hidden_samples.tsv` (168 Bladder blood/urine masqués, futurs visibles). `*.tsv` gitignorés (locaux, comme export_labs_users.tsv)

## Conventions

- Les workflows terminaux (SUCCEEDED/FAILED/CANCELLED) ne sont pas re-syncés
- `CREATE TABLE AS SELECT` ne préserve pas les PK — utiliser DDL + INSERT INTO
- **Backfill d'une nouvelle colonne : JAMAIS via `check <UUID>`** — cette commande re-stage les ~54 objets S3 du sample et recalcule les 3 statuts. Sur des samples terminaux (jamais re-scannés depuis des mois), l'état S3 a bougé entre-temps → bascules de statut non désirées. Le 2026-08-10, un backfill Themelio par `check` a fait passer 13 samples `dna-methyl*` de SUCCESSED à FAILED (`bioit KO [bam_merged]`), rollback nécessaire. Faire un `UPDATE` ciblé de la seule colonne : 12 samples en 3,6 s contre plusieurs minutes, et zéro effet de bord
- **Rollback DuckDB** : `cp` du seul fichier `.duckdb` ne suffit pas — le WAL non checkpointé est rejoué à la réouverture et réapplique les transactions qu'on croyait annulées (constaté sur 2 `checked_at` résiduels). Vérifier l'état après restauration, pas seulement après la copie
- **Décalage base/S3 connu** : 13 samples `dna-methyl*` du compte Imagenome sont SUCCESSED en base alors que leur `.merged.bam` a été supprimé de S3 (seul le `.bai` reste). Un re-scan les classerait FAILED. Gelé car un statut terminal n'est jamais re-scanné — arbitrage métier en attente : « amont nettoyé mais rapport livré » doit-il rester un succès ?
