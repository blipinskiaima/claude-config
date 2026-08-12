---
name: gdoc-qc-ratio-n50
description: "Google Doc 'QC' onglet Ratio N50/N75 — document de restitution des seuils QC, 5 figures, outillage python d'edition dans le scratchpad"
metadata: 
  node_type: memory
  type: reference
  modified: 2026-08-12T10:51:02.761Z
  originSessionId: b56b0f4a-9a7a-4318-bb95-549d981af39e
---

# Google Doc « QC » — onglet Ratio N50/N75

<https://docs.google.com/document/d/1X1KxOCR-eHRU04R3eSfyTlxa_C47R114pCw_BkoUHwQ/edit?tab=t.w79cz9osn5oa>

Document de restitution du travail QC. 4 onglets : **Ratio N50/N75** (`t.w79cz9osn5oa`),
Nb reads mapped, List_Of_Features, Figure du pipeline. L'onglet Ratio compte 6 sections et
**5 figures** legendees `[Figure N — …]`.

## Acces

API Google Docs v1 avec les credentials **gspread** (`~/.config/gspread/authorized_user.json`,
via `~/.claude/skills/qara-tower/scripts/qara_lib.py`). **`includeTabsContent=true` est
obligatoire** — sans ce parametre l'API ne renvoie aucun onglet.

Outillage python (scratchpad de session, a recreer si besoin) : `read_gdoc.py` (lecture),
`locate_images.py` (position des images inline + legende suivante), `make_figs.py` (les 5
figures en **matplotlib**), `insert_images.py`, `replace_figs12.py`.

## Remplacer une image

Les images sont des `inlineObjectElement` occupant **1 caractere**, inserees juste avant leur
paragraphe de legende. Pour en remplacer une : `deleteContentRange` sur `[startIndex,
endIndex]` puis `insertInlineImage` au meme index, dans **une seule** `batchUpdate`, en
traitant de l'index le plus grand vers le plus petit. L'image doit etre uploadee sur Drive et
partagee par lien **le temps de l'insertion seulement** — Docs copie le binaire, le partage
peut etre retire ensuite.

## Figures 1 et 2 — refaites en logique autosomes (2026-08-12)

Elles reposaient sur `chr2:50-56 Mb` (12-17 k reads). Refaites sur **chr1-22 entiers**
(5,9 a 7,9 M reads). La comparabilite region/genome a ete verifiee avant : ecart moyen
0,16-0,24 point de masse, max 1,91 — la region etait representative.

**Le choix des autosomes n'est pas cosmetique** : la section 4 du doc definit la population
comme « autosomes chr1 a chr22 seulement », et 7,5-8,1 % des alignements sont hors chr1-22
(surtout chrX). Surtout, il **aligne les figures 1-2 sur les donnees des parties 5-6**, qui
viennent de `read_lengths.csv` : la partie 5 annonce 57 %, la mesure autosomes donne 57,5 %,
la mesure tout-genome 55,9 %.

Trois valeurs du texte harmonisees en consequence : `3,5 % -> 3,1 %` (deux fois),
`63 % -> 57 %` (ce qui leve une incoherence interne 63/57 preexistante), et
`57 105 pb -> 451 105 pb` (l'ancienne valeur etait le max sur `chr2` seul).

⚠ **Ecart residuel non corrige** : la section 4 dit « longueur = sequence moins les
soft-clips », alors que les figures 1-2 utilisent `length(SEQ)` **brut**. Cet ecart
preexistait ; il explique aussi pourquoi les donnees de `bin/length_distribution/` ne
correspondent a aucune de ces extractions — elles viennent de `read_lengths.csv`.

Voir [[qc-palier1-candidats-ecartes]] et [[n50-ratio-qc]].
