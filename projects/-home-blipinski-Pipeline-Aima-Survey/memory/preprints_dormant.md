---
name: Preprints biorxiv/medrxiv — dormant (leçons 2026-04-22)
description: Pourquoi `build_sources()` commente les sources preprint + ce qu'il faudrait revoir avant de réactiver
type: project
originSessionId: 0fc5d0c1-b5d3-48a1-ab0d-ba53c941f740
---
Support biorxiv/medrxiv ajouté puis désactivé en fin de session 2026-04-22. Code conservé, réactivable en décommentant 2 lignes dans `lib/sources/__init__.py:build_sources()`.

**Why** : le moteur de recherche web medrxiv.org/search (utilisé par `BiorxivSource`) retourne une **union très lâche** sur les queries OR-groupées. Sur la query `fragmentomics OR "fragment size" OR "fragmentation pattern" OR DELFI OR "end motif"` en medrxiv 14j, il retourne 50 DOIs dont **~49 sont du bruit** (obésité, Klebsiella, Seychelles warbler…) qui ne contiennent aucun keyword. Le filtre client-side `_matches_keywords` nettoie bien ces 49 cas mais **raterait le papier cible** si on filtrait juste sur le title (le papier Sauer a "fragmentomics" que dans son abstract, pas dans son titre).

**How to apply** :
- Ne PAS réactiver les sources preprint telles quelles — faux positifs massifs contre le vrai fichier Aima-Tower.
- Avant réactivation, refactor `search()` pour **1 recherche par keyword** (split OR → N searches mono-keyword → union dédupée). Le moteur medrxiv.org est précis sur un keyword seul (`fragmentomics` → 3 DOIs pertinents) mais chaotique sur les unions OR.
- L'API officielle `api.biorxiv.org` **est cassée** pour le nouveau préfixe DOI medRxiv `10.64898` (adopté 2025). Seul `api.medrxiv.org` répond — mais pas de fetch par DOI, uniquement fetch par fenêtre temporelle. D'où le choix du web scraping medrxiv.org/search comme solution.
- Performance actuelle : 1m30 par query (50 DOIs × 1 GET page). 7 queries = ~10 min. Acceptable pour cron daily mais pas pour itération dev.

**Fichiers** :
- `lib/sources/biorxiv.py` — web scraping implémenté (186 lignes + docstrings)
- `tests/test_biorxiv.py` — 16 tests verts (pagination, meta parsing, filtre keywords, match_scope institution)
- `queries.json` — 17 queries preprints (7 medrxiv + 10 biorxiv) calquées sur les 13 pubmed, avec champ `categories` (devenu noop) et `match_scope: "institution"` pour les competitive_affiliations
- `lib/fetcher.py` — transmet `categories` + `match_scope` aux sources preprints (4 lignes conditionnelles)

**Côté Tower** : changements **conservés** même avec preprints dormants car inoffensifs :
- `src/survey_service.py:392` : filtre `WHERE source='pubmed'` retiré (préparé pour multi-source quand on réactivera)
- `src/survey_render.py` : badge source (PubMed/bioRxiv/medRxiv), labels "Indexé/Publié" génériques
- `tests/test_survey_duckdb.py` : schéma stub aligné + assertions acceptent preprints
