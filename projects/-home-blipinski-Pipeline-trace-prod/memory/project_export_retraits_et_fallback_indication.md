---
name: project-export-retraits-et-fallback-indication
description: "Retrait de N50 et mVAF v1.3 de l'export (colonnes gardées en base) + fallback Indication dérivé du nom dans get_qc_unified (Bladder_Urine, Colon)"
metadata:
  node_type: memory
  type: project
---

# Retraits d'export + fallback Indication (21/08/2026)

## 1. Masquer une colonne sans la supprimer

`N50` retiré de `_LIQUID_QC` **et** `_SOLID_QC` ; `mVAF v1.3` retiré de `_LIQUID_QC`.
**Un seul fichier touché : `lib/utils.py`.** Les mappings `TSV_TO_DB_QC["N50"]` et
`TSV_TO_DB_RETD["mVAF v1.3"]` sont **conservés** → les colonnes restent alimentées par `check`
et `update-column` (`n50` 849/849 CGFL, `mvaf_v13` 1464 valeurs). C'est le statut de `n75`
depuis v22 : **mappé en écriture, absent de l'export**. Réversible en remettant la ligne.

**Why:** Boris voulait alléger la gsheet sans perdre la donnée ni casser les checkers.

**Gotchas gsheet après un retrait de colonne :**
- `export_data` fait `worksheet.clear()` **sans `resize()`** → les valeurs partent mais la
  **grille garde sa largeur** : une colonne vide subsiste à droite (56 col pour 55 en-têtes).
  Sans effet sur les données. Seul `export_rarefaction` redimensionne.
- `clear()` n'efface **pas les formats de cellule** : tout ce qui était à droite de la colonne
  retirée glisse d'un cran et hérite du format de la position précédente. À signaler si des
  formats numériques sont posés (ex. `Ratio N50/N75`, `% Masse > 1kb`).

## 2. `Indication` de l'export `QC read` : fallback par nom

**`Indication` n'est PAS une colonne de la table `qc`** — elle vient de `metadata.class`, via
`get_qc_unified()` (lib/duckdb.py), avec un `CASE` dérivé du nom pour les samples sans metadata.
Étendu de `Lung_Alc%` → `Lung Alc` à **`Bladder_Urine%` → `Bladder`** et **`Colon%` → `Colon`**.

**Why:** 76 `Bladder_Urine_*` et 8 `Colon_*_rep*_OK` n'avaient **aucune ligne** dans `metadata` —
un `UPDATE metadata SET class=...` n'aurait affecté 0 ligne. Deux options : insérer des lignes
metadata quasi-vides, ou étendre le fallback. Le fallback gagne : rien n'est écrit en base, donc
rien à réécraser au prochain `import-metadata`, et si la gsheet finit par fournir un `class` il
reprend automatiquement la main.

**Le `COALESCE` protège les valeurs réelles** : les `Colon*` typés `Rectum` (40),
`Rectosigmoïde` (25), `Sigmoïde` (8) gardent leur indication — le `CASE` ne sert qu'aux `NULL`.
⚠ Vérifier ce point avant d'élargir un pattern : `LIKE 'Colon%'` semble large mais ne touchait
que les 8 samples visés (contrôlé par requête avant l'edit).

Liens : [[project_schema_v22_n75_ratio]] (précédent « mappé mais jamais exporté »),
[[project_schema_v21_n50]], [[project_schema_v25_qc_28m_cpg]] (table `qc`).
