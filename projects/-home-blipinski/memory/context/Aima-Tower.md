# Context — Aima-Tower — 2026-09-11 (clôture session)

**Branche** : main (poussée, origin/main = df7159a)
**Dernier commit** : df7159a — fix(charte): tuiles et échelle d'Exploration sur la grille d'état
**Status** : clean (hors untracked `.claude/worktrees/` et `Exis 1.1.pdf`, hors scope depuis le 24/07)

## Où j'en suis
Chantier terminé et **déployé** : la charte graphique du site officiel
(preview.aima-diagnostics.com) est appliquée à toute la Tour, en **v5.6.0**.
Quatre checkpoints validés par Boris (accès et outils → charte extraite en tokens →
rendu QARA côte à côte → plan de déclinaison), puis trois phases d'exécution.
Le conteneur tourne avec la charte **et** le correctif trace-prod v34 de la session
parallèle, mergé sans conflit. Comportement, données et routes inchangés.

## Ce qui marche / ce qui foire
- ✓ Conteneur reconstruit et vérifié en ligne : santé 200, `/api/samples` 200,
  API en 5.6.0, logos servis, QARA / Échantillons / Exploration / Reproductibilité
  capturés avec données, zéro erreur console.
- ✓ Couche de tokens dans `frontend/src/index.css` : les anciens noms de palette et les
  193 classes Tailwind nommées sont en **alias**, donc aucun composant n'a été édité
  pour changer de couleur. Diff confiné aux styles.
- ✓ Tests : 138 passent. Les 2 échecs restants sont les snapshots `exploratory`
  **préexistants** (383 vs 416 samples cancer), sans lien avec la charte.
- ✗ **Un alias ne porte pas le sens de la couleur remplacée** : la tuile « Spécificité AI »
  et le palier 60-80 % d'`/exploration` sortaient en magenta (= alerte) pour de bonnes
  valeurs. Vu seulement **en ligne avec données**, corrigé en df7159a. D'autres endroits
  où l'ancien violet codait un état peuvent rester à relire.
- ✗ Le bandeau de `/sample/:id` affiche encore « Aima Tower · v4.2 · ISO 15189-ready »
  (texte hérité du mockup, jamais relié à la version réelle).
- ⚠ La section « Structure » du README décrit encore l'arbo Dash v2 (`src/pages.py`,
  `callbacks.py`, `assets/`) et ignore tout le frontend React. Obsolète **avant** cette
  session, signalée, non corrigée.
- ⚠ `MEMORY.md` fait 28 Ko pour une limite de 24,4 Ko : une partie n'est pas chargée au
  démarrage. Les entrées d'index sont trop longues, à consolider.

## Prochaine étape
Trancher les deux restes cosmétiques : la mention de version en dur du bandeau
`/sample/:id`, et la relecture des derniers endroits où l'alias violet → magenta fait
passer une valeur normale pour une alerte (chercher `--aima-violet-` dans `Qualite.tsx`
et `AimaComparaison.tsx`). Puis, toujours en suspens depuis le 26/08 : valider 416/374
comme nouvelle référence des snapshots `exploratory`, ou comprendre les +33 samples.
