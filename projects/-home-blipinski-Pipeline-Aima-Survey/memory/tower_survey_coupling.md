---
name: couplage-r-el-aima-tower-aima-survey
description: "Tower lit la DuckDB en read-only, toutes ses vues (pas seulement month/all) lisent la DB, et son seen/bookmark vit dans des JSON séparés"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2cf74f69-f6e5-4e35-926d-561f28925c84
  modified: 2026-07-22T16:10:28.891Z
---

Cartographié le 2026-07-22. **Corrige plusieurs affirmations obsolètes de la doc.**

## Ce qui est vrai

- **Tower n'écrit JAMAIS dans `aima_survey.duckdb`.** Aucun INSERT/UPDATE dans tout le repo.
  Connexions **read-only**, ouvertes et fermées à chaque requête, avec sa propre boucle de
  retry (5 tentatives, backoff jusqu'à 4 s). Côté Survey, le cron n'ouvre jamais de connexion
  longue → risque de lock à 8h00 réellement mitigé.
- **Le seen/bookmark/note de Tower vit dans des fichiers JSON séparés**
  (`survey_seen.json`, `survey_bookmarks.json`), pas en DB. Les colonnes `seen`, `bookmarked`,
  `note` de DuckDB sont **mortes des deux côtés** : `update_state()` existe dans `lib/db.py`
  mais rien ne l'appelle. D'où `seen=46` / `bookmarked=3` figés depuis la migration d'avril.
- Tower lit **17 colonnes en dur**, dont `first_seen_at`, `score`, `sector`, `org_type`,
  `org_name`. Renommer ou supprimer une colonne côté Survey **fait crasher Tower sans
  fallback** (son `except` ne rattrape que les erreurs d'I/O, pas une `BinderException`).

## Ce qui est FAUX dans la doc (CLAUDE.md des deux projets)

❌ « day/week parsent les rapports markdown, month/all lisent la DB »
→ **Faux depuis le 2026-04-22** : un commit a migré *toutes* les vues sur DuckDB. Le parsing
markdown par regex n'est plus qu'un **fallback de secours** si la DB est inaccessible.

Le format markdown de `lib/render.py` reste à préserver (c'est le filet), mais la contrainte
« ne jamais y toucher » est moins bloquante qu'annoncée.

Un test de Tower nommé `test_day_and_week_views_untouched` documente encore l'ancien
comportement dans sa docstring tout en ne vérifiant que l'existence des méthodes — test-fantôme.

## Autres points

- ~500 lignes de Dash legacy (`src/app.py`, `pages.py`, `callbacks.py`, `survey_render.py`)
  référencent encore `survey_service` alors que la prod tourne sur FastAPI + React.
- La synthesis IA est générée à la volée en **cache RAM**, jamais persistée (les colonnes
  `synthesis*` de la DB ne sont écrites par personne).

**How to apply :** avant de toucher au schéma DuckDB, vérifier le SELECT de Tower. Avant de
citer la répartition markdown/DB des vues, relire le code — la doc ment. Voir aussi
[[entrez_date_bug]] : Tower trie sur `first_seen_at`, que ce bug corrompt.
