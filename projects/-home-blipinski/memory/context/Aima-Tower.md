# Context — Aima-Tower — 2026-06-10T12:26:03+00:00

**Branche** : main
**Dernier commit** : bbeccca — docs(v4.4.0): Venn cohorte + best combos cliquables + Top N & filtres présence/absence
**Status** : clean (origin/main synchronisé ; .claude/worktrees/ untracked exclu)

## Où j'en suis
Session de polissage de la page /exploration-beta (Tower v4.4.0) : 6 features livrées, committées,
déployées (conteneur healthy) et poussées sur origin/main. En parallèle, étude de faisabilité du
redessin natif du PNG d'eval.R — verdict rendu, mise de côté à la demande de Boris.

## Ce qui marche / ce qui foire
- ✓ Venn composition cohorte (positifs 285 / négatifs 50 / suspects 24) + Total scoré dans la carte, 50/50 avec les conditions
- ✓ Best combos cliquables → charge le résultat ; Top N (5/10/20/50) + filtres présence/absence (backend token-safe `list_contains`, vérifié contre la DB : 0 fuite substring)
- ✓ CSV Résultat masque nb_healthy/nb_cancer
- ✓ Tout déployé (conteneur healthy) + poussé (bbeccca)
- ✗ Rendu visuel non vérifié par moi (aucun navigateur connecté au MCP Chrome, serveur headless) → à confirmer par F5 de Boris
- ⚠ Faisabilité redessin PNG : OUI via `scores.csv` (par-sample, déjà accessible mount RO), NON via `feature_runs.duckdb` seul (agrégats à 1 seuil only)

## Prochaine étape
Reprendre la faisabilité validée du **redessin natif du PNG** sensibilité/spécificité en Plotly : lire `scores.csv`,
répliquer `curve_for` (quantile type=1 ⟺ np `inverted_cdf`, grille 0.80–1.00, 5 strates × 2 modèles). Optionnel : auto-scroll vers Résultat au clic d'un combo.
