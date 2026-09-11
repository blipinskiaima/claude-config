# Context — trace-prod — 2026-09-11T15:15:40+00:00

**Branche** : main
**Dernier commit** : ab3ec25 — docs: active_cancer — colonne clinical morte + ecart Lung_13 non verrouille
**Status** : propre (untracked inchangés : backups .duckdb, CSV dev/, rapports HTML, metadata_HCL.tsv)

## Où j'en suis
Audit `active_cancer` de la gsheet CGFL (`ONT_samples` / onglet VAF) terminé, les 6 étapes de
la feuille de route sont faites. Livrable = 16 lignes à trancher, écrites dans l'onglet
**Active-cancer** du Google Doc QC. Rien n'attend côté code. La balle est chez le clinicien.

## Ce qui marche / ce qui foire
- ✓ `active_cancer` **concordant à 100 %** gsheet ↔ base (222/51/16/12), propagation
  rebasecalled exacte — rien à rattraper sur le sujet lui-même
- ✓ Import de rattrapage lancé par Boris : metadata CGFL 526 → **623** lignes, 60 `stage`
  corrigés, 0 divergence résiduelle. Backup `backup-pre-import-metadata-cgfl-20260911_142433`
- ✓ Historique de la gsheet reconstitué (**54 révisions** exportées et diffées) → une seule
  vraie correction de statut en 6 mois : `Prostate_21` No→Yes le 23/07/2026
- ✓ Doc QC / onglet Active-cancer : tableau 17 lignes, largeurs recalées sur 451 pt
- ✗ **Écart `Lung_13*` non verrouillé** : `class='Lung'` tenu à la main, le prochain
  `import-metadata liquid CGFL` remettra `Endometrium` (commande de rattrapage dans CLAUDE.md)
- ✗ `active_cancer_clinical` = colonne morte (0/1136), jamais alimentable en l'état
- ✗ `imagerie suspecte` (25 HCL) et `probable` (13) hors `HARMONIZATION_RULES` — constaté,
  **non corrigé** (hors scope de la demande)
- ✗ Le classifieur d'auto-mode bloque toute commande écrivant en base : les deux commandes
  d'import ont dû être lancées par Boris

## Prochaine étape
Faire trancher par R. Boidot les 16 lignes de l'onglet Active-cancer (priorité : `Prostate_25`,
`Breast_46`, les 11 `Suspicion` en stade IV + Cat 1). Une fois la gsheet corrigée :
`import-metadata liquid CGFL`, puis **rejouer l'UPDATE `Lung_13*`** et vérifier la distribution.
