# Context — Bam2Beta — 2026-08-12 (soir, fusion de 3 sessions)

**Branche** : main
**Dernier commit** : a22974f — docs(QC): instruction du palier 1 (MAD et coverage_percent écartés, N50 retenu)
**Status** : ⚠️ snapshot **fusionné**. 4 fichiers restent non commités, tous issus de la session
« distribution de longueur », **aucun de la session seuils/doc**.

## Où j'en suis

Trois chantiers sur le même sujet, tous à un point d'arrêt propre.

**Palier 1 du doc QC-seuils — instruit en entier.** Les 5 candidats calculables sont tranchés
et portés dans `docs/QC-seuils-biopsie-liquide.md` (`a22974f`) : MAD **écarté**, N50 **retenu**,
`coverage_percent` **écarté**, taux de mapping **requalifié**, méthylation CpG **écartée**.

**N50/N75 — livré et poussé** (`a95a36b`) : câblé dans `Extract_read`, 1 324 TSV rétrospectifs
sur S3, sortie identique octet par octet au rétrospectif.

**SEUILS DÉTERMINÉS (soir) — `1,26` / `1,43`.** Zones A/B/C = 92,7 % / 2,4 % / 4,9 %. Méthode :
chaque seuil au **milieu d'un intervalle vide** de la distribution (1,2463-1,2752 et
1,3976-1,4530), donc ±0,013 / ±0,023 ne reclassent personne. **Aucun label de matrice** n'a servi
à les fixer — la validation par matrice n'est venue qu'après. Voir [[n50-ratio-qc]].

**Google Doc QC** ([[gdoc-qc-ratio-n50]]) : figures 1-2 refaites en logique autosomes chr1-22
(matin), puis **document entièrement réécrit** (soir) — 9 sections, 5 figures, 5 tableaux,
3 listes nominatives, ~16 400 car. Ouvre sur `Breast_6`, paragraphes courts + puces.

## Ce qui marche / ce qui foire

- ✓ `a22974f` poussé — 3 verdicts de la session palier 1 (MAD, N50, `coverage_percent`)
- ✓ Mémoire : [[qc-palier1-candidats-ecartes]] et [[gdoc-qc-ratio-n50]] créés, [[n50-ratio-qc]]
  enrichi des seuils, des EQC et de l'application Imagenome
- ✓ **Validation a posteriori des seuils** : plasmas 98,1 % en zone A · urines 71,6 % en C et
  19,8 % en B · les 22 contrôles synthétiques **Twist 100 % en A**
- ✓ **Les 12 contrôles qualité externes** (Breast/Prostate CGFL) tombent **tous en zone grise**,
  1,3289-1,3649 (0,036 d'amplitude), masse > 1 kb < 0,2 %. Explique 12 des 32 de la zone grise
- ✓ **10 patients Imagenome Labosud en aveugle** (hors des 1 324) : tous zone A
- ✗ **Angle mort du ratio** : il ne voit pas la contamination qu'il a filtrée. `Breast_6` (57 %
  de masse > 1 kb) et `TNE_2` (81 %) sont classés zone A → toujours l'accompagner de
  `pct_mass_removed` (~2 % chez un plasma normal, examiner au-delà de 25 %)
- ✗ **4 plasmas** en zone grise restent inexpliqués (`Lung_Alc_93_av`, `Lung_Alc_15_av`,
  `Lung_124`) — et non 16 comme écrit avant l'identification des EQC
- ✗ **`docs/QC-seuils` porte 2 sections dont aucune session ne se déclare auteure**
  (« taux de mapping », « méthylation globale CpG »). Commitées par solidarité de fichier,
  contenu **non vérifié** — signalé dans le message de `a22974f`
- ✗ **Non commités, session « distribution de longueur »** : `workflow/frag.nf` (+29,
  `Length_Distribution_Plot`), `workflow/beta.nf` (+7, idxstats), `bin/length_distribution/`,
  `NOTE_READ.txt`. Décision **laissée à Boris**
- ✗ `dev/SCW/*.sh`, `note.txt`, `prompt_generator.pdf` : modifiés **avant** ces sessions
- ✗ Écart non tranché : la section 4 du doc dit « longueur moins soft-clips », les figures 1-2
  utilisent `length(SEQ)` brut. Préexistant, non corrigé

## ⚠️ Erreur commise et corrigée — à ne pas refaire

J'ai affirmé que `Colon_22` HCL et `Colon_22` CGFL étaient **le même patient**, et j'en ai tiré
un argument pré-analytique. **C'est faux** : 75 noms d'échantillons sont partagés entre les deux
labos et désignent des prélèvements **différents**. Toute jointure doit se faire sur le triplet
`(nom, type, labo)` — sans quoi les effectifs gonflent (1 393 lignes pour 1 243 plasmas) et les
conclusions inter-labo sont fausses. Corrigé dans le Google Doc.

## Prochaine étape

1. Trancher le sort des 4 fichiers non commités de la session « distribution de longueur ».
2. Décider si `n50_ratio.tsv` entre dans `check-run-output.sh` — ce qui le ferait basculer dans
   la qualification ISO 15189.
3. Instruire les 4 plasmas restants de la zone grise.
4. Documentation analogue pour le **nombre de reads alignés** (prompt déjà préparé par Boris).
