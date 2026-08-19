---
name: gdoc-qc-ratio-n50
description: "Google Doc 'QC' onglet Ratio N50/N75 — document de restitution des seuils QC, 5 figures, outillage python d'edition dans le scratchpad"
metadata: 
  node_type: memory
  type: reference
  modified: 2026-08-17T14:13:54.269Z
  originSessionId: b56b0f4a-9a7a-4318-bb95-549d981af39e
---

# Google Doc « QC » — onglet Ratio N50/N75

<https://docs.google.com/document/d/1X1KxOCR-eHRU04R3eSfyTlxa_C47R114pCw_BkoUHwQ/edit?tab=t.w79cz9osn5oa>

Document de restitution du travail QC. **5 onglets depuis le 2026-08-17** : **Ratio N50/N75**
(`t.w79cz9osn5oa`), Nb reads mapped (`t.8yj4pfggwlai`), List_Of_Features (`t.0`), Figure du
pipeline (`t.8zlmqz7ccpjt`), **Lung_Alc** (`t.zdeivtsmvstg`, cree par Boris le 2026-08-17 —
voir [[lung-alc-qc-recensement]]).

**Etat au 2026-08-12 fin de journee** : l'onglet Ratio a ete **entierement reecrit** — il compte
**10 sections, 10 figures, 7 tableaux et 3 listes nominatives**, ~24 900 caracteres.
La **partie 10** (croisement ratio x masse) a ete ajoutee le 2026-08-12 au soir. La section
« Pourquoi chercher un nouvel indicateur » a ete supprimee : le document ouvre directement sur
le constat factuel `Breast_6`. Redaction en paragraphes courts **+ puces**.

Plan : 1 constat `Breast_6` · 2 mediane vs N50 · 3 definitions et passage au ratio · 4 donnees
et filtres FRAG · 5 les trois cas (sain / rattrape / degrade) · 6 les seuils · 7 verification a
posteriori · 8 **qui tombe hors zone verte** (4 tableaux : zone rouge, grise, verte, + les
10 patients Imagenome en aveugle, + les 12 controles qualite externes) · 9 lecture et limites ·
**10 croisement avec la masse** (grille des 6 cas, arbre de decision, seuil 22 %, pourquoi 1 kb).

⚠ Sous les tableaux des 3 zones : **liste nominative complete** des echantillons (nom + ratio),
en corps 8 pt gris. 65 / 32 / 7 entrees.

## Acces — corrige le 2026-08-17

API Google Docs v1 avec les credentials **gspread** (`~/.config/gspread/authorized_user.json`).
**`includeTabsContent=true` est obligatoire** — sans ce parametre l'API ne renvoie aucun onglet.

⚠ **`googleapiclient` (`google-api-python-client`) n'est PAS installe** — verifie par `find /`,
zero resultat, et il n'existe aucun venv dans `~/Pipeline/*/`. `from googleapiclient.discovery
import build` echoue donc toujours. **Ne pas installer** : `gspread` 6.2.1 est dans
`~/.local/lib/python3.12/site-packages/` et apporte `google.oauth2.credentials` +
`google.auth.transport.requests`, ce qui suffit a rafraichir le token et a appeler l'API REST
directement avec `requests` (`https://docs.googleapis.com/v1/documents/{id}` et `:batchUpdate`).

⚠ **`qara_lib.py` ne porte AUCUNE logique Docs** — seulement la constante `GSPREAD_CREDS`.
L'ancienne formulation de cette fiche (« via qara_lib.py ») etait trompeuse.

⚠ **Scopes du token : `spreadsheets` + `drive` uniquement, PAS `documents`.** Le scope `drive`
suffit neanmoins a l'API Docs, en lecture **comme en ecriture** (verifie le 2026-08-17).

⚠⚠ **`tabId` est OBLIGATOIRE dans chaque `Location` et chaque `Range` d'un `batchUpdate`** sur ce
document multi-onglets. Omis, l'ecriture part dans le **premier onglet** (`Ratio N50/N75`, 27 084
caracteres) — risque de corruption silencieuse du plus gros onglet. Garde-fou a reproduire : une
fonction `batch_update` qui **leve une exception** si une requete contient `deleteContentRange`,
`replaceAllText`, `deleteTableRow`… (cf. [[feedback_gdoc_no_overwrite]]).

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
