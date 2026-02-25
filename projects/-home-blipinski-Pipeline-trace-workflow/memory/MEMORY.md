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

## Patterns
- `retry_on_lock()` pour toute operation DB (backoff 500ms-5s, 20 retries)
- `batch_sync()` pour minimiser la duree du lock en ecriture
- Pattern diff (hash MD5) pour eviter re-render inutile dans Dash
