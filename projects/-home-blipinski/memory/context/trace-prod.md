# Context — trace-prod — 2026-06-08

**Branche** : main
**Dernier commit** : 251326e — feat: schema v11 — mvaf_v13 + frag_score_v2_sc + bascule props epics v1.3
**Status** : clean (untracked non commités : backups .duckdb, csv dev/, html rapport/, .claude/)

## Où j'en suis
Session terminée — 2 features livrées, committées, pushées sur main. (1) Schema v11 : colonnes `mvaf_v13` + `frag_score_v2_sc` dans retd_suivis (liquid only). (2) Bascule source props epics `props_v1.tsv` → `props_v1.3.tsv`. Les deux exécutées en base + exportées vers gsheet.

## Ce qui marche / ce qui foire
- ✓ Schema v11 vérifié : Healthy_826 mVAF v1.3=2,581, Frag Score v2=-0,0682464198886691 ; 26BM01841 Frag Score v2=0,00755156001789226 (= exemple Boris)
- ✓ Props epics recalculées liquid CGFL+HCL (Healthy_826 blood_0 : 0,945857 → 0,8239526 avec v1.3)
- ✓ update-column props_epic_status CGFL+HCL OK (481 HCL) ; export gsheet CGFL (753) + HCL (481) pushés
- ✓ README + CLAUDE.md à jour (bloc v11 + note props_v1.3) ; mémoire v11 déjà à jour
- ✗ Bascule props_v1.3 NON répercutée sur short_read/dilution (pipelines séparés, choix assumé)

## Prochaine étape
Rien en attente. Si Boris veut basculer aussi short_read (checkers_short_read.py:85) et dilution (checkers_dilution.py:105) sur props_v1.3.tsv, c'est un chantier séparé à valider.
