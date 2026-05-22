# Context — Dilution — 2026-05-22T17:13+02:00

**Branche** : master
**Dernier commit** : 139f475 — Add README.md + CLAUDE.md
**Status** : clean

## Où j'en suis
Projet Dilution créé from scratch dans la session (génération 480 BAMs dilués in silico).
Phase 1 (1 BAM A→Z) ✓ validée end-to-end (BAM + Bam2Beta downstream OK). Phase 2 (479 BAMs
restants) tentée via 1 tmux mais ARRÊTÉE par Boris après que le worker a fail "MM:Z absent"
sur 4 jobs successifs (bug pipefail/SIGPIPE en command substitution — fix commité 30ff946).

## Ce qui marche / ce qui foire
- ✓ Phase 1 : `Colon_7_Healthy_807_target_1_0` sur S3, validé Bam2Beta (mVAF=0 sous seuil, normal à 1%)
- ✓ Worker `scripts/generate_dilution.sh` (cache flock + log S3 + -@ 2 threads) + run_all.sh
- ✓ Fix MM/ML check via fichier temp (commit 30ff946) — VÉRIFIÉ OK sur le BAM failed
- ✓ Cache `/scratch/boris/dilution-cache/` populé : Colon_7 + Healthy_807 (~11 Go)
- ✗ Workdirs partiels à nettoyer dans `/scratch/boris/dilution/Colon_7_Healthy_{756,780,807,823}_target_5_0/`
- ✗ Pas de remote git pour ce projet (local seulement)

## Prochaine étape
1. Cleanup workdirs partiels : `rm -rf /scratch/boris/dilution/Colon_7_Healthy_*_target_5_0/`
2. Re-lancer 1 tmux test pour valider le fix :
   `tmux new -d -s dil_colon_50 'cd ~/Pipeline/Dilution && ./scripts/run_all.sh --tumor Colon_7 --target 5_0; bash'`
3. Si OK → lancer les 11 autres tmux (cf `./scripts/run_all.sh --help`)
4. Après les 12 tmux finis → `rm -rf /scratch/boris/dilution-cache/`
