---
name: project-schema-v22-n75-ratio
description: "Schema v22 — n75 INTEGER (stocké mais JAMAIS exporté) + n50_n75_ratio DECIMAL(10,4) (stocké ET exporté sous 'Ratio N50/N75') dans qc_metrics, les 3 combos. Réutilise le helper read_last_line_by_header de v21. Gotcha : float('NaN')/float('inf') ne lèvent pas ValueError"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6a5dcc87-06b5-4ed0-8355-81a5e4b56941
  modified: 2026-08-10T19:46:32.004Z
---

# Schema v22 — n75 + ratio n50/n75 (qc_metrics, août 2026)

Suite directe de [[project-schema-v21-n50]], **même fichier source**, mêmes 3 combos
(liquid CGFL + HCL, solid CGFL). Deux colonnes dans `qc_metrics` :

| Colonne | Type | En base | Exporté |
|---|---|---|---|
| `n75` | INTEGER | oui | **NON** |
| `n50_n75_ratio` | DECIMAL(10,4) | oui | oui — header `Ratio N50/N75` |

**Why:** Boris veut le n75 tracé en base mais **ne veut pas** de colonne n75 dans la gsheet —
seul le **ratio n50/n75** l'intéresse à la lecture : c'est un indicateur de dispersion des
longueurs de reads qui sépare nettement les matrices (liquid ≈ 1,11 / solid ≈ 1,60-1,71).

## Le point d'architecture à retenir

**`TSV_TO_DB_QC` (mapping d'ÉCRITURE) et `_LIQUID_QC`/`_SOLID_QC` (listes d'EXPORT) sont
indépendants.** Une colonne doit être dans `TSV_TO_DB_*` pour que le `check` général l'écrive
en base (`upsert_sample` → `_prepare_data(…, mapping, table)`), et dans `_*_QC` pour partir en
gsheet. `n75` est donc dans le premier, absent des secondes.

Précédent déjà en place, vérifié : `mVAF v1 10M`, `mVAF v1 20M`, `mVAF v1 ft0.92`,
`mVAF v1 ft0.95` sont mappées et jamais exportées.

## How to apply

- **Aucun nouveau helper** : `TSVExtractor.read_last_line_by_header()` créé en v21 est réutilisé
  tel quel. `lib/extractors.py` n'est pas touché → **4 fichiers** au lieu de 5.
- `get_n75()` = calque de `get_n50` (résolution `.merged` + fallback ancien nommage dupliquée).
  **`get_n50` n'a PAS été refactorisé** : il est commité, testé et backfillé, et la duplication
  est déjà le pattern du fichier (`get_epic_reads` duplique `get_cramino_reads`).
- `get_n50_n75_ratio()` **compose** `get_n50` + `get_n75` (2 relectures du petit TSV, coût
  négligeable — le backfill n50 des 1471 samples avait pris ~5 min exports compris).
  Sortie `format_comma(f"{r:.4f}")` → `1,1258`. `NUMERIC_COLUMNS` reconvertit virgule→point.
- **4 décimales obligatoires** : en liquid toute la plage tient entre 1,09 et 1,17 — à 2
  décimales la colonne s'écraserait sur `1,11` et perdrait tout pouvoir discriminant.
- 2 entrées `COLUMN_CHECKERS` → **2 `update-column` distincts**. Le ratio **ne se déduit pas**
  du remplissage de `n75` : contrepartie assumée du checker dédié (choisi contre un dérivé SQL),
  qui garantit en échange que les futurs `check` remplissent tout sans intervention.
- Export : `Ratio N50/N75` juste après `N50` → position **10/54** liquid, **8/41** solid.

## Gotcha majeur — `float('NaN')` et `float('inf')` ne lèvent PAS ValueError

Deux défauts trouvés **par les tests de cas limites**, pas par relecture :

1. `n75 = "NaN"` → `float("NaN")` réussit → le ratio sortait la chaîne `nan` vers la base.
2. Correction naïve par `isfinite(ratio)` : **insuffisante**. `n50 / inf = 0.0`, un résultat
   *fini* → `0,0000` écrit en base. Une valeur **silencieusement fausse**, qui passe tous les
   contrôles de cohérence — pire qu'une absence.

Version retenue : valider les **deux opérandes**, jamais le résultat.

```python
try:
    n50, n75 = float(self.get_n50(...)), float(self.get_n75(...))
except ValueError:
    return "NA"
if not (math.isfinite(n50) and math.isfinite(n75)) or n75 == 0:
    return "NA"
```

À rejouer pour toute future colonne calculée à partir d'un fichier produit par un outil externe.

**Vérifié** : contrôle croisé indépendant sur 6 samples des 3 combos (0 écart) ; 13 cas limites
(nominal, ancien nommage, `n50 == n75` → `1,0000`, div/0, NaN et inf sur chacun des 2 opérandes,
colonne absente ×2, header seul, fichier vide, dossier absent) ; `typeof(n75)` = `INTEGER`,
`typeof(n50_n75_ratio)` = `DECIMAL(10,4)` avec `ratio * 2` = `2.2516` (4 décimales conservées) ;
ratio stocké == `round(n50::DOUBLE / n75, 4)` recalculé en SQL ; `N75` **absent du header** des
3 exports TSV alors que la colonne est remplie en base ; `depth`/`mvaf_v1` et le backfill n50 de
v21 intacts. Checkpoint `checkpoint-pre-n75` (7b75c16).

Liens : [[project-schema-v21-n50]] (même source, helper réutilisé), [[project_columns_index]].
