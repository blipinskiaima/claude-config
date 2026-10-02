# Context — trace-platform — 2026-10-02T13:17+0000

**Branche** : main
**Dernier commit** : 44a3d37 — feat(rapports): rapport de production PDF + correctif .done/.failed residuel
**Status** : clean (seuls les backups .duckdb / logs / captures restent non suivis)

## Où j'en suis
Session 28/09 → 01/10 close. Rétrospective prod 15-30/09 écrite dans le Google Doc EACR (onglet
`Prod 15-30/09`) + diaporama Google Slides. Nouveau rapport de production PDF (`rapports/`) et skill
global `/create-rapport-prod`, testés sur le 01/10 (8 runs IRCCS) et la semaine du 23-29/09.
Rapport du jour copié dans `Bam2Beta/docs/rapport_plateforme_2026-10-01_IRCCS.pdf`.

## Ce qui marche / ce qui foire
- ✓ Rapport de prod : sélection par période, vérification de fraîcheur base vs S3, re-check par clé
  exacte avec backup, PDF identique à la v12 validée (Nb molécule = nb_reads_filtered)
- ✓ Correctif `.done`/`.failed` résiduel : les 8 RC24 du 01/10 en WARNING (pas de .bai), 3/3 OK
- ✗ Suivi faussé par les renommages de patients (copie data/ + ancien results/) : cause non traitée,
  seulement détectable via `verifier_fraicheur.py`
- ✗ AIMA_016 EN RETARD en base (3 runs FAILED_QC_INPUT non relus), laissé tel quel
- ✗ Correspondance Éxís = version_mvaf / Éxís CUP = version_too déduite du code, non confirmée

## Prochaine étape
Faire confirmer à Boris la correspondance des versions Éxís / Éxís CUP, puis décider si le cron
`check` doit re-scanner les terminaux dont un flag S3 est plus récent que `checked_at`.
