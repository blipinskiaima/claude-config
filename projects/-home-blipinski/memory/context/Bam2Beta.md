# Context — Bam2Beta — 2026-08-12T11:05:00+00:00

**Branche** : main
**Dernier commit** : a22974f — docs(QC): instruction du palier 1 (MAD et coverage_percent écartés, N50 retenu)
**Status** : ⚠️ snapshot **fusionné de 2 sessions parallèles** (celle du N50/N75 + celle du palier 1).
7 fichiers restent non commités, tous issus de la session N50/N75.

## Où j'en suis

Deux chantiers menés en parallèle sur le même sujet, tous deux à un point d'arrêt propre.

**Palier 1 du doc QC-seuils — instruit en entier.** Les 5 candidats calculables sont tranchés
et portés dans `docs/QC-seuils-biopsie-liquide.md` (`a22974f`) : MAD **écarté**, N50 **retenu**,
`coverage_percent` **écarté**, taux de mapping **requalifié**, méthylation CpG **écartée**.

**N50/N75 — livré et poussé** (`a95a36b`) : câblé dans `Extract_read`, 1 324 TSV rétrospectifs
sur S3, sortie identique octet par octet au rétrospectif.

**Google Doc QC** ([[gdoc-qc-ratio-n50]]) : figures 1 et 2 refaites en logique **autosomes
chr1-22**, 3 valeurs du texte harmonisées. Comparabilité région/génome vérifiée avant.

## Ce qui marche / ce qui foire

- ✓ `a22974f` poussé — 3 verdicts de ma session (MAD, N50, `coverage_percent`) avec leurs mesures
- ✓ Mémoire : [[qc-palier1-candidats-ecartes]] (les 2 écartés, pour ne pas les réinstruire)
  et [[gdoc-qc-ratio-n50]] (accès API Docs + méthode de remplacement d'image) créés
- ✓ Google Doc à jour et vérifié après écriture : 5 images en place, figures 3-5 intactes
- ✗ **`docs/QC-seuils` porte 2 sections dont aucune des 2 sessions ne se déclare auteure**
  (« taux de mapping » et « méthylation globale CpG »). Commitées par solidarité de fichier,
  contenu **non vérifié** — signalé dans le message de `a22974f`
- ✗ **Non commités, appartenant à la session N50/N75** : `workflow/frag.nf` (+29,
  `Length_Distribution_Plot`), `workflow/beta.nf` (+7, idxstats), `bin/length_distribution/`
  (R + références), `NOTE_READ.txt`. Décision de commit/abandon **laissée à Boris**
- ✗ `dev/SCW/*.sh`, `note.txt`, `prompt_generator.pdf` : modifiés **avant** ces deux sessions
- ✗ Workflow feature « figure de distribution dans le pipeline » : arrêté à l'**Étape 1**
  (compte rendu rendu). L'autre session a implémenté la feature entre-temps, en **R/ggplot2**
  et depuis `read_lengths.csv` — ce qui est le bon choix, et rend mon Étape 2 caduque
- ✗ Écart non tranché : la section 4 du doc dit « longueur moins soft-clips », les figures 1-2
  utilisent `length(SEQ)` brut. Préexistant, non corrigé

## Prochaine étape

Trancher le sort des 4 fichiers non commités de la session N50/N75 (commit ou abandon) —
c'est le point bloquant commun aux deux snapshots. Ensuite : décider si `n50_ratio.tsv` entre
dans `check-run-output.sh`, ce qui le ferait basculer dans la qualification ISO 15189.
