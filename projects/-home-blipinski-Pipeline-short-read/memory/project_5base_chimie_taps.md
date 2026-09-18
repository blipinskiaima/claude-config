---
name: 5base-illumina-est-une-chimie-taps
description: "La chimie 5base Illumina convertit le C METHYLE en T (convention TAPS, comme Watchmaker) — pas bisulfite. Donc rastair est le bon caller, MethylDackel inverserait beta."
metadata: 
  node_type: memory
  type: project
  originSessionId: d6877158-bd11-4b5a-86db-42013f8d2b7a
  modified: 2026-09-18T12:48:12.503Z
---

Le 5base Illumina suit la **convention TAPS** : le C **méthylé** est lu **T**, le non-méthylé reste C. Ce n'est PAS du bisulfite (qui convertit le C non-méthylé). Mesuré sur Healthy634, pileup du BAM DRAGEN contre le `CX_report` du même sample :

| CpG brin + (réf = C) | C dans les reads | T dans les reads |
|---|---|---|
| CX_report = 100 % méthylé | 52,6 % | **47,0 %** |
| CX_report = 100 % non-méthylé | **99,0 %** | 1,0 % |

Le 47/53 au lieu de 100 % T vient de la directionnalité (`--methylation-protocol directional`, OT 35,73 % / OB 35,73 %) : à un CpG brin +, seuls les reads OT portent la conversion.

**Why:** Piège majeur. La conversion TAPS ne touche que ~4,9 % des C (290,9 M méthylés sur 5 936 M analysés) — elle est donc **invisible en composition globale de bases** : les FASTQ affichent C = 20,45 %, G = 22,70 %, soit du génomique normal. Conclure « reads non convertis » depuis la composition est une erreur ; il faut piler des CpG à état connu.

**How to apply:**

- Le pipeline **Watchmaker s'applique au 5base** : nf-core/methylseq 4.2.0 avec `--aligner bwamem --taps` → Rastair. Ne **jamais** utiliser `--aligner bwameth` (MethylDackel, convention bisulfite) : β sortirait inversé sans erreur visible.
- **FASTQ disponibles** : `s3://aima-bam-data/data/CGFL/5base/` — 70 samples appariés R1/R2, 101 bp, 0,7 To (bien au-delà des 8 de BP_5base : Prostate, Breast, Colon, Healthy ; uploads 2026-09-14/16). Pas besoin de repasser par `samtools fastq`.
- **BAM + miroir BaseSpace complet** : `s3://aima-bam-data/processed/short-read/basespace/5base/` (773 Go, 9 BAM, M-bias, methyl_metrics, VCF germline).
- Le doute « 5base non tranché, rastair est un outil TAPS, la chimie 5-base ne l'est pas » est **levé** : elle l'est. Le r = +0,97 de `rastair per-read` sur 5base est cohérent, pas suspect.

Voir [[project_mvaf14_short_read]] et [[project_bp5base_deux_apps_basespace]].
