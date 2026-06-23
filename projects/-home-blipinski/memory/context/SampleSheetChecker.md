# Context — SampleSheetChecker — 2026-06-23T08:51:11+0000

**Branche** : main
**Dernier commit** : a6312c1 — add audit & purge raw workflow + ss_healthy/ssN2b
**Status** : 9 fichiers untracked (ss10.tsv + 8 rapports dans rapport/)

## Où j'en suis
Traitement de ss10.tsv : 32 samples Healthy_151-182, 8 runs du 08/06/2026
(NANO26 N1-N4 + NANO27 N1-N4). Cycle audit/purge raw terminé. Reste à committer.

## Ce qui marche / ce qui foire
- ✓ ss10.tsv créé et validé (format TSV conforme, 8 run dirs résolus dans raw)
- ✓ 8 rapports HTML MinKNOW copiés dans rapport/ avec préfixe `NANO{}__` (convention historique)
- ✓ Raw des NANO26/27 nettoyé par Boris lui-même (purge + upload.done hors session Claude)
- ✗ ss10.tsv + rapport/*.html encore untracked → pas committés

## Prochaine étape
git add ss10.tsv rapport/NANO2[67]_*.html && commit
(à l'image du commit "add sample sheets ss5-ss9"). Vérifier au passage si sync liquid
de ss10 a bien eu lieu avant de clore.
