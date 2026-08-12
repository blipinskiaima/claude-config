# Context — Bam2Beta — 2026-08-12 (fusion de 4 sessions)

**Branche** : main
**Dernier commit** : fca2844 — feat(mito): active MITO sur les profils prod et solid
**Status** : ⚠️ snapshot **fusionné**. La session « distribution de longueur » est desormais
**commitee et poussee** (e8eac18 + fca2844). Restent 4 fichiers non commites, tous **anterieurs**
a ces sessions : `dev/SCW/*.sh`, `note.txt`, `NOTE_READ.txt`, `prompt_generator.pdf`.

## Où j'en suis

Quatre chantiers sur le même sujet, tous à un point d'arrêt propre.

**Palier 1 du doc QC-seuils — instruit en entier.** Les 5 candidats calculables sont tranchés
et portés dans `docs/QC-seuils-biopsie-liquide.md` (`a22974f`) : MAD **écarté**, N50 **retenu**,
`coverage_percent` **écarté**, taux de mapping **requalifié**, méthylation CpG **écartée**.

**N50/N75 — livré et poussé** (`a95a36b`) : câblé dans `Extract_read`, 1 324 TSV rétrospectifs
sur S3, sortie identique octet par octet au rétrospectif.

**SEUILS DÉTERMINÉS — `1,26` / `1,43`.** Zones A/B/C = 92,7 % / 2,4 % / 4,9 %. Méthode :
chaque seuil au **milieu d'un intervalle vide** de la distribution (1,2463-1,2752 et
1,3976-1,4530), donc ±0,013 / ±0,023 ne reclassent personne. **Aucun label de matrice** n'a servi
à les fixer — la validation par matrice n'est venue qu'après. Voir [[n50-ratio-qc]].

**CASCADE DE COMPTAGE DES READS — bouclée de bout en bout.** Les 12 comptages sont définis,
mesurés sur les 1 332 liquides, exportés en gsheet et documentés. Voir [[read-counting-cascade]].
- Pipeline : `idxstats` publié par `BAM_Count` (`c5e3765`) — la strate des reads non alignées
  n'était mesurable nulle part, elle vaut 9,2 % sur Lung_9 et jusqu'à 18 % ailleurs
- Rétrospectif : les 1 471 samples calculés et déposés sur S3 (créations pures, zéro écrasement)
- Base : table `qc` trace-prod, schema v23, 25 colonnes — commitée par une autre session (`dce1d45`)
- Doc : Google Doc QC, onglet « Nb reads mapped » — 3 parties, 13 titres, 5 figures, 2 tableaux

**DISTRIBUTION DE LONGUEUR — livree et poussee** (`e8eac18`). Process
`Length_Distribution_Plot` dans `frag.nf` : un PNG par sample, 4 courbes (sample courant + 3
references embarquees), ligne de seuil a 1 kb, publie dans `Fragmentomics/filtered_softclipped`.
References calculees avec la **methode exacte d'`Extract_read`** (`-F 3840` + BED chr1_22 +
soft clips retires) : Breast_28 0,31 % / Bladder_Urine_02_041 23,08 % / Breast_6 57,26 % de masse
au-dela de 1 kb. ggplot2 3.5.2 deja dans `bam2beta:latest`, binning awk en streaming (3,8 s pour
9,2 M de reads). Verifie sur 3 samples reels.

**MITO active prod + solid** (`fca2844`) : corrige le KO systematique de l'etape 2 de
`/test_bam2beta`, qui exigeait `mito_qc.tsv` des que le sample est liquid alors que le profil
`prod` desactivait le module. ⚠ Jamais execute sur du solid a ce jour.

**Google Doc QC ratio** ([[gdoc-qc-ratio-n50]]) : 9 sections, 5 figures, 5 tableaux,
3 listes nominatives. Ouvre sur `Breast_6`, paragraphes courts + puces.

## Ce qui marche / ce qui foire

- ✓ `a22974f` poussé — 3 verdicts de la session palier 1 (MAD, N50, `coverage_percent`)
- ✓ Mémoire : [[qc-palier1-candidats-ecartes]], [[gdoc-qc-ratio-n50]], [[read-counting-cascade]]
  créés ; [[n50-ratio-qc]] enrichi des seuils, des EQC et de l'application Imagenome
- ✓ **Validation a posteriori des seuils** : plasmas 98,1 % en zone A · urines 71,6 % en C et
  19,8 % en B · les 22 contrôles synthétiques **Twist 100 % en A**
- ✓ **Les 12 contrôles qualité externes** (Breast/Prostate CGFL) tombent **tous en zone grise**,
  1,3289-1,3649 (0,036 d'amplitude), masse > 1 kb < 0,2 %. Explique 12 des 32 de la zone grise
- ✓ **10 patients Imagenome Labosud en aveugle** (hors des 1 324) : tous zone A
- ✓ **Cascade validée deux fois** : A+B+C+D = Total sur 1 332/1 332 samples, et concordance
  exacte avec `samtools flagstat` sur 10 samples couvrant tous les profils
- ✓ **`flagstat` n'apporte rien** : duplicates et QC-failed à 0 sur 10/10 (le pipeline ne marque
  pas les duplicats) → toute la cascade se reconstitue depuis les fichiers publiés + `idxstats`
- ✓ **Validation croisee forte** : sur `Bladder_Urine_02_041`, le `pct_mass_removed` calcule
  par le run (23,08 %) est **identique** a la masse > 1 kb de la reference embarquee, par deux
  chemins de calcul entierement independants (BAM re-merge depuis 144 BAM horaires vs BAM RetD)
- ✓ **Non-regression** : `check-conformity` vs QUALIF V2.2.0 conforme **41/41**
- ✓ **Mecanisme des chimeres qualifie** (2 mecanismes distincts, pas un) : CGFL `Lung_Alc` =
  **concatemeres de ligation** (90,9 % des morceaux sur un autre chromosome, dispersion conforme
  au hasard genomique, aucun adaptateur interne alors que le test le detecte chez le temoin) ;
  HCL `Colon`/`Lung_12x` = **reads palindromiques** (95 % meme locus brin oppose < 1 kb,
  exactement 2 morceaux) → **double comptage de profondeur** cote HCL
- ✗ **`/test_bam2beta` etape 1 KO** : echec d'upload S3 du BAM de **16,8 Go** de `Lung_9`
  (+ `read_start_time.tsv` de 2,5 Go). `Healthy_826` exit 0. Incident reseau, pas un bug — mais
  Nextflow ne reessaie pas et tout le test tombe
- ✗ **Angle mort du ratio** : il ne voit pas la contamination qu'il a filtrée. `Breast_6` (57 %
  de masse > 1 kb) et `TNE_2` (81 %) sont classés zone A → toujours l'accompagner de
  `pct_mass_removed` (~2 % chez un plasma normal, examiner au-delà de 25 %)
- ✗ **4 plasmas** en zone grise restent inexpliqués (`Lung_Alc_93_av`, `Lung_Alc_15_av`,
  `Lung_124`) — et non 16 comme écrit avant l'identification des EQC
- ✗ **`28M` et `MAPQ<20` NULL partout** dans la table `qc` : `Preprocess_28M` s'exécute 22 fois
  par run sans publier aucun comptage (todo posée, basse priorité)
- ✗ **8 Bladder_Urine sans `idxstats`** (1 324/1 332) : ajoutés en base pendant la session,
  postérieurs au rétrospectif
- ✗ **Mécanisme des 4 plasmas HCL NON tranché** (`Colon_49/51/58`, `Lung_122`) : 17-24 % de
  lignes supplémentaires. Mesures exploratoires sur 2 Mb de chr2 seulement → **session dédiée
  demandée par Boris**, ne pas conclure sur cet échantillonnage
- ✗ **`docs/QC-seuils` porte 2 sections dont aucune session ne se déclare auteure**
  (« taux de mapping », « méthylation globale CpG »). Commitées par solidarité de fichier,
  contenu **non vérifié** — signalé dans le message de `a22974f`
- ✗ **Non commités, session « distribution de longueur »** : `workflow/frag.nf` (+29,
  `Length_Distribution_Plot`), `bin/length_distribution/`, `NOTE_READ.txt`,
  `conf/{prod,solid}.config` (MITO=true). Décision **laissée à Boris**
- ✗ `dev/SCW/*.sh`, `note.txt`, `prompt_generator.pdf` : modifiés **avant** ces sessions
- ✗ Écart non tranché : la section 4 du doc dit « longueur moins soft-clips », les figures 1-2
  utilisent `length(SEQ)` brut. Préexistant, non corrigé

## ⚠️ Erreur commise et corrigée — à ne pas refaire

J'ai affirmé que `Colon_22` HCL et `Colon_22` CGFL étaient **le même patient**, et j'en ai tiré
un argument pré-analytique. **C'est faux** : 75 noms d'échantillons sont partagés entre les deux
labos et désignent des prélèvements **différents**. Toute jointure doit se faire sur le triplet
`(nom, type, labo)` — sans quoi les effectifs gonflent (1 393 lignes pour 1 243 plasmas) et les
conclusions inter-labo sont fausses. Corrigé dans le Google Doc.

**Le piège a resservi le 12/08** : le rétrospectif `idxstats` nommait ses sorties
`out/{ID}.tsv`, donc les 75 homonymes CGFL/HCL s'écrasaient — et l'idempotence faisait hériter
le second du résultat du premier, soit **75 fichiers faux**. Corrigé en `out/{type}/{labo}/{ID}`.
Vérifier ce point à chaque script qui indexe par nom de sample.

## Prochaine étape

1. **Investigation dédiée sur les 4 plasmas HCL** (`Colon_49/51/58`, `Lung_122`) : le
   **mecanisme est desormais identifie** — ce sont des reads **palindromiques** (95 % des
   morceaux au meme locus, brin oppose, < 1 kb), donc bien un **double comptage** et non une
   couverture legitime. Mais la mesure porte toujours sur **2 Mb de chr2 uniquement**. Reste a
   confirmer sur le genome entier et a chiffrer l'impact reel sur `depth` : `mosdepth` ne filtre
   pas les supplementaires (`-F 1796` par defaut), donc le seuil de rendu a 0,25x en depend.
2. Décider si `n50_ratio.tsv` entre dans `check-run-output.sh` — ce qui le ferait basculer dans
   la qualification ISO 15189.
4. Instruire les 4 plasmas restants de la zone grise.
5. ~~Documentation analogue pour le nombre de reads alignés~~ — **FAIT** (onglet « Nb reads
   mapped », 12/08).
