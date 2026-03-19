---
name: Batch 3b1c780b sub (Breast_1 + Lung_10, multi-version)
description: Re-basecalling run 3b1c780b subset (2 samples) in V4.3.0, V0.7.4_V4.3.0 — completed 2026-03-19
type: project
---

## Batch 3b1c780b_sub — complété 2026-03-19

**Run** : `20250625_1437_P2I-00117-B_PBE76589_3b1c780b`
**Samples** : Breast_1 (barcode60) + Lung_10 (barcode59)
**POD5** : 131 fichiers, 280G (S3 standard path)

### Versions lancées

| Version | Script | Container | Basecall | Demux | Total | S3 sync |
|---------|--------|-----------|----------|-------|-------|---------|
| V4.3.0 | Pod2Bam_3b1c780b_sub.sh | pod2bam:0.9.6 | ~40min | ~20min | ~1h40 | OK (73 files) |
| V0.7.4_V4.3.0 | /tmp/launch_v074_v430.sh | pod2bam:0.7.4 | 1h22min | ~2h | ~2h27 | OK (73 files, 55G) |

### Observations Dorado 0.7.4 vs 0.9.6

- **VRAM** : 0.7.4 utilise 48-68G vs 29G pour 0.9.6
- **Demux** : 0.7.4 ~2h vs ~20min pour 0.9.6 — **10x plus lent**
- **Basecall** : 0.7.4 ~1h22 vs ~40min pour 0.9.6 — **2x plus lent**

### Barcode sheets

- `tables/..._subV4.3.0.tsv` : noms sans suffixe version (Breast_1, Lung_10)
- `tables/..._subV5.0.0.tsv` : noms avec suffixe (Breast_1_rebasecalled_V5.0.0, ...)

### S3 output

- `s3://aima-bam-data/processed/Pod2Bam/RetD/20250625_..._3b1c780b_sub/V4.3.0/`
- `s3://aima-bam-data/processed/Pod2Bam/RetD/20250625_..._3b1c780b_sub/V0.7.4_V4.3.0/`
- Global log : `Pod2Bam_3b1c780b_sub_Pod2Bam_20260319_180240.log`

### V0.9.6_V5.0.0 — non lancé

- Préparé dans le script mais annulé par l'utilisateur
- Barcode sheet prête (`_subV5.0.0.tsv`)

### Bug rencontré

- Script Pod2Bam_3b1c780b_sub.sh supprime les POD5 à la fin → le script chaîné pour V5.0.0 n'a pas trouvé les POD5
- Fix : ajout du download S3 dans le script chaîné

**Why:** Re-basecalling de 2 samples spécifiques pour comparaison multi-version (V4.3.0 vs V0.7.4_V4.3.0).
**How to apply:** Pour relancer d'autres versions sur ce run, les POD5 doivent être re-téléchargés. Image pod2bam:0.7.4 buildée sur le serveur.
