# Context — Bam2Beta — 2026-09-11T09:59

**Branche** : main
**Dernier commit** : bbbc009 — chore(perf): right-sizing des ressources mesure sur 46 traces, paires dilution en 4 lots
**Status** : clean (seul `pair_current.tsv` non suivi, temporaire du lanceur)

## Où j'en suis

Session d'optimisation des performances, pas de feature. Cartographie du module EXIS puis
analyse de perf sur **46 traces Nextflow récupérées sur S3** (les lanceurs passent
`-with-trace` en CLI malgré `trace.enabled=false` — c'est LA source, `cleanup=true` purge
le workDir local). Right-sizing de `conf/base.config` appliqué et poussé. Fiches mémoire
écrites : `perf-exis-traces`, `ressources-dimensionnement`, `dependencies-provisioning`.

## Ce qui marche / ce qui foire

- ✓ Diagnostic solide : `Raima_score_mVAF` = 74-81 % du wall-clock EXIS sur 7 samples de
  0,4 à 44 Go, queue mono-tâche à 12 % d'occupation ; phase MERGE = 40 % du run
- ✓ Right-sizing poussé (`0856f3f` + `bbbc009`) : `IV_call` 8→16 G (2 OOM réels corrigés),
  ternaire `Mosdepth_qc` rendu cohérent à 16 G, ~20 sur-allocations ramenées à 2 G,
  MERGE monté à 16 cpus (`BAM_sort` 40 G)
- ✓ Déterminisme prouvé : `samtools sort` entre threads (md5 SAM identique) et
  `GNU sort -S/--parallel` (hôte 9.4 + container 8.32)
- ✗ **Optimisation de la boucle de tri jamais appliquée** — mesurée 10,82 → 4,96 s par
  chromosome, contenu md5-identique, ≈ −300 s sur Lung_9. C'est le seul levier restant
  dans notre code
- ✗ `Raima_score_mVAF` passé à 8 cpus **sans A/B** : `--ncores` pilote `setDTthreads`, qui
  agit sur des sommes flottantes de raima → peut changer une sortie qualifiée. Et les
  workers étaient déjà affamés (2,2 cœurs sur 4), donc gain douteux
- ✗ `Read_Start_Time` commenté dans `qc.nf` — supprime aussi `sequencing_time.tsv`
  (chemin rapide trace-prod). Réactivation prévue par Boris
- ✗ `ichorCNA/` (5 fichiers) n'existe que sur ce serveur, absent de `s3://aima-resources`
- ✗ Machine sursouscrite : jusqu'à 9 runs Nextflow simultanés, load 119 sur 32 cœurs

## Prochaine étape

Appliquer l'optimisation de la boucle de tri dans `workflow/beta_28M.nf` (~ligne 166) :
`sort -S 2G --parallel=${task.cpus}`, `gzip -1`, et `xargs -P` sur les 22 itérations.
`xargs` est dans le container raima, `pigz` non.
