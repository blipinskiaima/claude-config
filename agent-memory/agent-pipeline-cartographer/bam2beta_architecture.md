---
name: bam2beta_architecture
description: Architecture Bam2Beta — workflow, inputs BAM, conventions naming, scoring RAIMA, outputs S3, profiles
metadata:
  type: project
---

## Bam2Beta V1.2.0 — Architecture et conventions

**Version manifest** : V1.1.2 (nextflow.config) mais README dit V1.2.0 (IV module ajouté 2026-05-11)

### Input BAM
- `--input` = chemin S3 vers un **dossier** contenant des `.bam` (pas un fichier individuel)
- Bam2Beta découvre les BAMs via `find "${BAM}/" -maxdepth 1 -type f -name "*.bam"` (workflow/merge.nf:47)
- L'ID sample = **nom du dossier** (path.name dans main.nf:125)
- Pas de validation explicite ni de check de headers/tags en entrée — samtools merge/sort sans contrainte
- Le BAI est **généré par le pipeline** (BAM_sort produit .bam + .bai) — pas nécessaire en input
- Pas de vérification de read groups ni MD tag — modkit pileup travaille sur les mod-tags ONT (MM/ML)
- Profil liquid : rarefaction `merged,20M,15M,10M,5M,2M,1M`

### Naming samples
- L'ID = nom du dossier S3 passé à --input, sans contrainte regex
- Pas de routing automatique tumoral vs healthy — le pipeline traite tout identiquement
- Le naming `${SAMPLE}_Healthy_${X}_target_${Y}` est compatible (juste un ID string opaque)
- Le rapport PDF utilise `cut -d '.' -f 1` sur l'ID pour extraire le "name" patient (beta.nf:326)

### Scoring RAIMA / mVAF (TF)
- `raima_score.R` : appelle `raima::model_v1()` + `raima::model_v2()` sur le bedMethyl
- Output TSV : colonnes model / score / mVAF (alias TF depuis V1.0.1)
- Le mVAF est extrait pour le rapport via `awk -F'\t' '$4 == "v1"' | cut -f 3` (beta.nf:354)
- Pas de seuil positif/négatif codé dans Bam2Beta — le seuil est dans le package `raima` R (opaque)
- `raima_score_v1.2.R` : scoring rétrospectif v1.2 (range_w=c(0,10) selon changelog)
- `raima_score_cnv.R` : scoring CNV via raima (depths + score_cnv.tsv)

### Outputs S3
- Arborescence : `{OUTPUT}/{SAMPLE_ID}/BETA/{ID}.merged.epic.raima_score.V2.tsv`
- JSON : `{OUTPUT}/{SAMPLE_ID}/REPORT/{ID}.merged.epic.raima_score.V2.json` (champs: score, tf, nb_reads_raw, depth)
- 17 fichiers attendus par sample (critère conformité)

### Profils
- `prod` : MERGE+BETA+FRAG+CNV+IV, rarefaction=merged, cpus_max=8, mem=32GB
- `liquid` : tous modules + rarefaction 7 niveaux (merged,20M,...,1M)
- `scw` : profil AWS Scaleway fr-par

### Paths S3 inputs connus
- Données CGFL liquid : `s3://aima-bam-data/data/CGFL/liquid/`
- Sample test : `Healthy_826` dans `s3://aima-bam-data/data/CGFL/liquid/`
- BAM merges R&D : `s3://aima-bam-data/processed/MRD/RetD/*.merged.bam` (~18.62 To)
- Profil AWS : toujours `scw` (endpoint https://s3.fr-par.scw.cloud)

### Points d'attention pour dilutions in silico
- Pas de stress-test documenté sur 0.1% VAF — territoire inconnu pour Bam2Beta
- BAM_Subsampling skipe silencieusement si total_reads <= target (ex: 1M skip si BAM < 1M reads)
- Modkit pileup filtre avec `--include-bed epic850K.extended.100.clean.bed` — les reads hors EPIC sont exclus
- La profondeur effective sur les CpGs EPIC est ce qui compte pour la qualité du score
