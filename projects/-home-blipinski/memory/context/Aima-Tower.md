# Context — Aima-Tower — 2026-08-26 (clôture session)

**Branche** : main (poussé, origin/main = 35caa2f)
**Dernier commit** : 35caa2f — feat(qara): page QARA — onglets Exis 1.1, Themelio 1.0 et CUP 1.0
**Status** : clean (hors untracked `.claude/worktrees/` et `Exis 1.1.pdf`, hors scope
depuis le 24/07)

## Où j'en suis
Session close via /end-session. Une seule feature livrée et déployée : la page QARA
(`/qara`, entrée sidebar sous Tableau de bord) et ses 3 onglets Exis 1.1 / Themelio 1.0
/ CUP 1.0, qui restituent les sections de performance du Google Doc `Aima_QARA`.
La prod a été rebuildée en dernier, elle est alignée sur main (API en 5.3.0).

En début de session, Boris a redirigé une tentative de lecture du Doc via
claude-in-chrome vers le pattern API du skill /qara-tower — ce chemin est désormais
consigné en mémoire ([[google_docs_api_read_access]]).

## Ce qui marche / ce qui foire
- ✓ 3 onglets déployés. tsc 0, build 0, docker build 0, conteneur healthy,
  `/qara` → 200, les 5 chaînes marqueuses présentes dans le bundle servi.
- ✓ Fidélité vérifiée mécaniquement : 42 contrôles verts (30 valeurs + phrases
  verbatim vs le doc, 12 sur les matrices de confusion transcrites de l'image —
  elles reproduisent exactement les accuracies ET balanced accuracies publiées).
- ⚠ Divergence prouvée dans le document CUP : les tableaux §4/§5 donnent
  medium = 94 / high = 95, la figure et la phrase de conclusion du §5 l'inverse.
  Seuls 95/94 reproduisent les % publiés (45/95 = 47,4 % ; 85/94 = 90,4 %).
  Rendu verbatim + encart, aucune valeur corrigée — décision Boris.
  **C'est le document qui reste à corriger, côté Google Doc.**
- ⚠ Piège consigné : jamais dériver une valeur sur cette page. J'avais reconstitué
  un numérateur depuis un pourcentage pour les barres CUP → supprimé.
- ✗ tests/test_dilution.py échoue toujours à la COLLECTE :
  `ImportError: cannot import name 'mvaf_threshold' from 'dilution_service'`.
  Panne PRÉ-EXISTANTE (déjà là le 12/08), non traitée cette session non plus —
  elle masque tout le module de tests dilution.
- ℹ Non vérifié faute d'outil : le rendu de `/qara` en thème sombre. Je n'utilise
  que des variables `--aima-*`, donc il devrait suivre, mais je ne l'ai pas constaté
  (impossible de piloter le toggle en headless). `--aima-amber-600` est le seul
  risque connu (ReproStatsTable lui préfère amber-400 en sombre).

## Prochaine étape
Deux candidates, au choix :
1. Réparer tests/test_dilution.py — seule chose cassée du repo, elle masque un module
   entier. Vérifier ce qu'est devenu `mvaf_threshold` (probablement supprimé lors du
   passage de l'onglet Dilution à l'archi α, cf. combined_dilution_tab.md).
2. Ouvrir `/qara` en thème sombre et corriger si `--aima-amber-600` passe mal.
