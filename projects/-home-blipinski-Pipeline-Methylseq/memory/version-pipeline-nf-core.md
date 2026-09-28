---
name: version-pipeline-nf-core
description: Methylseq = clone nf-core/methylseq v4.2.0 ; dépôt aligné sur master upstream le 2026-09-18, état antérieur sauvegardé sous le tag v4.2.0-aima
metadata:
  type: project
---

`~/Pipeline/Methylseq` (remote `github.com/aima-dx/Methylseq`) est un clone de
**nf-core/methylseq v4.2.0** — release upstream du 2025-12-05, tag `5aa5646`.
C'est la version du workflow **TAPS** (modules `rastair`, subworkflows
`bam_taps_conversion` et `fastq_align_dedup_bwamem`), d'où le `--taps --aligner bwamem`
de `launch.sh`.

C'est le pipeline qui a servi aux analyses short-read du couloir
`NF_Watchmaker_Methylseq` / `NF_Methylseq` (cf. [[../-home-blipinski/memory/context/short-read]]).
⚠️ **La période de ces analyses n'est tracée nulle part dans le dépôt** — ne pas la dater
sans source. Seuls repères disponibles : customisations AIMA modifiées le **2026-02-27**,
commit `initial clone` du **2026-03-03**, fichiers upstream datés du **2026-02-05**.

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

Seuls 3 fichiers divergent, et ils sont restés intacts lors de la sync du 2026-09-18 :

- `nextflow.config` — `workDir = /scratch/nxf-work`, `cleanup = true`, `TMPDIR`/`NXF_TMPDIR`,
  + 4 profils : `scw` (S3 Scaleway fr-par, chunk 150 MB, 10 retries), `tower`,
  `local_docker` (32 CPU, `-u 0:0 -v /scratch:/scratch`), `local_singularity`.
- `conf/base.config` — `scratch = /scratch/nxf-work/`, `process_high` 24 CPU / 60 GB
  (upstream 12 / 72), `BWA_MEM` 16 CPU, `time = 6.d`.
- `launch.sh` — non-upstream : pull S3 des FASTQ `CGFL/Watchmaker` (8 samples
  Breast/Colon/Lung) puis run `--taps --aligner bwamem --genome hg38`,
  `-profile local_docker`, outdir `/scratch/methylseq/HG38reste/`.

⚠️ `launch.sh` pointe `~/Pipeline/methylseq/` (minuscule) alors que le répertoire réel est
`Methylseq` — chemin mort tel quel.

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
