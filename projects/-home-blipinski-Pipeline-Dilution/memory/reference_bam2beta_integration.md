---
name: reference-bam2beta-integration
description: "Conventions Bam2Beta — format input dossier S3, tags MM/ML, naming, paths sources"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 37da32d5-7cbd-4dc3-8643-5111d2fb4e16
---

Bam2Beta (~/Pipeline/Bam2Beta) consomme un dossier S3, pas un fichier BAM individuel.

**Format input attendu** :
- `--input "s3://.../{SAMPLE_DIR}"` — Bam2Beta cherche les .bam dans ce dossier ou son sous-dossier `BAM/` (à confirmer dans `workflow/merge.nf` ligne ~47 : `find "${BAM}/" -maxdepth 1 -type f -name "*.bam"`).
- L'ID sample = nom du dossier S3 (`main.nf:125 : path.name`).

**Pré-requis BAM** :
- Tags MM/ML (modifications ONT) REQUIS — sans eux, `modkit pileup` produit silencieusement un `bedMethyl` vide → mVAF absent.
- `.bai` pas nécessaire en input (généré par `BAM_sort`).
- Pas de validation header/MD tag explicite.
- Coordonnées hg38 implicites.

**Naming sample** :
- Underscore obligatoire, JAMAIS de point — `target_1_0` ✓, `target_1.0` ✗ (casserait `cut -d '.' -f 1` dans `Raima_report` beta.nf:326).

**Paths S3 sources** :
- BAMs CGFL : `s3://aima-bam-data/processed/MRD/RetD/liquid/CGFL/{sample}/BAM/{sample}.merged.bam`
- BAMs HCL : `s3://aima-bam-data/processed/MRD/RetD/liquid/HCL/{sample}/BAM/{sample}.merged.bam`
- Suffixe `_rebasecalled_V5.0.0_trimmed` = sample retraité depuis POD5 ancien. Sans ce suffixe = sample basecallé directement en dorado v5 (Breast_34, HCL healthys).

**Outputs Bam2Beta** :
- `${SAMPLE}/BAM/`, `BETA/` (bedMethyl + raima_score V2 tsv), `CNV/`, `Fragmentomics/`, `QC/`, `REPORT/` (PDF + JSON)
- Fichier clé pour KPI : `BETA/{ID}.merged.epic.raima_score.V2.tsv` (colonnes score / mVAF / model v1+v2)

**Profil recommandé** : `prod` (rarefaction = merged uniquement). Pas `liquid` (7 niveaux de rarefaction = 7x plus de jobs).

Liens : [[project-phase1-state]] [[reference-aws-scaleway]]
