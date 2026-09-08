---
name: project-export-run
description: "Commande export-run (sept. 2026) — une ligne par run de séquençage (liquid hors rebasecallés) vers une gsheet dédiée, onglet 'Run'. Aucune colonne créée en base : tout est dérivé à l'export. ⚠ bam_metadata.reads_per_flowcell somme les rebasecallés et surestime jusqu'à ×3,7"
metadata:
  node_type: memory
  type: project
---

# Export `run` (septembre 2026)

`export-run` → gsheet dédiée `1rGasqTmeGXi69k0jbeZibX0F-yrYTXhMp_HfgCXilq8`, onglet **`Run`**
(majuscule — le brief disait `run`, `worksheet("run")` a levé `WorksheetNotFound` puis
`add_worksheet` a échoué en 400 « feuille déjà existante » ; même piège que `Prop` en v32/v33.
Lister `sh.worksheets()` reste le réflexe).

**291 runs × 14 colonnes**, périmètre `sample_type='liquid'` + `NOT LIKE '%rebasecalled%'`
= 1163 samples, 0 `run_id` NULL. **Aucune colonne ni calcul ajouté en base** : tout est dérivé
par `GROUP BY (run_id, labo)` dans `DuckDBService.get_run_export()`.

## `reads_per_flowcell` : le bug et sa correction (08/09/2026)

**Avant correction**, `update-column reads_per_flowcell` (`check_samples.py:1342`) sommait
`nb_reads_total` par `run_id` **sans exclure les rebasecallés**, et écrivait la valeur sur eux
aussi. Sur `9fc13cc1` (HCL) : `Healthy_23/25/26` comptés **5 fois chacun** (original + 4
rebasecalls) → **876,15 M** stockés pour 238,13 M réellement produits. C'était le maximum de
toute la colonne — toute la queue au-delà de 400 M était du double comptage.

Un histogramme Aima-Tower « reads par flowcell hors rebasecalled » en héritait, avec **deux**
défauts cumulés : sa requête lisait `b.reads_per_flowcell` **une ligne par sample** (n=1309,
liquid+solid) — l'axe comptait donc des **samples**, pas des flowcells (325 runs distincts
seulement) — et son filtre écartait les **lignes** rebasecallées sans retirer leur contribution
à la **valeur**. Dédupliquer par `run_id` n'en corrige que la moitié.

**Corrigé le 08/09/2026** dans `_update_aggregate_column`, 4 edits :
`nb_reads_total` → **`nb_reads_aligned`** (Boris veut des *molécules*, pas des lignes) ·
garde `'rebasecalled' not in sample_name` dans l'agrégation · la liste `no_runid` des samples
mis à `NULL` devient `excluded` (sans run_id **ou** rebasecallé) · docstring.
Recalcul sur les 3 combos : **1515 valeurs modifiées, 208 rebasecallés passés à NULL**.
Max liquid **876,15 → 335,92**. Base ↔ export `run` : **291/291 runs identiques**.

⚠ **Le solid n'a aucun sample rebasecallé** (0/147) : l'exclusion y est un no-op, seul le
changement de métrique a bougé ses 147 lignes.
⚠ Les appelants n'ont pas eu à changer — `Bam2Beta/dev/SCW/Bam2Beta.sh:80-81` et
`trace-prod/launch.sh:51-52` passent par la même fonction. `Bam2Beta.sh` republie Trace Prod
juste après, mais **pas** `export-run`.
Backup `samples_status.backup-pre-aggregate-rebasecalled-20260908_110256.duckdb`.

⚠ Aucune des deux mesures ne dit ce que la **flow cell a produit** : elles somment les reads
*attribués aux samples en base*, hors reads non démultiplexés. 262 runs / 291 ont exactement
4 samples en base, 17 en ont moins — sans le rapport MinKNOW, impossible de trancher entre
« run peu chargé » et « samples absents de la base ». Cf [[project_pore_scan_analyse]].

## Autres points

- **`sequencing_time` n'est pas une donnée de run mais de barcode** : 26 runs / 291 portent
  plusieurs valeurs, jamais un NULL vs valeur (0 cas). Écarts de 2 min (dernier read de chaque
  barcode) à **30 h** (`07834101` : 20h56m vs 51h04m — un barcode s'arrête bien avant les autres).
  Choix Boris : lister les valeurs distinctes triées. Idem `multi_run` (2 runs).
- **`samples_per_run` diverge du périmètre sur 61 runs / 291** (même cause : rebasecallés) →
  l'export utilise `COUNT(*)`, cohérent avec la liste `Samples dans le run` affichée à côté.
- **`metadata.run_number`** (`20250319_1427_P2I-00117-A_PBA88487_1389c053`) donne date, heure,
  position et **flow cell ID** : toujours 5 segments, **0 run hétérogène**, mais présent sur
  **209 runs / 291** seulement (les `Lung_Alc` re-basecallés offline n'en ont pas). Seule source
  du flow cell ID en base → permet de croiser avec les pore scans.
- ⚠ **`_export_rarefaction_horaire` applique `.replace(".", ",")` à toute colonne hors
  `text_cols`** : sans `_RUN_TEXT_COLS`, `dna_r10.4.1_e8.2_400bps_hac` devenait
  `dna_r10,4,1_e8,2_400bps_hac`. Sur 14 colonnes, une seule est numérique.
- Le helper fait `clear()` → `update()` → **`resize()`** : la grille est recadrée, pas de colonne
  fantôme (contrairement à `export_data` des onglets trace-prod).
- ⚠ `USER_ENTERED` convertit `19-03-2025` en **date native** (sérialisée 45735). L'affichage
  reste bon et le tri devient possible, mais une relecture `UNFORMATTED_VALUE` annonce des
  centaines de faux écarts. Normaliser avant de conclure (cf [[project-schema-v26-mvaf-v15]]).

Tag de rollback `checkpoint-pre-export-run` (sur `560622b`).
4 fichiers : `lib/duckdb.py`, `lib/gsheets.py`, `database/check_samples.py`, `gsheets_config.json`.

Liens : [[project_schema_v33_dilution_lung]] (le pattern calqué, v33),
[[reference_infra_pod5_bam_export.md]] (`reads_per_flowcell` / `samples_per_run` via update-column).
