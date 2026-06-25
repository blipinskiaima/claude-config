# Context — Bam2Beta — 2026-06-25T13:07:44+0000

**Branche** : main
**Dernier commit** : 5d6e1b0 — feat(mvaf): score mVAF v1.4 = mean(sqrt(bootstrap_scores))^2 (R&D)
**Status** : clean (seul dev/SCW/bacasable.sh untracked, sandbox)

## Où j'en suis
Feature **mVAF v1.4** committée et pushée (R&D, NON qualifiée). `mean(sqrt(scores))²`
sur les 200 scores bootstrap, 2 flux : `--bootstrap` (file 1 → 3 sorties scores+props+V1.4)
et `--MVAF1_4` rétrospectif (file 2 `bootstrap_trasnfo.R`, transfo seule). Aucune tâche en cours.

## Ce qui marche / ce qui foire
- ✓ Vérif statique : R parse OK ×2, bloc transfo bit-à-bit identique entre file 1 et file 2, zéro orphelin MVAF1_3/Raima_score_v1_3
- ✓ Renommage `--MVAF1_3` → `--MVAF1_4` (ancien rétrospectif v1.3 supprimé), import swap, param config
- ✓ file 2 = container défaut bam2beta (R base, pas de raima) ; file 1 = raima:0.5.3, option `--id`
- ✗ **Gate bit-à-bit SORTIE 1 NON faite** : `rowSums(props 4 cancers)` vs ancien appel direct `.bootstrap_v1.tsv` — à valider sur un vrai run `--bootstrap`
- ⚠️ Boris a **reverté** mes fixes (guard `needs_bam`, filtre `.exists()`, param `--exclude`) → `main.nf` garde BAM_FILE inconditionnel + MVAF1_4 en `checkIfExists` strict. Glob-all rétrospectif plante si un sample n'a pas son merged.bam → lancer par sample / s'assurer du merged.bam. NE PAS re-proposer ces fixes.

## Prochaine étape
Lancer un vrai run `--bootstrap` (depuis ~/Run) pour valider la gate bit-à-bit SORTIE 1 + vérifier que `raima:0.5.3` est buildé avec `bootstrap_model_v1` exporté. Puis, si OK, qualification/montée en version.
