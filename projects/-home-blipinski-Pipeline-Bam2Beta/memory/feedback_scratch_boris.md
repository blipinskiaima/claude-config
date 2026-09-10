---
name: feedback_scratch_boris
description: "Les fichiers temporaires de travail sur le serveur vont dans /scratch/boris, pas ailleurs sous /scratch"
metadata:
  type: feedback
---

Tout fichier temporaire creé sur le serveur de calcul va dans **`/scratch/boris`**.

**Why:** demande explicite de Boris (2026-09-09), pendant un test de determinisme de
`samtools sort` ou j'avais creé `/scratch/claude_sorttest` a la racine de `/scratch`.
`/scratch` heberge `nxf-work` (runs Nextflow actifs) et `dependencies` : y semer des
dossiers ad hoc rend l'arborescence illisible et risque la confusion avec des données de run.

**How to apply:**
- Tests lourds necessitant `/scratch` (docker `-v /scratch:/scratch`, gros BAM) → `/scratch/boris/<sujet>`.
- Ne jamais ecrire a la racine de `/scratch`, ni toucher `/scratch/nxf-work` (runs en cours).
- Le scratchpad de session reste le defaut pour les petits fichiers ; `/scratch/boris` sert
  quand le container doit voir le fichier (le scratchpad sous /tmp n'est pas traversable
  depuis un container, meme en `-u 0:0` — "Permission denied" verifie).
- Nettoyer apres soi ; cela ne releve pas de la regle S3 never-delete.
