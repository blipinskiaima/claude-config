# Context — Aima-Tower — 2026-09-10 (clôture session)

**Branche** : main (poussé, origin/main = 0379bf9)
**Dernier commit** : 0379bf9 — feat(qara): vue d'ensemble, bandeaux produit
et toggle EN/FR — v5.5.0
**Status** : clean (hors untracked `.claude/worktrees/` et `Exis 1.1.pdf`,
hors scope depuis le 24/07)

## Où j'en suis
Session entière sur le **rendu** de `/qara`, à valeurs et périmètre inchangés
— `qara-data.ts` n'a pas été touché de la journée. Ajout d'une vue d'ensemble
(3 cartes, ordre Themelio · Exis · CUP), d'un bandeau de synthèse par produit
et d'un toggle EN/FR limité à l'habillage. Puis ~15 itérations de mise en page
pilotées par les commentaires de Boris sur un aperçu artifact publié
(`claude.ai/code/artifact/97e777e5…`), généré depuis les vrais composants via
`react-dom/server`. Terminé par une vérification complète contre le Google Doc.

## Ce qui marche / ce qui foire
- ✓ Vérification finale contre `Aima_QARA` relu en API (GET) : **143/143**
  valeurs affichées retrouvées onglet par onglet (Exis 60, Themelio 64, CUP 19),
  et les 3 matrices reproduisent exactement accuracy ET balanced accuracy
  publiées (36,8/30,0 · 47,4/42,5 · 90,4/72,9).
- ✓ `qara-ui.ts` ne contient **aucun littéral numérique** : ses chiffres sont
  lus dans `qara-data.ts`. Vérifié par grep.
- ✓ v5.5.0 alignée sur les 4 sources, Tower rebuildée, `healthy`, aucune erreur.
- ✗ **47 pourcentages calculés** dans les matrices CUP en mode « row % » (le
  défaut) : compte ÷ total de ligne, absents du texte du document. Les comptes
  sont validés, les pourcentages restent dérivés. Signalé à Boris, non corrigé.
- ✗ **4 seuils écrits en dur** dans `CupTab.tsx` (`mVAF v1.4 > 0`, `≥ 0.32`,
  `max_p < 0.826`, `≥ 0.826`) : conformes aujourd'hui, mais ils ne suivront pas
  une mise à jour de `CUP_STRATA`.
- ✗ Les 2 tests `test_exploratory_compute.py` restent rouges. **Inchangés depuis
  le 26/08**, non traités : snapshots figés à 383 samples cancer contre 416.
- ⚠ Piège de méthode : le contrôle « nombre affiché ∈ données » ne signalait que
  **4** valeurs manquantes — les 43 autres pourcentages calculés coïncident par
  hasard avec des nombres du fichier. Compter les cellules, pas les absents.
- ⚠ Ne pas rebuilder le container à chaque itération : `docker compose build`
  refait le build vite dans l'image, soit ~2× le cycle pour rien.

## Prochaine étape
Trancher les deux dérivations restantes de `/qara` : basculer le défaut des
matrices sur « counts » (ou assumer les 47 % calculés), et sourcer les 4 seuils
du schéma de gating depuis `CUP_STRATA`. Puis, toujours en suspens depuis le
26/08 : valider 416/374 comme nouvelle référence des snapshots `exploratory`,
ou comprendre les +33 samples cancer.
