---
name: project-phase1-state
description: "État du projet Dilution au 25 mai 2026 — Phase 1 validée, worker stable (5 fixes), Phase 2 prête à lancer en 12 tmux"
metadata:
  node_type: memory
  type: project
  originSessionId: 37da32d5-7cbd-4dc3-8643-5111d2fb4e16
---

Phase 1 (1 BAM A→Z) terminée et validée le 2026-05-22 :
- Output : `s3://aima-bam-data/processed/MRD/RetD/liquid/dilution/Colon_7_Healthy_807_target_1_0/BAM/`
- Spec : Colon_7 + Healthy_807 + target 1% (VAF effective 0.284%)
- Bam2Beta downstream OK : mVAF=0 (sous seuil) mais bedMethyl + raima_score produits → pipeline propre.
- 13 commits sur master, working tree clean, **pas de remote git** (local only).

5 fixes du worker accumulés (tous nécessaires pour Phase 2 robuste) :
1. `e39a60e` — MM/ML check initial + `-@ 2` threads samtools + `--no-progress` sur aws s3 cp
2. `30ff946` — MM/ML check via fichier temp (bug SIGPIPE/pipefail dans `$(... | head ...)`)
3. `e023058` — aws s3 ls filter par basename exact (le ls fait un prefix match qui renvoie aussi .bai)
4. `fa9ff27` — Seed tumor varie par healthy_id : SEED_TUMOR = 42 + healthy_id → 40 réplicats tumoraux indépendants (au lieu d'un même set de reads tumoraux partagé pour les 40 jobs)
5. `e3c38cb` — @SQ header check via capture en variable + test bash pur (même bug que MM/ML : `samtools view -H | grep -q`)

**Design des dilutions** (clarifié 2026-05-25) :
- Pour un même couple `(tumor, healthy)`, les 4 BAMs aux 4 targets sont des dilutions emboîtées (samtools --subsample à seed fixe = sous-ensembles déterministes).
- Pour un même tumor à un target donné, les 40 réplicats (1 par healthy) utilisent des sets tumoraux différents (seed varie par healthy_id depuis fa9ff27) → variance statistique combinée tumor + healthy.

**Why:** Sert de référence pour la Phase 2 — si un BAM dilué produit en Phase 2 a un comportement inattendu (mVAF, count, ratio modkit no-modbase-info), comparer avec ce BAM Phase 1 qui est connu OK.

**How to apply:**
- Si Boris revient sur le projet → audit complet du script déjà fait le 2026-05-25 : aucun risque destructif S3, configs OK (40 healthys + 3 tumors paths vérifiés), 480 OUTPUT_NAME uniques, plus de pattern `... | grep -q ...` buggy restant.
- État scratch au 2026-05-25 : cache populé (3 tumors + 7 healthys + lock files), 5 workdirs partiels dans `/scratch/boris/dilution/` (3 Breast_34+807 avec BAMs valides + 2 Lung_4+780 incomplets) — peuvent être manual finish ou cleané.
- Tous les outils sont prêts : `./scripts/run_all.sh --help` liste les 12 commandes tmux.
- Cleanup cache `/scratch/boris/dilution-cache/` à faire UNIQUEMENT après les 12 tmux terminés.

Liens : [[reference-bam2beta-integration]] [[feedback-bash-pipefail-sigpipe]] [[feedback-manual-finish-pattern]]
