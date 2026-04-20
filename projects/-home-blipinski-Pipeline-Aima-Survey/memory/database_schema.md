---
name: Database schema v6 (DuckDB)
description: Schéma DuckDB single-table multi-source de Aima-Survey, stratégie UPSERT avec COALESCE sur état utilisateur
type: project
originSessionId: 39895026-ccd6-4902-95d9-095b93ed61ed
---
## Table `articles` — source de vérité unique (refonte v6)

Fichier : `/home/blipinski/Pipeline/Aima-Survey/data/aima_survey.duckdb`

### PK composite multi-source

```
PRIMARY KEY (source, external_id)
```

- `source` : `pubmed` (défaut), puis `biorxiv`, `medrxiv`, `europepmc`, `manual` au fur et à mesure
- `external_id` : PMID pour PubMed, DOI ou slug pour preprints

**Why :** anticipation de l'ajout de sources futures (todo optimisation : évaluer MCPs NCBI/Ensembl/S3 vs scripts Python directs). Un seul refactor à payer maintenant plutôt qu'à chaque nouvelle source.

**How to apply :** ne jamais faire `WHERE pmid = ?` — toujours `WHERE source = ? AND external_id = ?`. Dans le code CLI et la doc, `PMID` reste synonyme de `external_id` quand `source='pubmed'` (rétrocompat ergonomique).

### Stratégie UPSERT

Lors d'un `fetch` PubMed (ou futur) :

- Métadonnées article (`title`, `abstract`, `authors`, `journal`, `pub_date`, `queries_matched`, `priority`) → **overwrite**
- `doi`, `url` → **COALESCE** (on préserve ce qu'on a si la nouvelle source n'en fournit pas)
- État utilisateur (`seen`, `bookmarked`, `note`) → **JAMAIS écrasé**
- Scoring IA (`score`, `score_why`, `score_tags`, `score_model`, `scored_at`) → **jamais touché par fetch** (mis à jour uniquement par `upsert_score`)
- Synthèse (`synthesis`, …) → **jamais touchée par fetch**
- `email_sent_at` → **jamais écrasé** (géré par `mark_email_sent` avec `COALESCE` sur la valeur existante)

**Why :** un re-fetch d'un article déjà lu/noté/scoré ne doit rien perdre. Boris peut poser un bookmark depuis Aima-Tower et relancer un `fetch` le lendemain sans rien casser.

**How to apply :** dans `lib/db.py`, la requête `_UPSERT_FETCH_SQL` ne mentionne QUE les colonnes métadonnées dans `DO UPDATE SET`. Ne jamais y ajouter `seen`, `score`, etc. Passer par les méthodes dédiées (`update_state`, `upsert_score`, `upsert_synthesis`, `mark_email_sent`).

### DuckDB piège : `CURRENT_TIMESTAMP` dans ON CONFLICT DO UPDATE SET

DuckDB 1.4.x interprète `CURRENT_TIMESTAMP` comme un nom de colonne dans une clause
`DO UPDATE SET` ou `UPDATE SET` → `Binder Error: Table "articles" does not have a
column named "CURRENT_TIMESTAMP"`.

**Workaround** : utiliser `now()` (fonction built-in) à la place. `DEFAULT CURRENT_TIMESTAMP`
reste OK dans le DDL CREATE TABLE.

**How to apply :** toujours `updated_at = now()` dans les SET — jamais `CURRENT_TIMESTAMP`.

### Méthodes publiques `DB`

| Méthode | Rôle |
|---|---|
| `init()` | DDL idempotent (table + 6 index) |
| `upsert_article(dict)` | Insert/update métadonnées, préserve user/scoring/synth/email |
| `upsert_score(src, eid, score, why, tags, model)` | UPDATE scoring uniquement |
| `update_state(src, eid, seen=?, bookmarked=?, note=?)` | UPDATE état utilisateur |
| `mark_email_sent(src, eid)` | `email_sent_at = COALESCE(email_sent_at, now())` |
| `upsert_synthesis(src, eid, synthesis, model)` | UPDATE synthèse Sonnet |
| `delete(src, eid) -> bool` | DELETE + `RETURNING` pour savoir si la ligne existait |
| `get(src, eid) -> dict \| None` | SELECT row, renvoie dict des colonnes |
| `query(sql, params) -> (cols, rows)` | SQL passthrough (pour CLI) |
| `stats() -> dict` | Compteurs globaux + `by_source` + `by_priority` |

### Usage

```python
from lib.db import DB

with DB() as db:
    db.init()
    db.upsert_article({"external_id": "40123456", "title": "...", ...})
    print(db.stats())
```
