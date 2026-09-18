# Memory — trace-platform

## Architecture

- CLI Python (Click) pour le tracking des échantillons clients sur la plateforme AIMA
- Base DuckDB : `platform.duckdb` — schema **v22** (22 migrations, dont 8 le 2026-09-17)
- Export vers Google Sheets via gspread
- **Scan 100% S3 (boto3, profil scw), plus de mount /mnt** : découverte (list_objects_v2) + staging tmpdir pour le contenu (petits TSV, mtime S3 préservé) + BAM via URL présignée (samtools view -H, header seul, pas les 8Go). Le mount s3fs est non fiable (dossiers fantômes, mtimes incohérents) — abandonné.

## Points clés

- Projet en production, utilisé pour le suivi des échantillons clients
- Fait partie du trio traçabilité : trace-prod + trace-platform + trace-workflow → Aima-Tower
- Schema DB v22 : v10 = override `samples.case`, v11 = drop `report_date`, v12 = `creation_date`, v13 = `commentaire`/`cancer_type`, v14 = `themelio_score`, **v15 = chronologie d'upload (+ drop `creation_date`/`upload_date`), v16 = `annotations_history`, v17 = TOO, v18 = versions produits, v19 = `version_mvaf`, v20 = `product`, v21 = statuts QC Exis/Themelio, v22 = `sequencing_time`**
- **Themelio** (v14, 2026-08-10) : score du module THEMELIO de Bam2Beta >= V2.2.0, lu dans `THEMELIO/{sample}.themelio_predictions.csv` (colonne `themelio_score`). Probabilité XGBoost dans **[0,1]**, PAS un %. Seuils Bam2Beta : >0,921 Detection / 0,725-0,921 Suspicious / ≤0,725 Negative. Module conditionnel (`params.THEMELIO` : ON liquid/prod, OFF solid) → 12 samples sur 327 en ont un, le reste est NA. Export gsheet colonne #20 après mVAF, 6 décimales virgule via `SCORE_6_DECIMALS_COLS` (surtout pas `NUMERIC_COLS` qui arrondit à 2). Staging S3 : suffixe **complet** `.themelio_predictions.csv` déclaré, jamais `.csv` — les `read_lengths.csv` pèsent 5,7 Go sur le bucket
- Annotations manuelles (Commentaire / Cancer type) : saisies dans le gsheet, sauvegardées en base à chaque export. Le sheet gagne si la cellule est non vide, sinon la base restaure. Avant v13 elles n'existaient que dans le sheet → 15 annotations perdues entre le 2026-06-30 et le 2026-07-27, récupérées via l'historique de versions Google Sheets (l'API Drive n'expose PAS les anciennes révisions d'un fichier Sheets natif : `revisions.list` ne renvoie que la révision courante — seule l'UI permet la récupération)
- run_status : WAITING (état 0, pas de .dl-complete) → RUNNING → SUCCESSED/WARNING/FAILED ; ARCHIVED (rétention) posé hors-calcul par `check_platform.py archive` (DEV >2 mois, sticky). bioit ne requiert PLUS rapport_pdf (aligné v11)
- PROD granulaire : `PROD_CUTOFFS` dans check_platform.py (un compte passe prod à partir d'une date d'upload). **case effectif = COALESCE(samples.case, labs_users.case, 'PROD')** — compte détecté mais NON déclaré dans labs_users (TSV) = PROD par défaut (non archivé). Aligné aussi dans Aima-Tower services.py
- Commandes : `check --new` (incrémental, ajoute seulement) vs `check` (full = nouveaux + re-scan WAITING/RUNNING, pas les terminaux) ; `delete` (unitaire), `prune` (purge samples absents de S3, backup auto), `daemon` (check --new + re-scan récents Nj + export, en boucle/tmux). En prod : cron check+export toutes les 30 min
- Occultation export gsheet : snapshot figé `data/export_hidden_samples.tsv` (168 Bladder blood/urine masqués, futurs visibles). `*.tsv` gitignorés (locaux, comme export_labs_users.tsv)

## Session du 2026-09-17 — 8 migrations (v14 → v22)

- **Les timestamps se lisent DANS les flags JSON**, pas dans le `LastModified` S3 : ce dernier date le dépôt du fichier, pas l'événement décrit. `Bam2Beta.start` porte `startedAt` et `.dl-complete.txt` porte `completedAt` depuis un backfill plateforme du 2026-09-09 (264/264 fichiers convertis, y compris ceux de 2025). **150 valeurs étaient faussées par un bug de fuseau du mount s3fs** — l'offset correspondait exactement au fuseau de Paris à la date du sample, basculement hiver/été compris, et tous ces samples précédaient le refactor S3 du 2026-06-24. 254 corrections + 8 comblages appliqués, 0 changement de statut.
- **`data/` n'est PAS le lieu de l'upload client** : c'est une destination de copie. Le vrai transfert se passe sous `bulk/{date}/{client}/{session}/`, que le scan n'avait jamais regardé. Sur `Sample1_2` : run ONT le 09/09, session ouverte le 14/09 à 14:08, transfert 14:32→14:44, clôture par timeout à 16:55, **copie vers `data/` à 17:06→17:07** — et c'est cette copie de 80 s que les colonnes affichaient comme « l'upload ». `bulk/` n'est conservé que depuis le 2026-09-14 (2 sessions sur 11), le reste est purgé définitivement.
- **La machine est en `Etc/UTC`** : `.astimezone()` et `fromtimestamp()` ne convertissent rien. Base et JSON directement comparables. Le CLAUDE.md disait « heure locale » — c'est vrai mais trompeur.
- `product` (l'analyse choisie par l'utilisateur : EXIS / EXIS_CUP / THEMELIO) vit dans `metadata.product` du `.dl-complete.txt`, renseigné depuis juillet 2026. Affiché sous l'en-tête `Analysis` — **`analysis_name` n'a pas été remplacée**, elle vaut MRD pour tous et sert à construire les chemins S3.
- Les 4 samples `test_00*` classés PROD sont en réalité **GenDx** (Imogen Oldfield), et leurs commentaires révèlent des **tests de non-conformité délibérés** (fastq sans bam, pod5 résiduel, bam corrompu) : leurs FAILED sont le résultat attendu, pas des incidents.
- Les 4 `Bladder_Urine_02_*` FAILED du 13/08 (CGFL, PROD) ont démarré le pipeline **2h30 à 4h avant la fin de l'upload** — invisible tant que les timestamps venaient tous du `LastModified`, qui imposait mécaniquement l'ordre de dépôt.

## Dette ouverte — staging générique (NON corrigé)

`_STAGE_CONTENT_SUFFIXES` déclare `.tsv`, `.txt` et `.log` génériques : **60,66 Go du bucket sont éligibles au téléchargement à chaque scan de sample**, dont des `read_start_time.tsv` jusqu'à **3 Go** et deux `sequencing_summary_*.txt` de 2,1 Go — qu'aucun extracteur n'ouvre jamais. 1290 fichiers dépassent 500 ko.

Le motif s'est déjà produit 3 fois et a été contourné au cas par cas en déclarant le nom complet : `.csv` → `.themelio_predictions.csv`, `.json` → `metadata.json`. Correctif proposé mais non appliqué (hors périmètre demandé) : **une garde de taille** dans `_stage_sample_s3` (`_STAGE_MAX_BYTES = 1_000_000`), qui ferme le motif définitivement — tous les fichiers réellement lus sont sous 300 ko, le plus gros étant un `metadata.json` de 120 ko.

## Conventions

- Les workflows terminaux (SUCCEEDED/FAILED/CANCELLED) ne sont pas re-syncés
- `CREATE TABLE AS SELECT` ne préserve pas les PK — utiliser DDL + INSERT INTO
- **Backfill d'une nouvelle colonne : JAMAIS via `check <UUID>`** — cette commande re-stage les ~54 objets S3 du sample et recalcule les 3 statuts. Sur des samples terminaux (jamais re-scannés depuis des mois), l'état S3 a bougé entre-temps → bascules de statut non désirées. Le 2026-08-10, un backfill Themelio par `check` a fait passer 13 samples `dna-methyl*` de SUCCESSED à FAILED (`bioit KO [bam_merged]`), rollback nécessaire. Faire un `UPDATE` ciblé de la seule colonne : 12 samples en 3,6 s contre plusieurs minutes, et zéro effet de bord
- **Rollback DuckDB** : `cp` du seul fichier `.duckdb` ne suffit pas — le WAL non checkpointé est rejoué à la réouverture et réapplique les transactions qu'on croyait annulées (constaté sur 2 `checked_at` résiduels). Vérifier l'état après restauration, pas seulement après la copie
- **Fusions de la ligne méta du gsheet** : elles SURVIVENT au `clear()` de l'export. Restées sur l'ancien découpage après un ajout de colonne, une catégorie tombe dans la fusion voisine et **disparaît sans aucune erreur** — `BAM` s'est volatilisée ainsi. Corrigé : `export_platform` défusionne AVANT d'écrire puis refusionne depuis `META_ROW`. L'ordre est essentiel, écrire d'abord perd les valeurs des cellules masquées.
- **Toujours lire un CSV/TSV par NOM de colonne, jamais par index** : les sorties Bam2Beta changent d'index en cours de route (`too_version` absente sur 2 des 28 fichiers TOO, `themelio_version` ajoutée après coup). Et `confidence_stratum` du CSV TOO contient une virgule qui casse un `split(",")` sur 22 des 28 fichiers.
- **DuckDB refuse tout `ALTER TABLE` tant qu'un index existe** sur la table (même portant sur d'autres colonnes) : les retirer puis les rebâtir dans la migration.
- **Un fallback doit avoir une borne haute.** `version_bam2beta` retombe sur `pipeline_version` pour les runs < V2.2.0, `product` vaut EXIS avant le 2026-09-17 — au-delà, l'absence reste visible. Sinon un pipeline qui cesserait d'écrire sa version serait silencieusement comblé.
- **Décalage base/S3 connu** : 13 samples `dna-methyl*` du compte Imagenome sont SUCCESSED en base alors que leur `.merged.bam` a été supprimé de S3 (seul le `.bai` reste). Un re-scan les classerait FAILED. Gelé car un statut terminal n'est jamais re-scanné — arbitrage métier en attente : « amont nettoyé mais rapport livré » doit-il rester un succès ?

## Alignement Bam2Beta V2.3.0 (2026-09-14)

- **Le contrat de sortie n'est pas dans les `publishDir` du pipeline mais dans `Bam2Beta/conformity/check-run-output.sh`** : c'est cette liste qui conditionne le depot de `Bam2Beta.done`. A chaque version de Bam2Beta, differ CE fichier pour savoir si trace-platform doit suivre. Boris l'avait deja purge cote pipeline (commit `f970c69`, 2026-09-01) sans repercussion cote plateforme -> 12 runs V2.3.0 bloques en FAILED, 0 SUCCESSED.
- V2.3.0 coupe `*.epic.bedMethyl.gz`, `*.raima_score.V2.tsv`, `*.props_v1.tsv`, `*.depths.tsv`, `*.score_cnv.tsv` (process `Modkit_pileup` / `Raima_score_epic` commentes dans `workflow/beta.nf:30-31`). Seule sortie mVAF au contrat : `raima_score.V1.4.tsv` (le V1.5 est produit mais hors contrat).
- **Piege symetrique du statut terminal** : la memoire documentait le risque de RE-scanner un terminal. L'inverse mord aussi — un run qui touche FAILED puis est relance avec succes n'est JAMAIS relu. Constate sur 3 runs `TEST_V230_*` (`.done` depose 14 min apres le check) et sur le patient reel `BEN_Dav_29_11_1983` (V2.2.0, `2/3 : BioIT KO [has_failed]`, en realite SUCCESSED). **Non corrige** — piste : ajouter FAILED a `get_active_sample_keys()` (`lib/platform_db.py:615`), au prix d'un scan S3 sur ~142 samples par passage.
- Les runs `<= V1.3.3` n'ont PAS de `raima_score.V1.4.tsv` : exiger V1.4 les ferait basculer FAILED (24 samples concernes). Ils ne sont proteges que parce qu'un terminal n'est pas re-scanne — d'ou l'obligation du `--sample` cible, jamais `check <UUID>` en masse (cf. regle backfill ci-dessus).
