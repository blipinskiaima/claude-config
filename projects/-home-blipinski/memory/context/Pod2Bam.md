# Context — Pod2Bam — 2026-06-05T08:30+02:00

**Branche** : main
**Dernier commit** : c60e998 — Set RUNS_FR to complete HCL V6.0.0 batch (11 samples, all done)
**Status** : clean

## Où j'en suis
Batch HCL simplex V6.0.0 **terminé** : 11/11 samples basecallés avec Dorado 2.0.0, BAM sur S3, sync vérifié. Image `pod2bam:2.0.0` buildée et validée. `Pod2Bam.sh` devenu le launcher unique bi-mode (simplex/multiplex) avec retry-loop upload/download, détection BAM final, upload auto GLOBAL_LOG. 319 GB de résultats locaux encore dans `/scratch/results/` (doublons de S3).

## Ce qui marche / ce qui foire
- ✓ Dorado 2.0.0 + modèle V6.0.0 fonctionnent sur H100 PCIe (driver 580, CUDA 13)
- ✓ Mode simplex pipeline (basecall+align en 1 étape, 2 process) OK
- ✓ Retry-loop upload S3 fonctionne (tous UPLOAD OK 1ère tentative)
- ✓ 3 logs globaux archivés sur S3 (dont 1 auto via le nouveau code)
- ✓ Sort/index 16 CPU (au lieu de 4) — pas de problème de ressources

## Prochaine étape
Nettoyer `/scratch/results/` (319 GB de doublons S3) si besoin de place. Sinon, le projet est prêt pour un prochain batch (multiplex CGFL en V6.0.0, ou nouveaux samples HCL). Penser à lancer dans tmux la prochaine fois.
