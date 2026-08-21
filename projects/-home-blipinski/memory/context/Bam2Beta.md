# Context — Bam2Beta — 2026-08-21T08:40:17+00:00

**Branche** : main
**Dernier commit** : b2d5401 — docs(QC): manuel d'utilisation du duo ratio N50/N75 x masse > 1 kb
**Status** : 16 fichiers non propres — dont une feature `--MVAF15_RETRO` (mVAF v1.5)
écrite le 20/08 dans une AUTRE session, non commitée. Rien de cette session dans le dépôt.

## Où j'en suis
Onglet **Synthèse** du Google Doc QC (`t.bw3qo6n8aizg`) construit de bout en bout :
5 QC liquid chiffrés sur 1 324 échantillons, 5 sous-onglets, arbres de décision en
figures matplotlib, tableaux croisés matrice/statut. Le doc est dans un état livrable.

## Ce qui marche / ce qui foire
- ✓ Onglet Synthèse **en paysage** (seul des 14), 2 flowcharts : version **Exis** puis
  version **Thémélio** — elles ne diffèrent que par `NON PLASMATIQUE` (jaune / rouge)
- ✓ 5 sous-onglets alignés sur l'arbre principal : libellés, code couleur, QC3 simplifié
  en une question à 3 sorties
- ✓ Tableaux croisés **plasma/urine** et **healthy/cancer**, % avec dénominateur explicite
  en **prélèvements** (981 / 81 / 232 / 830 — pas en lignes)
- ✓ Cascade d'exclusion en fin d'onglet : 72 / 7 / 48 / 6 / 1 = **134 lignes écartées**,
  + tableau nominatif des 104 prélèvements
- ✓ Outillage Docs dans le scratchpad : garde-fous `tabId` obligatoire, refus des requêtes
  destructrices sauf opt-in, vérification d'intégrité avant toute suppression
- ✗ **Aucun QC n'est implémenté** — ni en base, ni dans le pipeline, ni dans
  `check-run-output.sh`. Le doc est une recommandation de lecture
- ✗ « Zone grise » subsiste **15× dans le Deep Dive**, 1× dans Lung_Alc, 1× dans On site —
  Boris a explicitement dit d'y toucher plus tard
- ✗ Les 2 figures de l'onglet Synthèse **n'ont aucun titre** dans l'image ; seuls les
  libellés « Exis : » / « Thémélio : » du texte les distinguent

## Prochaine étape
Aligner « zone grise » → « suspicion d'artefact » dans l'onglet Deep Dive (15 occurrences),
en `replaceAllText` avec `tabsCriteria` et phrases entières.
