---
name: Intégration DuckDB Aima-Survey (v6)
description: Lecture de aima_survey.duckdb depuis Aima-Tower pour les vues month/all, pattern ATTACH READ_ONLY retry, traduction queries
type: project
---

## Depuis 2026-04-20 : vues `month` et `all` lisent DuckDB

### Contexte

La refonte Aima-Survey v6 a créé une source unique `~/Pipeline/Aima-Survey/data/aima_survey.duckdb` (table `articles` multi-source, PK composite `(source, external_id)`). Aima-Tower `/survey` consomme cette DB pour les vues temporelles étendues.

### Ce qui a changé côté Tower

- `src/config.py` : +2 settings `aima_survey_db_path` et `aima_survey_queries_path` (pattern `_docker_or_local` existant)
- `docker-compose.yml` : mount `${SURVEY_PATH}:/aima-survey` (sans :ro pour les .lock DuckDB, comme trace-platform / trace-workflow). Le sous-path `/aima-survey/reports` reste accessible.
- `src/survey_service.py` : +2 méthodes publiques `get_month_articles_deduped()` et `get_all_articles_deduped()`. Helper `_articles_from_duckdb(where_sql, limit)` avec retry backoff 5x (pattern identique au `DuckDBMixin._query` des autres services).
- `src/pages.py` : RadioItems `survey-mode` étendu de 2 à 4 valeurs, défaut `week`
- `src/callbacks.py` + `src/survey_render.py` : routent vers les nouvelles méthodes selon `mode`

### Contrat de lecture

**Why :** La table `articles` stocke `queries_matched` en CSV de names machine (`cancer_detection_cfDNA`), alors que `RUBRIQUE_SHORT_LABELS` et les onglets UI attendent des descriptions humaines (`Detection cancer par methylation cfDNA`). Traduction au mapping load via `_QUERIES_NAME_TO_DESC` lu depuis `queries.json` (mount Docker).

**How to apply :**
- Si `queries.json` change : le mapping est chargé au module load → nécessite restart Aima-Tower (`docker compose restart`).
- Un name absent de `queries.json` est laissé tel quel (fallback gracieux).
- Day/Week restent sur les markdowns → aucune régression possible de ce côté.

### Sémantique des vues temporelles

| Mode | Filtre SQL / source |
|---|---|
| day | rapport markdown d'une date précise |
| week | 7 derniers rapports markdown (dédup par PMID) |
| month | `pub_date >= today-30d OR first_seen_at >= now()-30d` (DuckDB) |
| all | pas de filtre temporel, LIMIT 2000 (DuckDB) |

Le OR `first_seen_at` dans `month` couvre les articles indexés en retard par PubMed et les backfills récents : un article publié il y a 2 mois mais fetché cette semaine apparaît dans "Mois".

### Fallback

Si `aima_survey.duckdb` est inaccessible (fichier absent, `IOException` après 5 retries avec backoff 500ms→4s) :
- `month` → 30 derniers markdowns dédupliqués (approx, dépend des .md présents)
- `all` → tous les markdowns dédupliqués

**Pas de crash UI, pas d'alerte visuelle** (V1 — à ajouter si Boris le veut en phase suivante).

### Lock DuckDB

Concurrence : `Aima-Survey/veille.py` (cron 8h/lundi 8h05) écrit pendant que Tower peut lire. Pattern retry 5x avec backoff géré dans `_articles_from_duckdb`. Tower n'ouvre QUE en `read_only=True`.

### Tests

`tests/test_survey_duckdb.py` : 7 tests verts (lecture DuckDB, exclusion des sources non-pubmed, tri, traduction queries, fallback markdown, vues day/week intactes).

### Changement éventuel à anticiper

Si une 2e source devient active dans Aima-Survey (bioRxiv, EuropePMC…), la requête actuelle `WHERE source='pubmed'` exclut les autres. **À revoir** quand Boris activera une nouvelle source : soit retirer le filtre, soit ajouter un nouveau RadioItem "Source".
