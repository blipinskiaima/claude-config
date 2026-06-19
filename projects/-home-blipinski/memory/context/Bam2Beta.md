# Context — Bam2Beta — 2026-06-19T16:27:57+0000

**Branche** : main
**Dernier commit** : e1362a1 — feat(dev): outils analyse couverture mosdepth (per-base -> bins 100kb)
**Status** : 6 fichiers modifiés (tous PRÉ-EXISTANTS, hors session : conf/base.config, workflow/beta.nf, workflow/merge.nf, dev/PLT/*, dev/SCW/launch_SCW.sh, bacasable.sh)

## Où j'en suis
Session "analyse de couverture mosdepth" terminée. Outil `dev/coverage_analysis/` créé et commité (scripts seuls, outputs gitignorés). Figures produites pour 3 analyses : (1) 20 samples mixtes merged+epic, (2) Healthy CGFL vs HCL (231 samples, all + matched 0.6-1.5x). Conclusion : couverture autosomale équivalente entre labos, trous = régions non-mappables hg38, pas d'effet labo.

## Ce qui marche / ce qui foire
- ✓ Binning per-base→100kb en streaming NFS (aucune copie des 145 GB sources), parallèle idempotent, relançable en tmux
- ✓ Figures PNG (VSCode ne lit pas les PDF) : cumulative + positionnelle médiane/IQR par labo
- ✓ Finding : batch effect CGFL/HCL absent sur la couverture (présent uniquement sur les scores)
- ✗ `Healthy_780.merged.per-base.bed.gz` CORROMPU (CRC error) → exclu (231/232). Fichier non touché
- ✗ epic non comparable entre labos (Healthy CGFL sans fichier epic) ; epic dilué en bins 100kb (peu lisible)

## Prochaine étape
2 points en suspens proposés à Boris, non tranchés : (1) scan intégrité `gzip -t` des autres per-base QC pour voir si la corruption Healthy_780 est isolée ou systémique (lecture seule) ; (2) intersection des trous merged avec blacklist ENCODE pour confirmation. Sinon, analyse close.
