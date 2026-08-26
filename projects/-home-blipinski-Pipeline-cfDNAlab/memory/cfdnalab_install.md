---
name: cfdnalab-install
description: Installation and usage gotchas for the BesenbacherLab/cfdnalab Rust CLI tool (fragmentomics)
metadata: 
  node_type: memory
  type: project
  originSessionId: 5a11d752-d0d0-4ab8-bb8f-f2373e6b1257
  modified: 2026-08-26T05:59:11.596Z
---

Le repo BesenbacherLab/cfdnalab est cloné directement dans ce répertoire (`~/Pipeline/cfDNAlab`), qui reflète l'upstream tel quel (pas de fork/wrapper AIMA dessus).

**Installation** (2026-08-18) : pas de conda/cargo/rustc sur le serveur au départ. Installé via Miniforge local (`~/miniforge3`, pas Anaconda — évite tout souci de licence commerciale) → env conda `cfdnalab` (rust=1.94.0, clang/clangdev=21.*, zstandard, perl, fontconfig, canal conda-forge) → `cargo install cfdnalab --locked`. Binaire résultant : `~/.cargo/bin/cfdna` (ajouté au PATH via `.bashrc`). Le binaire a un RPATH conda embarqué (pointe vers `~/miniforge3/envs/cfdnalab/lib`) donc pas besoin d'activer l'env conda pour l'exécuter — mais l'env conda doit rester présent sur disque (dépendances dynamiques : libfreetype, libstdc++, libz, libpng16).

**Gotcha critique — données ONT/Nanopore** : les BAM AIMA (pipeline [[bam2beta]], ONT) sont non-paired (`0 paired in sequencing` en `samtools flagstat`). Le mode par défaut de cfdnalab suppose du paired-end (Illumina) et exclut silencieusement quasi 100% des reads, sans erreur ni warning explicite, si on oublie `--reads-are-fragments`. **Toujours ajouter `--reads-are-fragments` sur les BAM AIMA/ONT** (flag documenté "e.g. Nanopore" dans le help). Vérifié en test : sans le flag → 0/107982 fragments comptés (échec silencieux, exit 0) ; avec le flag → 78150/107982 (72.37%) acceptés.

**Test de référence** : `Healthy_826.merged.bam` (échantillon standard qualif Bam2Beta, liquid), tiré de `s3://aima-bam-data/processed/MRD/DEV/V0.0.21/run1/Healthy_826/BAM/` (variante majuscule du 2025-12-23, plus récente que la variante minuscule `healthy_826` du 2025-12-12 — utiliser la majuscule). Copié localement dans `~/Run/cfdnalab_test/BAM/` (hors du clone git, qui n'a pas d'exclusion `.gitignore` pour des données de test).

**Why** : Boris a demandé l'installation + un test fonctionnel du toolkit fragmentomique cfDNAlab (BesenbacherLab) dans ce projet, en parallèle d'une recharge de contexte trace-prod/bam2beta.

**How to apply** : toute commande `cfdna` (fcoverage, midpoints, ends, lengths, gc-bias...) lancée sur un BAM issu du pipeline Bam2Beta/ONT doit inclure `--reads-are-fragments`. Sans ce flag, le run "réussit" en apparence (exit 0, fichier produit) mais le résultat est vide/inutilisable — piège silencieux à vérifier systématiquement (regarder "Initially accepted reads" dans les stats de sortie).

**Commandes testées OK sur Healthy_826** (2026-08-26, toutes avec `--reads-are-fragments`) :
- `fcoverage` → bedGraph .zst, 77935 fragments
- `lengths` → TSV large (1 ligne × 971 colonnes `count_30`…`count_1000`, PAS une table longue) + PNG. Total 77935 (cohérent avec fcoverage), mode à 166 bp, bosse dinucléosomale ~320-340 bp — signature cfDNA canonique
- `ends --k-inside 4 --k-outside 0` → zarr sparse, 101693 motifs sur 256/256 4-mers non nuls. `--k-outside 0` évite d'avoir besoin du génome de référence 2bit (les bases "outside" viennent de la référence ; les bases "inside" viennent de la read par défaut)
- `midpoints` → exige `--intervals`, un BED trié d'intervalles **tous de taille identique** avec nom de groupe en col. 4. Sortie zarr + 1 PNG par groupe, lissage Savitzky-Golay ordre 3

**Gotchas outils** : les sorties zarr utilisent un chunking par dimension — les arrays 1D sont dans `c/0`, les 2D dans `c/0/0`. Le `zstandard` du système n'existe pas ; utiliser `~/miniforge3/envs/cfdnalab/bin/python` pour décoder. Warnings htslib `index file is older than the data file` = bruit après un download S3 (mtime), corrigeable par `touch` sur le `.bai`.

**Limite du test midpoints** : faute de BED biologique sous la main (aucun .bed dans Bam2Beta), le test a utilisé un BED synthétique ancré sur les débuts de couverture → le profil obtenu est mécaniquement correct mais biologiquement dénué de sens (pic + oscillations négatives = artefacts de lissage sur un bord franc). Pour un vrai usage midpoints, il faut un BED de sites biologiques (TSS, sites de fixation de facteurs de transcription).
