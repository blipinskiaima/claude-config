---
name: dilution-lung
description: "Module DILUTION_LUNG (workflow/BAM/dilution_lung.nf, 2026-09-04) — BAM dilue 50/50 lung/healthy par paire, N = min des molecules primaires, N premiers reads generes (st:Z:), verification independante Lung_100/Healthy_16, gotchas (clef read_id, set -e, --input inutilise)"
metadata: 
  node_type: memory
  type: project
  modified: 2026-09-08T07:40:34.599Z
  originSessionId: a0018c06-5782-4201-b2ab-d9705ab44ad9
---

# Module DILUTION_LUNG — dilution 50/50 lung early / healthy (2026-09-04)

Cahier des charges Boris : 22 lungs early HCL x 10 healthy HCL tires au hasard = **220 paires**
(`early_lung_dilution_pairs.tsv`, 2 colonnes tab sans en-tete, 122 healthy distincts, 141 samples
tous sous `RetD/liquid/HCL/`). Pseudo-sample `{LUNG}_{HEALTHY}_50_50`, publie sous
`--dilution_lung_output` (= `RetD/liquid/dilution_lung/`) en `{NAME}/BAM/{NAME}.merged.bam` + `LOG/`.
R&D, hors qualification. Tag rollback `pre-dilution-lung` (sur `b97fd0b`).

```
paire (LUNG, HEALTHY) ─ splitCsv du TSV ─ sources lues sous ${params.output}/{ID}/BAM/
   samtools view -F 0x900 | awk : st:Z: -> epoch (mktime - offset, TZ=UTC), tag MM, comptage  (x2, 1 passe chacun)
   N = min(primaires lung, primaires healthy)
   le plus petit : repris ENTIER (secondaires/supplementaires compris)
   le plus grand : sort (epoch, read_id) | head -n N | samtools view -N   (ramene aussi ses sec./suppl.)
   samtools merge (2 entrees triees -> sortie triee, pas de sort) + index
   verification : 2N primaires ET autant de MM que MM_small + MM_big_selectionnes, sinon exit 1
```

## Decisions (validees par Boris)

- « nb de reads » = **molecules primaires A+D** (`-F 0x900`), comme le module threshold.
- **Un seul process par paire** : decouper comptage/merge n'economiserait que l'awk, pas le
  staging S3 (~40 Go par paire) qui domine.
- **Pas de sortie `optional`** : tout doit etre genere, un sample a 0 molecule fait echouer la tache.
- **Verification methylation** demandee par Boris : sur les primaires du dilue, compte exact des
  tags MM attendus (calcule gratuitement dans le meme awk que le st:Z:).
- Destination par **param explicite `dilution_lung_output`** (garde `error` dans main.nf) : le patron
  `${params.output}_suffixe` donnerait `HCL_dilution_lung`, pas `dilution_lung`.

## Validation

- **Run synthetique local** (2 mini-BAM, profil docker) : selection par `mktime` prouvee la ou l'ordre
  lexicographique aurait pris un autre sous-ensemble ; secondaires/supplementaires conserves.
- **Lung_100 + Healthy_16 en reel** (1 h, BAM 40,7 Go) : lung 45 459 407 primaires (entier),
  healthy 50 874 907 -> 45 459 407 premiers. Verification INDEPENDANTE du module (passe complete sur le
  BAM copie en local + reconstruction depuis `QC/Samtools/{ID}.read_start_time.tsv`) : origine lue sur
  l'UUID de run du tag RG (1 UUID healthy, 2 lung), **50/50 exact, 0 ecart dans les 2 sens sur les
  45 459 407 ids healthy, MM sur 100 % des primaires**, 7 558 @RG = union sans renommage, `SO:coordinate`.
- ⚠ **La coupure tombe au milieu d'une seconde** (dernier retenu et premier exclu a l'epoch
  1770182875) : sans la clef secondaire `read_id`, le sous-ensemble changerait d'un run a l'autre.
  Meme lecon que [[bootstrap-model-v1]] et [[rarefaction-horaire]].

## Gotchas

- ⚠ **`.command.sh` tourne en `bash -o pipefail` SANS `-e`** (`conf/base.config:11`, verifie sur un
  script reel) : un `samtools` qui echoue a mi-parcours ne stoppe pas le process. `set -e` pose en tete
  du script, seul ecart au patron des modules voisins. Voir [[debugging-gotchas]].
- **`--input` reste obligatoire** (`checkIfExists` dans main.nf) alors que le module ne le lit pas :
  le lanceur passe le dossier du lung. Contrainte preexistante, Boris veut y revenir.
- **Sans `--dilution_pairs`**, le pipeline prend le TSV du depot et lance les **220 paires d'un coup**.
  Le lanceur `dev/SCW/dilution_lung.sh` ecrit un TSV a 1 paire par run, temoin d'idempotence
  = le BAM sur S3, puis purge les 2 sources stagees dans `/scratch/nxf-work` (~40 Go/paire).
- Le TSV initial fourni par Boris portait **7 paires en double** (6 lungs a 8-9 replicats) :
  regenere par lui a 220 uniques. Verifier `sort | uniq -d` avant tout lancement.
- `samtools view -N` selectionne par nom : le BAM dilue porte plus de lignes que 2N (secondaires et
  supplementaires des reads choisis), les comptes de PRIMAIRES sont exacts.
- Temps 2 = patron habituel : `--input …/dilution_lung/{NAME} --output …/dilution_lung --MERGE false
  --EXIS true`, temoin `BETA/{NAME}.merged.epic.raima_score.V1.4.tsv`.

## Dilution 480 pseudo-samples (autre chantier, ne pas confondre)

`RetD/liquid/dilution/` = 480 BAM `{TUMOR}_Healthy_{ID}_target_{X}_{Y}` du projet `~/Pipeline/Dilution`
(mai 2026, tirage ALEATOIRE `--subsample`, 3 tumeurs CGFL x 40 healthy x 4 targets). Trace documentaire
non cablee : `workflow/BAM/dilution_trace.nf` (ecrit par Boris le 2026-09-04).

Fichiers de controle de la verification : `/scratch/boris/dilution_lung_check/` (16 Go, supprimables).

## Origine des 480 dilues — preuve retrouvee (2026-09-04)

Script identifie : **`~/Pipeline/Dilution/scripts/generate_dilution.sh`** (commit `e3c38cb`), bash +
samtools 1.19.2 de l'hote, orchestre par `run_all.sh` en 12 tmux (2026-05-22 -> 05-26). **Preuve
directe : les lignes `@PG` des BAM S3 portent ses commandes mot pour mot** (`--subsample FRAC
--subsample-seed SEED /scratch/boris/dilution-cache/...`, `merge -@ 2 -f`, `sort -@ 2`). Seed tumeur
= `42 + healthy_id`, seed healthy = 42, cible 12,5 M LIGNES (`idxstats`), `N_CA = 12.5M x target / VAF`.
480 logs locaux `~/Pipeline/Dilution/logs/` + 3 manifests (480 output_name uniques). ⚠ **Aucun log
sur S3** : `--log-path` relatif + `cd $WORKDIR` dans le worker -> upload saute en silence.
`dilution_trace.nf` reprend le coeur (l.52-53, 119-127, 144-159) sans include ni param.
