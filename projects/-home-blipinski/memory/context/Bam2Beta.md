# Context — Bam2Beta — 2026-08-14 (fusion de 3 sessions : 10h11, QC deux niveaux, fin de journée)

**Branche** : main
**Dernier commit** : b2d5401 — docs(QC): manuel d'utilisation du duo ratio N50/N75 x masse > 1 kb
**Status** : 7 fichiers non commités, tous **antérieurs** (dev/SCW/*.sh, note.txt,
NOTE_READ.txt, qualifStatus.txt, 2 PDF). Aucun code touché dans la journée.

## Où j'en suis

### Session 10h11 — manuel ratio N50/N75 × masse (restitution, pas de code)

Livrable commité : `docs/QC-manuel-ratio-n50-masse.md` — 5 définitions d'une phrase + les
6 cas de l'arbre, vulgarisé, sans méthodologie de seuils. **Tous les effectifs du Google Doc
vérifiés en base** : matrice croisée 3×4 (1217/10/15/14/3/65), case `C × <0,2 %` vide, vallée
de masse vide entre 18,07 % et 25,94 %. Aucun chiffre publié n'est faux.

### Session QC deux niveaux — Partie 6 du Google Doc (terminée, aucun code)

Architecture de contrôle qualité instruite puis rédigée dans l'onglet « Nb reads mapped »,
partie 6. Mémoire : [[qc-deux-niveaux]]. **Rien n'est implémenté.**

- **QC primaire** = `nb_reads_aligned` → à renommer **`nb_reads_primary`** (A+D), seuil **5 M**,
  arrêt du workflow, actionnable client. **QC contributif** = `reads_primary_mapped` (D),
  seuil **4 M**, résultat rendu avec réserve, appelle un nouveau prélèvement.
- Seuils fondés sur la **table `rarefaction`** : 458 échantillons aux 5 niveaux, **11,1 % de
  faux positifs induits** sous 5 M ; coude à 4 M pour le contributif.
- Effectifs : arrêt 72 (5,41 %) · non contributif 6 (0,45 %) · contributif 1 246 (93,54 %).
- 4 figures produites (périmètres existant / ajout / synthèse + arbre de décision), scripts
  dans le scratchpad de session, **non versionnés**.

### Session fin de journée — origine des reads non alignés des urines (terminée)

Parti de la Partie 5 du Google Doc QC (« 16 échantillons, le génome ne les accueille pas »),
**les 16 ont été instruits de bout en bout**. Résultat porté dans le doc (fin de Partie 5,
sous-section + figure) et en mémoire ([[unmapped-reads-urines]]).

**Deux populations, sans recouvrement, séparées par le VOLUME séquencé (3,31 M / 9,09 M)
et non par le taux de non-alignement :**
- 8 à forte charge (9,1-70,6 M) : une bactérie occupe 52 à 87 %. **6 espèces différentes**,
  aucune partagée. 2 co-infections.
- 8 à faible volume (0,6-3,3 M) : aucun organisme dominant. **Pas des contaminations** —
  des séquençages qui ont produit trop peu d'ADN.

## Ce qui marche / ce qui foire

### Reads non alignés

- ✓ **Référence d'alignement identifiée** : MinKNOW 6.5.14, GRCh38 no_alt (195 contigs),
  **sans decoy hs38d1**. ≠ le hg38 UCSC de `params.fasta`. Porté en Architecture Notes.
- ✓ **Contamination de labo écartée** : `01_001` et `01_003` ont le même *P. mirabilis*
  mais des **souches distinctes** (86,5 % vs 62,8 % sur le même génome).
- ✓ **Sous-estimation de Kraken2 résolue** : reads courts + mauvaise souche de référence.
  K-12 → UTI89 = **+19,4 pts**. On passe de 15-35 % à 52-87 % expliqués.
- ✓ Finding `067` de covdepth **requalifié** : pas 34 M de reads alignés, mais 99,82 % de
  **non alignées**. Corrigé dans MEMORY.md.
- ✗ **Origine du portage NON déterminable** : infection / colonisation / souillure au recueil /
  prolifération avant congélation donnent le même profil. Demande l'ECBU et le délai avant
  congélation — données côté biologiste.
- ✗ `02_044` non identifié (reads de 72 pb). Statut uropathogène **non vérifié** pour
  *Citrobacter*, *Providencia*, *Morganella*, *Alcaligenes*. PlusPF-16 abandonné en cours.

### QC deux niveaux

- ✓ **`nb_reads_aligned` ≡ `reads_primary`** vérifié 1332/1332 : le nom est faux, la valeur est
  bonne. Source tracée dans le pipeline : `cut -f 6` sur cramino = `num_reads` (et non
  `num_alignments`, colonne 4). Le renommage du champ JSON n'est **pas** engagé — breaking
  change pour trace-platform et Aima-Tower.
- ✓ **Le seuil de 5 M n'est appliqué automatiquement NULLE PART** : ni Bam2Beta ni trace-prod.
  Uniquement `qc_threshold=5.0` dans `Aima-Tower/src/callbacks.py:954` — une ligne rouge sur
  boxplot. Toute la journée était partie de l'hypothèse inverse.
- ✓ **Le seuil « > 97 % de mapping » (PMID 37442577) est réfuté** : max cohorte **96,42 %**,
  il rejetterait 1324/1324. Le doc de palier 1 le pressentait sur **1** échantillon.
- ✗ **Recouvrement de 85,9 %** entre les deux critères : le contributif ne vaut pas par le
  nombre (6 échantillons) mais par leur nature. À assumer explicitement en revue.
- ✗ Le seuil de 5 M est mesuré sur des **lignes** raréfiées ≈ **4,2 M molécules** : retenir 5 M
  sur `reads_primary` est plus strict que la mesure. Écart à consigner si le seuil est discuté.
- ✗ **INCIDENT** : j'ai écrasé la réécriture de la partie 6 par Boris (`deleteContentRange`
  alors que la taille avait changé de 6118 → 5152). **Non récupérable** via l'API Drive.
  Boris a tout réécrit. Règle actée : [[feedback_gdoc_no_overwrite]].

### Manuel ratio N50/N75

- ✗ **2 incohérences internes du Google Doc non corrigées** (Boris a choisi de ne pas les
  consigner) : §9 dit « au-delà de 25 % » là où §10 fixe **22 %** ; §7 dit « 16 urines et
  16 plasmas » en zone grise là où §8.3 établit 16 urines + 12 EQC + **3 plasmas**
- ✗ **Le « 10/16/20/6 » de la partie 10 n'est pas reproductible** sans la définition exacte
  de « plasma » retenue : un proxy hors-urines donne 23/16/33/6. Seul « les deux = 6 » est invariant
- ✗ Boris écrit systématiquement « % de masse < 1 kb » alors que la colonne est
  `% Masse > 1kb` — signalé 3 fois, jamais tranché explicitement

## Prochaine étape

1. **4 plasmas HCL (`Colon_49/51/58`, `Lung_122`) — chantier du 12/08 toujours ouvert.**
   Avancé en passant : leurs 17 à 24 % de lignes supplémentaires sont désormais **mesurés sur
   le génome entier** (et non plus sur 2 Mb de chr2), avec un non-alignement normal de 6-7 %.
   **Reste non tranché** : palindromes vs concatémères — `reads_supplementary` dit qu'elles
   sont en excès, pas **où** les morceaux retombent, donc ne sépare pas couverture réelle et
   double comptage. Enjeu : `mosdepth` ne filtre pas les supplémentaires, le seuil de rendu
   à 0,25× en dépend.
2. Intégrer le manuel ratio N50/N75 dans le Google Doc « QC » — cible jamais confirmée
   (onglet *Ratio N50/N75*, ou ailleurs).
3. Demander au biologiste l'ECBU et le **délai avant congélation** des 8 urines à forte
   charge bactérienne — ce qui trancherait infection vs prolifération post-prélèvement.
4. Instruire `reads_unmapped_pct` comme signal QC direct : le seuil de profondeur intercepte
   14 des 16 **sans voir la cause**, qui diffère entre les deux groupes. **Recoupe le QC
   contributif** (`reads_primary_mapped ≥ 4 M`), qui attrape 6 de ces urines — mais par le
   volume utile, pas par le taux de non-alignement.
5. **Décider du renommage `nb_reads_aligned` → `nb_reads_primary`** dans `metadata.json` :
   breaking change pour `trace-platform/check_platform.py` et Aima-Tower. Documenté, non engagé.
6. **Seuil de contributivité propre à FRAG** : `reads_primary_mapped` est en amont de FRAG
   (hors chr1-22, médiane 3,27 %) et de 28M (MAPQ<20). `reads_frag` est publié et calculable
   tout de suite ; `reads_28m` reste **NULL 1332/1332** tant que Preprocess_28M ne publie rien.

Matériel du chantier reads non alignés : `/scratch/boris/unmapped` (29 Go, index Kraken2
Standard-16 inclus).
