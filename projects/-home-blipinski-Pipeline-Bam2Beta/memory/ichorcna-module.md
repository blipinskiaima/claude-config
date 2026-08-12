---
name: ichorcna-module
description: "Module ichorCNA (fraction tumorale HMM/CNA) — container, workflow, panels, gotchas d'installation"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c6971ef-9e62-46ae-935a-5026efb56aa3
  modified: 2026-08-11T08:47:45.629Z
---

# Module ichorCNA (2026-03-20)

- **Container** : `blipinskiaima/ichorcna:latest` (R + hmmcopy readCounter + ichorCNA +
  BSgenome.Hsapiens.UCSC.hg38)
- **Workflow** : `workflow/ichorCNA.nf` — 2 process (`IchorCNA_readCounter` → `IchorCNA_run`)
- **Scripts** : `bin/ichorCNA/` (`run_readCounter.sh`, `run_ichorCNA.R`,
  `create_panel_of_normals.sh`)
- **Panel par defaut** : Florian (`ichorCNA-panel-of-normals_median.rds`) ; Broad et custom
  aussi disponibles
- **Dependances** : `/scratch/dependencies/ichorCNA/` (gc_wig, map_wig, centromere, panels)
- **Test Healthy_826** : TFx = 0.026, ploidy = 2.306 — PASS
- **Actif** : `ICHORCNA=true` en liquid et solid, **false en prod** et par defaut. Les lanceurs
  `dev/SCW/` utilisent `-profile docker,tower,$TYPE,scw` (donc liquid/solid → actif).

## Gotchas d'installation

- `getwilds/ichorcna` teste et **rejete** (pas de readCounter, pas de libs graphiques png)
- `remotes::install_github` n'installe **pas** `inst/scripts/` → scripts clones separement
  dans le Dockerfile
- `runIchorCNA.R` ne cree pas le `outDir` → `mkdir -p` necessaire dans le process NF

## Sorties utiles au QC

`{OUTPUT}/{ID}/ichorCNA/{ID}.params.txt` contient **`GC-Map correction MAD`**, metrique de bruit
publiee par les auteurs de l'outil (seuils < 0.15 haute qualite · < 0.20 « sufficient » · > 0.30
« too noisy »). Instruit comme candidat QC le 2026-08-10 → **ecarte** (aucun rejet nouveau a tous
les seuils publies, et correle a la longueur de read contrairement a ce qui etait annonce).
Voir `docs/QC-seuils-biopsie-liquide.md`.
