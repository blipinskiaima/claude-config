# Context — trace-prod — 2026-06-25T13:05:19+0000

**Branche** : main
**Dernier commit** : cd72c61 — feat: schema v13 — colonne mvaf_v14 (retd_suivis)
**Status** : clean (tracké)

## Où j'en suis
Schema v13 (colonne mvaf_v14) implémenté de bout en bout via le skill add-trace-prod
et committé (cd72c61). Calque de mvaf_v13 sauf extraction cols[1] (colonne mvaf du
fichier V1.4 à 3 colonnes) + formatage format_mvaf4. Code poussé, doc à jour.

## Ce qui marche / ce qui foire
- ✓ Colonne mvaf_v14 créée (schema v13), migration idempotente OK, version DB = 13
- ✓ check_mvaf_v14 testé : 26BM01841 → 0,0121 ; valeur scientifique → 0,00005074 ; absent → NA
- ✓ format_mvaf4() : 4 décimales, ou 4 chiffres signif. si <1e-4, jamais de e-05
- ✓ Export _LIQUID_QC : mVAF v1.4 après mVAF v1.3, bout-en-bout validé
- ✓ Doc complète : README (table + section), CLAUDE.md (v13), mémoire (topic + MEMORY.md)
- ⚠ Seuls 2 samples passés en test (26BM01841 + Bladder_Blood_01_001) — backfill complet non lancé

## Prochaine étape
Rétrospectif PAR BORIS (single writer lock, séquentiel) :
update-column mvaf_v14 liquid CGFL → liquid HCL → export --gsheet CGFL → HCL.
Checkpoint rollback dispo : tag checkpoint-pre-mvaf-v14.
