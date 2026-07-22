---
name: bam2beta-report-json-consumers
description: Consommateurs de REPORT/metadata.json et REPORT/*.raima_score.V2.json (Bam2Beta) à travers l'écosystème Pipeline — qui lit par existence vs par nom de champ
metadata:
  type: project
---

## Constat général (scan live 2026-07-20)

Aucun projet ~/Pipeline/ (trace-prod, trace-platform, Aima-Tower, trace-workflow, email-hub, export)
ne fait de `json.load()`/`json.loads()` sur `metadata.json` ou `raima_score.V2.json`. Tous les
"consommateurs" externes à Bam2Beta ne regardent que l'**existence du fichier** (booléen) ou
recalculent les métriques (mvaf/depth/coverage) **indépendamment** depuis les TSV/QC bruts
(BETA/*.tsv, QC/Mosdepth, QC/Cramino) — pas de dépendance au contenu des 2 JSON.

## Seul consommateur PAR NOM DE CHAMP trouvé : Bam2Beta lui-même

`~/Pipeline/Bam2Beta/conformity/check-conformity.sh:228-277` — qualification Lung_9, lit
`raima_score.V2.json` avec un `sed` par clé (`"key": value`) : too_prob_Lung/Colon/Breast/Prostate/
Bladder_Pancreas, sex, too_CupMaxProba_threshold, exis_classification_threshold,
exis_positivity_threshold, exis_quantification_threshold, themelio_score,
themelio_CancerPattern_threshold, themelio_OutlierPattern_threshold. Design assumé "par nom" (commentaire
l.199-201) pour survivre à l'ajout de champs — mais un **renommage** de clé casse ce script (à mettre à
jour dans le même commit, contrôlé par Boris).

## Consommateurs par EXISTENCE/CHEMIN uniquement (renommer une clé interne ne casse rien, supprimer le fichier casse)

- `trace-platform/check_platform.py:302-304,327-330` (`rapport_json` = REPORT/*.raima_score.V2.json,
  requis pour `bioit_status=OK`) et `:246,265-266` (`clinical_report_json` = résultat renommé sur
  bucket plateforme, requis pour `rapport_status=OK`) → stockés en BOOLEAN dans
  `trace-platform/lib/platform_db.py:35-36`.
- `Bam2Beta/dev/PLT/Bam2Beta_SCW_plateforme.sh:134,136` copie les 2 JSON vers le bucket
  `aima-platform` (metadata.json même nom ; raima_score.V2.json → `${SAMPLE}_clinical_report.json`).
  Ligne 119 : `grep -q FAILED_QC_INPUT` sur metadata.json = check par **valeur** (champ `status`,
  voir `workflow/merge.nf:96`), pas par nom de clé — renommer la clé `status` ne casse pas ce grep,
  changer la valeur `FAILED_QC_INPUT` le casse.
- `trace-prod` et `trace-platform` ne lisent NI metadata.json NI raima_score.V2.json — ils
  reparsent BETA/QC/Mosdepth/Cramino directement (voir trace-prod-schema.md). Donc les colonnes
  DuckDB `mvaf`/`depth`/`coverage_percent` ne dérivent PAS de ces JSON — coïncidence de nommage,
  pas de couplage.
- `Aima-Tower` ne touche aucun fichier Bam2Beta : lit uniquement les DuckDB (trace-prod,
  trace-workflow, trace-platform) en read-only (`Aima-Tower/CLAUDE.md`).

## Risque non vérifiable : consommateur externe potentiel

`Bam2Beta/overview/S3.md:24` (dupliqué dans `trace-platform/S3.md` et `Aima-Tower/overview/S3.md`) :
commentaire `${SAMPLE}_clinical_report.json # JSON pour affichage des info sur la plateforme` —
suggère qu'une appli client-facing ("la plateforme", bucket `aima-platform`) lit ce JSON pour
affichage. **Code source introuvable dans ~/Pipeline/** — si cette appli existe, elle est hors
écosystème Boris (bus factor 1 ne la couvre pas) → impossible de garantir qu'elle ne lit pas des
champs par nom. À vérifier avec Boris avant tout renommage/suppression.
