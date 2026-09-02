---
name: debugging-gotchas
description: "Gotchas outils/debugging Bam2Beta sans fiche dediee — S3/s3fs, bedtools, mosdepth, samtools, doublons sample_name, unites, kraken2, Nextflow (detail des insights de l'index)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 330ade70-5566-438a-a5d4-abcaab9e189a
  modified: 2026-09-02T15:51:36.229Z
---

# Gotchas outils & debugging (detail de l'index MEMORY.md)

## Nextflow / pipeline

- **Container assigne par `withName:` dans `conf/base.config`**, pas dans le process : tout
  nouveau process raima sans entree `withName` herite du defaut `bam2beta:latest`.
- **`raima:latest` doit etre rebuild** apres modification du Dockerfile, sinon Docker sert
  l'image cachee. (Historique : raima 0.4.5 cassait `Raima_process_CNV`, `depth_per_region`
  non exportee.)
- **Channel vide → emit de sous-workflow qui plante** (NF 25.04) : `No such property: X for
  DataflowBroadcast` a la CONSTRUCTION. Ne frappe que les emits **jamais consommes**.
  Voir [[check-input-qc]].
- **`Channel.fromPath` = queue channel a 1 item** : limite le process a une execution par
  invocation ; droppe des samples en batch. Fix `.first()`. Pose sur RAIMA_LOYFER +
  RAIMA_V1_WL ; **subsiste sur RAIMA_MODEL1/2, ANCESTRY_MODEL, BED, FASTA, FAI**.
- **`checkIfExists: true` dans un `.map` de mode retro tue TOUT le run batch** (exception a
  la construction du channel). Fix : `.filter { .exists() }` + `log.warn`.
  (Depuis V2.3.0 les modes retro historiques sont archives ; le patron reste valable —
  applique a RETRO_FRAG_AMPLITUDE.)
- Voir [[restructuration-v2-3-0]] pour les gotchas DSL2 decouverts en 2026-09 (ordre de
  declaration des invocations, auto-include interdit, 2 workflows partageant un process,
  limites de `--help`, non-determinisme ichorCNA, hook pretool cwd).

## S3 / s3fs / outils

- **`samtools view <bam> '*'`** cible les reads non places **via l'index** — 7 min sur un BAM
  de 10,7 Gio au lieu d'une passe complete (debit s3fs ~26 000 reads/s). ⚠️ **`The index file
  is older than the data file` sur TOUS les BAM de `RetD/`** : le `.bai` est systematiquement
  anterieur au `.bam`. Comptages exacts sur 16/16 vs table `qc`, donc index exploitables —
  mais l'anomalie est generale.
- **`bedtools -sorted` exige le MEME ordre de contigs** dans les 2 fichiers : indispensable
  pour la vitesse (30 s contre > 12 min) mais un `sort -k1,1` donne l'ordre **lexicographique**
  (chr1, chr10, chr11…) alors que les BAM sont **karyotypiques** → **perte silencieuse de la
  moitie des donnees**, sans avertissement. Detectable seulement en comptant les lignes.
- **`aws s3 cp` + calcul local ≈ 8× plus rapide que lire via s3fs** (44 s contre 340 s pour un
  per-base) : s3fs tient en lecture sequentielle (~240 Mo/s) mais s'effondre a ~4 Mo/s sur les
  lectures fragmentees avec decompression. `tabix -R` n'aide pas quand les regions sont
  dispersees (tous les blocs bgzip sont touches).
- **mosdepth — defauts et options jamais utilisees** : `-F 1796` garde les supplementaires
  (profondeur = C+D), `-Q 0` aucun filtre MAPQ. Le pipeline n'utilise ni `--by`, ni
  `--thresholds`, ni `--use-median` ; il genere 195 lignes de summary et ~1 300 de global.dist
  pour n'en lire qu'une de chaque, plus un per-base de 456 Mo jamais lu.

## Donnees / unites

- **75 `sample_name` sont portes par 2 echantillons distincts** (un CGFL, un HCL, profondeurs
  differentes — `Colon_1` = 1,06× / 3,51×) : nommer un fichier de sortie par le nom seul en
  ecrase la moitie **en silence**. Cle TYPE+LABO+ID obligatoire.
- **`nb_reads_aligned` est en MILLIONS dans `trace-prod`**, en unites dans `metadata.json`
  (26BM03032 : `22.06` contre 22 064 525).

## Metagenomique (2026-08-14)

- Le `master` de `kraken2` **ne compile pas** (`compare_header` manquant dans `classify.cc`)
  → `git checkout v2.17.1` avant `install_kraken2.sh`.
- URLs d'index de Ben Langmead : format passe de `k2_standard_16gb_<date>` (**404**) a
  `k2_standard_16_GB_<date>` → extraire les liens de la page, ne pas les deviner.
- Sortie `kraken2 --output` : la **longueur est en colonne 4**, la 3 est le taxID.

## Architecture (complements sans fiche)

- CNV log2ratio : bins de 100 kb ; en liquid/prod `bin_coverage` **ne filtre aucun flag**
  (seule la longueur 120-400 filtre) ; solid applique `-F 260`.
- `raima_score_loyfer.R` : `max_read_len` conditionnel (solid = Inf, liquid = 1000) via `--type`.
- BED en `/scratch/dependencies/bed/` — ciblent chr1-22+X+Y uniquement.
- Le BAM merged est traverse ~4 fois par run rien que pour compter (BAM_Count, cramino,
  Extract_read, 22× Preprocess_28M).
- `mVAF` renomme `TF` au commit 7837cd0 ; `params.cpu`/`memory` → `cpus_max`/`memory_max`
  en V1.0.1.
