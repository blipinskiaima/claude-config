---
name: cross-project-raima-mvaf-shortread-gap
description: raima (dépendance partagée Bam2Beta + short-read) convertit DRAGEN/rastair en bedMethyl, mais la mVAF v1.4/v1.5 reste structurellement ONT-only
metadata:
  type: project
---

`raima::bedmethyl_dragen()` / `bedmethyl_rastair()` (présentes depuis raima 0.4.5, confirmées
présentes dans 0.5.3 ET 0.5.4) convertissent un CX_report DRAGEN ou un fichier rastair call en
bedMethyl 4 colonnes (chr, pos, n, n_meth), consommable par `model_v1()` / `prop_loyfer()` via
`bedMethyl_select = 1:4`. C'est exactement ce que `~/Pipeline/short-read/loyfer_short_read/`
exploite déjà (`prop_loyfer`, offset=1). Mais `raima::bootstrap_model_v1()` — le moteur de la
mVAF v1.4, et donc de la v1.5 via `transfo_mvaf_by_cov` — ne prend PAS un bedMethyl : il lit des
tables "extract full" PAR READ (colonnes base_qual/mod_qual/read_id/mod_strand), produites
uniquement par `modkit extract full` sur un BAM avec tags MM/ML (ONT). Aucune fonction raima ne
convertit un output DRAGEN/rastair vers ce format par-read.

**Why:** le bedMethyl est un agrégat par-site (le détail par read est déjà perdu) ; le bootstrap
rééchantillonne au niveau read, il a donc besoin d'un détail par-read que le bisulfite/TAPS
short-read n'expose pas dans le même schéma que modkit.
**How to apply:** avant d'évaluer un portage de la mVAF v1.4/v1.5 sur du short-read, vérifier que
ce blocage est structurel (raima lui-même, pas juste un manque de code Nextflow côté Bam2Beta).
Voir `docker/raima_0.5.4.tar.gz` (package R, extrait dans le tar) : `R/model-v1-boot.R` (colonnes
attendues), `R/bedmethyl-dragen.R`, `R/bedmethyl-rastair.R`, `NEWS.md` (historique des versions).
