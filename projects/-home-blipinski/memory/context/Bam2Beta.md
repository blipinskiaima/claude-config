# Context — Bam2Beta — 2026-07-22T07:47:02+0000

**Branche** : main
**Dernier commit** : 03ffa1c — docs(qualif): trace l'equivalence depot sur 6 samples
**Status** : 2 fichiers modifiés (dev/PLT + dev/SCW, modifs de Boris, non commitées)

## Où j'en suis
Module THEMELIO (dépistage cancer, Themelio 1.0.0) intégré, qualifié et **releasé en V2.2.0**
(tag + release GitHub + QUALIF/V2.2.0 sur S3, QUALIF OK 37/37). Chantier terminé côté Bam2Beta.
Reste 3 dettes hors-périmètre, non traitées.

## Ce qui marche / ce qui foire
- ✓ V2.2.0 releasée : module THEMELIO, metadata.json contrat unique (29 champs, raima_score.V2.json
  supprimé), bloc versions lu des artefacts, mode --THEMELIO_RETRO, gardes-fous SCRIPT_FOR_MODEL
- ✓ Qualif THEMELIO : Lung_9 (0.855261) + Lung_100 (0.846397) figés dans check-conformity.sh ;
  6 samples example_scores reproduits au dernier chiffre via --THEMELIO_RETRO (tracé, pas rejoué)
- ✓ Comparaison QUALIF vs plateforme TESTV220 : 0 différence de résultat (seuls identité/horodatage)
- ✗ **trace-platform/check_platform.py** : correctif "OU metadata.json" ÉCRIT mais NON COMMITÉ
  (mêlé aux modifs de Boris) + colonne metadata_json en base pas ajoutée → session dédiée
- ✗ **beta_28M.nf:215** pointe vers bin/bootstrap_trasnfo.R déplacé dans bin/archive/ → casse --MVAF1_4
- ✗ **Token Tower en clair** dans nextflow.config (+ historique git) → à révoquer côté Seqera

## Prochaine étape
Traiter les 3 dettes hors-périmètre, en priorité check_platform.py (bloque le dashboard sur les
runs V2.2.0). Décider du sort du correctif déjà écrit dans trace-platform (garder/committer).
