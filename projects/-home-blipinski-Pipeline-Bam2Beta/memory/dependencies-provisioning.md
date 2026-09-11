---
name: dependencies-provisioning
description: "Provisionner /scratch/dependencies sur un nouveau serveur — les 23 fichiers sont eclates sur 2 prefixes S3, ichorCNA/ n'est PAS dans le bucket, le depot Hub raima est prive"
metadata:
  node_type: memory
  type: project
---

# Provisionner les dependencies sur un nouveau serveur (2026-09-11)

Les **23 fichiers** reellement lus (ceux references par `${params.dependencies}/…` dans
`nextflow.config`) totalisent ~**9,1 Go**. Ils ne sont **pas** dans un seul endroit.

## Ou vit quoi

| Bloc | Source | Volume |
|---|---|---:|
| `bed/`, `CNV/`, `genomes/hg38/`, `raima-model/` (4 fichiers) | `s3://aima-resources/**dependencies/**` | 8,9 Go |
| `raima-model/model_v1_data_whitelist.tsv.gz` | `s3://aima-resources/` **racine** | 221 Mo |
| `themelio-model/`, `too-model/` | `s3://aima-resources/` **racine** | 512 Ko |
| `ichorCNA/` (5 fichiers) | ⚠ **NULLE PART sur S3** — serveur courant uniquement | 852 Ko |

⚠ `ICHORCNA=false` en profil `prod` mais **`true` en `liquid`**, et le lanceur de production
utilise `liquid` -> ces 5 fichiers sont bien necessaires en pratique. Ils n'ont **aucune copie**
hors de cette machine : trou a boucher (`aws s3 cp` vers `dependencies/ichorCNA/`, nouveau
prefixe donc sans ecrasement).

Le prefixe `dependencies/` contient aussi `ATLAS/` (21 Go), `bwa_index/` (17 Go), `ONT/`,
`methylation/` : **inutiles a Bam2Beta**, a exclure du sync.
`genomes/GRCh38/` (3,0 Go) n'est pas requis (`nextflow.config` ne pointe que hg38).

## Faux positifs connus

- `ichorCNA/hg38_1000kb_custom_panel_of_normals.rds` est absent **partout** : le param
  `ichorcna_panel_custom` n'est reference dans **aucun `.nf`**. Param mort, sans impact.
- Regle d'or S3 : `aws s3 sync` saute des fichiers au hasard -> **boucler** jusqu'a egalite
  des comptes local/S3.

## Aucune nouvelle dependance depuis V2.2.0

Les chemins `${params.dependencies}/…` sont **strictement identiques** en V2.2.0, V2.3.0 et
HEAD (23 fichiers). Ce qui change en V2.3.0 est **dans le container** (raima 0.5.3 -> 0.5.6)
et dans le code. Une procedure de provisioning vaut donc pour toutes ces versions.

## Containers : le depot raima est PRIVE

`docker manifest inspect` (avec les creds locales) confirme `blipinskiaima/raima:latest` **et**
`:0.5.6` presents sur le Hub ; `:0.5.3` absent. L'API Hub publique repond
`{"message":"object not found"}` parce que le depot est **prive** — ne pas en conclure une
absence. Un nouveau serveur doit donc `docker login`.

Les 9 autres depots sont publics : `bam2beta`, `bam-merger`, `cramino`, `mosdepth`, `cnv`,
`ichorcna`, `rapportv2`, `too:0.4.1`, `themelio:1.0.0`.

Le tarball `raima_0.5.6.tar.gz` est sur `s3://aima-resources/raima-model/` (plus seulement
sur `/mnt/temp/florian`). Cela **corrige** les points "en suspens" de
[[restructuration-v2-3-0]], perimes.
