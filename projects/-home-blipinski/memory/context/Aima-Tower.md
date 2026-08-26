# Context — Aima-Tower — 2026-08-26 (clôture session, 2e passe)

**Branche** : main (poussé, origin/main = 09d6a11)
**Dernier commit** : 09d6a11 — refactor(profil-aima): retirer toute comparaison chiffree nous/concurrents
**Status** : clean (hors untracked `.claude/worktrees/` et `Exis 1.1.pdf`, hors scope
depuis le 24/07)

## Où j'en suis
Longue session de réparation puis de nettoyage, en 3 commits. Partie d'un `/explore-projet`
et d'une demande de tour de `/analytics` : découvert que **toute la couche IA était morte**
(E2BIG sur le system prompt), réparée, puis durcie à la demande de Boris pour rendre
« Draw with Aima Analyser » générique quelle que soit la requête. Terminé par le retrait de
toute comparaison chiffrée nous/concurrents sur `/profil-aima`.
Prod rebuildée après chaque étape, alignée sur main en 5.3.2.

## Ce qui marche / ce qui foire
- ✓ `1017ff0` — couche IA : `--system-prompt-file`, sous-processus tuable, boucle
  d'auto-réparation, allowlist ↔ requirements, `/overview` sorti de `pages.py`.
- ✓ `f9ca7f7` — synthèse `/survey` en Opus 5 (vérifiée : 4 205 car. sur un article de
  méthylation cfDNA).
- ✓ `09d6a11` — `/profil-aima` sans comparaison chiffrée, 667 → 462 lignes, 8 composants
  orphelins supprimés. Vérifié dans le bundle réellement servi : les 10 libellés retirés
  sont absents, les 8 conservés présents.
- ✓ 5 endpoints qui renvoyaient 500 ce matin répondent tous. 120 tests passent.
- ✗ 2 tests `test_exploratory_compute.py` rouges : snapshots figés à 383 samples cancer
  contre 416 en base (+33). **Préexistant, vérifié par git stash** — dérive de données,
  le nouveau chiffre demande une validation métier de Boris.
- ⚠ `DeprecationWarning` sur `fork()` en Python 3.12. Inoffensif ici, mais `fork` change
  de statut en 3.14.
- ⚠ Boris n'a pas encore regardé le rendu de `/profil-aima` à l'écran. J'ai fait un choix
  au-delà de son énoncé : garder dans la fiche un tableau **descriptif du concurrent seul**
  (produit, cohorte, sensibilité, spécificité, contexte) plutôt que de le supprimer. Aucune
  de nos valeurs n'y figure. Question posée, restée sans réponse.
- ℹ Piège rencontré : `/profil-aima` (Profil AIMA) ≠ `/profils` (Deep dive concurrent).
  J'ai smoke-testé la mauvaise route avant de m'en apercevoir.
- ℹ Non traités, assumés : onglet « Avancé » d'`/analytics` (feature à construire), latence
  DB Q&A (2 appels IA en série, structurel), 5 660 lignes de Dash mort (gardées pour le
  rollback v2.3.0 — la dépendance est coupée, pas le code).

## Prochaine étape
Trancher les 2 snapshots `exploratory` : soit valider 416/374 comme nouvelle référence,
soit comprendre pourquoi la cohorte a gagné 33 samples cancer. C'est la seule chose rouge
du repo.
