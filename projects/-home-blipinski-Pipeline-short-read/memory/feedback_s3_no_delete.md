---
name: Never delete from S3
description: Golden rule - never delete anything from S3 buckets under any circumstances
type: feedback
---

Ne JAMAIS supprimer quoi que ce soit des buckets S3.

**Why:** Règle d'or absolue de l'utilisateur. Les données sur S3 sont considérées comme précieuses et irremplaçables.

**How to apply:** Même si des fichiers semblent dupliqués, obsolètes ou inutiles sur S3, ne jamais proposer de `aws s3 rm` ou `aws s3 rm --recursive`. Si un nettoyage semble nécessaire, le signaler à l'utilisateur sans agir.
