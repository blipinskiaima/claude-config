---
name: project-schema-v33-dilution-lung
description: "Schema v33 — table dilution_lung (63 col, autonome, PK sample_name seule), couples Lung_N_Healthy_M_50_50 du labo HCL, calque de rarefaction_horaire_threshold (mêmes 6 sous-dossiers, epic bootstrapé, Loyfer valeur unique). Export vers la gsheet dédiée « Trace Dilution Lung » (onglets mVAF 17 col / Prop 52 col)"
metadata: 
  node_type: memory
  type: project
  originSessionId: bce6fa23-fc10-4ef4-9362-163faa533ed0
  modified: 2026-09-07T07:44:23.441Z
---

# Schema v33 — `dilution_lung` (septembre 2026)

Table **autonome** de 63 colonnes, une ligne par couple dilué `Lung_N_Healthy_M_50_50`
(un échantillon lung + un healthy, 50 % chacun, **tout le lot vient de HCL**). Un seul dossier
`s3://aima-bam-data/processed/MRD/RetD/liquid/dilution_lung/`, un seul labo → **PK `sample_name`
seule**, comme `dilution` (v9), pas de PK composite.

**Why:** Boris veut suivre les jeux dilués lung/healthy comme les raréfactions, et comparer les
valeurs du couple aux valeurs initiales du **parent lung** (pas du healthy).

## Le point qui a tout décidé : le contenu, pas le nom

Le brief disait « sur le modèle de `dilution` ». Le listing S3 (1580 clés) a montré exactement
les **6 sous-dossiers de `rarefaction_horaire_threshold`** (`BAM, BETA, BETA_28M, BOOTSTRAP,
EXTRACT_FULL_28M, QC`), `BETA/` ne contenant que `raima_score.V1.4/V1.5`, aucun `CNV`,
`Fragmentomics`, `ichorCNA`, `IV`. Le checker est donc un calque de **threshold**, pas de
`dilution` : il importe `_bootstrap_means` (horaire) et `_read_props` (dilution), 0 règle réécrite,
et les deux exports réutilisent `_export_rarefaction_horaire` tel quel. Toujours lister le dossier
avant de choisir le modèle.

## Colonnes (63)

- Identité (5) : `sample_name` PK, `lung_id`, `healthy_id`, `lung_pct`, `healthy_pct` (INTEGER) —
  parsés par `split_couple()` (regex `^(Lung_\d+)_(Healthy_\d+)_(\d+)_(\d+)$`, rejette `LOG`).
- Statuts (2) : `bam_status_dilution_lung` (demandé), `prod_status_dilution_lung` (ajouté :
  BAM vaut **OK sur 33/33** et ne discrimine rien, PROD = `BAM+BETA+QC` vaut 12/33).
  **Pas** de `bootstrap_props` OK/KO (redondant avec les 16 epic à NULL).
- Métriques (8) : nb reads total/alignés/epic, ratio, depth, coverage (DECIMAL, `NA` si absent,
  garde sur le brut contre le `0,00` fantôme), `mvaf_v14`/`mvaf_v15` (VARCHAR, `format_mvaf4`,
  littéral `'NA'` si absent — même convention que threshold, 465 `NA` là-bas).
- Probs (47) : 16 epic = **moyenne des 200 réplicats bootstrap**, 31 Loyfer = valeur unique
  (`props_loyfer.tsv` 2 × 31 ; aucun bootstrap Loyfer n'existe, limite physique déjà vue v28/v32).

Suffixe `_dilution_lung` sur statuts/métriques/probs ; les 5 colonnes d'identité sans suffixe.

## Câblage (5 fichiers + 1 créé)

`lib/checkers_dilution_lung.py` (nouveau) · `lib/duckdb.py` (DDL, `ALL_TABLES`, 5 constantes
`*_DILUTION_LUNG`, migration v33 = commentaire + description, `compact()`, `upsert_dilution_lung`,
`get_dilution_lung_all/_mvaf/_prop`) · `lib/utils.py` (`DILUTION_LUNG_DIR`) · `lib/gsheets.py`
(2 headers + 2 exports) · `database/check_samples.py` (`check-dilution-lung`,
`update-column-dilution-lung` 12 clés avec garde-fou anti-création de ligne,
`export-dilution-lung-mvaf`, `export-dilution-lung-prop`, tous `-o fichier.tsv`) ·
`gsheets_config.json` (`dilution_lung_mvaf`, `dilution_lung_prop`).

## Export — gsheet dédiée « Trace Dilution Lung »

`1UESVfh53-6c3ycQUatHnse0wmnguZ1aUGz-hVbex1y8`, distincte de toutes les autres.
⚠ L'onglet s'appelle **`Prop`** (majuscule) — le brief disait `prop`.

| Onglet | Col | Contenu |
|---|---|---|
| `mVAF` | 17 | `ID complet` (= `sample_name`, déjà concaténé) · `ID Lung` · `ID Healthy` · `% Lung` · `% Healthy` + 6 paires parent lung / dilué (`Nb lignes total`, `Nb molécule`, `Depth`, `Coverage`, `mVAF v1.4`, `mVAF v1.5`, suffixe ` dilution`) |
| `Prop` | 52 | 5 identité + 47 probs, en-têtes nus, **point** décimal |

Valeurs initiales : jointure `lung_id` → `samples` avec **`labo = 'HCL'` en dur** (vérifié : les
34 parents sont tous en base HCL avec leurs métriques → 0 `NA` côté initial). En-têtes
`Nb lignes total` / `Nb molécule` repris du threshold à la demande de Boris (« renommer comme pour
la raréfaction »), les colonnes DB gardent `nb_reads_*`.

## État (07/09/2026)

**33 lignes** (32 au listing du matin, 33 au check : le lot grossit, `Lung_106` n'a que 3
couples). BAM 33/33 · PROD 12 (Lung_100 10/10, Lung_102 2/10, Lung_104 0, Lung_106 0) ·
métriques QC + Loyfer 13 · mVAF + epic 12 (un couple a `QC/` sans `BETA/`, vague de production).
Somme des 16 epic = 1,0000 sur les 12. Relecture gsheet : **0 écart sur 578 (mVAF) + 1768 (Prop)
cellules**. `compact()` testé sur copie : table + PK préservées.

## Gotchas / observations données

- `Lung_100_Healthy_84` : 55,5 M reads contre ~106 M pour les autres Lung_100. C'est la règle
  du `LOG/{couple}.dilution_lung.log` : le lung est ramené au nombre de molécules du healthy
  (Healthy_84 = 27,7 M). Le LOG donne les molécules de chaque parent — **hors scope** pour
  l'instant (« nombre de reads apporté par chaque parent non traité »), mais la source existe.
- Les mVAF dilués de Lung_100 valent `0,0000` sur 8/10 alors que le parent vaut `0,0023` —
  donnée, pas bug (fichiers relus).
- `rarefaction_horaire_threshold` est passée de 308 à 1564 lignes entre le 03/09 et le 07/09
  (check relancé hors de cette session).

Tag `checkpoint-pre-dilution-lung` (sur `bbd1027`), backup
`samples_status.backup-pre-dilution-lung-20260907_070739.duckdb`.

Liens : [[project_schema_v32_rarefaction_horaire_threshold]] (le calque réel),
[[project_schema_v9_dilution]] (PK simple, `_read_props`),
[[project_schema_v28_rarefaction_horaire]] (`_bootstrap_means`, helper d'export),
[[project_probs_bootstrap_mode]].
