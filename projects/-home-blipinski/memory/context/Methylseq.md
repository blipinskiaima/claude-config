# Context — Methylseq — 2026-10-02T13:14+00:00

**Branche** : main
**Dernier commit** : b429809 — feat: QC export script + WM batch2 (48 samples) launch traceability
**Status** : 1 fichier non suivi (samplesheet_alone.csv, test Breast_26 volontairement exclu)

## Où j'en suis
Les 48 samples WM (batch2, 4 lots de 12) sont passés dans methylseq. Le QC des 64 samples
(batch1 + batch2) est exporté dans la gsheet, onglet "Watchmaker - Methylseq - Element",
via methylseq_qc.py (16 colonnes, définitions validées une à une : Nb reads = 2×(A+D+E),
Nb molécules = A+D+E, % mappés, Depth et Coverage version ONT + "utile méthylation"
avec le filtre rastair). Arrêt après l'export avec la colonne Batch simplifiée (batch1/batch2).

## Ce qui marche / ce qui foire
- ✓ Script QC : S3 ou --local, CSV de cache, garde anti-écrasement de la Sheet, 64/64 samples, non-régression vérifiée
- ✓ Définitions raccord ONT (même référence hg38, 195 contigs, mosdepth par défaut = Bam2Beta)
- ✗ Taille insert moy. = NA pour 5 samples batch1 (Colon_12, Colon_13, Colon_50, Healthy_637, Lung_13) : pas de .stats publié
- ✗ batch2_4 pas encore remonté sur S3 (local seulement : /scratch/methylseq/batch2_4)
- ✗ À surveiller : Lung_13 (4 indicateurs hors norme), Healthy_772 (méthylation globale 0,625)

## Prochaine étape
Synchroniser batch2_4 vers S3 (boucle jusqu'à local = S3), puis combler la taille d'insert
des 5 samples batch1 via samtools stats sur le BAM dédupliqué, après validation sur Colon_3
(le .stats du pipeline est calculé avant dédup).
