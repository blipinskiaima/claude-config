# Context — Bam2Beta — 2026-05-27T15:10:00+02:00

**Branche** : main
**Dernier commit** : 6baeb2c — docs: update CHANGELOG, README and CLAUDE.md for V1.3.0
**Status** : clean (working tree)

## Où j'en suis
V1.3.0 officiellement releasée et qualifiée. La session a livré 5 refactors structurels majeurs
(Raima_score_all fusion, Beta_epic encapsule BAM_Count/Read_ST, Merge chain BAM_sort→BAM_index,
QC découplé de MERGE, suppression Beta_filter) + absorption de V1.2.0 (module IV + bump raima
0.4.17 effectif après rebuild raima:latest). Tag V1.3.0 pushé, release GitHub publiée, QUALIF
officielle promue dans `s3://...QUALIF/V1.3.0/`. Aucune tâche en cours.

## Ce qui marche / ce qui foire
- ✓ 14 commits propres V1.1.2 → V1.3.0, working tree clean, tout pushé sur origin/main + tag V1.3.0
- ✓ raima:latest contient maintenant raima 0.4.17 (rebuild 27/05, était 0.4.13 par accident depuis 9 mai)
- ✓ 6× /test_bam2beta TEST OK bit-à-bit identique vs V1.1.2 sur Healthy_826
- ✓ Cross-validation Bladder_Blood_02_110 : 44/44 fichiers identiques vs RetD baseline (9 avril)
- ✓ Cross-validation Bladder_Urine_02_050 : 25/25 fichiers identiques vs RetD baseline (26 mai)
- ✓ /qualif_bam2beta : QUALIF OK (RUN + QUALIF CONFORME vs V1.1.2)
- ✓ Containers Docker BETA : -50% (3 Raima_process → 1 Raima_score_all)
- ⚠ `raima:latest` (0.4.17) pas encore pushée sur Docker Hub → si distrib via Seqera Tower / autres workers, faire `docker push blipinskiaima/raima:latest`
- ⚠ 3 tags lightweight pollueurs git : `bam2beta-pre-qc-refactor`, `checkpoint-pre-cleanup`, `pre-raima-refactor` (à nettoyer optionnellement)

## Prochaine étape
Aucune tâche bloquée. Si nouvelle session :
1. Push image raima:latest sur Docker Hub (`docker push blipinskiaima/raima:latest`)
2. Optionnel : nettoyer tags lightweight pollueurs (`git tag -d ...` + `git push origin --delete ...`)
3. Optionnel : bump VERSION=V1.1.2 → V1.3.0 dans `dev/SCW/Bam2Beta.sh` (script launch SCW)
4. Sinon, attendre la prochaine demande (intégration rapport Typst V2 dans le pipeline est la prochaine grosse étape à terme)
