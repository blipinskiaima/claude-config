---
name: qc-export-methylseq
description: "methylseq_qc.py → CSV + onglet gsheet \"Watchmaker - Methylseq - Element\" ; définitions validées Nb reads / Nb molécules (paires) en paired-end"
metadata:
  node_type: memory
  type: project
  originSessionId: 08f7a23b-e69f-4f22-a31a-236ff313703e
  modified: 2026-10-01T12:29:14.100Z
---

`~/Pipeline/Methylseq/methylseq_qc.py` (créé 2026-09-29/10-01) extrait le QC des sorties methylseq
(S3 `processed/short-read/Methylseq/batch*/`, ou `--local <dossier batch>`) → `methylseq_qc.csv`
(= cache, clé (Batch, Sample)) → `--gsheet` vers sheet `1FN4VCENXic6TAxUPRAOe-yq6-5MAWBc74whVx3tFYCo`,
onglet `Watchmaker - Methylseq - Element`. 64 samples au 2026-10-01 (batch1 16 + batch2_1..2_4 4×12).

**Définitions validées par Boris (2026-10-01)** — paired-end : **1 molécule = 1 paire = 2 reads** (ONT : 1 read = 1 molécule) :
- Principe : comparer **tout ce qui sort du séquenceur** (ONT : cramino sur BAM merged) → comptés sur les
  **FASTQ bruts, avant trimming** (TrimGalore `Total reads processed`, R1 et R2). Doublons PCR inclus (font partie du process).
- `Nb reads` = R1 + R2 bruts (tous confondus : trimmés ou non, éliminés, mappés ou non, pairés ou non). Colon_14 = 64,61 M.
- `Nb molécules (paires de reads)` = paires brutes = R1 brut = Nb reads ÷ 2. Colon_14 = 32,31 M.
  (Ancienne version abandonnée : comptes BAM post-trim via Picard, 64,51 / 32,26.)
- **Définition validée (2026-10-01) : Nb molécules = A + D + E**, en molécules (paires) :
  A = non mappées, D = mappées (A+D = paires qui entrent dans l'alignement = reads primaires BAM ÷ 2),
  E = paires éliminées au trimming (une read < 20 pb, AVANT l'alignement). Colon_14 : 32 255 420 + 50 740 = 32 306 160.
  ONT : Nb molécule = A + D (cramino num_reads, pas d'étape de trim). Base commune = ce que l'instrument
  livre pour le sample : ONT = BAM MinKNOW `*_pass_barcodeNN_*` uniquement (fail exclus), short-read = FASTQ
  livrés (PF + démux). Les filtres instrument diffèrent et ne sont pas quantifiés.
- **% mappés = D / Nb reads** (raccord ONT : Bam2Beta n'a que % non alignées A/(A+D), rapport.nf:76).
- **% reads utiles méthylation = samtools view -c -f 3 -F 3852 -q 1 / Nb reads** = filtre par défaut de rastair
  (call ET per-read, aucune option passée) : paires propres seulement, sans doublons ni MAPQ 0 ni singletons.
  Propre au short-read (ONT : modkit sur -F 3840, pas de MAPQ). Prostate_4 : 99,78 % mappés vs 83,97 % utiles.
- **Depth / Coverage %** = mosdepth défaut (= Bam2Beta) ; **Depth / Coverage utile méthylation** = mosdepth
  `-i 2 -F 3852 -Q 1` (-i = ANY bit, d'où 2 et pas 3). Réf ONT et short-read identique : 195 contigs, 3 099 922 541 pb.
- **Nb reads = 2 × (A + D + E)** validé (R1 + R2 bruts ; 1 molécule = toujours 2 reads, R1 = R2 vérifié 64/64 ;
  « non pairé » = statut d'alignement, jamais une read orpheline). ONT : Nb reads = Nb molécule = A + D.
- `Nb lignes total` (CSV seulement, retiré de l'export avec `Batch`).

Depth / Coverage % = mosdepth (défauts, -F 1796, chevauchement R1/R2 compté 1 fois) sur BAM dédup —
définition Bam2Beta. ≠ DRAGEN (BP_Watchmaker_summary.tsv) dont la depth est ~25 % plus haute
(chevauchement compté 2 fois). Coverage plafonne à 94,67 % (165 M de N dans la réf iGenomes 3,10 Gb).

**Why:** Boris revoit les 4 notions une à une (Nb molécule ✓, puis % mappés, Depth, Coverage %).
**How to apply:** ne pas réintroduire un « Nb molécule » = reads ; la garde gsheet bloque si l'onglet a des
en-têtes inconnus du script — après un renommage de colonne, vérifier que l'onglet = notre export puis clear.
Lien : [[run-5base-healthy767]], [[version-pipeline-nf-core]].
