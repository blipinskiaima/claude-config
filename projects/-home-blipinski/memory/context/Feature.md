# Context — Feature — 2026-06-26T14:55:16+00:00

**Branche** : main
**Dernier commit** : 867e4f2 — docs(eval): README + CLAUDE.md — unité suspect + mvaf_v14 (2047 combos)
**Status** : clean (result/ régénéré, gitignoré ; untracked: "result backup/")

## Où j'en suis
Cohortes train régénérées après backfill trace-prod du champ `cohort` (32 healthy HCL
qui étaient `cohort=NULL` → désormais `Validation tech`, `speedvac=No`). Les 2 variantes
ont été re-run en tmux (feat_no/feat_yes), scores + KPIs à jour dans result/speedvac_{no,yes}/.

## Ce qui marche / ce qui foire
- ✓ Diagnostic : 192→224 H (speedvac_yes) venait du filtre `--cohort` (in_or_null n'ajoute
  IS NULL que si 'NULL' listé) qui excluait les 32 healthy cohort=NULL. Même classe de bug que le backfill précédent.
- ✓ Backfill validé : 32 H ajoutés, tous depth≥0.96 → 0 exclu par depth ⇒ 224 correct (pas 222).
- ✓ Re-run OK (DONE 08:52, 2047 combos × 12 unités, 0 erreur).
- ✓ Compo train vérifiée : no=82H+294C+24susp (376 lab) ; yes=224H+340C+25susp (564 lab).
  Cancer inclut Bladder_Blood (règle spéciale preset cohorte). Suspects côté éval (label NULL).
- ⚠ Aucun changement de code cette session (opérationnel : backfill + régen result/ gitignoré).
- ⚠ Train déterministe à cohorte constante (seed 42, nthread=1) MAIS suit trace-prod live ;
  +32 H ⇒ seuil recalé ⇒ KPIs déplacés (à comparer, notamment lung_I n=15 instable).

## Prochaine étape
Comparer les KPIs nouveau vs ancien run (impact des +32 healthy sur seuil & sensibilités),
en particulier le classement des combos sur lung_I (target 0.95, depth 0.25) — divergence
collègue à éclaircir (config XGBoost : R/Python, nthread, version, seed).
