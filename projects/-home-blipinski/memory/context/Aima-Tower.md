# Context — Aima-Tower — 2026-10-02

**Branche** : main
**Dernier commit** : d7e39ab — docs(platform): README à jour et version 5.10.0
**Status** : propre (3 non suivis à laisser : `frontend/.apercu/`, `.claude/worktrees/`, `Exis 1.1.pdf`)

## Où j'en suis
Page Plateforme terminée et déployée en 5.10.0. Le menu déroulant de chaque analyse
affiche les 47 colonnes de l'onglet Platform (trace-platform `lib/gsheets.py`), en deux
côtés (résultats du pipeline / parcours), suivies de la frise de /indicator avec les
durées du sample. La colonne Analysis affiche le produit (EXIS, EXIS CUP, THEMELIO).

## Ce qui marche / ce qui foire
- ✓ Durées de la frise lues dans /api/indicator/data, sans recalcul (~3 s au premier dépliage).
- ✓ Vérif visuelle headless : playwright-core@1.47 (Node 18) dans le scratchpad + chromium_headless_shell-1223.
- ✗ Liste des 47 colonnes recopiée à la main : à resynchroniser si trace-platform enrichit l'export.
- ✗ Données : AIMA_010 a copy_start > copy_stop (segment Copy « — ») ; trace-workflow muet depuis le 15/08 (Input/Output S3 vides pour les samples récents).
- ✗ 2 tests test_exploratory_compute en échec, préexistants (snapshots /exploration).

## Prochaine étape
Rien en attente sur /database-platform. Restent ouverts : la panne trace-workflow
(depuis le 15/08) et le fil des compteurs sous les indicateurs clés de /indicator.
