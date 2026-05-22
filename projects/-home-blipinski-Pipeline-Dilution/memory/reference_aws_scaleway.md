---
name: reference-aws-scaleway
description: "Spécificités AWS CLI sur Scaleway S3 — profile scw, STS non supporté, retry sync"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 37da32d5-7cbd-4dc3-8643-5111d2fb4e16
---

Scaleway expose une API compatible S3 mais avec des limitations vs AWS.

**Configuration** :
- `AWS_PROFILE=scw` obligatoire (cf `~/.aws/credentials`)
- Endpoint : `https://s3.fr-par.scw.cloud`

**STS non supporté** :
- `aws sts get-caller-identity` retourne `An error occurred (Unknown)` — Scaleway n'implémente pas cet endpoint.
- Tester l'accès via `aws s3 ls s3://bucket/` à la place.

**`aws s3 sync` skip silencieux** :
- Le sync skip des fichiers de manière non-déterministe → toujours retry en boucle jusqu'à ce que `local_count == s3_count` (cf `~/.claude/rules/s3-safety.md`).
- Pour `aws s3 cp` unitaire : pas le même bug, mais wrapper dans une boucle retry est recommandé en environnement à haute concurrence.

**Bonnes pratiques** :
- `--no-progress` sur `aws s3 cp` pour des logs lisibles (sinon les progress bars `\r` polluent à 2.8 MB pour 20 lignes utiles).
- `--cli-read-timeout 0` quand bandwidth peut être saturée (e.g. 12 tmux parallèles).
- Vérifier la taille après upload : `stat -c %s local.bam == $(aws s3 ls s3 | awk '{print $3}')`

**Règle absolue** : `~/.claude/rules/s3-safety.md` = ne JAMAIS supprimer ni écraser sur S3 Scaleway. Idempotence via `aws s3 ls` avant upload.

Liens : [[project-phase1-state]] [[reference-bam2beta-integration]]
