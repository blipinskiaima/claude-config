# Context — Bam2Beta — 2026-08-21T16:58:13+00:00

**Branche** : main
**Dernier commit** : 5693a43 — feat(dev): backfill retrospectif du ratio N50/N75
**Status** : 8 fichiers non propres (3 dev/SCW/*.sh + 5 non trackés) — tous
préexistants, volontairement non commités

## Où j'en suis

Session de **backfill rétrospectif sur les Bladder_Urine CGFL**, tout est terminé.
mVAF v1.5 (chantier A du matin) est commitée ET déployée : 1 362/1 362 liquides.

## Ce qui marche / ce qui foire

- ✓ **MITO 37/37**, **SMALL_FRAGMENTS 7/7**, **n50_ratio 38/38** — plus rien ne tourne
- ✓ `dev/backfill_n50_ratio.sh` commité : recalcul depuis le `read_lengths.csv` S3,
  **le BAM n'est jamais stagé**, `cmp`-identique au pipeline sur Healthy_826 + Breast_6
- ✓ mVAF v1.5 : V1.4 et V1.5 au même périmètre, 1 362/1 362 liquides, 0 écart
- ✗ **`raima:0.5.4` toujours LOCALE, non poussée** — bloquant avant toute qualification
- ✗ **v1.5 jamais testée en régime normal** (2-5 M reads EPIC) : `Healthy_826` sature
- ✗ **8 runs Nextflow en parallèle ont saturé `/scratch`** (8 × 21 Go de staging) →
  24 échecs `No space left on device`. Repris en série, tout récupéré.
  `/scratch` est reparti à **237 Go libres**, les workdirs ne se recyclent pas
- ✗ 25/55 samples relancés pour rien en SMALL_FRAGMENTS (sorties de juin déjà bonnes,
  module inchangé depuis `d6d4556`) — croiser avec l'existant AVANT de lancer
- ✗ `--bootstrap` sur 12 samples **annulé** : les 3 sorties existaient déjà
- ✗ `MEMORY.md` à 21,2 Ko, au-dessus du seuil de 17,1 Ko — compactage à faire

## Prochaine étape

Au choix :
- Vider `/scratch/nxf-work` (sorties déjà sur S3) avant toute nouvelle vague
- Pousser `raima:0.5.4` puis tester la v1.5 sur un sample à 2-5 M reads EPIC
- Compacter `MEMORY.md` sous 17,1 Ko
- Faire entrer les 38 nouveaux `n50_ratio.tsv` en base (30/38 en zone C →
  déplacera les stats de la cohorte urinaire)
