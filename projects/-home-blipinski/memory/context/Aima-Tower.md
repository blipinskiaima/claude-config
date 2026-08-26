# Context — Aima-Tower — 2026-08-26 (clôture session)

**Branche** : main (poussé, origin/main = 1017ff0)
**Dernier commit** : 1017ff0 — fix(ia): couche IA hors service (E2BIG) + durcissement /analytics
**Status** : clean (hors untracked `.claude/worktrees/` et `Exis 1.1.pdf`, hors scope
depuis le 24/07)

## Où j'en suis
Session de réparation, pas de feature. Partie d'un `/explore-projet` + une demande de tour
de la page `/analytics` : découvert que **toute la couche IA de la Tower était morte** —
`PIPELINE_CONTEXT` (164 Ko) passé dans un argument unique de `claude -p`, au-delà de
MAX_ARG_STRLEN (128 Ko). Corrigé, puis les 10 autres problèmes relevés sur la page, puis
un durcissement demandé par Boris pour rendre Draw with Aima Analyser générique.
Prod rebuildée en dernier (`--no-cache` puis rebuild simple), alignée sur main en 5.3.1.

## Ce qui marche / ce qui foire
- ✓ 4 endpoints qui renvoyaient 500 répondent : `/analytics/chat`, `/analytics/db-qa`,
  `/overview/database`, et la synthèse `/survey` (même `call_claude`).
- ✓ Vérifié en réel sur le conteneur, pas seulement en test : requête de la capture de
  Boris rejouée (figure OK, 25,8 s), boucle infinie tuée en 5,0 s, 0 zombie,
  `px.scatter(trendline="ols")` → 2 traces, 11 modules de l'allowlist importables.
- ✓ 120 tests passent, dont `tests/test_analytics.py` (18 nouveaux).
- ✓ `tests/test_dilution.py` échouait à la COLLECTE depuis juin et **bloquait toute la
  suite** — débloqué (4 des 5 classes testaient l'API supprimée par 80f6330).
- ✗ 2 tests `test_exploratory_compute.py` rouges : snapshots figés à 383 samples cancer
  contre 416 en base (+33). **Préexistant, vérifié par git stash** — dérive de données,
  le nouveau chiffre demande une validation métier de Boris.
- ⚠ `DeprecationWarning` sur `fork()` en Python 3.12 (process multi-thread). Inoffensif
  ici (le child ne fait que du calcul + une connexion DuckDB neuve), mais `fork` change
  de statut en 3.14.
- ⚠ Survey laissée en Sonnet : question posée à Boris (Opus sur les synthèses d'articles ?),
  restée sans réponse.
- ℹ Non traités, assumés : onglet « Avancé » d'`/analytics` (feature à construire, pas un
  bug), latence DB Q&A (2 appels IA en série, structurel), 5 660 lignes de Dash mort
  (`pages.py` + `callbacks.py`, gardées pour le rollback v2.3.0 — la dépendance est
  coupée, pas le code).

## Prochaine étape
Trancher les 2 snapshots `exploratory` : soit valider 416/374 comme nouvelle référence,
soit comprendre pourquoi la cohorte a gagné 33 samples cancer. C'est la seule chose rouge
du repo.
