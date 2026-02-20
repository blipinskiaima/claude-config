# Aima Tower — Auto Memory

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
