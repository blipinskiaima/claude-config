---
name: n50-ratio-qc
description: "QC N50/N75 avant-apres filtre 1 kb — detecteur de contamination gDNA du plasma, dans Extract_read (frag.nf), sortie QC/Samtools/{ID}.n50_ratio.tsv"
metadata: 
  node_type: memory
  type: project
  originSessionId: ccc47027-333b-40a9-a728-dd1f326dc446
  modified: 2026-08-14T10:11:34.002Z
---

# QC N50/N75 — detecteur de contamination gDNA (2026-08-12)

Ajoute dans le process **`Extract_read`** ([workflow/frag.nf]) au commit `a95a36b`.
Sortie : `QC/Samtools/{ID}.n50_ratio.tsv`, **12 colonnes**, une ligne par sample.

## Ce que ca detecte, et pourquoi les seuils actuels ne le voient pas

La paire de seuils de rendu (5 M reads OU 0,25x) compte la **quantite**. La contamination
du plasma par de l'ADN genomique leucocytaire est un defaut de **forme** — les deux sont
independants, donc le QC actuel trie au hasard vis-a-vis de ce defaut.

**Le N50 pondere par la MASSE d'ADN** (somme longueur x effectif), pas par le nombre de
reads. C'est ce qui le rend sensible la ou la mediane est aveugle : sur les 8 plasmas
contamines identifies, `median_length` vaut 163-176 pb (parfaitement normal) pendant que
le n50 monte a 1 608 et 3 647.

## Valeurs de reference (1 324 samples liquid, mesure 2026-08-11)

| | mediane | p95 | p99 | max |
|---|---:|---:|---:|---:|
| **plasma** (n=1 243) | **1,10** | 1,19 | 1,89 | 24,4 |
| **urine** (n=81) | 1,78 | 2,75 | 3,59 | 3,6 |

Distribution plasma extremement serree : 95 % entre 1,10 et 1,19. Les urines forment un
**mode separe** (matrice differente, cellules urotheliales desquamees) -> un seuil unique
serait faux pour l'une des deux.

Part de masse portee par les reads > 1 kb : plasma mediane **2,3 %** · **9 plasmas > 50 %**,
dont **5 sont rendus** aujourd'hui sans signalement.

## Les 2 gotchas a ne jamais perdre

1. **Les DEUX jeux (avant/apres filtre) sont indispensables.** L'ecart fait le diagnostic,
   pas l'une des deux valeurs. `Breast_6` : ratio **24,44** avant, **1,11** apres -> son
   cfDNA est sain, la contamination s'est ajoutee par-dessus. Ne garder que l'apres-filtre
   le rendrait indistinguable d'un plasma normal.
   Le `ratio_f` separe meme deux profils : `Breast_6`/`TNE_2` retombent a 1,11 (contamination
   pure) alors que la serie `Colon_22` reste a 1,86-2,09 (cfDNA lui-meme altere).

2. **NOS N50 NE SONT PAS COMPARABLES A CEUX DE CRAMINO.** Sur `Breast_6` : cramino 3 808,
   nous 4 643 (**+22 %**). Le n75 concorde (185 vs 190) car il tombe dans le pic
   nucleosomal ; le n50 non car il est dans la queue. Cause : cramino voit 9,41 M reads
   contre 7,86 M pour FRAG — perimetre BED chr1-22, `-F 3840` et soft-clips retires
   diffèrent. Ne jamais melanger les deux sources dans une analyse ou un seuil.

## Implementation

Lit `${ID}.read_lengths.csv` **que le process vient d'ecrire** (pas de relecture du BAM).
awk + sort, aucune dependance nouvelle, container `bam2beta:latest` (awk 5.1.0, sort 8.32).

Algorithme : histogramme `cnt[longueur]++` -> `sort -k1,1rn` sur les **~50 000 valeurs
distinctes** (pas les 8 M lignes) -> double cumul de masse. Le filtre n'agit qu'au cumul,
avec un **denominateur reduit** (`totf`) — sans quoi le cumul filtre n'atteindrait jamais
50 % du total complet. Seuil `L <= 1000` (une read de 1 000 pb est **conservee**), en dur,
recopie dans la colonne `length_threshold`.

Optimisation : un tri par insertion en awk etait quadratique sur 50 k valeurs -> 65 s/sample.
Le passage a `sort` externe donne **2,7 s**, resultat identique.

## Retrospectif deja en place

**1 324 TSV uploades sur S3** (811 CGFL + 513 HCL) dans `QC/Samtools/`, verifies par scan
recursif. Le pipeline produit un fichier **identique octet par octet** (verifie sur
`Healthy_826` et `Breast_6`). Aucun recalcul retrospectif necessaire.

## Non traite

- `conformity/check-run-output.sh` ne verifie **aucun** fichier de `QC/Samtools/`. Ajouter
  `n50_ratio.tsv` au contrat verifie le ferait entrer dans la qualification ISO — decision
  non prise.
- ~~Aucun seuil de rendu n'est fixe~~ → **SEUILS DETERMINES le 2026-08-12, voir ci-dessous.**
  Reste vrai : le sens **haut uniquement** — la sur-fragmentation est sans objet (plancher
  biologique du nucleosome a ~147 pb, le plasma le plus court fait 136 pb, soit x0,82 de la
  mediane).

## Seuils (2026-08-12) — sur `ratio_n50_n75_filtered`, reads <= 1 kb

Determines **sans aucun label de matrice**, par la seule geometrie de la distribution : elle est
multimodale, et chaque seuil est place **au milieu d'un intervalle ou aucun echantillon n'existe**
(1,2463-1,2752 et 1,3976-1,4530). Deplacer un seuil de +/-0,013 (bas) ou +/-0,023 (haut) ne
reclasse donc **personne** — c'est ce qui manque aux seuils 5M/0,25x, qui coupent en pleine densite.

| zone | condition | n | % |
|---|---|---:|---:|
| A — analysable | ratio <= **1,26** | 1 227 | 92,7 |
| B — zone grise | 1,26 < ratio <= **1,43** | 32 | 2,4 |
| C — non interpretable | ratio > **1,43** | 65 | 4,9 |

Distribution plasma : mediane **1,10** · p95 1,19 · p99 1,89. Le seuil unique (1,26 seul) reste
possible ; le double est prefere car la zone grise est une population **reellement ambigue**.

**Validation a posteriori** (labels utilises seulement APRES) : plasmas 98,1 % en A · urines
71,6 % en C et 19,8 % en B · les 22 controles synthetiques **Twist 100 % en A**.

⚠ **Angle mort** : le ratio filtre ne voit pas la contamination qu'il a filtree. `Breast_6`
(57 % de masse > 1 kb) et `TNE_2` (81 %) sont classes en **zone A**. Toujours l'accompagner de
`pct_mass_removed` — voir la grille croisee ci-dessous.

## Grille croisee ratio x masse (2026-08-12) — partie 10 du Google Doc

Source : `qc_metrics.n50_n75_ratio` (= le ratio **filtre**, verifie identique a la mesure de
session) et `qc_metrics.pct_mass_removed`, schema **v24**. 1 324 liquides portent les deux.

**Les deux criteres ne se recouvrent qu'a moitie** — sur 1 208 plasmas : ratio > 1,26 seul
**10**, masse > 22 % seule **16**, l'un ou l'autre **20**, les deux **6**. `corr` = 0,725 en
lineaire mais **0,408 en log-log** : ils partagent une tendance, pas une information.

### Seuil de masse : 22 % (et non 25 %)

Meme methode que le ratio : **aucun plasma entre 18,07 % et 25,94 %** (vallee de 7,87 points),
milieu = **22 %**, marge ±3,9. Le 25 % initialement propose tombait dans la meme vallee mais a
0,94 point de son bord haut — meme classement, moins robuste. Descendre a 10 % couperait en
pleine densite (p90 = 5,6 · p95 = 8,5 · p98 = 13,9) et ajouterait 28 samples sans motif
structurel. Alternative conservatrice : **32 %** (vallee 28,98-35,94), 10 plasmas au lieu de 16.

**Seconde bascule : 0,2 %** — les 12 EQC y sont tous, contre 1 % des plasmas et 0 % des Twist.

### Matrice croisee complete — VERIFIEE en base le 2026-08-14

Les 6 cas ci-dessous sont une lecture de cette grille (1 324 liquides) :

| ratio \ masse | < 0,2 % | 0,2-10 % | 10-22 % | > 22 % | total |
|---|---:|---:|---:|---:|---:|
| **A** <= 1,26 | 13 | 1 176 | 28 | **10** | **1 227** |
| **B** 1,26-1,43 | **15** | **14** | 2 | 1 | **32** |
| **C** > 1,43 | **0** | 14 | 16 | 35 | **65** |
| total | 28 | 1 204 | 46 | 46 | **1 324** |

Tous les effectifs publies dans le Google Doc tombent exactement (1217 / 10 / 15 / 14 / 3 / 65),
**case vide `C x <0,2 %` comprise**. La vallee de masse est confirmee vide entre `Prostate_31`
(18,07 %) et `Pancreas_6_rebasecalled` (25,94 %).

⚠ Le « 10 / 16 / 20 / 6 » de la partie 10 suppose une definition de « plasma » **plus stricte**
qu'un simple hors-urines : ce proxy donne 23 / 16 / 33 / 6. Seul le « les deux = 6 » est invariant.

### Les 6 cas

| cas | ratio | masse | n | lecture |
|---|---|---|---:|---|
| Nominal | <= 1,26 | <= 22 % | 1 217 | rendu sans reserve |
| **Contamination masquee** | <= 1,26 | > 22 % | **10 plasmas** | **signaler** — `TNE_2` 81,4 %, `Breast_6` 57,3 %, `TNE_5` 35,9 %, 4x `Colon_20` 27-29 %, `Pancreas_6` 26,3 %. ⚠ 6 prelevements distincts seulement |
| Controle externe | 1,26-1,43 | < 0,2 % | 15 | ne pas alerter — 13 lignes EQC (12 distincts) + **2 urines** tres propres |
| Artefact d'alignement | 1,26-1,43 | 0,2-10 % | 14 | 12 urines ; chez les plasmas = chimeres (`Lung_Alc_93_av`) |
| Contamination averee | 1,26-1,43 | > 10 % | 3 | dont `Lung_124` (17,4 %) |
| Non plasmatique | > 1,43 | indifferente | 65 | ne pas rendre — 89 % d'urines |

⚠ **La case `ratio > 1,43` + `masse < 0,2 %` est VIDE** : un ratio franchement eleve s'accompagne
toujours d'ADN long. Un ratio rouge n'est jamais un pur artefact de calcul.

### Le seuil de 1 kb est le bon compromis — ne pas le bouger

Instruit en recalculant ratio et masse a 6 seuils (500 pb -> 3 kb) :

- **Descendre coupe dans le cfDNA legitime** : un plasma sain a 2 pics nucleosomaux (160 et
  296 pb) et plus rien au-dela. A 500 pb, `Healthy_826` (sain) passerait de 2,4 % a **6,2 %** de
  masse « retiree ».
- **Descendre detruit la detection** : a 500 pb `Colon_22_rep1` — le plasma le plus altere —
  tombe a **1,158**, soit en zone verte. On retire le signal de l'anomalie avec les reads.
- **Monter fait perdre la masse** : a 3 kb l'urine la plus chargee n'a plus que 2,5 % de masse,
  sous la mediane plasma → invisible au critere qui rattrape justement l'angle mort.
- **Stabilites** : `Breast_28` (sain) reste a 1,0972 de 500 a 3 000 pb ; `Breast_17` (EQC) a
  1,3333. 1 kb ≈ **6 nucleosomes** — au-dela, plus de signature apoptotique.

**Aucun flag QC implemente** : c'est une recommandation de lecture, ni en base ni dans le pipeline.

⚠ **Perimetre de mesure — piege confirme le 12/08.** Les valeurs de reference de `Breast_6`
doivent etre lues sur **tout** `read_lengths.csv` (perimetre BED chr1-22), pas sur un
echantillonnage regional :

| | `chr2:50-56 Mb` | **tout le fichier** |
|---|---:|---:|
| reads > 1 kb | 3,5 % | **3,02 %** |
| masse portee | 63 % | **57,26 %** |
| read la plus longue | 57 105 pb | **109 561 pb** |

Les 2 premieres sont dans `n50_ratio.tsv` ; la longueur max **n'existe nulle part**, il faut
relire le CSV. Les mesures sur `chr2` restent legitimes pour **qualifier un mecanisme**
(chimeres, palindromes, continuite d'alignement) mais jamais pour **chiffrer une proportion**.

## Les 12 controles qualite externes forment un mode a part

Les 12 EQC de CGFL (`Breast_17/32/47/49/50/52`, `Prostate_2/3/23/37/38/39`) tombent **tous les 12
en zone grise**, entre **1,3289 et 1,3649** — 0,036 d'amplitude, le groupe le plus resserre de
toute la cohorte — avec une masse > 1 kb de **0,00 a 0,19 %** (les plus propres du jeu).

Materiel de reference industriel : distribution plus etalee qu'un cfDNA natif, mais identique
d'un flacon a l'autre. **Leur position en zone grise est attendue, ce n'est pas une alerte.**

Consequence : la zone grise se decompose en **16 urines + 12 EQC + 3 plasmas** reellement
inexpliques (et non 16 plasmas « de cause inconnue » comme ecrit avant cette identification).
A l'inverse les controles **Twist**, concus pour mimer un profil de cfDNA, sont tous en zone A —
l'indicateur distingue les deux types de controle.

## Les 3 plasmas de la zone grise — mecanismes tranches par la mesure

Une fois urines et EQC retires, il reste **3 plasmas** (et non 4 : le 4e etait
`Breast_17_rebasecalled`, donc un EQC). **Causes distinctes, pas de mecanisme commun.**

Critere discriminant = sur les reads **>= 1 kb**, part **splittee** et part de sequence
**alignee en continu** (le meme test qui avait etabli que `Breast_6` portait du vrai gDNA) :

| sample | ratio | masse >1kb | align/read | reads >=1kb splittees | continu | len max |
|---|---:|---:|---:|---:|---:|---:|
| `Lung_Alc_93_av` CGFL | 1,3976 | 6,4 % | **1,453** (rang 3/1229) | **91,5 %** | **48 %** | 5 201 |
| `Lung_124` HCL | 1,3081 | **17,4 %** | 1,008 (rang 1159) | **2,7 %** | **99,3 %** | **29 255** |
| `Lung_Alc_15_av` CGFL | 1,3014 | 1,9 % | 1,115 (rang 28) | 62,5 % | 71,9 % | 4 026 |
| *(ref)* `Breast_6` | — | 57,3 % | — | 1,8 % | 98,8 % | 65 204 |

- **`Lung_Alc_93_av` = chimeres.** 31,6 % de reads chimeriques, et 91,5 % de ses molecules
  longues sont **decoupees** avec moins de la moitie de sequence alignee d'un tenant : ce sont
  des assemblages, pas des molecules.
- **`Lung_124` = vraie contamination par ADN long.** Meme signature que `Breast_6` (99,3 %
  continu, jusqu'a 29 kb) mais plus modeste : 2 379 pb de moyenne contre 8 926 pb. D'ou une
  traine qui s'eteint vers 3 kb sur la figure.
- **`Lung_Alc_15_av` : indecidable** — seulement **16 reads >= 1 kb**, effectif trop faible.
  Son ratio vient plutot de ses 14,7 % de chimeres. Il est de toute facon **deja rejete** par
  les seuils actuels (0,11x, 2,19 M reads).

⚠ Ne pas conclure sur le seul `align/read` : c'est un proxy. Le test direct (splittees + continu)
est ce qui separe un artefact d'alignement d'une vraie molecule longue.

## Application en aveugle — 10 patients Imagenome Labosud (s3://aima-platform)

Hors des 1 324 ayant servi aux seuils, nature inconnue a l'avance. **Les 10 en zone A**, ratio
1,0764 a 1,1481 (tous sous le p95 de 1,19), masse > 1 kb de 0,22 a 9,95 %. Premiere application
reelle de l'indicateur.

## Cablage trace-prod (schema v22 + v24)

Table `qc_metrics`, override des getters dans `LiquidChecker` (`lib/checkers.py:703-733`) ;
`BaseChecker` reste sur cramino et demeure la voie du **solid**.

| colonne DB | type | source liquid |
|---|---|---|
| `n50` | INTEGER | `n50_filtered` |
| `n75` | INTEGER | `n75_filtered` — **stocke, JAMAIS exporte** en gsheet |
| `n50_n75_ratio` | DECIMAL(10,4) | `ratio_n50_n75_filtered` — **lu, pas recalcule** |
| `pct_mass_removed` | DECIMAL(5,2) | `pct_mass_removed` — **liquid uniquement** |

Export gsheet `Trace PROD` (onglets liquid), colonnes **9-11** : `N50` · `Ratio N50/N75` ·
`% Masse > 1kb`. 4 decimales obligatoires sur le ratio (toute la plage tient entre 1,06 et 2,20).

⚠ **`N50` a DEUX definitions selon l'onglet** : samtools filtre en liquid (mediane 174 bp,
max 574), cramino **non filtre** en solid (mediane 3 804 bp, max 9 727). Non comparables.
Consequence assumee de la bascule v24 — `n50_ratio.tsv` n'existe pas en solid (0/40 sondes).

⚠ **Gotcha `NaN`/`inf`** : `float('NaN')`/`float('inf')` ne levent pas `ValueError`, et
`n50/inf = 0.0` est *fini* — une garde `isfinite(resultat)` laisse passer un `0,0000` faux.
**Valider les deux OPERANDES, jamais le resultat.**

## Manuel d'utilisation

`docs/QC-manuel-ratio-n50-masse.md` (2026-08-14) — 5 definitions d'une phrase + les 6 cas de
l'arbre, vulgarise, **sans methodologie de determination des seuils**. Destine a une lecture en un
coup d'oeil ; l'instruction detaillee reste dans `docs/QC-seuils-biopsie-liquide.md` et le
[[gdoc-qc-ratio-n50]].

⚠ **Le nom de la metrique est `% Masse > 1kb`** (`pct_mass_removed` = masse **au-dessus** du
seuil). L'inverser changerait le sens de lecture des seuils : 2 % deviendrait 98 %.

Voir [[softclip-fragmentomics-length]] pour la convention de longueur, et
[[covdepth-qc-valorization]] pour le chantier QC dont ce travail est issu.
