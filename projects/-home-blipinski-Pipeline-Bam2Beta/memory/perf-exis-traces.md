---
name: perf-exis-traces
description: "Analyse de perf du module EXIS (2026-09) — les traces Nextflow vivent sur S3, Raima_score_mVAF pese 74-81% du wall-clock, structure interne de bootstrap_model_v1"
metadata:
  node_type: memory
  type: project
---

# Performance du module EXIS (2026-09-09/11)

Analyse menee sur **46 traces reelles**, sans relancer un seul run.

## Ou trouver les traces (le point non evident)

`nextflow.config` a `trace/report/timeline/dag` tous a `enabled = false`. **Mais les lanceurs
passent `-with-trace -with-report -with-timeline -with-dag` en ligne de commande** :
`dev/SCW/Bam2Beta.sh`, `Bam2Beta_qualif.sh`, `Bam2Beta_relaunch.sh`, `dev/PLT/*`,
`skills/qualif-bam2beta/scripts/run-qualif.sh`.

=> **chaque run prod/qualif depose une trace complete (39 colonnes) sur S3** :
`{output}/{SAMPLE}/LOG/{SAMPLE}_Bam2Beta_trace_{date_tag}.txt`

Couverture : les 16 versions de `QUALIF/`, et la majorite des ~1 370 dossiers
`RetD/liquid/{CGFL,HCL}`. Les runs lances a la main (sans ces flags) n'en produisent pas, et
`cleanup = true` purge le `workDir`, donc **pas de `.command.trace` en local** : S3 est la
seule source fine. Colonnes utiles : `realtime`, `%cpu`, `peak_rss`, `read_bytes`,
`write_bytes`, `attempt`, `submit`/`start`/`complete`.

## Ou passe le temps

`Raima_score_mVAF` (ex `bootstrap_model`) = **74 a 81 % du wall-clock EXIS**, constant sur
7 samples de 0,4 a 44 Go de BAM, sur les architectures V2.2.0 **et** V2.3.0.

| Sample | wall EXIS | mVAF | part | queue mono-tache |
|---|---:|---:|---:|---:|
| Bladder_175 (44 Go) | 4 257 s | 3 410 s | 80 % | 2 630 s |
| Lung_9 (17 Go) | 1 612 s | 1 300 s | 81 % | 963 s |
| Healthy_826 (0,05 Go) | 367 s | 285 s | 78 % | 207 s |

Pendant la queue, **une seule tache a 4 cpus tourne sur 32 coeurs = 12 % de la machine**,
sur 30 a 62 % du wall-clock. Le fan-out a 22 (`Preprocess_28M` / `Modkit_*`) est la **seule**
phase saturee (32/32 coeurs) : rien a y gagner. La phase MERGE est a l'oppose : mediane
**40 % du run total** a ~12 % d'occupation (1 tache a la fois).

## Pourquoi mVAF est lent : la structure de `bootstrap_model_v1`

```
PARENT (1 thread)                              4 WORKERS (future multisession)
  ├─ sample() sous with_seed(1)
  ├─ agregation data.table
  ├─ bigreadr::fwrite2(tempfile())  ─────────►  model_v1(fichier)
  └─ x 200 iterations, EN SERIE                 seed = NULL
```

- Les **tirages sont faits dans le parent** sous `with_seed(seed=1)`, les futures portent
  `seed = NULL` => **`ncores` ne change PAS les tirages**.
- Les 200 `fwrite2` expliquent l'amplification d'ecriture : Lung_9 ecrit **142,6 Go** pour
  1,88 Go de bgzf en entree (= 713 Mo x 200). Bladder_175 : 257 Go. ⚠ risque de saturation
  de `/scratch`.
- **L'efficacite CPU s'effondre quand le sample grossit** : 3,83 coeurs/4 sur le sample a
  4 min, **1,57 coeurs/4** sur celui a 57 min. Moyenne 2,20/4 (55 %). Les workers attendent
  le parent => **monter `ncores` ne sert a rien** (piste explicitement abandonnee).

## Le seul levier dans notre code : la boucle de tri

`workflow/beta_28M.nf` (bloc `script:`, ~ligne 166) trie les 22 bgzf **en serie** :
`zcat | sort | gzip -c`. Le tri est **obligatoire** (ordre non deterministe de
`modkit extract full` + somme flottante en aval, cf. [[bootstrap-model-v1]]).

Mesure sur chr20 de Lung_9, meme machine, meme container :

| variante | temps | md5 du contenu decompresse |
|---|---:|---|
| actuelle (`sort` nu, `gzip`) | 10,82 s | `6c817755…` |
| `sort -S 2G --parallel=4` | 8,75 s | identique |
| `+ gzip -1` | **4,96 s** | identique |

Le `gzip` pese plus que le tri. Extrapolation Lung_9 : boucle ~390 s des 1 300 s du process
(~30 %), ramenable a ~50-90 s avec `xargs -P` (present dans le container ; `pigz` **absent**).
Cout de la relecture par le R : +0,19 s/chromosome (zcat 1,62 -> 1,81 s), soit ~4 s sur 22.
**Non applique** au 2026-09-11.

Le reste (~900 s) est le parent serialise de `raima`, hors de notre portee.

Voir [[ressources-dimensionnement]] pour la lecture des colonnes `%cpu`/`peak_rss`.
