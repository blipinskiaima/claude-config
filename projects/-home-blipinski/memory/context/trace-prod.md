# Context — trace-prod — 2026-09-02T17:03:20+00:00

**Branche** : main
**Dernier commit** : c7fb7b4 — docs: README + CLAUDE.md pour les schemas v28 et v29
**Status** : propre, synchro avec origin/main (24 untracked inchangés : backups .duckdb,
CSV dev/, rapports HTML, metadata_HCL.tsv)

## Où j'en suis
Schema v29 (`frag_amplitude_sc`) terminé de bout en bout via /add-trace-prod : colonne, checker,
backfill 1362 samples, export gsheet, doc et mémoire. Session ouverte sur une dette : v28
(rarefaction_horaire) était terminé mais traînait en working tree non commité — commité en début
de session pour poser un checkpoint propre, puis documenté avec v29 dans le même push.

## Ce qui marche / ce qui foire
- ✓ v29 : 4 fichiers, 29 lignes. Backfill 849 CGFL + 513 HCL = 1362, couverture 100 %, 0 KO,
  0 erreur (~20 min à -j 4). Contrôle croisé exhaustif base↔1362 fichiers source : 0 écart ;
  relecture gsheet↔base : 0 écart, colonne en position 25/55 après Sex Predicted
- ✓ Format du TSV vérifié sur les 1362 fichiers AVANT de coder (pas un échantillon) — le
  précédent v1.3→v1.4 avait déplacé une colonne sans prévenir
- ✓ v28 enfin historisé (97e56e4) + documenté (README section 12, CLAUDE.md)
- ✓ Piège évité : `_LIQUID_QC` et `_SOLID_QC` sont textuellement identiques autour de
  `Sex Predicted` → l'Edit a dû élargir son contexte jusqu'à `Small Fragments`
- ✗ Formats de cellule de la gsheet non vérifiés : `clear()` ne les efface pas, l'insertion en
  position 25 décale d'un cran tout ce qui était à droite. Aucun effet sur les données
- ✗ Chemin KO non observable en prod (couverture 100 %) : prouvé sur sample inexistant seulement

## Prochaine étape
Rien de bloquant sur v29. Fils ouverts hérités des sessions précédentes :
1. Barcodes des 12 `Colon_*_rep*` via les logs Pod2Bam (UPDATE SQL manuel)
2. Adresse POD5 des 12 Twist + 3 Ma_SAB (Taille/Complétude POD5 vides)
3. `28M %` / `CpG %` : QCChecker les code en dur à None, câblage quand Bam2Beta publiera
4. `update-column mvaf_v14 liquid CGFL` comblerait 12 `Bladder_Urine_*` à NULL
