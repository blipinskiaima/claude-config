---
name: scratch-workspace-readonly-bams
description: Analyses ad-hoc dans /scratch/boris/<topic>/ ; les BAM/POD5 source restent strictement en lecture seule (jamais écrire/écraser/copier par-dessus)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9c09127f-ca8b-4ec5-816e-ee694f453d50
---

Pour tout travail d'analyse ad-hoc / exploratoire sur le serveur (samtools, parsing CIGAR, scripts jetables, sorties intermédiaires), travailler dans `/scratch/boris/<topic>/` (créer le sous-dossier au besoin). Le BAM/POD5 source reste **strictement en lecture seule** — jamais d'écriture, d'écrasement, ni de copie par-dessus la source.

**Why:** Boris a interrompu une analyse soft-clip où j'allais écrire les sorties dans `/tmp` et streamer le BAM source ; il a explicitement demandé de travailler dans `/scratch/boris/soft-clip` et que « le bam initial doit rester intact sur le s3 ». `/scratch/boris/` contient déjà ~17 sous-dossiers thématiques = workflow établi. Renforce la golden rule s3-safety (jamais supprimer/écraser S3).

**How to apply:** Quand Boris demande une analyse exploratoire sur des données de prod (BAM, POD5…), créer/utiliser `/scratch/boris/<topic>/` pour tous les scripts + outputs. Lecture seule en streaming depuis le mirror NFS = OK (samtools view ne modifie pas la source). Pas de copie inutile des gros fichiers (28 Go) sauf nécessité explicite (simplicité Karpathy). `/scratch` ≈ 700 Go libres.
