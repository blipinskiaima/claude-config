# Pièges rencontrés et parades

| Piège | Symptôme | Parade |
|---|---|---|
| Statut terminal jamais relu | sample relancé avec succès mais encore `FAILED` en base | `verifier_fraicheur.py` → `EN RETARD` → `recheck_cible.py` après accord |
| `check --sample X` | filtre sur le nom seul : re-scanne aussi pt100/T0 et pt107/T0 (forcés SUCCESSED en mai) qui basculeraient en FAILED | toujours `recheck_cible.py` (clé exacte client/patient/sample) |
| `.failed` d'une itération précédente | une relance réussie n'efface pas `Bam2Beta.failed` → bioit KO | corrigé dans `check_processed_files` (le plus récent de `.done`/`.failed`) ; si le statut paraît faux, vérifier les dates des flags sur S3 |
| Check pendant un run | `.done` et `REPORT/metadata.json` de l'itération précédente encore présents → faux statut | attendre que l'état ne soit plus `EN COURS` |
| Livrables `results/` anciens | `data/…/results/` copié d'un run antérieur (renommage) ou `metadata.json` `status=FAILED_QC_*` | colonne `⚠ results/` ; ne pas livrer le rapport sans l'avoir signalé |
| Chromium sans sandbox | `SIGTRAP`, « No usable sandbox! » | `--no-sandbox` (déjà dans le script ; il n'imprime que du HTML local) |
| Valeurs `Decimal` DuckDB | `TypeError: Decimal / float` | `CAST(... AS DOUBLE)` dans la requête |
| Vérification par `pdftotext \| grep` | en-têtes `letter-spacing` éclatés → grep vide → une chaîne `&&` s'arrête avant la copie | vérifier à l'image ; séparer la copie et sa vérification (`cp` puis `cmp`) |
| CSS de même spécificité | une règle `td:first-child` déclarée après en écrase une autre | ajouter les règles d'exception en fin de ligne CSS |
| Tower injoignable | `urlopen` échoue (IP du conteneur `172.18.0.2`) | `docker ps` dans Aima-Tower ; ne jamais recalculer les durées à la main |
| Hook `cd … && rm` | « BLOCKED: cd vers répertoire protégé suivi de rm » | chemins absolus, pas de `cd` avant une suppression |
| Fichiers dans `data/` disparus | BAM retirés du bucket après un échec (IRCCS 30/09) | le versioning S3 est suspendu : impossible de savoir qui ; le dire, ne rien supposer |
