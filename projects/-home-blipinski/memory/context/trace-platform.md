# Context — trace-platform — 2026-09-15T13:44:56+00:00

**Branche** : main
**Dernier commit** : dc47c87 — docs: aligne README, S3 et CLAUDE.md sur le contrat Bam2Beta V2.3.0
**Status** : clean (seuls backups .duckdb / logs cron / captures en untracked, comme d'habitude)

## Où j'en suis
Réalignement de trace-platform sur Bam2Beta V2.3.0 TERMINÉ et déployé. La condition
`bioit_status` exigeait `bedMethyl.gz` et `raima_score.V2.tsv`, deux sorties coupées en
V2.3.0 : tous les runs V2.3.0 tombaient en FAILED. Corrigé (raima_score pointe désormais
sur `raima_score.V1.4.tsv`, bedmethyl retiré, extraction score_cnv supprimée), 12 samples
rejoués en base, export gsheet relancé. Reste 3 décisions ouvertes, aucune bloquante.

## Ce qui marche / ce qui foire
- ✓ 11 des 12 runs V2.3.0 passés FAILED → SUCCESSED ; KO2 reste FAILED (vrai Upload KO)
- ✓ Anciens samples intacts : comptages par version identiques avant/après
- ✓ Tag de sauvegarde `pre-v230-realign` poussé sur GitHub
- ✗ `BEN_Dav_29_11_1983` (V2.2.0, vrai patient) toujours FAILED à tort — pipeline relancé
  avec succès mais statut terminal jamais relu. Un recheck ciblé le passe SUCCESSED
- ✗ Piège structurel non corrigé : un run qui touche FAILED puis est relancé n'est jamais
  relu. Piste = ajouter FAILED à `get_active_sample_keys()` (lib/platform_db.py:615)
- ✗ Token Seqera en clair dans Bam2Beta/nextflow.config (tâche séparée déposée, non traitée)

## Prochaine étape
Débloquer BEN_Dav_29_11_1983 :
`check_platform.py check <uuid> --sample BEN_Dav_29_11_1983` — jamais `check <uuid>` seul,
qui recalculerait les anciens samples du compte et les ferait basculer FAILED.
