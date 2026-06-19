# Context — Aima-Tower — 2026-06-19T12:11:15+00:00

**Branche** : main (synchro origin/main)
**Dernier commit** : 8a7e067 — docs(dilution): documente /dilution (README v4.6.0 + table Pages CLAUDE.md)
**Status** : 6 fichiers modifiés non commités (WIP exploration-beta, PAS de cette session)

## Où j'en suis
Feature **page `/dilution`** entièrement livrée cette session (V1 en 8 tâches TDD + sélecteur
statistique mVAF / mVAF v1.3), **déployée en prod** (conteneur healthy), **pushée** (12 commits
`c1cf97f`→`964b379` + doc `8a7e067`) et documentée (README/CLAUDE.md/mémoire). Rien en cours sur
dilution. Le **WIP exploration-beta** (6 fichiers) reste non commité — c'est le travail antérieur à reprendre.

## Ce qui marche / ce qui foire
- ✓ `/dilution` live : 2 panneaux Twist (principale/Rep2), axe X d1..d8+Diluant parsé depuis sample_name, d8 principale KO → trou
- ✓ Sélecteur stat mVAF (`mvaf_v1`) / mVAF v1.3 (`mvaf_v13`, texte virgule parsé) + toggle spécificité 95/98/99 %, seuil `quantile_type1` speedvac_yes recalculé par stat (v1 0.9916 / v1.3 0.9904 @98 %)
- ✓ 17/17 tests `test_dilution.py` verts, build front OK, smoke endpoint v1/v1.3 confirmé en conteneur
- ✓ `mvaf_threshold` placé dans `dilution_service.py` (jamais touché feature_service.py = WIP)
- ✗ 7 tests `test_exploratory_compute` échouent = **dérive de snapshot pré-existante** (N_Cancer 298→371, trace-prod a grossi), sans lien avec dilution → à recalibrer un jour
- ⚠ WIP exploration-beta (6 fichiers : feature_curves/feature_service + 4 front) toujours non commité

## Prochaine étape
Reprendre le **WIP exploration-beta** : vérif visuelle des courbes Plotly sur quelques combos bench (cohortes speedvac), puis commit. (Optionnel : recalibrer les snapshots `test_exploratory_compute`.)
