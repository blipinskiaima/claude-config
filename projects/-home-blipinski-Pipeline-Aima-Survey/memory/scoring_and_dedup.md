---
name: Scoring IA et dédup cross-jours (v6)
description: Mécanisme scoring Claude Haiku 4.5 sur DuckDB + anti-spam email via colonne email_sent_at
type: project
originSessionId: 39895026-ccd6-4902-95d9-095b93ed61ed
---
## Refonte v6 (2026-04-20)

**OBSOLÈTE** : l'ancienne DB `data/scoring_cache.db` (SQLite avec 2 tables `scores` + `sent_articles`). Remplacée par la table `articles` de `data/aima_survey.duckdb`.

### Scoring

- Module : `lib/scorer.py` (plus `scorer.py` à la racine, supprimé)
- Modèle : `claude-haiku-4-5` (prompt système inchangé depuis v4)
- Cache : `WHERE score IS NULL` — un article scoré reste scoré (sauf `cli.py score --force`)
- Les scores migrés depuis l'ancien SQLite ont été réinjectés via `cli.py migrate`

### Anti-spam email

- Colonne `email_sent_at` (TIMESTAMP, NULL par défaut) sur la table `articles`
- `db.mark_email_sent(src, eid)` utilise `COALESCE(email_sent_at, now())` pour ne JAMAIS écraser un timestamp existant → idempotent par construction
- Le nouveau `veille.py` filtre `email_sent_at IS NULL` uniquement si `--email` est passé

**Why :** L'UPSERT d'un article via `upsert_article` préserve `email_sent_at` (cf. `database_schema.md`). Donc re-fetcher un article déjà envoyé ne le renverra pas.

**How to apply :**
- Reset dédup d'un article : `python3 cli.py query "UPDATE articles SET email_sent_at = NULL WHERE external_id = 'XXX'"` (nécessite mode write — utiliser l'API Python directement).
- Claude Haiku wrappe parfois sa réponse en `\`\`\`json ... \`\`\`` : `lib/scorer.py::score_one` strip les fences avant `json.loads`.
- Tri final des articles pour le render : priorité asc > score desc (NULLs en fin) > pub_date desc.
