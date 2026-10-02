# Context — Methylseq — 2026-10-02T13:53+00:00

**Branche** : main
**Dernier commit** : f4aa601 — feat(qc): fill insert size from dedup BAM when samtools .stats is missing
**Status** : 1 fichier non suivi (samplesheet_alone.csv, test Breast_26 volontairement exclu)

## Où j'en suis
Batch WM complet et clos : 64 samples (batch1 16 + batch2 48) traités par methylseq,
archivés sur S3 (5 batchs + logs dans Methylseq/log/), QC exporté dans la gsheet
"Watchmaker - Methylseq - Element" sans aucun NA (64 × 16). Plus rien en cours sur ce projet.

## Ce qui marche / ce qui foire
- ✓ methylseq_qc.py : S3 ou --local, CSV de cache, repli taille d'insert sur BAM dédup, garde anti-écrasement gsheet
- ✓ Définitions QC validées une à une, raccord ONT (même réf hg38 195 contigs, mosdepth = Bam2Beta)
- ✓ batch2_2 / batch2_4 identiques local/S3 fichier par fichier → ~395 Go libérables sur /scratch/methylseq (décision de Boris)
- ✗ À surveiller : Lung_13 (coverage 68 %, % utiles 79,9, supplémentaires 0,48 %), Healthy_772 (méthylation globale 0,625)
- ✗ Lots 1-3 sans qualimap (lot 4 seul) : laissé tel quel, le script ne l'utilise pas

## Prochaine étape
Côté projet short-read : mesurer l'écart NREADS du bootstrap mVAF v1.4 (`05_bootstrap.sh:24`,
-q 20 -F 3844) vs filtre rastair (-f 3 -F 3852 -q 1) sur EPIC. Côté Methylseq : relancer
methylseq_qc.py --gsheet quand de nouveaux samples arriveront.
