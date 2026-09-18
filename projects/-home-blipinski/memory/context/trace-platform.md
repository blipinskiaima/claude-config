# Context — trace-platform — 2026-09-18T10:23:39+00:00

**Branche** : main
**Dernier commit** : b66b98f — feat(db): sequencing_time (schema v22) + documentation alignee sur v22
**Status** : clean (seuls backups .duckdb / logs cron / captures en untracked, comme d'habitude)

## Où j'en suis
Session longue du 17/09 : la base est passée de v14 à v22 en 8 migrations, la gsheet de 30 à
47 colonnes en 8 rubriques. Tout est committé, poussé, exporté et documenté (README + CLAUDE.md
+ MEMORY.md). Rien n'est en cours — point d'arrêt propre.

## Ce qui marche / ce qui foire
- ✓ Timestamps : 254 corrections + 8 comblages, 150 valeurs faussées par le bug de fuseau
  s3fs redressées. 0 changement de statut, 0 changement de métrique
- ✓ Chronologie v15 en 6 horodatages, découverte que `data/` est une copie et que le vrai
  upload client se passe sous `bulk/` — conservé seulement depuis le 2026-09-14
- ✓ TOO, versions produits, `version_mvaf`, `product`, statuts QC Exis/Themelio,
  `sequencing_time` : tous remplis par UPDATE ciblé, jamais par `check <UUID>`
- ✓ Fusions de la ligne méta du gsheet désormais synchronisées automatiquement (elles
  masquaient silencieusement la catégorie BAM)
- ✗ **Staging générique non corrigé** : `.tsv`/`.txt`/`.log` rendent 60,66 Go éligibles au
  téléchargement à chaque scan, dont des `read_start_time.tsv` de 3 Go que personne ne lit.
  Correctif proposé (garde de taille à 1 Mo dans `_stage_sample_s3`), volontairement écarté
- ✗ `BEN_Dav_29_11_1983` toujours FAILED à tort — piège du statut terminal jamais relu,
  hérité de la session précédente
- ✗ Compte `f3fd87cd…` sans lab déclaré dans `labs_users` (1 sample dans la gsheet)
- ✗ Token GitHub PAT en clair dans l'historique git de Bam2Beta (commit `c1453da`) — tâche
  déposée, non traitée

## Prochaine étape
Décider du staging : appliquer la garde de taille `_STAGE_MAX_BYTES = 1_000_000` dans
`_stage_sample_s3` (check_platform.py), qui ferme les 60 Go d'un coup — ou s'en tenir à
l'exclusion nominale de `read_start_time.tsv`. Mesure et correctif déjà instruits dans
MEMORY.md, section « Dette ouverte ».
