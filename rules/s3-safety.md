# Golden Rules — S3 Scaleway

Ces règles sont ABSOLUES et s'appliquent à TOUS les projets, TOUS les buckets, sans exception.

## Interdictions

1. **Ne JAMAIS supprimer** de fichiers dans les buckets S3 — aucune commande `aws s3 rm`, `aws s3 rb`, `aws s3 sync --delete`, aucun script de suppression, aucune politique de lifecycle qui purge des objets.
2. **Ne JAMAIS écraser** de données existantes dans les buckets S3 — si un fichier existe déjà à la destination, ne pas le remplacer sans confirmation explicite de Boris.
3. **Ne JAMAIS supprimer les POD5** téléchargés dans `/scratch/basecall/dorado/data/` — source de vérité pour le re-basecalling.

## Obligations

4. **TOUJOURS utiliser le profil `scw`** pour les opérations S3 Scaleway : `AWS_PROFILE=scw`.
5. **TOUJOURS retry `aws s3 sync`** en boucle jusqu'à `local_count == s3_count` — le sync skip silencieusement des fichiers de manière aléatoire.
