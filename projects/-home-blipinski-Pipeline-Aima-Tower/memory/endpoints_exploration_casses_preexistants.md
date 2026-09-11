---
name: endpoints-exploration-casses-preexistants
description: "Cinq endpoints /api/exploration en 500 depuis avant la migration v34, avec la méthode A/B qui l'a prouvé"
metadata: 
  node_type: memory
  type: project
  originSessionId: 46c2b08d-a964-4578-a4ab-2079f75df9d0
  modified: 2026-09-10T15:11:41.625Z
---

Constaté le 2026-09-10, **indépendant de la migration v34** : cinq endpoints de
`backend/routers/exploration.py` renvoient 500 et le faisaient **déjà avant** la migration.

| Endpoint | Exception |
|---|---|
| `/api/exploration/scores` | `ValueError: could not convert string to float: 'h'` (ligne ~380) |
| `/api/exploration/bladder` | `ValueError: The truth value of a DataFrame is ambiguous` (ligne ~432) |
| `/api/exploration/qc-data` | `PydanticSerializationError: 'float' object cannot be interpreted as an integer` |
| `/api/exploration/mvaf-dotplot` | idem |
| `/api/exploration/filtered-dataset` | idem |

Cause probable de `scores` : `get_scores()` est typé `-> Dict[str, np.ndarray]` et le
routeur fait `healthy_arr, cancer_arr = get_scores(...)`. Dépaqueter un dict donne ses
**clés** (`"healthy"`, `"cancer"`), d'où `float('h')`. Non corrigé — hors périmètre de la
migration, à traiter séparément.

**Méthode qui l'a prouvé, réutilisable** — un `Binder Error` masque tout le reste, donc
comparer « avant / après » sur la même base ne dit rien. Il faut reconstituer l'état
d'avant :

```
git archive HEAD | tar -x -C <scratchpad>/pristine     # code d'origine
cp samples_status.duckdb copie.duckdb                   # copie, jamais l'originale
ALTER TABLE qc_metrics RENAME COLUMN nb_lignes_total TO nb_reads_total   # sur la COPIE
DUCKDB_PATH=copie.duckdb uvicorn backend.main:app --port 8055            # état « avant »
```

Puis comparer code d'origine + base ancienne (port 8055) contre code corrigé + base v34.
`config.py` lit bien `DUCKDB_PATH` en variable d'environnement. Résultat obtenu :
**statuts HTTP identiques sur les 17 endpoints testés**, et payloads `compute`,
`cohort-cascade`, `cohort-samples`, `depth-sweep` **octet pour octet identiques** après
normalisation des deux clés renommées. C'est ce qui permet d'affirmer « je n'ai rien
cassé » au lieu de l'espérer.

⚠ Comparer les lignes **positionnellement**, pas par `sample_name` : la table a 1323 lignes
pour 1248 noms uniques (variantes rebasecalled). Un dict indexé par nom écrase des lignes
et fabrique 686 fausses différences.

Voir aussi [[migration-v34-colonnes-reads]].
