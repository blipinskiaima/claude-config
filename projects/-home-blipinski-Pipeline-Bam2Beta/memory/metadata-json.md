---
name: metadata-json
description: "metadata.json — contrat de sortie unique depuis V2.2.0 : schema, 2 constructeurs exclusifs, provenance de chaque champ, gotchas"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c6971ef-9e62-46ae-935a-5026efb56aa3
  modified: 2026-08-11T08:48:12.414Z
---

# metadata.json — contrat de sortie unique

Introduit natif en **V1.3.1** (2026-05-27) dans `Raima_report`, DEPTH=merged uniquement.
Remplace le script externe `build_metadata_json.sh`. Devenu le **contrat de sortie UNIQUE en
V2.2.0** (29 champs) : `raima_score.V2.json` n'est plus produit, `metadata.json` en est un
sur-ensemble strict.

## Schema d'origine (10 champs, trace-platform)

`client_uuid`, `analysis_name`, `patient_name` (= patient_id), `sample_name`, `nb_reads_total`,
`nb_reads_aligned`, `nb_reads_m`, `depth`, `coverage_percent`, `mvaf`, `generated_at` (ISO 8601 UTC).

## Provenance reelle de chaque champ de comptage

| champ | source |
|---|---|
| `nb_reads_total` | `BAM_Count` → `QC/Samtools/{ID}.nb_reads_total.tsv` — `samtools view -c` **sans aucun flag** |
| `nb_reads_aligned` | **cramino col 6 (`num_reads`)**, pas col 4 |
| `nb_reads_m` | `nb_reads_aligned` / 1e6, arrondi adaptatif (0/1/2 decimales) |
| `depth` | mosdepth summary col 4, ligne `total` |
| `coverage_percent` | mosdepth global.dist |
| `mvaf` | colonne `mvaf` de `raima_score.V1.4.tsv` (mVAF v1.4 depuis V2.0.0 ; avant : V2 col3 v1) |

⚠ **`nb_reads_aligned` porte un nom faux** : `num_reads` inclut les reads **NON alignees**
(effet `--ubam` de cramino). Surestimation de 12 % (Lung_9) a 22 % (Lung_Alc_79_av) du nombre de
reads reellement alignees. Voir [[read-counting-cascade]] pour la cascade complete.

## 2 constructeurs distincts et mutuellement exclusifs (2026-07-20)

| chemin | fichier | comportement |
|---|---|---|
| **nominal** | `workflow/rapport.nf` | valeurs reelles, `${var:-null}` si extraction KO |
| **degrade input-KO** | `workflow/merge.nf` process `Check_Input` | memes champs, les 5 numeriques forces a **0**, + `status="FAILED_QC_INPUT"` + `reason` |

Meme chemin S3, **jamais les deux**.

⚠ **Cote consommateur** : `status` **absent** = run nominal OK. Ne pas chercher
`status=="SUCCESS"`, il n'existe pas. Un consommateur qui lirait `nb_reads_total` sans tester
`status` interpreterait un echec de QC d'entree comme un sample a 0 read.

⚠ **Duplication de schema** : les params `client_uuid` / `analysis_name` / `patient_name` sont
ecrits dans les DEUX blocs → toute evolution du schema doit toucher `rapport.nf` **et**
`merge.nf`.

## Gotchas

- **`.combine(by: 0)` et PAS `.join`** pour broadcaster `nb_reads_total` (1 fichier/sample) sur
  les N entrees `combined_results` (1/depth) — sinon N-1 entrees droppees. TEST OK bit-a-bit
  vs V1.3.0.
- **Aucun script de conformite ne verifie les champs de comptage** : `check-run-output.sh` ne
  teste qu'existence + taille non nulle. Les 3 champs `nb_reads_*` ne sont jamais qualifies
  (constat 2026-08-11).
