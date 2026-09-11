---
name: scaleway-links-disabled
description: "Retrait de tous les liens cliquables vers la console Scaleway ; les chemins S3 restent en texte."
metadata:
  node_type: memory
  type: project
  modified: 2026-06-12T00:00:00.000Z
---

# Liens Scaleway désactivés (2026-06-12)

Tous les liens cliquables vers la console Scaleway ont été retirés (commit `5744647`,
tag de rollback `pre-disable-scaleway`).

Décision Boris : **garder le chemin, retirer la navigation web**. Les chemins S3 restent
donc affichés en **texte non cliquable** (`<code>`) sur `/database › Platform`,
`/monitoring` et `/sample/:id` — où le bouton « Exporter rapport » a été supprimé.

⚠ Les helpers `s3ToScaleway` (frontend) et `_s3_to_scaleway` (Dash legacy, `callbacks.py`)
ont été **supprimés** : ne plus s'y référer.
