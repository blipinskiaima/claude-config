---
name: Survey — vues temporelles pilotees par first_seen_at
description: Refonte des filtres temporels Survey autour de `first_seen_at` = EDAT PubMed (2026-04-22)
type: project
originSessionId: 03964086-3177-42f8-b0e9-9c017f24ad77
---
# Vues temporelles Survey — `first_seen_at` comme pivot (2026-04-22)

## Problème résolu

Les vues Week/Month/Year de `/survey` filtraient sur `pub_date` (date de parution journal). Deux bugs :
1. **Dates futures** : PubMed renvoie parfois `pub_date = 2026-12-01` pour des articles en "epub ahead of print" d'un numéro de revue futur. Ces articles passaient le filtre `pub_date >= NOW - 7 DAY` car `2026-12-01 >= today`.
2. **Indexation tardive** : un article *découvert* récemment par le cron mais *publié* il y a 6 mois n'apparaissait pas dans Week/Month (pub_date > 30 jours).

## Solution

**Pivot = `first_seen_at`** (= `entrez_date` PubMed EDAT, alimenté par Aima-Survey). Propriétés :
- **Immuable** (PubMed ne re-indexe pas)
- **Jamais dans le futur** (c'est la date d'ajout à NCBI)
- **Stable cross-fetch** (cohérent entre machines et re-runs)

## Changements

### Aima-Tower (`src/survey_service.py`)

- `Article.first_seen: Optional[str]` (nouveau champ)
- `_row_to_article()` mappe `first_seen_at` → `first_seen`
- `get_week/month/year_articles_deduped()` : WHERE = `first_seen_at >= CURRENT_DATE - INTERVAL X DAY`
- `get_day_articles(date_str)` (nouveau) : `DATE(first_seen_at) = ?`
- `list_first_seen_dates()` (nouveau) : `SELECT DISTINCT DATE(first_seen_at) ... ORDER BY d DESC` pour peupler le date picker Jour

### Aima-Tower (`src/survey_render.py`)

Card article affiche 2 lignes distinctes :
- `Indexé : 2026-04-20` (= first_seen)
- `Publié : 2024-11-05` (= date/pub_date)

### Aima-Survey (`lib/db.py`, `lib/sources/pubmed.py`)

- Colonne `entrez_date DATE` (migration idempotente)
- Parser XML extrait `PubmedPubDate[@PubStatus="entrez"]`
- `upsert_article()` set `first_seen_at = entrez_date` au premier INSERT
- `entrez_date` omis du `ON CONFLICT DO UPDATE` (immutable, jamais modifié après l'insert initial)
- Script one-shot `scripts/backfill_entrez_date.py` : itère sur tous les articles, re-fetch NCBI EDAT, UPDATE `entrez_date` + aligne `first_seen_at`. 439/439 backfillé le 22/04.

## Gotcha découvert

Le match `source = 'pubmed'` échoue pour 28 articles (invisible trailing char ?). Le SELECT du script utilise `TRIM(source) = 'pubmed'` pour contourner. À surveiller si d'autres scripts filtrent sur `source = 'pubmed'`.

## Résultat

Avant backfill : Week=411/Month=411/Year=411 (toutes vues = tout, car `first_seen_at` était agglomérée au 20/04 post-migration v6).

Après backfill : Week=15 / Month=92 / Year=436 / Total=439. Distribution naturelle sur 13 mois.

## Références croisées

- Plan Tower : `~/.claude/plans/c-avec-sonnet-4-6-indexed-bubble.md` (plan migration CLI dont ce changement a émergé en fil rouge)
- Panel filtres redesigné : voir CLAUDE.md Tower section `Page Survey — architecture`
