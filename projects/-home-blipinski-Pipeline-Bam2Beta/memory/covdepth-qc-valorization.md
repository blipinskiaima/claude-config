---
name: covdepth-qc-valorization
description: Chantier R&D covdepth — valorisation analyse QC depth/coverage par sample + détection anomalies multi-échelle (roadmap) ; Étape 1 = figure(s) merged+epic sur Bladder_Urine_02_064
metadata: 
  node_type: memory
  type: project
  originSessionId: baa0c749-9109-466e-8649-b1ef4f18abb5
---

Chantier démarré le 2026-06-22 (dev model Opus 4.8 1M MAX thinking). Workspace local `/scratch/boris/covdepth/{data,result,script}` ; livrables (figures finales UNIQUEMENT) copiés dans `/home/blipinski/Pipeline/Bam2Beta/dev/coverage_analysis/test/`. S'appuie sur l'outil existant [[coverage-analysis-cgfl-hcl]] (binning per-base mosdepth 100kb, helper `save_png()`, exclusion chrX/Y + `total` + alt/random) — ne pas le réinventer.

Sample test : `Bladder_Urine_02_064` (CGFL liquid urine, ~1x). QC sur S3/NFS `.../RetD/liquid/CGFL/Bladder_Urine_02_064/QC/` (Cramino/, Mosdepth/merged/, Samtools/). **Deux jeux mosdepth** à ne pas confondre : `*.merged.*` (génome WGS, per-base ~260MB) et `*.merged.epic.*` (empreinte EPIC ciblée, per-base ~27MB). Source canonique depth/coverage = courbe cumulative `*.mosdepth.global.dist.txt` (piège : `depth_threshold` monte à ~1176, pas 144 ; exclure ligne `total` + contigs alt/random).

**Objectif global (ROADMAP — prévu dans les prochaines étapes, à ne PAS coder en spéculatif maintenant)** :
- Valoriser l'analyse QC pour les samples.
- Détecter des anomalies QC à l'échelle du sample.
- Détecter des anomalies de tendance à plusieurs échelles : sample → cohorte → indication → labo → multi-labo → tous samples réunis.

**Étape 1 (en cours)** : figure(s) R basique(s) depth/coverage pour les DEUX jeux (merged + epic), claires et lisibles biologiste + bioinfo — jusqu'à 2 figures, ou 1 figure comparative à 2 courbes (à challenger). Étapes suivantes non encore définies.

Process imposé : Karpathy Guidelines + gates d'approbation par phase (brainstorm → contexte → plan → impl → vérif), arrêt/validation après chaque modif. Prompt de lancement rédigé via prompt-creator le 2026-06-22 (cible Opus 4.8 1M MAX). Git du dossier `test/` : ignoré pour l'instant (décision Boris).
