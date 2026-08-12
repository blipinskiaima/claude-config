# Context — trace-platform — 2026-08-12T15:19:18+00:00

**Branche** : main
**Dernier commit** : 4656147 — feat(db): score Themelio en base et dans l'export gsheet (schema v14)
**Status** : clean (untracked = logs cron, backups DB, captures uniquement)

## Où j'en suis
Feature Themelio livrée de bout en bout et publiée : colonne themelio_score en
base (schema v14) + colonne "Themelio" dans le gsheet onglet Platform. 3 commits
poussés, dont les 2 chantiers qui traînaient non commités (metadata.json/mVAF
v1.4, et v13 annotations manuelles). Rien en cours.

## Ce qui marche / ce qui foire
- ✓ themelio_score DECIMAL(10,6) : 12 samples sur 327, le reste NA. Valeurs vérifiées dans le sheet publié (0,002698 → 0,994504), colonne #20 après mVAF, catégorie QC.
- ✓ extract_themelio_score : 6 cas de test passés (CSV réel, ancien header sans themelio_version, colonne absente, header seul, fichier vide, fichier absent).
- ✓ Staging S3 : suffixe complet `.themelio_predictions.csv` déclaré, PAS `.csv` — sinon 5,7 Go de read_lengths.csv téléchargés à chaque scan.
- ✓ Annotations manuelles intactes après publication (Commentaire 25 / Cancer type 20), backup TSV du sheet dans data/backup_manual_annotations_2026-08-10_11-10-21.tsv.
- ✗ Backfill via `check <UUID>` = erreur de méthode : recalcule les 3 statuts, a fait basculer 13 samples dna-methyl* de SUCCESSED à FAILED. Rollback fait, 0 changement de statut vérifié. Utiliser un UPDATE ciblé (3,6 s vs plusieurs minutes).
- ✗ Rollback DuckDB : le `cp` du seul .duckdb ne suffit pas, le WAL non checkpointé est rejoué à la réouverture (2 checked_at résiduels sur TESTV202/TESTV220, cosmétique).
- ⚠ Décalage base/S3 non tranché : 13 samples dna-methyl* SUCCESSED en base alors que leur .merged.bam a été supprimé de S3. Gelé car statut terminal jamais re-scanné.
- ⚠ Régression probable dans Bam2Beta (hors scope, tâche spawnée) : main.nf:217 référence assets/themelio_absent.csv, supprimé au commit c1bd572. Profil solid (THEMELIO=false + RAPPORT=true) emprunte ce chemin → run échouerait. Vérifié en lecture de code, PAS par exécution.

## Prochaine étape
Deux décisions en attente, aucune urgente :
1. Arbitrer « amont nettoyé mais rapport livré » → les 13 dna-methyl* doivent-ils rester SUCCESSED ?
2. Confirmer par un run la régression Bam2Beta themelio_absent.csv (tâche déjà préparée).
Nettoyage possible : platform.duckdb.rollback-discarded-11-39-11 (534 Mo, inutile).
