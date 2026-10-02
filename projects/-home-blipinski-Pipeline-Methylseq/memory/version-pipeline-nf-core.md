---
name: version-pipeline-nf-core
description: "Methylseq = clone nf-core/methylseq v4.2.0 aligné sur master (tag v4.2.0-aima = avant sync) ; écarts AIMA, dates des runs batch1/batch2, pièges index iGenomes et relance partielle"
metadata:
  node_type: memory
  type: project
  originSessionId: 08f7a23b-e69f-4f22-a31a-236ff313703e
  modified: 2026-10-02T13:14:36.478Z
---

`~/Pipeline/Methylseq` (remote `github.com/aima-dx/Methylseq`) est un clone de
**nf-core/methylseq v4.2.0** — release upstream du 2025-12-05, tag `5aa5646`.
C'est la version du workflow **TAPS** (modules `rastair`, subworkflows
`bam_taps_conversion` et `fastq_align_dedup_bwamem`), d'où le `--taps --aligner bwamem`
de `launch.sh`.

C'est le pipeline qui a servi aux analyses short-read du couloir
`NF_Watchmaker_Methylseq` / `NF_Methylseq` (cf. [[../-home-blipinski/memory/context/short-read]]).
Dates des runs (source : `pipeline_info` publiés sur S3) : **batch1 = 26-27/02/2026** (16 samples,
14 lancements `-resume` depuis `~/Run3`) ; **batch2 = lots 2_1 à 2_4, 28/09 → 30/09/2026** (48 samples).
Sorties : `s3://aima-bam-data/processed/short-read/Methylseq/batch1|batch2_N/` — détail [[qc-export-methylseq]].

## Historique du dépôt (au 2026-09-18)

```
200b5cb  initial clone                  (2026-03-03, 1 commit orphelin, arbre partiel)
c17d5dc  track the untracked configs    ← tag v4.2.0-aima  = SAUVEGARDE, état local d'avant
64121ef  sync CI workflows (cc11bd9)    ← HEAD = main, aligné sur nf-core master
```

- `c17d5dc` ajoute les 32 fichiers que `initial clone` n'avait jamais pris
  (`.github/`, `.gitignore`, `.nf-core.yml`, `.pre-commit-config.yaml`, `.devcontainer/`,
  `.vscode/`, `.prettier*`, `.gitattributes`). Avant ça, l'arbre git ≠ le disque.
- `64121ef` applique les 2 seuls commits que master a au-dessus de la release 4.2.0
  (PR #621 : `pull_request_target` → `pull_request`, `permissions: {}`, poster de
  commentaires unique `pr-comment.yml`). **GitHub Actions uniquement** — aucun process,
  module, subworkflow ni config de pipeline touché. Comportement d'exécution identique.

Retour arrière : `git checkout v4.2.0-aima` (tag annoté, poussé sur origin).

**4.2.0 reste la dernière release taguée upstream.** Veille sans rien télécharger :
`git -C ~/Pipeline/Methylseq ls-remote --tags --refs upstream | tail -3`
(remote `upstream` = nf-core/methylseq, push bloqué à `no_push`).

## Écarts AIMA vs upstream — à préserver sur toute future sync

3 fichiers upstream divergent (intacts lors de la sync du 2026-09-18), + 1 ajout AIMA
(`methylseq_qc.py`, export QC → [[qc-export-methylseq]]) :

- `nextflow.config` — `workDir = /scratch/nxf-work`, `cleanup = true`, `TMPDIR`/`NXF_TMPDIR`,
  + 4 profils : `scw` (S3 Scaleway fr-par, chunk 150 MB, 10 retries), `tower`,
  `local_docker` (32 CPU, `-u 0:0 -v /scratch:/scratch`), `local_singularity`.
- `conf/base.config` — `scratch = /scratch/nxf-work/`, `process_high` 24 CPU / 60 GB
  (upstream 12 / 72), `BWA_MEM` 16 CPU, `time = 6.d`, + `TRIMGALORE` 12 CPU / 8 GB (2026-09-28 :
  le module plafonne `--cores` à 8 = cpus−4 → même commande, 2 trims en parallèle, ~−1 h par lot).
- `launch.sh` — non-upstream : **journal de commandes** des lots WM batch2 (copie FASTQ
  `s3://aima-pod-data/data/CGFL/WM/` → `/scratch/methylseq/data/`, `nextflow run` par lot avec
  `samplesheet_lotN.csv`, outdir `/scratch/methylseq/batch2_N/`, sync S3). Chemins en `Methylseq` (corrigé).
  ⚠ ne pas l'exécuter en entier : `BWA_INDEX=` vide (l. 9), `sync --recursive` invalide, `rm -rf` des FASTQ locaux.

## Piège : index BWA = bucket public AWS iGenomes

`--genome hg38` tire l'index BWA de `s3://ngi-igenomes/.../UCSC/hg38/.../BWAIndex/version0.6.0/` (AWS).
Le profil `scw` redirige tous les `s3://` vers Scaleway → introuvable. Copie locale :
`/scratch/dependencies/genomes/hg38/BWAIndex_igenomes/` (`--bwamem_index`). Réf = 195 contigs,
3 099 922 541 pb, sans `_alt` — identique aux BAM ONT MinKNOW (≠ `hg38.fa` local de 3,21 Gb).

## Piège : impossible de relancer une seule étape sur des samples traités

Pas d'entrée BAM (samplesheet = FASTQ seulement) et `cleanup = true` vide les work dirs →
`--run_qualimap -resume` sur un sample déjà fait recalcule tout depuis les FASTQ. Pour du QC a
posteriori : outil direct sur le BAM dédupliqué (cf. `methylseq_qc.py`).

## Faille ouverte

Token Seqera Tower en clair et commité dans `nextflow.config` → [[secret-token-tower-expose]].

## Piège : `--trim_OT` / `--trim_OB` sont inertes (v4.2.0)

Déclarés dans `nextflow.config` (défaut `'0,0,10,0'`) et dans `nextflow_schema.json`, ils
n'alimentent que `ext.args` de `RASTAIR_CALL` (`conf/modules/rastair_call.config`, commentaire
« Pending the resolution of the mbiasparse process »). Or le module `rastair/call` définit
`args` et **ne l'utilise jamais** : il fait `meta.trim_OT ?: parsed_trim_OT`, et `meta.trim_OT`
n'est rempli nulle part (pas de colonne dans `schema_input.json`, aucune injection dans les
workflows). Donc le call prend **toujours** les valeurs du `MBIASPARSER` du run, et passer
`--trim_OT` en CLI n'a aucun effet. Pour forcer des valeurs : `rastair call` hors pipeline.
Vérifié par lecture de code — `cleanup = true` efface les `.command.sh` et l'index des tâches,
`nextflow log <run> -f script` ne renvoie plus rien après un run réussi.
