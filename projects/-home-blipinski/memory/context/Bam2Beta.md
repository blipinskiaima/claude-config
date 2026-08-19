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
- ✓ **Chargé en base par une session parallèle** — trace-prod **schema v25** (19/08 08:36) : `qc.reads_28m` et le nouveau `qc.reads_with_cpg` sont **1332/1332 non-NULL** (étaient 0)
- ✗ Le tableau de recensement redit l'axe Comptages déjà traité dans la partie 1 (choix assumé, format `Lung_Alc`)
- ✗ Aucune figure sur la partie Ratio (croisement ratio × masse et arbre de décision non régénérés)

## Prochaine étape
Écrire la **partie 3 de l'onglet `Nb reads mapped`**, restée vide : « proportion de reads
utilisés pour la mVAF 1.4 vs nombre total ». Les données sont désormais en base (v25), le
verrou est levé — restent aussi à lever les deux mentions « NON MESURÉ » des parties 4 et 5.
Repère mesuré sur Lung_9 : 29,3 M reads dans le BAM 28M dont **19,2 M portent au moins un CpG**
(65,4 %), soit **43,2 %** des 44,4 M lignes du BAM d'origine.

## Chantiers ouverts hérités (snapshot du 14/08)
- **4 plasmas HCL** `Colon_49/51/58`, `Lung_122` : 17-24 % de lignes supplémentaires mesurées
  sur génome entier, non-alignement normal 6-7 %. Non tranché : palindromes vs concatémères —
  `reads_supplementary` dit qu'elles sont en excès, pas **où** les morceaux retombent. Enjeu :
  `mosdepth` ne filtre pas les supplémentaires, le seuil de rendu 0,25× en dépend.
- **ECBU + délai avant congélation** des 8 urines à forte charge bactérienne — trancherait
  infection vs prolifération post-prélèvement. À demander au biologiste.
- **Renommage `nb_reads_aligned` → `nb_reads_primary`** dans `metadata.json` : breaking change
  pour `trace-platform/check_platform.py` et Aima-Tower. Documenté, jamais engagé.

Matériel du chantier reads non alignés : `/scratch/boris/unmapped` (29 Go, index Kraken2 inclus).
