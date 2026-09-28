---
name: secret-token-tower-expose
description: Token Seqera Tower en clair et commité dans Methylseq/nextflow.config — à révoquer, pas seulement à supprimer
metadata:
  type: project
---

`~/Pipeline/Methylseq/nextflow.config` contient un **token d'accès Seqera Platform en clair**,
répété dans 3 profils (`tower`, `local_docker`, `local_singularity`), sous la clé
`tower.accessToken`. Il est présent dans le commit `200b5cb` poussé sur
`github.com/aima-dx/Methylseq`.

**Why** : violation directe de `~/.claude/rules/secrets.md` et de la règle 2 de
`~/.claude/rules/nextflow.md`. Un token commité reste lisible dans l'historique git même
après suppression du fichier — toute personne ayant accès au dépôt (ou à un fork, ou à un
clone déjà fait) le conserve.

**How to apply** : ordre obligatoire — (1) **révoquer** le token dans Seqera Platform et en
émettre un nouveau, (2) remplacer les 3 occurrences par
`accessToken = System.getenv('TOWER_ACCESS_TOKEN')`, cohérent avec `TOWER_ENDPOINT` et
`TOWER_WORKSPACE_ID` déjà lus par `System.getenv` juste en dessous, (3) exporter le nouveau
token depuis `~/Pipeline/export/nextflow.sh` (déjà sourcé par `launch.sh`). La réécriture
d'historique git est optionnelle une fois le token révoqué.

Même schéma à vérifier sur les autres clones de pipelines nf-core du parc.
Contexte du dépôt : [[version-pipeline-nf-core]].
