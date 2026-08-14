# Context — Bam2Beta — 2026-08-14T10:11

**Branche** : main
**Dernier commit** : b2d5401 — docs(QC): manuel d'utilisation du duo ratio N50/N75 x masse > 1 kb
**Status** : 2 fichiers modifiés (`dev/SCW/*.sh`, antérieurs) + 4 untracked

## Où j'en suis

Session de **restitution**, pas de code : synthèse d'interprétation du duo
ratio N50/N75 × `% Masse > 1kb`. Exploration en lecture seule de trace-prod
(schema v22/v24, `LiquidChecker`), du calcul dans `frag.nf`, du Google Doc QC
et des gsheets. Livrable commité : `docs/QC-manuel-ratio-n50-masse.md` —
5 définitions d'une phrase + les 6 cas de l'arbre, vulgarisé, sans méthodologie
de seuils. Les 4 chantiers du 12/08 sont **au même point**, rien n'a avancé
côté pipeline.

## Ce qui marche / ce qui foire

- ✓ **Tous les effectifs du Google Doc vérifiés en base** : matrice croisée 3×4
  (1217/10/15/14/3/65), case `C × <0,2 %` vide, vallée de masse vide entre
  18,07 % et 25,94 %. Aucun chiffre publié n'est faux
- ✓ Manuel commité et poussé (`b2d5401`), mémoire `n50-ratio-qc` enrichie du
  câblage trace-prod et de la matrice
- ✗ **2 incohérences internes du Google Doc non corrigées** (Boris a choisi de
  ne pas les consigner) : §9 dit « au-delà de 25 % » là où §10 fixe **22 %** ;
  §7 dit « 16 urines et 16 plasmas » en zone grise là où §8.3 établit
  16 urines + 12 EQC + **3 plasmas**
- ✗ **Le « 10/16/20/6 » de la partie 10 n'est pas reproductible** sans connaître
  la définition exacte de « plasma » retenue : un proxy hors-urines donne
  23/16/33/6. Seul le « les deux = 6 » est invariant
- ✗ Boris écrit systématiquement « % de masse < 1 kb » alors que la colonne est
  `% Masse > 1kb` — signalé 3 fois, jamais tranché explicitement

## Prochaine étape

Intégrer le manuel dans le Google Doc « QC » (cible d'intégration jamais
confirmée : onglet *Ratio N50/N75* du Doc, ou ailleurs). Puis reprendre
l'investigation dédiée des **4 plasmas HCL** (`Colon_49/51/58`, `Lung_122`) :
mécanisme palindromique identifié mais mesuré sur 2 Mb de chr2 seulement,
à confirmer génome entier et chiffrer l'impact sur `depth`.
