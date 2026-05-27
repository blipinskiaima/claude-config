# Context — Dilution — 2026-05-25T17:40+02:00

**Branche** : master
**Dernier commit** : 1c2314d — CLAUDE.md : généralise gotcha #3 (pipefail/SIGPIPE)
**Status** : clean

## Où j'en suis
Session de débogage du worker Phase 2 + audit complet. 3 fixes commités depuis le 22/05
(`e023058` upload size, `fa9ff27` seed tumor varie, `e3c38cb` @SQ check) + CLAUDE.md
gotcha #3 généralisé. Audit final : aucun risque destructif S3, 40 healthys + 3 tumors
paths vérifiés, 480 OUTPUT_NAME uniques. Boris a stoppé un run en cours par interruption.

## Ce qui marche / ce qui foire
- ✓ Worker robuste : 5 bugs fixés, plus aucun pattern `cmd | grep -q` ou `cmd | head` buggy
- ✓ Audit complet validé : no aws s3 rm/rb/mv/sync, sources S3 read-only par construction
- ✓ Design dilution clarifié : seed tumor varie par healthy_id → 40 réplicats indépendants,
  dilutions emboîtées par couple (tumor, healthy) à différents targets
- ✗ 5 workdirs partiels dans `/scratch/boris/dilution/` :
    - 3 Breast_34+Healthy_807 (target 5_0, 1_0, 0_5) → BAMs finaux VALIDES (failed sur le
      check @SQ buggy, fix dans e3c38cb)
    - 2 Lung_4+Healthy_780 (target 5_0, 1_0) → incomplets, à cleanup
- ✓ Cache scratch populé : 3 tumors + 7 healthys + lock files

## Prochaine étape
1. Décider entre (a) manual finish des 3 Breast valides (upload + manifest) ou
   (b) `rm -rf /scratch/boris/dilution/*` et relancer proprement avec le worker fixé.
2. Cleanup Lung_4+780 partiels dans tous les cas.
3. Relancer les 12 tmux (`./scripts/run_all.sh --help`).
4. Après les 12 tmux finis : `rm -rf /scratch/boris/dilution-cache/`.
