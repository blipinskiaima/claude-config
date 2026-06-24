# trace-workflow Memory

## Architecture
- CLI Click dans `check_workflow.py`, services dans `lib/`
- DuckDB single-writer, partagee avec Aima-Tower (lecture seule)
- Daemon: sync continue toutes les 30s, compaction 6h, erreurs recuperables vs fatales

## Daemon robuste (2026-02-23)
- Logger dedie `"daemon"` avec RotatingFileHandler (10MB x 5) + console
- SIGTERM handler pour arret propre (Docker/systemd)
- Crash signal file pour diagnostic post-crash
- Erreurs recuperables (reseau, lock, OS) → WARNING + continue
- Erreurs fatales (schema, bug) → CRITICAL + crash signal + exit(1)
- Sleep interruptible (seconde par seconde)

## Integration Aima-Tower
- `WorkflowService.get_sync_state()` lit `seqera_sync_state`
- Badge "DAEMON" dans navbar: vert/jaune/rouge/gris selon etat sync
- Callback auto-refresh 60s avec tooltip detaille
- Fichiers: `src/services.py`, `src/pages.py`, `src/callbacks.py`

## Catch-up & limite API Seqera (2026-06-24)
- **API plafonne `max` a 100/requete** (workflows ET taches): `max>100` → 400 avale en `return []` par `list_workflows` (echec silencieux). Paginer via `offset`.
- Multi-workspace: scope = user (perso) + orgs dans ALLOWED_ORGS (showcase exclu). `_resolve_workspaces()` dedoublonne.
- **Catch-up** (`sync --catchup` + auto au boot daemon): pagine jusqu'a recouper la zone deja sync (arret apres 2 pages 100% terminales). Cible le trou en TETE d'un downtime. Trou profondement enclave (>200 sains au-dessus) non couvert → backfill manuel par dates.
- **Zombies RUNNING**: runs pousses par Nextflow externe (pas via Launchpad) = NON annulables par Tower (`cancel` → 400 "not supported"). Si 0 tache + lastUpdated fige a +10s → marquer UNKNOWN en base manuellement. Divergence cache/source assumee.

## Patterns
- `retry_on_lock()` pour toute operation DB (backoff 500ms-5s, 20 retries)
- `batch_sync()` pour minimiser la duree du lock en ecriture
- Pattern diff (hash MD5) pour eviter re-render inutile dans Dash
