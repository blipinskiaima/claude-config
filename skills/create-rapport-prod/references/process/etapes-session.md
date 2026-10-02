# Rejouer la session d'origine (2026-10-01, IRCCS RC24)

Ce que la session a fait, dans l'ordre, et ce que le skill en garde. Les scripts encapsulent les étapes
techniques ; les décisions ci-dessous restent à Claude.

## Chronologie de la session

| # | Étape de la session | Dans le skill |
|---|---|---|
| 1 | Repérage des samples arrivés (`created_at` récent) puis des runs du jour sur S3 | `verifier_fraicheur.py` (flags `Bam2Beta.start` datés de la période) |
| 2 | Constat : 6 doublons RC24 en `FAILED` terminal, jamais re-scannés malgré une relance réussie | état `EN RETARD` |
| 3 | Attente de la fin des runs (surveillance S3 toutes les 2 min, en arrière-plan) | état `EN COURS` → proposer la surveillance |
| 4 | Contrôle que `.failed` d'une itération précédente ne fausse pas le statut | corrigé dans `check_platform.py` (le plus récent de `.done`/`.failed` gagne) |
| 5 | Contrôle que `data/…/results/` contient les 3 livrables du DERNIER run (pas l'ancien `FAILED_QC_INPUT`) | colonne `results/` de `verifier_fraicheur.py` |
| 6 | Backup + re-check par clé exacte, jamais `check --sample` | `recheck_cible.py` (après accord) |
| 7 | Export gsheet | `check_platform.py export --gsheet` après re-check |
| 8 | Collecte trace-platform + Tower, vérification du mode d'upload | `rapport_plateforme.py` (frise choisie par sample selon `upload_mode`) |
| 9 | Génération du PDF, itérations de mise en forme validées par Boris | figées dans `rapport_plateforme.py` |
| 10 | Copie dans `Bam2Beta/docs`, aperçu dans le panneau de droite | étape 6 du SKILL.md |

## Surveillance d'un run EN COURS

Si l'utilisateur veut attendre : lancer en arrière-plan (`run_in_background: true`) une boucle qui relance
`verifier_fraicheur.py` toutes les 2 minutes et s'arrête quand plus aucune ligne n'est `EN COURS`. Ne pas
sonder à la main entre-temps : la fin de la tâche réveille la session.

## Cas particuliers déjà rencontrés

| Cas | Conduite |
|---|---|
| Aucun run PROD dans la période | le script sort sans PDF ; le dire et proposer une autre période |
| Renommage / regroupement de patient (VHIO p02/p05/p07) | anciennes lignes = autres patients ; `results/` vide sur l'ancien chemin est attendu |
| Run `FAILED` au contrôle d'entrée (`FAILED_QC_INPUT`) | `.done` présent mais pas de `results/` : normal, pas de rapport livré |
| Plusieurs clients | une seule page de garde, client listé par labo ; ne pas scinder sans demande |
| Période longue (> 6 samples) | pagination automatique : 6 frises / 8 lignes par diapositive, numérotées (i/n) |
| La Tower ne renvoie pas un sample | le script s'arrête : vérifier que le conteneur Tower tourne (`docker ps`), ne pas inventer les durées |
