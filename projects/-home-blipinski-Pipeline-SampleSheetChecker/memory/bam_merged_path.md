---
name: bam-merged-path
description: Vrai chemin S3 des BAM merged finaux après pipeline Bam2Beta. Ne PAS confondre avec data/HCL/liquid/ qui ne contient que des index .bam.bai
metadata: 
  node_type: memory
  type: reference
  originSessionId: cb1d1046-c95d-47dc-ad1f-843c27fe0fe3
---

# Chemin S3 des BAM merged AIMA

**Chemin réel des BAM finaux** :
```
s3://aima-bam-data/processed/MRD/RetD/liquid/HCL/{sample}/BAM/
├── {sample}.merged.bam       # BAM principal (10-80 GB typique)
├── {sample}.merged.bam.bai
├── {sample}.merged.epic.bam  # subset CpG / epic targets (~5% de la taille)
└── {sample}.merged.epic.bam.bai
```

**Piège à éviter** : `s3://aima-bam-data/data/HCL/liquid/{sample}/` ne contient **PAS** les .bam — uniquement :
- `{sample}_bam_list.txt`, `{sample}_bai_list.txt`, `{sample}_header.txt`
- Les `.bam.bai` (index)
- Pas le `.bam` lui-même

→ Pour vérifier la présence du BAM final d'un sample, toujours regarder dans `processed/MRD/RetD/liquid/HCL/{sample}/BAM/`, pas dans `data/HCL/liquid/`.

## Autres sous-dossiers de `processed/MRD/RetD/liquid/HCL/{sample}/`
- `BAM/`, `BETA/`, `BETA_28M/`, `BETA_FILTER/`
- `CNV/`, `EXTRACT_FULL_28M/`, `Fragmentomics/`, `IV/`
- `LOG/`, `QC/`, `REPORT/`, `ichorCNA/`
- Marqueurs : `Bam2Beta.start`, `Bam2Beta.done`, `restart.sh`

## Versions rebasecalled
Les samples re-basecallés avec une nouvelle version Dorado sont stockés dans `{sample}_rebasecalled_V4.3.0/`, `_V5.0.0/`, `_V5.2.0/` etc. — c'est ce qui explique les "20 lignes en plus" dans la gsheet metadata_HCL.
