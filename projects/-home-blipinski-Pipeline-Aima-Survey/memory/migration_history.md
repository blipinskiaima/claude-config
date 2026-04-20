---
name: Migration v5 → v6 (consolidation 4 sources → DuckDB)
description: Mapping des 4 anciennes sources vers aima_survey.duckdb, piège de la clé title NOT NULL, résultat smoke live
type: project
originSessionId: 39895026-ccd6-4902-95d9-095b93ed61ed
---
## Migration one-shot

Commande : `python3 cli.py migrate`
Module : `lib/migrate.py`

### Les 4 sources consolidées

| Source | Chemin | Contenu | Devient |
|---|---|---|---|
| SQLite `scores` | `data/scoring_cache.db` | pmid, score, why, tags, model, scored_at | colonnes `score*` de `articles` |
| SQLite `sent_articles` | `data/scoring_cache.db` | pmid, first_sent_at | `email_sent_at` |
| JSON `survey_seen.json` | `Aima-Tower/data/` | `{"seen_pmids": [pmid, …]}` | `seen=TRUE` + `seen_at` |
| JSON `survey_bookmarks.json` | `Aima-Tower/data/` | `{pmid: {ts, note, article: {title, abstract, …}}}` | `bookmarked=TRUE` + `note` + hydrate l'article complet |

### Ordre d'import (pour maximiser l'hydratation)

1. **Bookmarks en premier** : ce sont les seuls qui contiennent les métadonnées complètes (title, abstract, authors, journal, pub_date). Les PMIDs bookmarkés héritent d'articles bien renseignés.
2. **Scores ensuite** : crée un stub si PMID absent, puis `upsert_score`. Les PMIDs bookmarkés conservent leurs vraies métadonnées.
3. **sent_articles** : stub si absent + `mark_email_sent`.
4. **seen_pmids** : stub si absent + `update_state(seen=True)`.

### Piège : `title NOT NULL`

La table `articles` impose `title NOT NULL`. Les PMIDs venant seulement de `scores` ou `seen_pmids` n'ont pas de titre. **Stratégie** : stub de la forme `"(Migrated stub) pubmed:{pmid}"`. Un `fetch` PubMed ultérieur (étape 4) réécrira ce titre sans toucher au score/seen/bookmarked (cf. UPSERT COALESCE dans `database_schema.md`).

**How to apply :** en étape 4, lancer `cli.py fetch --days N` sur les PMIDs déjà migrés enrichira les stubs. Pas de perte d'état.

### Idempotence

Vérifiée : 2 runs consécutifs → même total d'articles, mêmes compteurs `seen`/`bookmarked`/`emailed`.

Mécanismes :
- `upsert_article` sur PK composite → UPSERT, pas de doublon
- `upsert_score`, `update_state` → UPDATE idempotent
- `mark_email_sent` → `COALESCE(email_sent_at, now())` ne réécrit pas un timestamp existant

**How to apply :** `migrate` peut être relancé sans risque. Utile si les JSON Tower sont mis à jour après la première migration.

### Résultat smoke live (2026-04-20)

- bookmarks hydratés : 3
- scores importés : 29
- sent_articles → `email_sent_at` : 29
- seen_pmids : 46
- **Total articles uniques : 49** (cohérent avec la dédup cross-source)

Pub_date min/max = 2026-04-07 / 2026-04-15 (viennent des bookmarks uniquement, les stubs ont `pub_date=NULL`).
