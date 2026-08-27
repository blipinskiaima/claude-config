# Context — Aima-Tower — 2026-08-27 (clôture session)

**Branche** : main (poussé, origin/main = b45b14a)
**Dernier commit** : b45b14a — feat(reproductibilite): mVAF v1.5, seuils traces,
filtre de conformite QC
**Status** : clean (hors untracked `.claude/worktrees/` et `Exis 1.1.pdf`, hors scope
depuis le 24/07)

## Où j'en suis
Session entièrement sur `/reproductibilite`, en un seul commit, à partir de quatre
demandes successives de Boris : ajouter mVAF v1.5, rendre la coloration lisible,
afficher les zéros en échelle log, et filtrer sur la conformité QC. Prod rebuildée
et vérifiée à l'écran après chaque étape. Versions réalignées en 5.4.0.

## Ce qui marche / ce qui foire
- ✓ mVAF v1.5 sélectionnable. Seuil 0,0042 **reporté** de v1.4 (choix Boris), pas
  recalibré — la recette Exis donnerait 0,0025, écrit dans le code et la doc.
- ✓ Seuils tracés sur le graphe (`thresholds` accepte `s2: null`). Zéros posés sur
  un plancher en marqueur creux. Filtre QC qui recalcule les stats.
- ✓ La « diagonale » signalée par Boris = axe log allant à 1e-48, range retenu du
  rendu précédent. `autorange` ne suffit pas → range explicite.
- ✗ **Erreur de ma part corrigée en cours de route** : j'avais affirmé que Plotly
  attend du `log10` pour les `shapes` et que themelio était déjà cassé. C'est
  l'inverse — valeur brute, le code d'origine était juste. Mesuré sur le SVG.
  Leçon : j'ai théorisé longtemps avant d'aller regarder la page.
- ✗ Les 2 tests `test_exploratory_compute.py` restent rouges. **Inchangés depuis
  le 26/08**, non traités cette session : snapshots figés à 383 samples cancer
  contre 416 en base (+33). Dérive de données, arbitrage métier de Boris.
- ⚠ J'ai laissé un onglet ouvert sur son navigateur (tower.aima-diagnostics.com
  /reproductibilite) après l'avoir piloté pour diagnostiquer.
- ℹ Le filtre QC écarte 11 runs = exactement les 11 aliquots de QARA §2.5. À
  réutiliser comme argument de traçabilité si la question revient.

## Prochaine étape
Toujours la même qu'au 26/08, jamais traitée : trancher les 2 snapshots
`exploratory` — valider 416/374 comme nouvelle référence, ou comprendre pourquoi
la cohorte a gagné 33 samples cancer. Seule chose rouge du repo.
