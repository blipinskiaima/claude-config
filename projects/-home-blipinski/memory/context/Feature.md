# Context — Feature — 2026-06-26T07:50:53+00:00

**Branche** : main
**Dernier commit** : 867e4f2 — docs(eval): README + CLAUDE.md — unité suspect + mvaf_v14 (2047 combos)
**Status** : clean (seul `result backup/` non tracké, intact — artefact local)

## Où j'en suis
Feature "unité d'éval suspect" (imageries suspectes) TERMINÉE et déployée sur 2 repos,
poussée. Dev 1 Feature (flag --include-suspicious) + Dev 2 Aima-Tower (onglet Suspects,
dotplot). Stack Tower redémarrée (docker), healthy. mvaf_v14 (11e feature) aussi intégrée
cette session.

## Ce qui marche / ce qui foire
- ✓ Feature : 25 suspects (unit='suspect', label NULL) dans result/speedvac_{no,yes}/scores.csv
- ✓ Additivité PROUVÉE 2 variantes : eval_kpis byte-identique, scores existants 0 diff (yes 699×2047, no 511×2047)
- ✓ Tower : pytest test_suspect 4/4, tsc 0 erreur, npm build OK, endpoint live → 25 pts / 6 au-dessus du seuil
- ✓ train.R / eval.R / feature_service / feature_curves / EVAL_UNITS INCHANGÉS (suspect hors-KPI comme dilution)
- ✓ Push OK : Feature 867e4f2, Aima-Tower 040e515
- ⚠ Vérif visuelle onglet "Suspects" par Boris non encore confirmée (stack ouverte sur /combined)

## Prochaine étape
Boris confirme le rendu visuel de l'onglet "Suspects" (dotplot + seuil + compteur N/25).
Si ajustement souhaité : couleurs/jitter/taille des points dans SuspectChart.tsx.
