---
name: project-qc-status-retro-backfill
description: Rattrapage rétrospectif des statuts QC v34 (44 NULL → 10) + génération des qc_status.tsv / sequencing_time.tsv sur la plateforme. ⚠⚠ --RETRO_REPORT republie AUSSI metadata.json et y perd version_raima ; le flag RETRO_QC_ONLY isole le seul TSV.
metadata: 
  node_type: memory
  type: project
  originSessionId: b7e6f1b9-aa8b-4be9-8a7c-f455327f7263
  modified: 2026-09-18T10:09:45.823Z
---

# Rattrapage rétrospectif des statuts QC (17/09/2026)

Combler les `exis_qc_status` / `themelio_qc_status` manquants (schema v34) sur les samples
arrivés après le backfill du 08/09, puis porter la même information sur le bucket plateforme.

## ⚠⚠ `--RETRO_REPORT` écrit DEUX fichiers, pas un

Le module lance `QC_status` **puis** `Raima_report`. Le second republie
`REPORT/metadata.json` — et comme il force `raima_version.txt` à un fichier vide,
le JSON régénéré sort avec **`version_raima: null`** alors que l'original portait `v0.5.6`.

Constaté après coup sur les 34 samples RetD relancés : listing S3 exhaustif → exactement
**2 objets modifiés par sample**, `QC/{s}.qc_status.tsv` (créé) et `REPORT/metadata.json`
(réécrit, 29 → 33 champs). Non restaurable : versioning du bucket `Suspended`, et la valeur
n'est nulle part dans les logs (elle vient de `packageVersion("raima")` au runtime du
container). Sans gravité en R&D — les 1352 samples backfillés le 08/09 sont déjà dans cet
état, et trace-prod ne lit jamais `version_raima` (0 occurrence) — mais **inacceptable sur
un bucket client**.

**Le réflexe** : avant tout retro sur un périmètre client, lire le `publishDir` de chaque
process du workflow, pas seulement celui qu'on croit lancer.

## Le flag `RETRO_QC_ONLY` (patch Bam2Beta, non commité au 17/09)

```groovy
// workflow/retro_report.nf
QC_status(...)
if (!params.RETRO_QC_ONLY) {          // ← saute Raima_report
    report_full = ...
    Raima_report(report_full)
}
// nextflow.config : RETRO_QC_ONLY = false
```

`QC_status` ne déclare qu'un output (`${ID}.qc_status.tsv`) → **un seul fichier publié**,
neuf. Vérifié par snapshot S3 avant/après sur les 10 samples plateforme :
`162 → 164 objets, 0 modifié, 0 supprimé` (le 2ᵉ ajout est le marqueur de dossier `QC/`).

⚠ Le même piège guette `Read_Start_Time` : son `publishDir` a `pattern: "${ID}.*_time.tsv"`,
qui matche **`read_start_time.tsv` (1,6 Go) ET `sequencing_time.tsv`**. Un retro via ce
process réécrirait le gros fichier.

## ⚠ Ne jamais lancer un retro avec `-profile liquid`

`conf/liquid.config` met `MERGE EXIS CNV FRAG ICHORCNA IV TOO THEMELIO RAPPORT MITO = true`
→ relance du pipeline complet. Le module retro est un `if` indépendant dans `main.nf` et tous
les modules sont `false` par défaut : lancer **sans profil métier**, `-profile docker,scw`.

⚠ Et le module retro (`e988b21`, 08/09) **n'est pas dans le tag `V2.3.0`** (02/09) que le
launcher de prod utilise via `-r $VERSION` → passer par `-r main` ou le `main.nf` local.

## Résultat R&D : 44 NULL → 10

34 samples comblés (24 CGFL : 17 `Bladder_Urine_02_*` + 7 `Twist_*_rep_4` ; 10 HCL :
`Healthy_183-187` + `Routine_1-5`), puis `update-column exis_qc_status liquid {labo}`
(n'importe laquelle des 4 clés met à jour les 4 colonnes).

**Les 10 restants ne sont pas rattrapables** :
- 6 CGFL — `26BM01841`, `26BM03032`, `ANG-CA-11081963`, 3 × `Ma_SAB_12-1958_Run_*` :
  leur dossier RetD **ne contient plus que 28 marqueurs de dossier à 0 octet**, aucun fichier,
  alors que la base garde leurs métriques. Explication trouvée en explorant trace-platform :
  ces samples ont été **traités sur la plateforme** (`aima-platform`), leur sortie RetD a été
  nettoyée. Ne pas chercher un bug d'extraction.
- 3 HCL `Twist_*_rep_4` : `Bam2Beta.failed`, dossier réduit à `LOG/`.
- 1 HCL `Healthy_26_rebasecalled_V4.3.0` : pas de dossier `THEMELIO/`.

## Plateforme : 9 samples sur 51, et c'est structurel

Sur les 51 samples `case=PROD` du bucket `aima-platform`, **seuls les 9 en V2.3.0**
(client `c88556a5-…`, Imagenome Labosud) ont les 10 fichiers d'entrée. Les 42 autres
(V1.0.x → V2.0.2) n'ont ni `QC/Samtools/{s}.idxstats.tsv`, ni `{s}.n50_ratio.tsv`, ni
`Fragmentomics/filtered_softclipped/{s}.amplitude_fragmento_qc.tsv` : **les mesures d'entrée
de l'arbre n'existent pas**, le calcul est impossible même rétrospectivement. Inutile de
chercher un contournement — c'est une limite de données, pas d'outillage.

⚠ Leur `metadata.json` reste à **29 champs** (choix assumé) → côté trace-platform la source
des 4 statuts doit être **le TSV**, jamais le JSON. Divergence volontaire avec trace-prod.

## `sequencing_time.tsv` — 8 fichiers préexistaient

Un scan exhaustif des 1408 samples liquid RetD a trouvé **8** `sequencing_time.tsv`, tous
les `Twist_*_rep_3`, tous datés du **08/09 13:48-14:03** (jour du dev du chemin rapide v34)
et tous à `69h07m / no`. Fabriqués à la main pour tester la lecture — le pipeline ne les
produisait pas à cette date. ⚠ Le chemin rapide de `scan_read_start_time()` **les lit en
priorité** sur le balayage : un `update-column sequencing_time` sur ces 8 samples reprendra
ces valeurs sans les vérifier.

10 fichiers ont été créés sur la plateforme (les 9 + `TEST_V230_THEMELIO`) par balayage du
`read_start_time.tsv` déjà présent, **sans relire le BAM** : script jetable
`seqtime_platform.py` (scratchpad, non versionné) qui importe
`BaseChecker.scan_read_start_time` de trace-prod — aucune réimplémentation — et fait **un
seul `put_object`** précédé d'un `head_object` de garde. 10 Go lus en 1 min,
diff S3 `164 → 165, 1 ajout, 0 modifié` sur chacun.

Valeurs : `79h56m` sur les 9 (même `run_id` `ccfa21b3-…`, barcodes 10-18, une seule flow
cell) et `71h55m` sur le sample de test. ⚠ `multi_run = NA` parce que **deux formats de
timestamp coexistent dans le même fichier** — 5,22 M reads en `…52.602876+02:00` et 30 683
(0,58 %) en `…25+00:00`, sans fraction et avec un autre offset. Décision Boris : on est en
mono-run, ne pas porter `multi_run` côté plateforme.

**38 trous `sequencing_time` restent en R&D** (28 CGFL + 10 HCL, tous avec
`read_start_time = OK`), comblables par `update-column sequencing_time liquid {labo}`
(~95 Go, ~10 min). Les 3 `Twist_*_rep_4` HCL sont perdus (dossier vide).

## ⚠ Bug de perf repéré dans trace-platform

`_STAGE_CONTENT_SUFFIXES` (`check_platform.py:165`) contient `".tsv"` **générique**, et le
dossier `QC/Samtools/` contient `read_start_time.tsv` à **1,6 Go** → il est téléchargé
intégralement à **chaque `check` de sample**. C'est exactement le piège que le commentaire
au-dessus de la constante documente pour `.read_lengths.csv` (contourné par le suffixe
complet `.themelio_predictions.csv`), mais `.tsv` est resté large.

## Méthode à rejouer pour toute écriture sur un bucket de prod

1. snapshot `aws s3 ls --recursive` (clé + taille + date) **avant**
2. exécuter sur **un seul** sample
3. re-snapshot → `diff` : exiger **0 ligne `<`** (aucune modification)
4. seulement ensuite, le reste du lot

C'est ce qui a permis de garantir l'innocuité sur la plateforme après que le cas
`metadata.json` a montré qu'une analyse du code ne suffit pas.

Liens : [[project_schema_v34_qc_status]] (les 4 colonnes),
[[project_schema_v30_v31_sequencing_time]] (l'algorithme et ses pièges),
[[feedback_scratch_workspace]] (script jetable hors repo).
