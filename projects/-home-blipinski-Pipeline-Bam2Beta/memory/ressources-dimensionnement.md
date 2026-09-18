---
name: ressources-dimensionnement
description: "Dimensionner cpus/memory des process : mecanique docker reelle, censure de peak_rss, risque numerique de task.cpus sur les process raima, plafond != allocation"
metadata:
  node_type: memory
  type: project
---

# Dimensionnement cpus / memory (2026-09-09/11)

Right-sizing de `conf/base.config` a partir de ~5 500 taches mesurees (46 traces, cf.
[[perf-exis-traces]]).

## Ce que Nextflow passe reellement a docker

Verifie dans un `.command.run` :
`docker run -i --cpu-shares 2048 --memory 8192m --ulimit nofile=65536:65536 …`

| Directive | Effet reel |
|---|---|
| `memory` | **`--memory` = plafond DUR**. Depassement -> OOM kill `exit 137` -> retry avec doublement. |
| `cpus` | **`--cpu-shares` = poids relatif, AUCUN plafond**. Un process peut consommer plus que declare. |

Consequences : sur-allouer la RAM **bloque l'ordonnancement** (l'executeur local gate sur
`executor.memory`, defaut = RAM totale) ; sous-allouer coute 2 attempts. Cote CPU, la directive
ne sert qu'a la **comptabilite d'admission** : les scripts R CNV consomment 5,5 a 7 coeurs pour
2 declares et volent des coeurs pendant la phase saturee.

## ⚠ `peak_rss` est CENSURE par le plafond

Aucune tache des 5 500 n'excede jamais son allocation : le cgroup force le reclaim avant.

```
ratio peak_rss/alloc  <<  100 %   ->  sur-allocation PROUVEE, reduction sure
ratio                  ~= 100 %   ->  INDECIDABLE (bien dimensionne OU sous pression)
```

Ne jamais conclure "bien dimensionne" depuis un ratio eleve. `IV_call` etait a 100 % de 8 Go
**avec 2 `exit 137` reels** -> passe a 16 Go. `Raima_score_mVAF` touchait 16,0 Go sur 16.

## ⚠ Risque numerique : `task.cpus` -> `--ncores` sur les process raima

`Raima_process_loyfer` et `Raima_score_mVAF` passent `-c/--ncores ${task.cpus}` a raima, qui
fait `data.table::setDTthreads(ncores)`. Or raima agrege en **flottant** :
`sum(mod_qual - 0.001953125)` (`bedmethyl_prob`, `bootstrap_model_v1`) et `mean(meth_sum)`.
Ces sommes sont **sensibles a l'ordre** — c'est d'ailleurs la raison d'etre du tri deterministe.

=> **changer les `cpus` d'un process raima peut changer une sortie qualifiee**
(mVAF v1.4/v1.5, `props_loyfer.tsv` -> TOO, THEMELIO, `metadata.json`).
data.table affecte des groupes entiers par thread, donc c'est *probablement* stable, mais
**VERIFIE le 2026-09-18** : la qualif V2.3.1 a compare Healthy_826 + Lung_9 a 8 cpus contre la QUALIF
V2.3.0 produite a 4 -> mVAF v1.4 (0.58), fragmento, les 5 probas TOO, le sexe et themelio_score
(0.855261) **strictement identiques**. Le risque est leve POUR `Raima_score_mVAF` seul ;
`Raima_process_loyfer` (4 cpus) n'a pas ete soumis au meme A/B. Protocole si besoin (`ncores=4` vs `8`,
comparaison des TSV) avant tout changement.

Les process qui n'utilisent PAS `task.cpus` dans leur script (`Check_Input`, `Raima_report`,
`IchorCNA_*`, `Mito_qc`) sont sans risque : la directive n'y est que comptable.

Durcissement possible non applique : figer `--ncores` independamment de `task.cpus`.


## ⚠⚠ DEUX MACHINES, DEUX PROFILS — la lecon de V2.3.2 (2026-09-18)

| profil | machine | lanceur | plafonds |
|---|---|---|---|
| `prod` | **plateforme client, 8 cpus / 32 Go** (31,3 vus par NF) | `dev/PLT/Bam2Beta_SCW_plateforme.sh` | `cpus_max=8`, `memory_max=24.GB`, `executor.cpus=8` |
| `liquid` | **serveur de calcul, 32 cpus / 125 Go** | `dev/SCW/*.sh` (`-profile ...,$TYPE,...`) | `cpus_max=32`, `memory_max` herite |

Le right-sizing de V2.3.1 a porte `prod.config` a 16 cpus / 48 Go **d'apres des traces prises sur le
serveur de calcul**. Resultat en production : `Process requirement exceeds available memory --
req: 40 GB; avail: 31.3 GB` sur `BAM_sort`. Le commentaire d'en-tete de `prod.config` disait
pourtant deja « CPU max 8, RAM max 32GB » — il n'a pas ete lu.

- **`BAM_sort` consomme `task.cpus x samtools_memory`** : 33,3 Go mesures a 16 cpus (`-m 2G`),
  ~16 Go a 8. Baisser ses cpus baisse sa RAM d'autant — ce n'est pas une privation.
- **Sur-allocations revelees par les peak_rss de la QUALIF V2.3.1** (trace S3, `{sample}/LOG/`) :
  `Raima_score_mVAF` 10,3 Go pour 32 alloues, `Raima_process_loyfer` 13,7/16, `Mosdepth_qc` 10,5/16.
- **`executor.cpus` de `conf/base.config` vaut 32 pour TOUS les profils** : a override par profil,
  sinon NF admet 4x trop de taches sur la machine de prod (seul le gate memoire l'en empeche).
- ⚠ **Ne jamais reporter des mesures d'une machine vers les plafonds de l'autre.** Toute trace
  analysee doit etre rattachee au profil qui l'a produite.

## Plafond != allocation

```groovy
cpus = { Math.min( N * Math.pow(2, task.attempt-1), params.cpus_max ) }
                   ▲ decide au 1er essai        ▲ n'ecrete que les RETRY
```

Monter `cpus_max` **ne donne aucun coeur de plus au 1er essai** — il faut changer le `N` du
bloc `withName`. Plafonds : defaut 10 / 125 Go, `prod` 16 / 48 Go, `liquid` 32 / herite.
⚠ **`params.cpu` n'existe pas** : le `--cpu 32` de `dev/SCW/Bam2Beta.sh` est un **no-op**
(renomme `cpus_max` en V1.0.1). Le lanceur prod utilise le profil `liquid`, pas `prod`.

## Piege vecu : ternaire memory incoherent

`Mosdepth_qc` avait `memory = { (8.GB * …) < memory_max ? (16.GB * …) : memory_max }` — test a
8, valeur rendue a 16. Corriger "dans le sens evident" (8 partout) aurait tue **54 % des taches
mosdepth** (moyenne mesuree 7,8 Go, max 11,5 Go). Audit : 1 incoherence sur 40 blocs.

## Etat applique le 2026-09-11 (commit `0856f3f` + suite)

Correctifs : `Mosdepth_qc` ternaire coherent a 16 Go (cpus 4->2) · `IV_call` 8->16 Go ·
`Raima_score_mVAF` 16->24 Go (puis 8 cpus/32 Go par Boris ; **A/B fait a posteriori par la qualif V2.3.1, sans ecart**).
Sur-allocations ramenees a 2 Go : `BAM_mergering` (24), `BAM_index` (16), `BAM_Subsampling` (8),
`Modkit_pileup_28M` (8), `TOO_score` (8), `IchorCNA_run` (8), `BAM_Count`/`Preprocess_28M`/
`Check_Input`/`Raima_report`/`IchorCNA_readCounter`/`THEMELIO_score` (4) et les 7 process CNV.
Phase MERGE montee a 16 cpus : `BAM_sort` 40 Go, `BAM_mergering` 8 Go, `BAM_index` 4 Go.

**Non touche volontairement** : `Raima_process_loyfer` (cpus laisses a 4 — risque `ncores`).

## Contexte machine

32 coeurs / 125 Go, `executor { queueSize = 16 ; cpus = 32 }`. Boris fait tourner **jusqu'a 9
runs Nextflow simultanes** (load observe : 119) — chaque Nextflow croit disposer des 32 coeurs,
il n'y a **aucune coordination inter-runs**. Les runs concurrents sont tous `--MERGE false` :
la phase MERGE, elle, est toujours mono-sample, d'ou l'interet de la muscler.
