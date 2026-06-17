# Context — short-read — 2026-06-17T13:46+00:00

**Branche** : main
**Dernier commit** : 92be8f7 — docs: add Loyfer pointer to README and project CLAUDE.md
**Status** : clean (seul `dl.sh` untracked, préexistant, non lié)

## Où j'en suis
Calcul des **proportions Loyfer** (déconvolution cellulaire, 31 types) sur les pipelines short-read. **2/4 pipelines faits et versionnés** dans [loyfer_short_read/](loyfer_short_read/) (commits eb235e7 + 92be8f7) : NF_Watchmaker_Methylseq (rastair) + BP_5base (DRAGEN). Méthode établie et réutilisable.

## Ce qui marche / ce qui foire
- ✓ `loyfer_short_read/` dans le repo : 2 scripts + 2 TSV + README. Données de travail dans `/scratch/boris/loyfer_short_read/`.
- ✓ **Methylseq** → `prop_loyfer_methylseq.tsv` (16 samples × 9 variantes rastair = 144 lignes)
- ✓ **BP_5base** → `prop_loyfer_bp5base.tsv` (8 samples DRAGEN). Sommes=1, nommage underscore, `Variant=5base`
- ✓ Pattern validé : source méthylation → `bedmethyl_rastair`/`bedmethyl_dragen` → bedMethyl 4col → copie fidèle de `prop_loyfer` (`max|diff|=0`, raima intact), **modèle 4.1G préchargé 1×**, **offset=1** (calibré rastair+dragen)
- ✓ **Résultat clé** : décrochage high-TF **reproductible** Methylseq↔BP_5base — Breast_18/Colon_3/Lung_8 (mVAF>12) → `Erythroid_Progenitor` dominant, granulocyte≈0 → signal lié à la TF, pas un artefact
- ✗ DRAGEN lent (~50 min/run : CX_report 6.3G/sample, I/O-bound sur le mount)

## Prochaine étape
Étendre aux **3 sources restantes** sur les mêmes samples : NF_Watchmaker_Aima (rastair, rapide), BP_Watchmaker (DRAGEN, lent), puis **ONT** (référence — recalculer pour comparer short-read vs ONT). Cloner le script existant (changer source + fonction + offset à confirmer pour DRAGEN).
