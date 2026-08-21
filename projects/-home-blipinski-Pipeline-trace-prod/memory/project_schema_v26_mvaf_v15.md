---
name: project-schema-v26-mvaf-v15
description: "Schema v26 — colonne mvaf_v15 (retd_suivis, liquid only), calque EXACT de mvaf_v14 (V1.4→V1.5), structure fichier identique 3 col cols[1] + format_mvaf4. S'AJOUTE à mvaf_v14 sans la remplacer : v1.3/v1.4/v1.5 coexistent. Backfill 100% (1362 samples)"
metadata:
  node_type: memory
  type: project
---

# Schema v26 — mvaf_v15 (août 2026)

Colonne `mvaf_v15` VARCHAR DEFAULT 'KO' dans `retd_suivis`, **liquid uniquement**
(`LiquidChecker` seul, Solid intact — 0 fichier V1.5 en solid, vérifié 0/150).
Hors `STATUS_COLUMNS` et `NUMERIC_COLUMNS` → virgule préservée.

**Why:** Boris a produit un modèle raima V1.5 et veut le tracer comme le v1.4, exporté juste
après lui. Demande explicite en cours de session : **« 1.4 et 1.5 doivent coexister, l'un ne
remplace pas l'autre, le 1.5 est ajouté »**.

## Calque EXACT de mvaf_v14 — zéro différence de logique

Seule la chaîne `V1.4` → `V1.5` change dans le nom de fichier. Contrairement au passage
v1.3 → v1.4 (qui avait changé d'index de colonne, `cols[2]` → `cols[1]`, parce que V1.4 avait
perdu la colonne `score`), **le V1.5 a la même structure que le V1.4** :

```
name    mvaf    model          <- 3 colonnes, valeur en cols[1]
26BM..  1.21    v1.5
```

⚠ **Cette structure a été vérifiée sur un fichier réel AVANT d'écrire le checker**, précisément
parce que le précédent v1.3→v1.4 avait déplacé la colonne. Ne jamais présumer qu'une nouvelle
version raima garde le même format.

## How to apply

- Source `BETA/{sample}.merged.epic.raima_score.V1.5.tsv`, ligne 2 `cols[1]`, `NA` si absent.
- **`format_mvaf4()` indispensable** — les V1.5 contiennent de la notation scientifique
  (`3e-06`, `7e-05`, `1.4e-05`) → `0,000003000`, `0,00007000`. Jamais de notation scientifique
  en base ni à l'export.
- `check_mvaf_v15` (BaseChecker) · câblé `LiquidChecker.check_sample()` après `"mVAF v1.4"`
  + fallback dict (groupe NA) · `COLUMN_CHECKERS['mvaf_v15']` (pattern simple, `'NA'`→NULL)
  · `_LIQUID_QC` header `mVAF v1.5` après `mVAF v1.4` → position **16/56**.
- **4 fichiers, 10 edits** : `lib/duckdb.py` (5 : SCHEMA_VERSION 25→26, DDL, `TSV_TO_DB_RETD`,
  migration idempotente v26, description) · `lib/checkers.py` (3) · `database/check_samples.py`
  (1) · `lib/utils.py` (1). **Aucune ligne contenant `mvaf_v14` modifiée** (vérifié sur le diff).
- Checkpoint `checkpoint-pre-mvaf-v15` (sur `151e4ff`).

## Coexistence — le point demandé explicitement

`mvaf_v15` est une colonne **ajoutée à côté**, jamais un remplacement. Les 3 versions vivent
ensemble en base et dans la gsheet (col 14/15/16) :

| sample | mvaf_v13 | mvaf_v14 | mvaf_v15 |
|---|---|---|---|
| `26BM01841` | 1,368 | 1,2100 | 1,2100 |
| `Bladder_Blood_02_023` | 0 | 0,000004000 | 0,000003000 |
| `Bladder_Urine_02_098` | 2,7 | NULL | 38,3500 |

## Backfill 20/08/2026 — couverture 100 %

**849 CGFL + 513 HCL = 1362 samples, 0 erreur, 0 NA, 0 KO résiduel.** ~18 min en tmux
(update-column CGFL → HCL → 2 exports gsheet, séquentiel pour le single writer lock ;
exports OK dès la 1ʳᵉ tentative, aucun APIError 503).

Vérifs : contrôle croisé DB↔fichier source (20 samples, 0 écart) ; relecture gsheet↔base
(1362 lignes, 0 écart) ; `mvaf_v14` toujours à 1497 non-NULL et `mvaf_v13` à 1464 (inchangés) ;
solid resté à `KO` sur 147 lignes (jamais backfillé).
**`v1.4 ≠ v1.5` sur 443 CGFL + 94 HCL** → c'est bien un nouveau modèle, pas une copie.

## Gotchas

- ⚠ **Homonyme `Lung_120`** : dossier présent sous `CGFL/` **et** `HCL/` sur le disque, mais le
  sample n'est en base que côté **HCL** ; le dossier CGFL est orphelin (aucun V1.5, non
  référencé). Choisi d'abord comme cas KO de test, il ne prouvait rien : un
  `update-column ... CGFL -s Lung_120` affiche « 1 sample mis à jour » sans toucher une ligne
  (compteur d'itérations, cf. [[project-schema-v20-mito]]). **Toujours confirmer en base qu'un
  sample de test existe pour le labo ciblé** avant d'en tirer une conclusion.
- ⚠ **Chemin `NA → NULL` non observable en prod** (couverture 100 %) : prouvé par monkeypatch du
  checker → `None` en base, puis vraie valeur restaurée. Même situation que
  [[project-schema-v21-n50]].
- ⚠ **12 `Bladder_Urine_*` CGFL ont `mvaf_v14` à NULL alors que leur fichier V1.4 existe
  désormais** — arrivé après le dernier backfill v14 (décalage temporel, pas un bug ; même
  mécanique que [[feedback_probs_loyfer_lag]]). Le backfill v1.5 les a tous remplis. Un
  `update-column mvaf_v14 liquid CGFL` comblerait ces 12 trous.
- ⚠ **Relecture gsheet — deux faux écarts à 100 %** : `get_all_values(UNFORMATTED_VALUE)` renvoie
  des **nombres** (`1.21`) là où la base stocke une **chaîne à virgule** (`"1,2100"`) ; et `None`
  (base) s'exporte `'NA'` (gsheet). Normaliser (virgule→point puis `float`, et `None ≡ 'NA'`)
  avant de conclure à une divergence. Complète le gotcha de [[cohort-export]] sur les valeurs
  formatées.
- **Hors scope assumé** : `dilution` et `rarefaction` ont leur propre `mvaf_v14_*` — **non
  propagé** au v1.5 (non demandé, Surgical Changes).

Liens : [[project_schema_v13_mvaf_v14]] (calque direct),
[[project_schema_v11_mvaf_v13_frag_score]], [[project_columns_index]].
