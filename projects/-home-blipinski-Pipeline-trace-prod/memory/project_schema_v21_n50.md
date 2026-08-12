---
name: project-schema-v21-n50
description: "Schema v21 — colonne n50 INTEGER dans qc_metrics (liquid CGFL+HCL ET solid CGFL), source TSV cramino {sample}.merged.cramino.tsv lue PAR NOM d'en-tête via le nouveau helper read_last_line_by_header, export entre Coverage et mVAF v1"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f2da004-5cea-4687-be3c-4471f9c51ada
  modified: 2026-08-12T10:56:39.511Z
---

# Schema v21 — n50 (qc_metrics, août 2026)

Ajout de la colonne `n50 INTEGER` dans **`qc_metrics`** (pas `retd_suivis` : c'est une valeur
numérique, et sa place à l'export tombe au milieu du bloc qc_metrics). **Scope : les 3 combos**
— liquid CGFL, liquid HCL **et solid CGFL** — contrairement aux features v18/v19/v20 qui étaient
toutes liquid-only.

**Why:** Boris veut suivre le N50 (longueur de read au-delà de laquelle 50 % du yield est
atteint) produit par le process `Cramino_qc` de Bam2Beta (`workflow/qc.nf:66`). La métrique
n'existe **nulle part ailleurs** : ni dans `metadata.json`, ni dans aucune table trace-prod.

## Source

`{sample}/QC/Cramino/{sample}.merged.cramino.tsv` — TSV 13 colonnes, header + 1 ligne.
Fallback ancien nommage `{sample}.cramino.tsv` (runs anciens, sans le `.merged`).

Header cramino : `file_name · file_path · creation_time · num_alignments · percent_from_total ·
num_reads · yield_gb · mean_coverage · yield_gb_long · n50 · n75 · median_length · mean_length`

## How to apply

- **Lecture PAR NOM D'EN-TÊTE** — nouveau helper `TSVExtractor.read_last_line_by_header(filepath,
  header)` (`lib/extractors.py`) : cherche l'index de `'n50'` dans la ligne 1, lit la dernière
  ligne. Choix explicite de Boris : le format cramino peut réordonner ses colonnes entre versions.
  ⚠ **Diverge de ses deux voisines immédiates** `get_cramino_reads` / `get_epic_reads` qui lisent
  une **position** fixe (`read_last_line_column`, **1-based** « comme cut -f »). Incohérence locale
  assumée, signalée par un commentaire dans `get_n50`. Preuve du gain : sur un TSV aux colonnes
  réordonnées, lecture par nom → `170`, lecture par position → `None`.
- `BaseChecker.get_n50(sample_dir, sample) -> str` — préfixe `get_` (pas `check_`) comme toutes
  les colonnes `qc_metrics` voisines (`get_depth`, `get_coverage`, `get_mvaf`). `"NA"` si absent.
- Câblé dans `LiquidChecker.check_sample()` **ET** `SolidChecker.check_sample()` après `"Coverage"`,
  + les 2 fallback dicts (groupe `"NA"`).
- `COLUMN_CHECKERS['n50'] = ('qc_metrics', 'get_n50', 'checker', None)` — **pattern simple**.
  Le dispatch générique convertit `'NA'` → `None` (`check_samples.py`, branche
  `if new_value in ('KO','NA')`). Remplissage rétroactif via `update-column n50 {type} {labo}`,
  **sans relancer de `check` complet** (demande explicite de Boris : trop long).
- Export : header `N50` entre `Coverage` et `mVAF v1` dans `_LIQUID_QC` **et** `_SOLID_QC`
  → position **9/53** en liquid, **7/40** en solid. Mapping `TSV_TO_DB_QC["N50"]`.
  Aucun edit dans `gsheets.py` (mapping repris par `_sample_to_row`).
- Dans `NUMERIC_COLUMNS`. Le checker renvoie une `str` (`"170"`) et **DuckDB caste
  implicitement en INTEGER** — vérifié : `typeof(n50)` = `INTEGER`, `n50 + 1` = `171`.

## Gotchas

- **Le dossier `QC/Cramino/` est À PLAT**, contrairement à Mosdepth (`QC/Mosdepth/{DEPTH}/`).
  Il contient ~14 fichiers pour un même sample : `{ID}.{1M,2M,5M,10M,15M,20M,merged}.cramino.tsv`
  × `{,.epic}`. **Un glob ramasse les raréfiés et la version EPIC filtrée** → toujours construire
  le chemin exact, jamais de wildcard.
- **`ALTER TABLE ADD COLUMN` place `n50` en position physique 17**, alors que le DDL le déclare
  en 8ᵉ. Sans conséquence : l'export, l'UPSERT et `compact()` accèdent aux colonnes **par nom**
  (`compact()` construit `INSERT INTO t (cols) SELECT cols`, **jamais `SELECT *`** — vérifié).
- ⚠⚠ **CE FICHIER DÉCRIT L'ÉTAT v21 (10/08/2026). La source du LIQUID a basculé le 11/08**
  vers `QC/Samtools/{s}.n50_ratio.tsv` bloc `*_filtered` — voir [[project-schema-v24-pct-mass-removed]].
  Tout ce qui suit reste vrai **pour le solid**, et vaut comme historique pour le liquid.
- **Ordres de grandeur au 10/08/2026** (cramino, avant bascule) : liquid n=1324, médiane **174** bp
  (min 131, **max 6010**) ; solid n=147, médiane **3804** bp (min 381, max 9727).
  → **Valeurs liquid actuelles** (filtrées) : médiane **174** (inchangée), **max 574**.
- ⚠ **Un n50 liquid élevé n'était PAS une erreur d'extraction** (j'avais d'abord écrit l'inverse).
  15 liquides ≥ 1000 bp sur 1324 (1257 sont < 250 bp) : surtout des `Bladder_Urine_*` — matrice
  **urinaire**, dont la fragmentation ne suit pas le profil mononucléosomal du plasma — plus
  `TNE_2` (6010) et `Breast_6` (3808). **Le contrôle pertinent est la cohérence entre réplicats** :
  `Breast_6` 3808 vs son rebasecalled 3647, `Colon_22_rep1` 1608 vs `rep2` 1491. Une confusion de
  fichier source (raréfié, EPIC) ne produirait pas cette corrélation.
  → **Confirmé quantitativement depuis** : ces samples sont exactement ceux qui ont le plus de
  masse au-delà de 1 kb (`pct_mass_removed` : `TNE_2` **81,40 %**, `Colon_22_rep1/rep2` 64,91/62,62 %).
  Le filtre ≤ 1 kb supprime cette queue de reads longs.
- **Blocs liquid et solid textuellement identiques** dans `checkers.py` (les 3 lignes
  `"Depth"/"Coverage"/"mVAF v1"` et la liste de fallback) → un `Edit` sur ces zones doit élargir
  le contexte (ligne discriminante : `"Ratio %"` en liquid, `"Nb read alignés"` en solid).
- **Cas `NA` non observé en prod** : aucun des 120 samples liquid CGFL sondés n'était dépourvu de
  cramino. Le chemin `"NA"` → NULL est prouvé par les tests synthétiques + lecture du dispatch,
  pas sur une donnée réelle.

**Vérifié** : 3 combos testés avec contrôle croisé indépendant du fichier (5 samples, 0 écart) ;
6 cas limites (ancien nommage, header seul, fichier vide, colonne absente, dossier absent,
colonnes réordonnées) ; câblage `check_sample()` + fallbacks ; `update-column` persiste sans
toucher `depth`/`coverage_percent`/`mvaf_v1` ; homonyme `Colon_1` CGFL/HCL correctement discriminé
par `WHERE labo = ?`. Checkpoint `checkpoint-pre-n50` (e1b13fa).

Liens : [[project-schema-v20-mito]] (schema précédent), [[project_columns_index]],
[[feedback_status_columns]] (pourquoi `qc_metrics` et non `retd_suivis`/STATUS_COLUMNS).
