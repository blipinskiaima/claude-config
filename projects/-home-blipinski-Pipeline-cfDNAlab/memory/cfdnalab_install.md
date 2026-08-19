---
name: cfdnalab-install
description: Installation and usage gotchas for the BesenbacherLab/cfdnalab Rust CLI tool (fragmentomics)
metadata: 
  node_type: memory
  type: project
  originSessionId: 5a11d752-d0d0-4ab8-bb8f-f2373e6b1257
  modified: 2026-08-18T14:06:27.861Z
---

Le repo BesenbacherLab/cfdnalab est cloné directement dans ce répertoire (`~/Pipeline/cfDNAlab`), qui reflète l'upstream tel quel (pas de fork/wrapper AIMA dessus).

**Installation** (2026-08-18) : pas de conda/cargo/rustc sur le serveur au départ. Installé via Miniforge local (`~/miniforge3`, pas Anaconda — évite tout souci de licence commerciale) → env conda `cfdnalab` (rust=1.94.0, clang/clangdev=21.*, zstandard, perl, fontconfig, canal conda-forge) → `cargo install cfdnalab --locked`. Binaire résultant : `~/.cargo/bin/cfdna` (ajouté au PATH via `.bashrc`). Le binaire a un RPATH conda embarqué (pointe vers `~/miniforge3/envs/cfdnalab/lib`) donc pas besoin d'activer l'env conda pour l'exécuter — mais l'env conda doit rester présent sur disque (dépendances dynamiques : libfreetype, libstdc++, libz, libpng16).

**Gotcha critique — données ONT/Nanopore** : les BAM AIMA (pipeline [[bam2beta]], ONT) sont non-paired (`0 paired in sequencing` en `samtools flagstat`). Le mode par défaut de cfdnalab suppose du paired-end (Illumina) et exclut silencieusement quasi 100% des reads, sans erreur ni warning explicite, si on oublie `--reads-are-fragments`. **Toujours ajouter `--reads-are-fragments` sur les BAM AIMA/ONT** (flag documenté "e.g. Nanopore" dans le help). Vérifié en test : sans le flag → 0/107982 fragments comptés (échec silencieux, exit 0) ; avec le flag → 78150/107982 (72.37%) acceptés.

**Test de référence** : `Healthy_826.merged.bam` (échantillon standard qualif Bam2Beta, liquid), tiré de `s3://aima-bam-data/processed/MRD/DEV/V0.0.21/run1/Healthy_826/BAM/` (variante majuscule du 2025-12-23, plus récente que la variante minuscule `healthy_826` du 2025-12-12 — utiliser la majuscule). Copié localement dans `~/Run/cfdnalab_test/BAM/` (hors du clone git, qui n'a pas d'exclusion `.gitignore` pour des données de test).

**Why** : Boris a demandé l'installation + un test fonctionnel du toolkit fragmentomique cfDNAlab (BesenbacherLab) dans ce projet, en parallèle d'une recharge de contexte trace-prod/bam2beta.

**How to apply** : toute commande `cfdna` (fcoverage, midpoints, ends, lengths, gc-bias...) lancée sur un BAM issu du pipeline Bam2Beta/ONT doit inclure `--reads-are-fragments`. Sans ce flag, le run "réussit" en apparence (exit 0, fichier produit) mais le résultat est vide/inutilisable — piège silencieux à vérifier systématiquement (regarder "Initially accepted reads" dans les stats de sortie).
