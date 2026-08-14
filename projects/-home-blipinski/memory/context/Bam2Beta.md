# Context — Bam2Beta — 2026-08-14 (fusion de 2 sessions : 10h11 et fin de journée)

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
   14 des 16 **sans voir la cause**, qui diffère entre les deux groupes.

Matériel du chantier reads non alignés : `/scratch/boris/unmapped` (29 Go, index Kraken2
Standard-16 inclus).
