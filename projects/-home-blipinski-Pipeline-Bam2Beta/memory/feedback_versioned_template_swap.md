---
name: Versioned template swap pour fichiers en prod
description: Quand on refonte un fichier directement référencé par un process Nextflow en prod, créer une copie versionnée et ne basculer qu'au moment du switch container/config — ne jamais modifier le fichier "live" en place
type: feedback
originSessionId: 957bf81d-a6c4-4701-a8df-8dc9a5b82a22
---
Quand un fichier est référencé par un process Nextflow actif (ex: `cp ${projectDir}/bin/ctdna_report_template.Rmd ./` dans `workflow/beta.nf`), **ne jamais modifier ce fichier en place** tant que le container associé n'a pas été switché.

**Why:** Le 2026-05-07, refonte du `ctdna_report_template.Rmd` pour XeLaTeX/IBM Plex. Modif faite directement sur le fichier `bin/ctdna_report_template.Rmd`, puis lancement du build `rapportv3:latest` en background. Pendant le build, Boris a relancé un test NF en parallèle → le pipeline a copié le NOUVEAU template (qui exige IBM Plex Sans) mais l'a fait rendre par le container `rapportv2:latest` (qui n'a ni la font ni XeLaTeX) → crash `fontspec Error: The font "IBM Plex Sans" cannot be found`. Stratégie "rapportv2 intact" cassée par effet de bord.

**How to apply:**
- Pattern correct : créer le nouveau fichier sous un nom versionné (`bin/ctdna_report_template.v3.Rmd`), garder l'original `bin/ctdna_report_template.Rmd` inchangé, et faire le `cp v3 → original` UNIQUEMENT au moment du switch des configs vers le nouveau container.
- Garder en parallèle un backup `bin/*.v1.Rmd` du fichier original avant tout swap.
- Cette logique s'applique à tout fichier "asset" (Rmd, R, py, sh, BED, config) référencé par un workflow actif — pas seulement aux templates rapport.
- Anticiper l'effet de bord : Boris peut lancer `/test_bam2beta` ou un run NF à tout moment pendant la session. Le filesystem `~/Pipeline/Bam2Beta/` est partagé en temps réel avec ses runs Nextflow.
