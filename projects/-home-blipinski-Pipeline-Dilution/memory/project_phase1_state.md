---
name: project-phase1-state
description: "État du projet Dilution au 22 mai 2026 — Phase 1 validée, Phase 2 prête à lancer en 12 tmux"
metadata: 
  node_type: memory
  type: project
  originSessionId: 37da32d5-7cbd-4dc3-8643-5111d2fb4e16
---

Phase 1 (1 BAM A→Z) terminée et validée le 2026-05-22 :
- Output : `s3://aima-bam-data/processed/MRD/RetD/liquid/dilution/Colon_7_Healthy_807_target_1_0/BAM/`
- Spec : Colon_7 + Healthy_807 + target 1% (VAF effective 0.284%)
- Bam2Beta downstream OK : mVAF=0 (sous seuil) mais bedMethyl + raima_score produits → pipeline propre.
- 10 commits sur master, working tree clean, **pas de remote git** (local only).

**Why:** Sert de référence pour la Phase 2 — si un BAM dilué produit en Phase 2 a un comportement inattendu (mVAF, count, ratio modkit no-modbase-info), comparer avec ce BAM Phase 1 qui est connu OK.

**How to apply:**
- Si Boris revient sur le projet → la suite est : (a) cleanup workdirs partiels dans `/scratch/boris/dilution/Colon_7_Healthy_*_target_5_0/`, (b) re-lancer un tmux test (Colon_7 × 5_0 recommandé) pour valider le fix MM/ML (cf [[feedback-bash-pipefail-sigpipe]]).
- Tous les outils sont prêts : `./scripts/run_all.sh --help` liste les 12 commandes tmux.
- Cleanup cache `/scratch/boris/dilution-cache/` à faire UNIQUEMENT après les 12 tmux terminés.

Liens : [[reference-bam2beta-integration]] [[feedback-bash-pipefail-sigpipe]] [[feedback-manual-finish-pattern]]
