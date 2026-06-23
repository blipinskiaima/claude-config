---
name: check-input-qc
description: "Process Check_Input (QC fichiers d'entree en amont du merge) + gotcha NF channel vide -> emit qui plante + retrait rapport PDF (2026-06-23)"
metadata: 
  node_type: memory
  type: project
  originSessionId: cea008d8-7d46-4e63-b926-d16b2c6cd03e
---

# Check_Input — QC des fichiers d'entree en amont du merge (2026-06-23)

## Feature

Nouveau process `Check_Input` dans `workflow Merge` ([workflow/merge.nf]), **en amont du merge**.
Valide chaque fichier du dossier `--input` :

```
.bam                                           -> samtools quickcheck ET view -c > 0 (sinon KO)
.bai / .dl_complete                            -> OK (ignores)
*_bam_list.txt / *_bai_list.txt / *_header.txt -> OK (whitelist par suffixe)
tout AUTRE fichier / extension                 -> KO
aucun .bam dans le dossier                     -> KO
```

Comportement :
- **Input KO** -> run Nextflow **SUCCESS**, **seul Check_Input** tourne, publie
  `REPORT/metadata.json` (schema 10 champs + `status="FAILED_QC_INPUT"` + `reason` listant
  les fichiers KO ; numeriques a 0, identite reelle). Aval **coupe**.
- **Input OK** -> pipeline normal.
- **Autre erreur** (bug aval, OOM...) -> crash normal (le json gracieux est reserve au seul input-KO).

Mecanisme (option A retenue) : `Check_Input` emet toujours `tuple(ID, path(BAM), env('QC_STATUS'))`
+ `metadata.json` optionnel ; le workflow route via `.branch{ pass: it[2]=='OK'; fail: it[2]=='FAIL' }`.
Le `dir` est chaine depuis le workdir -> **1 seul download S3**. `withName: Check_Input` dans
conf/base.config (cpus 2 / 4GB, container par defaut bam2beta:latest, samtools dispo).
`exit 0` toujours (verdict via QC_STATUS, pas via code retour) -> le retry par defaut ne se
declenche que sur vraie erreur infra.

## GOTCHA critique — channel vide -> emit de sous-workflow qui plante

En coupant l'aval par un **channel vide**, le pipeline plantait a la **construction** :
`Exception evaluating property 'rapport' for ChannelOut ... No such property: rapport for
DataflowBroadcast` ([beta.nf] emit). Cause : un sous-workflow invoque avec une entree vide
dont un `emit:` reference un process aval (`emit: rapport = Raima_report.out.rapport`) ne
resout plus l'output nomme. **Mon hypothese "channel vide = aval coupe silencieusement" est
FAUSSE** pour ce pipeline. Reproductible UNIQUEMENT sur la cascade reelle (join/combine/first),
pas en mini-isole.

**Fix** : retirer les `emit:` **inutilises** (jamais consommes dans main.nf) des sous-workflows
actifs : `Beta_epic` (beta.nf), `Frag` (frag.nf), `IV` (IV.nf). `CNV` n'a pas d'emit -> non
fragile. Apres retrait, l'aval tolere le vide (ne tourne juste pas). Non-regression Healthy_826
**TEST OK 3/3 bit-a-bit** (les emits ne servaient a rien).

## Retrait du rapport PDF (decision Boris, meme session)

- Generation desactivee par Boris : `beta.nf` output `rapport` (PDF) commente + `rmarkdown::render`
  commente. Le process `Raima_report` ne genere plus le PDF, seulement `raima_score.V2.json` +
  `metadata.json` (awk/cat). Container `rapportv2:latest` conserve (encore le container du process).
- Retrait du PDF du contrat de sortie : `conformity/check-run-output.sh`,
  `conformity/check-conformity.sh`, doc (README.md, CLAUDE.md, overview/S3.md, overview/README.md).
- Le retrait de l'emit `rapport = Raima_report.out.rapport` etait AUSSI requis ici (l'output etant
  commente, le reference aurait plante) -> converge avec le fix gotcha ci-dessus.

## Validation (2026-06-23)

- Chemin KO (garbage.bam + notes.csv) : run SUCCESS, 1 seul process (Check_Input), `metadata.json`
  publie avec status + reason listant les 2 KO.
- Chemin OK (Healthy_826) : `/test_bam2beta` **TEST OK 3/3** (RUN CONFORME + QUALIFICATION CONFORME
  bit-a-bit vs QUALIF V1.3.2).
