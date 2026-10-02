# Context — Pod2Bam — 2026-10-01T16:18+00:00

**Branche** : main
**Dernier commit** : e2b7745 — Extend retrim Colon CGFL script to 5 runs with sync retry
**Status** : 8 fichiers modifiés/non suivis (préexistants à la session, non commités)

## Où j'en suis
Session analyse coût/temps Pod2Bam : extraction des perfs des 24 flowcells 4-plex multiplex V0.9.6_V5.0.0 (mars 2026) depuis les traces + logs globaux S3, puis deck CEO 10 slides livré dans `Bam2Beta/docs/Pod2Bam_cout_operationnel.pdf` (commit Bam2Beta 9b13bb6). Référence : H100-1-80G à €2,8665/h → 3h52 et €11,1 par flowcell (€2,78/sample), calcul seul hors Bam2Beta.

## Ce qui marche / ce qui foire
- ✓ Métriques de référence sauvées dans `memory/perf-multiplex-v5.md` (source, périmètre, machine, décisions)
- ✓ PDF généré sans install via chrome-headless-shell (`~/.cache/ms-playwright`)
- ✗ Repo local en retard : travail V6.0.0 (commit c60e998, Dockerfile.2.0.0, Pod2Bam.sh bi-mode) absent ici et du remote
- ✗ Sorties `demux/` + `align/` de mars absentes de S3 pour PBE25131 (seuls basecall/ + *_trimmed/ restent) — non investigué
- ✗ Aucun log de simplex V5.x disponible (BAM seuls dans data/HCL/liquid/)

## Prochaine étape
Décider du sort des modifs préexistantes non commitées (launch.sh, 3 TSV 3b1c780b, PLAN_ACTION_PROD.md, dev/*) et récupérer le travail V6.0.0 depuis l'instance GPU si elle existe encore.
