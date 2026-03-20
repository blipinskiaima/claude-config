---
name: s3_never_delete
description: NEVER delete anything from S3 buckets - data is irreversible
type: feedback
---

Ne JAMAIS supprimer de fichiers dans les buckets S3 (`aws s3 rm`, `aws s3 rb`, `--delete`).

**Why:** Les données sont irréversibles. C'est une règle d'or absolue du projet, rappelée explicitement par l'utilisateur.

**How to apply:** Avant toute commande `aws s3`, vérifier qu'elle ne contient pas `rm`, `rb`, ou `--delete`. Cela s'applique aussi aux scripts, aux commandes Nextflow, et à tout code qui interagit avec S3.
