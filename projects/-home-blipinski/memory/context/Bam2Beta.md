# Context — Bam2Beta — 2026-05-27T16:30:00+02:00

**Branche** : main
**Dernier commit** : 98ff63f — chore(dev): backfill scripts (Bladder/Twist samples START_TIME + IV)
**Status** : clean

## Où j'en suis
V1.3.1 release + qualif officielle terminées. Patch qui ajoute la génération native
d'un metadata.json (10 champs schema trace-platform) dans Raima_report, remplaçant
le script externe `trace-platform/scripts/build_metadata_json.sh`. Tag V1.3.1 +
release GitHub publiés, QUALIF officielle promue `s3://...QUALIF/V1.3.1/`. Aucune
tâche en cours.

## Ce qui marche / ce qui foire
- ✓ V1.3.1 release : 2 commits feat + docs, pushés sur main + tag V1.3.1 + release GitHub
- ✓ /qualif_bam2beta : QUALIF OK (RUN + QUALIF CONFORME bit-à-bit vs V1.3.0)
- ✓ metadata.json natif testé : 10 champs valides en QUALIF (patient_name="QUALIF")
- ✓ Pattern Nextflow appris : `.combine(by:0)` pour broadcast 1 file/sample sur N entries
- ⚠ `~/Pipeline/trace-platform/scripts/build_metadata_json.sh` à marquer DEPRECATED (le pipeline le génère désormais nativement). Adapter le code trace-platform qui l'invoque.
- ⚠ Image `raima:latest` (raima 0.4.17) toujours pas pushée sur Docker Hub
- ⚠ 3 tags lightweight pollueurs git : `bam2beta-pre-qc-refactor`, `checkpoint-pre-cleanup`, `pre-raima-refactor` (cleanup optionnel)

## Prochaine étape
Aucune tâche bloquée. Si nouvelle session :
1. Côté trace-platform : marquer `build_metadata_json.sh` DEPRECATED + adapter code consommateur (le pipeline V1.3.1+ génère désormais nativement)
2. Push image `raima:latest` sur Docker Hub si distrib hors machine
3. Sinon, attendre la prochaine demande (intégration rapport Typst V2 dans le pipeline reste la prochaine grosse étape — `bin/rapport/test/V2final/report-grail-v2.typ` prêt à intégrer via Dockerfile.rapportv4)
