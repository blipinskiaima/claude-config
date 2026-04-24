# Aima Tower — Auto Memory

## Todo list — routing par section
Todo list `~/.claude/projects/-home-blipinski/memory/todo-optimisation.md` a 4 parties : À faire / En cours / Complété / Stand-by. Afficher UNIQUEMENT la partie demandée, pas le fichier complet. Détails : [feedback_todo_sections.md](feedback_todo_sections.md)

## DuckDB Cross-DB Join Pattern

Quand on doit joindre deux bases DuckDB read-only (ex: platform + trace-workflow), `_query()` ne peut pas ATTACH (connexion read-only). Solution : connexion in-memory avec ATTACH des deux bases :
```python
conn = duckdb.connect(":memory:")
conn.execute(f"ATTACH '{db1}' AS pl (READ_ONLY)")
conn.execute(f"ATTACH '{db2}' AS wf (READ_ONLY)")
# Utiliser pl.table et wf.table dans la requete
```
Voir `PlatformService.get_samples_overview()` pour l'implementation complete.
Details : [duckdb-patterns.md](duckdb-patterns.md)

## Scaleway S3 URL Mapping

`s3://aima-platform/` → `https://console.scaleway.com/object-storage/buckets/fr-par/aima-platform/files/`
Helper : `_s3_to_scaleway_url()` dans `callbacks.py:_build_platform_table()`

## Platform Detail Panel (Database > Platform)

- Layout : Donnees (lg=8) gauche, Trace (lg=4) droite
- Input/Output : liens cliquables vers console Scaleway (classe `detail-value-path`)
- Rapport : lien Click vers `{input_path}/results/`
- Log : lien Click vers `{output_path}/{sample_name}/LOG/`
- Police paths : `0.75rem` (plus petit que le reste)

## Gotcha: Python Closures in Loops

Definir les fonctions helper AVANT leur premier appel dans la boucle. UnboundLocalError si defini apres (Python voit l'assignation dans le scope et considere la variable locale).

## Docker Workflow

Rebuild rapide : `docker compose down && docker compose build && docker compose up -d`
Restart sans rebuild (si seul CSS change dans assets/) : `docker compose restart`
Note : `COPY src/` dans Dockerfile invalide le cache a chaque modif src/.

## Page Survey — patterns

Parser extensible, lazy tabs, state atomique, scoring IA découplé, persistence session. Tous les patterns réutilisables consolidés dans [survey_patterns.md](survey_patterns.md).

## Intégration DuckDB Aima-Survey (v6 — 2026-04-20)

Vues `month` et `all` lisent `~/Pipeline/Aima-Survey/data/aima_survey.duckdb` en READ_ONLY (retry backoff), fallback markdown si DB KO. Day/week inchangés. Traduction `queries_matched` (names) → `categories` (descriptions humaines) via `queries.json`. Détails : [survey_duckdb_integration.md](survey_duckdb_integration.md)

## Sécurité Tower (2026-04-21)

Tower accessible via `https://tower.aima-diagnostics.com` (Caddy reverse proxy + basic auth bcrypt + Let's Encrypt). Port 8050 non exposé à Internet. Password dans gestionnaire de mdp AIMA. Détails : [security_setup.md](security_setup.md)

## Sécurité — approche pragmatique

Boris valide le scope discipline en sécu : couches par iteration (Caddy d'abord, Security Group plus tard). Détails : [feedback_security_pragmatism.md](feedback_security_pragmatism.md)

## Incident `.env` tracked dans git

`.env` était tracked dans git jusqu'au 2026-04-21 (repo privé). Retiré via `git rm --cached`. Rotation secrets Anthropic/Seqera **reportée** (repo privé, Boris seul dev). Détails : [project_env_leak.md](project_env_leak.md)

## Backend IA via CLI `claude -p` (2026-04-22)

Tous les appels IA Tower (Survey synthese, Analytics chat, DB Q&A) passent par `src/claude_cli.py` subprocess `claude -p` + `CLAUDE_CODE_OAUTH_TOKEN` (abonnement Max au lieu credits API). `ANTHROPIC_API_KEY` **retire** du container (priorite CLI bypasse OAuth). HOME isole `/app/data/claude-home`. Contexte injecte = 14 CLAUDE.md Pipeline (~20K tokens). Détails : [ia_cli_migration.md](ia_cli_migration.md)

## Vues temporelles Survey pilotees par `first_seen_at` (2026-04-22)

Depuis backfill EDAT Aima-Survey, toutes les vues (Day/Week/Month/Year/All) filtrent sur `first_seen_at` = EDAT PubMed (stable, immuable, non-future). Plus de pub_date. Card UI affiche les 2 dates distinctes ("Indexé : ... • Publié : ..."). Vue Jour migree DuckDB avec `DATE(first_seen_at) = ?` + selecteur conditionnel. Détails : [survey_first_seen_at.md](survey_first_seen_at.md)

## Onglet Concurrence Survey étendu

`is_competitor_article(a)` matche desormais `a.org_name` OR `a.last_author_affiliation` contre `competitors.json` (23 entreprises tier_1/2/3 avec aliases). +IMBdx ajoute comme tier_2 MOYENNE. Passe de 11 a 29 articles concurrents. Reclassification Haiku ciblee en cours (script `reclassify_competitors.py` cote Aima-Survey).

## Guardant Health — stratégie Europe (2026-04-23)

Snapshot : Guardant360 CDx seul IVDR-certifié (mai 2024). Reveal MRD = LDT via labs hospitaliers (VHIO, Royal Marsden, Gemelli) — **aucun partenariat France**. Shield MCED **absent Europe**, priorité Asie 2026 (Manulife). Signatera devance Guardant sur CRC France (CIRCULATE-PRODIGE-70). Fenêtres AIMA : MCED CRC sanguin méthylation + MRD CRC France via UNICANCER/CLCC. IVDR classe C se ferme 2028. Détails : [competitors_guardant_europe.md](competitors_guardant_europe.md)
