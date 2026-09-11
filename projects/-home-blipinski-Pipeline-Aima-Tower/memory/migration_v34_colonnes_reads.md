---
name: migration-v34-colonnes-reads
description: Migration trace-prod v34 (nb_lignes_total / nb_molecule) et les deux pièges de propagation silencieuse dans la Tower
metadata: 
  node_type: memory
  type: project
  originSessionId: 46c2b08d-a964-4578-a4ab-2079f75df9d0
  modified: 2026-09-10T15:11:26.185Z
---

Le 2026-09-08, trace-prod (commit `19923c1`) a **renommé** deux colonnes de `qc_metrics`,
sur 7 tables au total (les suffixées `_small_fragments`, `_dilution`, `_dilution_lung`,
`_rarefaction`, `_horaire`, `_threshold` suivent le même schéma) :

```
nb_reads_total    ->  nb_lignes_total     (toujours en MILLIONS, inchangé)
nb_reads_aligned  ->  nb_molecule         (toujours en MILLIONS, inchangé)
nb_reads_epic     ->  nb_reads_epic       (inchangé)
```

⚠ **Ne pas confondre `nb_lignes_total` et `nb_molecule`** : le remplaçant de `nb_reads_total`
est `nb_lignes_total`. `nb_molecule` est l'ex-`nb_reads_aligned`. Un agent d'exploration a
proposé `nb_reads_epic` par analogie avec le protocole EPIC — c'est faux. La source est le
message du commit `19923c1` et `information_schema`, pas l'intuition.

`SCHEMA_VERSION` n'a **pas** été bumpé par ce commit (voir CLAUDE.md trace-prod ligne ~306).

Côté Tower (corrigé le 2026-09-10), la casse dépassait le `Binder Error` visible sur
`/api/samples`. Deux mécanismes propagent un renommage **sans lever d'erreur** :

1. **`DatabaseService.get_sample_detail()` fait `SELECT s.*, q.*, ...`** — donc aucune
   erreur, mais les clés JSON deviennent les nouveaux noms. `/sample/:id` affichait
   silencieusement du vide sur « Nb reads alignés » et « sur X M reads totaux ». Une
   page en 500 se voit ; celle-là non. À re-vérifier à **chaque** migration trace-prod.

2. **`_apply_dynamic_filters` fait `if df_col not in out.columns: continue`** — un filtre
   avancé portant sur une colonne renommée devient un **no-op silencieux**. Les colonnes
   des filtres viennent de `information_schema` (`filters_service.columns_by_table()`),
   donc les nouveaux noms arrivent seuls au frontend ; c'est `_DYN_COL_REMAP`
   (`exploratory_compute.py`) qui doit suivre, puisqu'il mappe `table.colonne_DB` vers le
   nom du DataFrame. Même chose pour `QC_ORDER` et la table de libellés de
   `AdvancedFilters.tsx`, qui se clefsent sur les noms DB introspectés.

**Choix de correction retenu** : un seul vocabulaire, celui de la base, de bout en bout
(SQL + DataFrame + payload + frontend). Pas d'alias de compatibilité — il aurait fallu un
`SELECT q.* EXCLUDE (...)` pour le point 1 et aurait laissé deux vocabulaires en place.
Les **libellés affichés** ont été conservés tels quels (« Reads totaux », « Reads Tot »,
« Reads mapped ») : renommer l'affichage est une décision produit, pas une correction.
Le seuil QC de `/reproductibilite` (`QC_MIN_READS_M = 5.0`) reste valable puisque l'unité
n'a pas bougé — vérifié : le filtre écarte toujours 11 runs dont 8 partiels.

Voir aussi [[endpoints-exploration-casses-preexistants]] et [[reproductibilite_v15_graphe_qc]].
