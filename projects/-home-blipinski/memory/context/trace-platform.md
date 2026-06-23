# Context — trace-platform — 2026-06-23T15:58:50+0000

**Branche** : main
**Dernier commit** : c878c33 — feat: JSON devient le livrable rapport (PDF non requis)
**Status** : clean (tout commité + pushé)

## Où j'en suis
Refonte complète du modèle de statuts trace-platform + pont Aima-Tower : TERMINÉE et déployée.
5 features livrées, commitées/pushées sur les 2 repos, tower rebuildée, DB migrée v11, gsheet exporté. Rien en cours.

## Ce qui marche / ce qui foire
- ✓ run_status : WAITING (état 0, pas de .dl-complete) → RUNNING → SUCCESSED/WARNING/FAILED + ARCHIVED. 281 réconcilient.
- ✓ Granularité PROD sample-level (`samples.case` v10, `PROD_CUTOFFS`). Compte 1 Romain Boidot (16342fc9) PROD depuis upload ≥ 2026-06-15 (26BM + futurs). Vérifié end-to-end (assignation/tower/export).
- ✓ ARCHIVED : commande `check_platform.py archive` (DEV >2 mois, base upload_date, sticky). 88 samples archivés.
- ✓ report_date supprimé (schema v11). JSON = livrable rapport (PDF non requis) → 4 Breast_Demo récupérés (FAILED→SUCCESSED).
- ✓ Tower : case effectif COALESCE, totals par (client,case) → bug 15≠17 fixé, WARNING séparé de SUCCESSED, badges WAITING/ARCHIVED, cartes Warning. Validé via API.
- ⚠ Colonne `clinical_report_pdf` conservée (info historique) — droppable en v12 si cleanup complet voulu.

## Prochaine étape
Aucune tâche en attente. Option ouverte : drop colonne `clinical_report_pdf` (v12) si Boris confirme le retrait total du PDF.
