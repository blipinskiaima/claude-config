# DuckDB Patterns — Aima Tower

## Cross-DB Join via ATTACH (in-memory)

### Probleme
`DuckDBMixin._query()` ouvre une connexion read-only vers une seule base. Les connexions read-only ne peuvent pas executer ATTACH (modification du catalogue).

### Solution
Ouvrir une connexion in-memory `:memory:` et ATTACH les deux bases en read-only :

```python
conn = duckdb.connect(":memory:")
try:
    conn.execute(f"ATTACH '{platform_db}' AS pl (READ_ONLY)")
    conn.execute(f"ATTACH '{seqera_db}' AS wf (READ_ONLY)")
    result = conn.execute('''
        SELECT ... FROM pl.samples s
        LEFT JOIN wf.seqera_workflows w ON ...
    ''')
    # ... process results
finally:
    conn.close()
```

### Retry pattern
Reproduire le meme retry IOException avec backoff que `_query()` (5 tentatives, 500ms * 2^attempt).

### Implementation
Voir `PlatformService.get_samples_overview()` dans `services.py`.

## Workflow JOIN — Matching platform samples to seqera workflows

La jointure utilise `split_part()` pour extraire client_uuid et sample_name depuis `input_path` :
- `split_part(input_path, '/', 5)` → client_uuid
- `split_part(input_path, '/', 8)` → sample_name

Filtre : `WHERE input_path LIKE '%aima-platform%'` (PROD uniquement).

Selection du meilleur workflow par sample via `ROW_NUMBER()` :
1. SUCCEEDED en priorite
2. Puis le plus recent (submit_time DESC)
