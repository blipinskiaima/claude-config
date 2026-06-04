---
name: setup-v6-0-0
description: "Setup Dorado 2.0.0 + modèle V6.0.0, Pod2Bam.sh devenu script unique bi-mode robuste, batch HCL simplex"
metadata: 
  node_type: memory
  type: project
  originSessionId: c4c1838a-3b59-4a74-95fb-3f14d5282353
---

# Setup V6.0.0 (Dorado 2.0.0) — 2026-06-04

## Image & modèles V6.0.0
- **`pod2bam:2.0.0`** = Dorado `2.0.0+20e87c8b` + modèles V6.0.0 baked dans `/opt/models`
- Simplex : `dna_r10.4.1_e8.2_400bps_hac@v6.0.0`
- Modif : `dna_r10.4.1_e8.2_400bps_hac@v6.0.0_5mCG_5hmCG@v1` (suffixe `@v1` — reset à chaque génération majeure : v5.0.0=@v3, v5.2.0=@v2, v6.0.0=@v1)
- `docker/Dockerfile.2.0.0` (calqué sur Dockerfile.1.4.0, install CDN ONT `dorado-2.0.0-linux-x64.tar.gz`)
- Entrée `V6.0.0` ajoutée dans les 4 version maps de `nextflow.config` → `pod2bam:2.0.0`, `/opt/models`
- **Dorado 2.0.0 requiert CUDA ≥12.8**. Seul `hac@v6.0.0` existe pour l'ADN (pas de sup/fast en v6.0.0).
- **GOTCHA** : `dorado download --list` en 2.0.0 écrit sur `/dev/tty` (pas stdout/stderr) → capturer via `script -qec "dorado download --list" out.txt`. Voir [[dorado-reference]] (rule globale).

## Pod2Bam.sh = LE script unique bi-mode + robuste
- **Variable `MODE`** en haut : `simplex` vs `multiplex`
  - simplex (HCL) : S3 `.../HCL/liquid/{sample}/` **SANS** sous-dossier `pod5/`, kit `SQK-NBD114-24`, pas de barcode_sheet ni min-qscore
  - multiplex (CGFL) : `.../CGFL/liquid/{sample}/pod5/`, `SQK-NBD114-96`, barcode_sheet, min-qscore 9
- **3 fixes de robustesse** (bugs connus jamais corrigés dans Pod2Bam.sh avant cette session) :
  1. retry-loop UPLOAD S3 dans `finalize()` (symétrique au download prefetch) : compare local vs S3 count, 5 tentatives, log `UPLOAD OK`/`UPLOAD INCOMPLETE`
  2. succès = présence BAM final (`find align_trimmed -name *.bam`) au lieu de `EXIT_CODE=0` hardcodé → workdir conservé si pas de BAM **OU** sync incomplet
  3. glob trace `Pod2Bam_trace*.txt` + `grep -qh` (nextflow.config ajoute `_${date_tag}`)
- Upload auto du GLOBAL_LOG sur S3 en fin de batch (`aws s3 cp` vers `RetD/`)
- `dev/*.sh` = archives des batchs passés, NE PAS lancer — tout passe par `Pod2Bam.sh`

## Mode simplex dans le pipeline (rappel)
`Dorado_basecall` avec `--reference` fait **basecall + alignement EN UNE ÉTAPE**, puis `Samtools_sort_index`. **PAS de demux, PAS d'align séparé → 2 process.** Routage via présence/absence de `--barcode_sheet` ([basecall.nf:32](workflow/basecall.nf)). Multiplex = 4 process (basecall→demux→align→sort).

## base.config
- `Samtools_sort_index` : 4 → **16 CPU** (basecall reste GPU-bound `cuda:all`, le sort profite des CPU libres)

## Batch HCL simplex V6.0.0 (lancé 2026-06-04)
- 11 samples HCL simplex (10 Healthy + Lung_1, ~1531 GiB POD5)
- Healthy_11/12/14 confirmés OK sur S3 (sync vérifié 10/10) → **V6.0.0 validé en production**
- Output : `s3://aima-bam-data/processed/Pod2Bam/RetD/{sample}/V6.0.0/`, BAM final dans `align_trimmed/{sample}/{sample}.bam`
- Référence GRCh38 vient de `s3://aima-resources/dependencies/genomes/GRCh38/` → `/scratch/dependencies/genomes/GRCh38/`

## Gotchas serveur GPU
- `/scratch` peut être **vierge** au démarrage d'une nouvelle instance GPU → référence GRCh38 à re-télécharger depuis `s3://aima-resources/...`
- GPU = **H100 PCIe 80GB** (pas le SXM 80G d'avant)
- `nextflow` dans `~/.local/bin` (Nextflow 25.10.4). **NE PAS sourcer** `export/nextflow.sh` qui force `NXF_VER=25.04.8`
