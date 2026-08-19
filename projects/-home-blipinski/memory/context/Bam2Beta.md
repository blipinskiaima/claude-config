# Context — Bam2Beta — 2026-08-19T08:06:32+00:00

**Branche** : main
**Dernier commit** : b2d5401 — docs(QC): manuel d'utilisation du duo ratio N50/N75 x masse > 1 kb
**Status** : 7 fichiers modifiés/non suivis, aucun de cette session (lanceurs dev/SCW édités à la main, PDF, notes)

## Où j'en suis
Onglet **`On site`** du Google Doc QC rempli avec **deux parties complètes** : *Nombre de reads*
(définitions, état des lieux 1 324 liquides, synthèse, ouverture) et *Ratio N50/N75 et masse
d'ADN long* (mêmes 3 sections, recensement au format `Lung_Alc`). 5 figures en place.
Aucune modification de code : la session a porté sur l'analyse trace-prod et la rédaction.

## Ce qui marche / ce qui foire
- ✓ **Backfill 28M TERMINÉ** — 1 506/1 506 samples, tous `OK`, 38,3 G reads. `/scratch/boris/nb_read_28M/nb_reads_28M.tsv`
- ✓ Méthode validée : `uniq(read_id extract_full) + skipped(log modkit)` = comptage exact à **0,002 %** (vérifié Healthy_826 et Lung_9)
- ✓ **Second critère QC refondu** : le seuil `reads_primary_mapped ≥ 4 M` est remplacé par `% reads non alignées > 70 %` (intervalle vide de 33 pts, 10 samples, tous urines)
- ✓ Outillage Google Doc réutilisable dans `/scratch/boris/qc_onsite/` (lecture par onglet, insertion, remplacement de chaînes exactes, remplacement d'images)
- ✗ **`reads_28m` toujours NULL 1332/1332 en base** — le TSV du backfill n'a pas encore été chargé dans trace-prod
- ✗ Le tableau de recensement redit l'axe Comptages déjà traité dans la partie 1 (choix assumé, format `Lung_Alc`)
- ✗ Aucune figure sur la partie Ratio (croisement ratio × masse et arbre de décision non régénérés)

## Prochaine étape
Charger `nb_reads_28M.tsv` dans la colonne `qc.reads_28m` de trace-prod, ce qui débloque la
partie 3 vide de l'onglet `Nb reads mapped` (proportion de reads utilisés pour la mVAF 1.4) et
les deux mentions « NON MESURÉ » des parties 4 et 5.
