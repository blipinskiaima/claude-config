# Context — trace-prod — 2026-06-08

**Branche** : main
**Dernier commit** : 251326e — feat: schema v11 — mvaf_v13 + frag_score_v2_sc + bascule props epics v1.3
**Status** : clean (untracked préexistants : backups .duckdb, csv dev/, html rapport/, .claude/)

## Où j'en suis
Session opérationnelle (aucun changement de code). Fix de 9 probs loyfer manquantes
sur HCL liquid rebasecalled V6.0.0 (Healthy_3/4/8/14/23/25/26/34 + Lung_1), puis export gsheet.
Aparté résolu : metadata.class contient déjà la nature du sample (Healthy/Colon/Lung...)
→ pas de colonne "indication" créée (info existe déjà).

## Ce qui marche / ce qui foire
- ✓ Diagnostic : loyfer NULL = décalage temporel (fichier props_loyfer généré après dernière passe loyfer), PAS un bug. upsert_probs préserve loyfer en mode v1 seul (ON CONFLICT ciblé)
- ✓ Fix : `probs liquid HCL -P -s {sample}` sur les 9 (epic v1.3 + loyfer) → couverture HCL loyfer 481/481
- ✓ Epic confirmé lire props_v1.3.tsv (valeur DB blood_0 == fichier)
- ✓ Export `export liquid HCL --probs --gsheet` (481 probs poussées)
- ✓ Note mémoire feedback_probs_loyfer_lag.md créée
- ✗ `probs -s` est mono-sample (pas multiple) → boucler pour plusieurs

## Prochaine étape
Rien en attente. Si Boris veut exposer metadata.class dans l'export QC liquid
(header "Indication"), c'est 1-2 edits dans lib/utils.py (sans nouvelle colonne ni recalc).
