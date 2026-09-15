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
  parsés par `split_couple()` (regex `^(Lung_.+?)_(Healthy_.+?)_(\d+)_(\d+)$`, rejette `LOG`, accepte les parents rebasecalled).
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
| `mVAF` | **24** (17 -> 21 le 10/09 -> 24 le 15/09) | `ID complet` (= `sample_name`, déjà concaténé) · `ID Lung` · `ID Healthy` + **un triplet par métrique** parent lung / parent healthy / dilué (`Nb lignes total`, `Nb molécule`, `Depth`, `Coverage`, `mVAF v1.4`, `mVAF v1.5`, suffixes ` lung` / ` healthy` / ` dilution`). Les `% Lung` / `% Healthy` (toujours 50) ont été **retirés de l'onglet**, pas de la base. Puis 3 colonnes en **fin de tableau** (schema v36, 15/09) : `Mode1`, `Mode2`, `Frag Score v2` |
| `Prop` | 52 | 5 identité + 47 probs, en-têtes nus, **point** décimal |

Valeurs initiales : deux jointures `lung_id` et `healthy_id` → `samples` avec **`labo = 'HCL'` en dur**
(vérifié le 10/09 : 9 lungs + 68 healthys, dont le rebasecalled, tous en base HCL → 0 `NA` côté parents). En-têtes
`Nb lignes total` / `Nb molécule` repris du threshold à la demande de Boris (« renommer comme pour
la raréfaction »). Depuis le refactor v34 (`19923c1`, 08/09) les colonnes DB s'appellent aussi
`nb_lignes_total_dilution_lung` / `nb_molecule_dilution_lung` (renommage global, toutes tables).

## État (15/09/2026, lot CLOS)

**220 lignes** = le plan complet de `Bam2Beta/early_lung_dilution_pairs_original.tsv`
(22 lungs × 10 healthys, aucun doublon, aucune paire hors plan). **BAM, PROD, mVAF v1.4/v1.5,
Mode1/Mode2/Frag Score v2, probs epic et Loyfer : 220/220** — aucune valeur manquante,
0 ligne sans identité, 0 ligne fantôme `LOG`. Somme des 16 epic = 1,0000.
Relectures gsheet successives : 0 écart (578 puis 1768, 5304 cellules).
`compact()` testé sur copie : table + PK préservées.

Montée en charge (07/09 → 15/09) : 33 → 41 → 67 → 74 → 89 → 107 → 196 → 220 lignes ;
PROD 12 → 15 → 24 → 26 → 69 → 91 → 181 → 220. Le lot a grossi **pendant** tout le suivi :
aucun décompte intermédiaire n'était définitif, la routine « nouveaux + PROD KO puis exports »
rattrape à chaque passe.

## Génération des BAM — deux pièges qui ont coûté cher

La boucle de génération (hors repo, `~/Run/dl/gen.sh`) teste la présence du BAM avec
`aws s3 ls "{prefix}/BAM/{name}.merged.bam"`. ⚠⚠ **`aws s3 ls` matche par PRÉFIXE** : un `.bai`
orphelin suffit à déclencher un faux `[SKIP]`. `Lung_141_Healthy_111` est resté invisible deux
jours pour cette raison (dossier créé avec l'index seul). **`aws s3api head-object` teste la clé
exacte** — c'est lui qu'il faut.

⚠⚠ Sa purge des BAM stagés balaie **tout** `/scratch/nxf-work`, pas le workdir de la boucle.
Deux boucles lancées sur un même parent se suppriment mutuellement le fichier en cours de
lecture → `Failed to open file "lung.merged.bam"`. A tué 3 paires. Correctif : un `-w` dédié
par boucle **et** la recherche limitée à ce `-w`. ⚠ Un `-w` dédié ne protège que des autres
boucles corrigées : une boucle restée sur la version non restreinte efface quand même tout,
y compris à l'interruption (son nettoyage tourne après le `Ctrl-C` du run).

## Schema v36 (15/09/2026) — 3 métriques fragmentomiques softclipped

`frag_mode1_sc_dilution_lung`, `frag_mode2_sc_dilution_lung`, `frag_score_v2_sc_dilution_lung`
(VARCHAR, virgule préservée). **Aucun code d'extraction écrit** : `extract_metrics` appelle les
`check_frag_mode1_sc` / `check_frag_mode2_sc` / `check_frag_score_v2_sc` de `BaseChecker`,
exactement comme `RarefactionChecker` le fait déjà. Sources
`Fragmentomics/filtered_softclipped/{s}.fragmentomics_modes.tsv` (`cols[0]`/`cols[1]`) et
`.fragmentomics_score.V2.tsv` (`cols[0]`).

**Export** : 3 colonnes en fin de l'onglet `mVAF` (positions 22/23/24). `Mode1`/`Mode2`
**arrondis à 2 décimales** (choix Boris, cohérent avec `ROUND2_HEADERS` en liquid et avec les
exports `Dilution`/`Rarefaction` qui ont leurs propres constantes) ; `Frag Score v2` en pleine
précision. Le helper partagé `_export_rarefaction_horaire` a reçu un paramètre optionnel
`round2_cols=frozenset()` — les 4 autres appelants (horaire et threshold, mVAF et Prop) sont
inchangés, vérifié par ré-export (16 et 52 colonnes identiques).

⚠ **Les 3 colonnes ne se remplissent pas en même temps** : les 3 `update-column` enchaînés à
06:20 / 06:33 / 06:39 ont vu 144, 149 puis 152 couples renseignés. Les 8 couples partiels ont
tous eu leur `fragmentomics_modes.tsv` écrit sur S3 **entre les passes** (06:30 à 06:42) —
décalage de production, pas un bug, même mécanique que [[feedback_probs_loyfer_lag]]. Hors ces
8, cohérence parfaite : 144 couples avec les 3 valeurs, 68 sans aucune.
⚠ Un `update-column-dilution-lung` sur les 220 prend **~5 min par colonne** (lecture S3
séquentielle, le `-j` n'est pas utilisé par la branche metric).

Tag `checkpoint-pre-dilution-lung-frag` (sur `ab3ec25`), backup
`samples_status.backup-pre-dilution-lung-frag-20260915_061747.duckdb`.

## Gotchas / observations données

- ⚠ **Les parents peuvent être des variantes rebasecalled** (`Lung_119_Healthy_34_rebasecalled_V6.0.0_50_50`, apparu le 10/09). La regex initiale `Healthy_\d+` le rejetait → ligne insérée **sans identité** (`lung_id` NULL) parce que ma routine de relance passait les nouveaux noms en `-s` sans le filtre `split_couple`. Regex élargie à `^(Lung_.+?)_(Healthy_.+?)_(\d+)_(\d+)$` (non-greedy, 89/89 noms reconnus, `LOG` toujours rejeté). Le parent `Healthy_34_rebasecalled_V6.0.0` existe bien en base HCL → valeurs initiales du lung inchangées (jointure sur `lung_id`).
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
