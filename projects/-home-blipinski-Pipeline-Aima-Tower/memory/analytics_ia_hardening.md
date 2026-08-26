---
name: analytics-ia-hardening
description: "Panne E2BIG qui a tué toute la couche IA de la Tower, /overview Database mort depuis le cutover v3, et le durcissement de /analytics qui a suivi."
metadata:
  node_type: memory
  type: project
  modified: 2026-08-26T00:00:00.000Z
---

# Couche IA + /analytics — panne et durcissement (2026-08-26)

## La panne racine : E2BIG sur `--system-prompt`

`claude_cli.call_claude()` passait `system_prompt + PIPELINE_CONTEXT` (les 14 `CLAUDE.md`
de `~/Pipeline/*`, **164 382 octets**) dans **un seul argument** de `subprocess.run`.
Linux plafonne un argument à `MAX_ARG_STRLEN` = **131 072 octets** → `execve` échoue en
`OSError [Errno 7] Argument list too long`, le binaire `claude` n'est **jamais lancé**.

**Aucun code n'avait changé** : c'est la doc des projets qui a grossi jusqu'à franchir le
seuil (`trace-prod/CLAUDE.md` 60 Ko + `Aima-Tower/CLAUDE.md` 30 Ko = plus de la moitié).
Bascule mesurée au bit près : 131 071 octets passe, 131 072 échoue.

⚠ La panne touchait **les 5 callsites**, pas seulement `/analytics` : la synthèse IA de
`/survey` était morte aussi. `call_claude` est le point de passage unique — le tester,
c'est tester toute la couche IA.

⚠ Le `describe` de figure ([analytics.py:137]) était dans un `try/except: description = ""`
→ échec **silencieux**, l'utilisateur voyait une description vide, pas une erreur.

**Fix** : `--system-prompt-file <tmpfile>` (l'option existe bien — l'aide du CLI l'écrit
`--system-prompt[-file]`, un `grep "system-prompt-file"` la rate à cause des crochets).
L'argument tombe à ~16 octets, la limite devient inatteignable quelle que soit la taille
future des `CLAUDE.md`. Fichier supprimé dans un `finally`.

## /overview › Database était en 500 depuis le cutover v3

`backend/routers/overview.py` faisait `from pages import _get_visible_filter_columns`.
`pages.py` est le Dash legacy et importe `dash`, **absent de l'image v3** → 500 permanent,
jamais remarqué. Il pointait en plus vers `/home/blipinski/Pipeline/Aima-Tower-g/src`,
worktree supprimé en mai 2026.

**Fix** : bascule sur `filters_view.get_visible_filter_columns()`, copie strictement
identique mais sans dépendance Dash (le fichier existe précisément pour ça : *« helper
extrait de pages.py pour casser la dépendance Dash »*). Renvoie 118 colonnes / 4 sections.

⚠ Corollaire : l'affirmation « supprimer `pages.py` casserait `/overview` » est fausse —
`/overview` était **déjà** cassé. Mais `pages.py` reste conservé pour le rollback `v2.3.0`.

## Durcissement /analytics

- **Sous-processus tuable** (`_run_ai_code`, `_AI_CODE_TIMEOUT` = 60 s) pour le code généré
  par le LLM. `exec()` dans le thread de la requête **ne peut pas être interrompu** :
  ni `signal.alarm` (le thread FastAPI n'est pas le thread principal), ni un thread Python
  (non tuable). Seul un processus se termine. Vérifié : boucle infinie tuée en 5,0 s, zéro zombie.
- **Boucle d'auto-réparation** (`_AI_MAX_REPAIRS` = 1) sur les deux cartes : l'erreur exacte
  (exception Python ou erreur DuckDB) est réinjectée au modèle qui corrige. C'est **le** levier
  qui rend la page générique — les dépendances et l'allowlist ne couvrent que le prévu.
- **Deux modèles par nature de tâche** : `MODEL_HEAVY = claude-opus-5` là où le modèle **écrit**
  (code Python, SQL) ; `MODEL = claude-sonnet-4-6` pour la rédaction (describe, answer, Survey).
  `call_claude(..., model=...)` — ne pas revenir à une constante unique.
- ⚠ **`_AI_CODE_ALLOWED_TOP_MODULES` doit rester aligné avec `requirements.txt`** : autorisé
  mais non installé → échoue à l'exécution (cas vécu : `statsmodels`, requis en interne par
  `px.scatter(trendline="ols")`) ; installé mais hors allowlist → refusé avant de tourner.
- `run_db_qa` passe par `database_service._query()` (retry/backoff face aux locks du daemon)
  au lieu d'un `duckdb.connect` brut.
- `apiFetch` remonte le `detail` FastAPI au lieu du seul `statusText` — l'UI n'affichait que
  « Internal Server Error » sans la cause.

## Tests

`tests/test_analytics.py` (18 tests) verrouille les 3 régressions. `tests/test_dilution.py`
**échouait à la COLLECTE** depuis juin (`mvaf_threshold` supprimée par `80f6330`), ce qui
bloquait **toute** la suite pytest : 4 de ses 5 classes testaient l'API disparue
(`get_series`, `mvaf_threshold`, `backend.routers.dilution`), retirées, la 5ᵉ gardée verbatim.

⚠ 2 tests de `test_exploratory_compute.py` échouent, **et préexistaient** (vérifié par
`git stash`) : snapshots figés à 383 samples cancer contre 416 en base (+33). Dérive de
données, pas un bug — le nouveau chiffre demande une validation métier.

⚠ `DeprecationWarning` sur `fork()` en Python 3.12 (process multi-thread). Inoffensif ici,
mais `fork` change de statut en 3.14 — à retraiter lors d'une montée de version.

Voir aussi [[ia_cli_migration]], [[duckdb-patterns]].
