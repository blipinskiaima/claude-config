---
name: lung-alc-qc-recensement
description: "Recensement QC de la cohorte Lung_Alc CGFL (226 samples) par case d'interpretation, publie dans l'onglet Lung_Alc du Google Doc QC — 94,2 % conformes, 3 des 6 cas de la grille croisee vides"
metadata:
  node_type: memory
  type: project
  originSessionId: 26ddc2c6-4453-4f2c-8844-a7dbb79c1a63
  modified: 2026-08-17T14:13:23.039Z
---

# Recensement QC des Lung_Alc CGFL (2026-08-17)

Etat des lieux de la cohorte au regard des seuils **deja ecrits** (aucun seuil nouveau).
Publie dans le Google Doc QC, **onglet `Lung_Alc` (`t.zdeivtsmvstg`)** — 5e onglet, cree par
Boris ce jour-la, vide avant l'insertion. Voir [[gdoc-qc-ratio-n50]].

⚠ **Le texte publie a ete retravaille a la main par Boris apres l'insertion initiale** — la
version ci-dessous decrit l'etat **final**, pas le premier jet. Les differences sont notables :
voir « Ce qui a ete retire au montage » en bas de fiche.

## Perimetre — 226 samples, pas 229

229 lignes `Lung_Alc%`, **toutes CGFL, toutes liquid, `prod_status='OK'` a 100 %**.
**3 ecartees** : `Lung_Alc_75_av`, `76_av`, `76_prog` en `_rebasecalled_V5.0.0` — meme POD5 que
leur homologue (rendement quasi identique : 81,32 vs 81,18 M). Choix de Boris : **226**.

- 150 `_av` + 75 `_prog` + 1 `Lung_Alc_76_prog_bis` (seconde replique de sequencage : 31,15 M
  contre 59,65 M, ce n'est PAS un retraitement).
- **151 patients** : 74 ont les deux temps, 76 en `_av` seul, **1 en `_prog` seul (n°91)**.
  ⚠ Un agent avait annonce 72/77 — **faux**, le decompte verifie est 74/76/1.
- `metadata` (clinique) est **vide 0/229** pour cette cohorte. `mvaf_v1_ft092/095` aussi (mais
  497/1493 sur le reste de la base).

## Le tableau publie — 13 lignes x 6 colonnes

Boris a restructure le tableau apres le premier jet : ajout d'une colonne **`QC`** qui groupe
les cases en `Primaire` / `Contributif`, et **suppression de la case « Controle qualite
externe »** (elle etait a 0, comme « Contamination masquee » et « Contamination averee » qui
restent affichees a 0).

| Axe | QC | Case | Condition | n | % |
|---|---|---|---|---:|---:|
| Comptages | Primaire | Profondeur — conforme | ≥ 0,25× | 215 | 95,1 |
| | | Profondeur — en defaut | < 0,25× | 11 | 4,9 |
| | | nb_reads_total | aucun seuil | 226 | 100,0 |
| | | nb_reads_primaire — conforme | `reads_primary` ≥ 5 M | 214 | 94,7 |
| | | nb_reads_primaire — en defaut | `reads_primary` < 5 M | 12 | 5,3 |
| | Contributif | QC contributif — conforme | `reads_primary_mapped` ≥ 4 M | 214 | 94,7 |
| | | QC contributif — en defaut | `reads_primary_mapped` < 4 M | 12 | 5,3 |
| Fragmentation | Contributif | Nominal | ratio ≤ 1,26 et masse ≤ 22 % | 223 | 98,7 |
| | | Contamination masquee | ratio ≤ 1,26 et masse > 22 % | 0 | 0,0 |
| | | Artefact d'alignement | ratio 1,26–1,43 et masse 0,2–10 % | 2 | 0,9 |
| | | Contamination averee | ratio 1,26–1,43 et masse > 10 % | 0 | 0,0 |
| | | Profil non plasmatique | ratio > 1,43 | 1 | 0,4 |

`nb_reads_primaire` (colonne 5 M) et `QC contributif` (colonne 4 M) affichent les **12 memes
samples** — recouvrement total, voir plus bas.

## Ce qui a ete retire au montage — a ne pas rechercher dans le doc

Le premier jet comportait un axe **« Profils »** (3 cases : non alignees > 30 %, supplementaires
> 10 %, et une case « Mixte » regroupant les 226 - 226 anormaux qui ne franchissent aucun des
deux seuils mais cumulent les deux defauts). **Boris l'a entierement retire** du texte final,
jugee trop complexe a la lecture — la case « Mixte » en particulier n'etait pas comprehensible
sans schema. Ont disparu avec lui :
- le detail des 21 valeurs aberrantes du Primary mapped % (test de Tukey)
- le constat « 14 des 21 aberrants sont conformes sur les deux axes »
- le bloc final a 4 puces (2x Etabli / NON ETABLI / NON MESURE), remplace par une **Synthese**
  a une seule phrase

**Ces constats restent vrais** (mesures sur le meme dump, non invalidees), mais ils ne sont
**plus dans le document** — a ne pas chercher, a ne pas supposer visibles pour un lecteur du doc.
Si reutilises ailleurs (autre onglet, autre cohorte), les rechiffrer plutot que citer le doc.

Nouveaute du montage final, non exploree cote Claude : l'intro mentionne desormais un **« rapport
Exis »** comme source des cases d'interpretation, en plus des deux onglets QC. Exis apparait par
ailleurs dans `qara_lib.py` (`SCORE_SOURCE = mvaf_v14 # Exis 1.1`) — lien non verifie avec ce
recensement.

## Les chiffres qui restent visibles dans le doc

| Axe | Case | n | % |
|---|---|---:|---:|
| Comptages | QC primaire/contributif KO (recouvrement total) | 12 | 5,3 |
| Comptages | Profondeur KO | 11 | 4,9 |
| Fragmentation | zone verte / grise / rouge | 223 / 2 / 1 | 98,7 / 0,9 / 0,4 |
| Synthese | conformes sur les **deux** axes | 213 | 94,2 |

## Les constats a retenir (mesures de session, partiellement publies)

1. ⚠ **Recouvrement 100 %** entre QC primaire et contributif (85,9 % sur les 1 332 liquides,
   cf. [[qc-deux-niveaux]]) : le second niveau **n'ecarte rien de plus** ici. Cause :
   `reads_unmapped_pct` plafonne a **20,47 %**, tres sous le seuil de 30 % qui motive le niveau
   contributif — le profil des urines de vessie en est absent. **Publie dans le doc.**
2. ⚠ **Le croisement ratio × masse ne reclasse aucun Lung_Alc** : la masse > 1 kb plafonne a
   **13,93 %** (`Lung_Alc_94_av`) contre une bascule a 22 %. Aucune contamination gDNA dans
   cette cohorte. Voir [[n50-ratio-qc]]. **Publie dans le doc.**
3. ⚠⚠ **14 des 21 aberrants sont conformes sur les deux axes**, dont `Lung_Alc_79_prog` —
   43,02 % de lignes supplementaires, mais 15,02 M de primaires, 1,59× et ratio 1,0932 → **rendu
   sans reserve**. 6 des 10 samples a suppl. > 10 % sont dans ce cas. **Retire du doc au montage
   final** (voir section ci-dessus) — reste vrai, non publie.
4. `Lung_Alc_73_prog` : **50,70 % de supplementaires** → sa profondeur de 0,31× est
   trompeusement conforme (mosdepth ne filtre pas les supplementaires). C'est le seuil de 5 M
   qui l'ecarte, pas la couverture. Recoupe le chantier ouvert des 4 plasmas HCL. **Publie dans
   le doc** (mentionne en toutes lettres dans « Axe des comptages »).

## Validation croisee

**21/229 = 9,2 %**, exactement le taux d'aberrants deja publie pour « Lung Alc » dans la partie 5
de l'onglet `Nb reads mapped` — le doc calculait donc sur 229 lignes. Et les **6 Lung_Alc deja
nommes dans le doc** tombent au chiffre pres sur la base (`15_av` 1,3014/1,93 %/0,11×/2,19 M ·
`27_prog` 1,6364/6,69 % · `79_av` 18,04 % · `79_prog` 43,02 %/4,31 % · `93_av` 1,3976/6,38 %).

## Reproduction

Dump 226 × 47 colonnes + script de recensement : scratchpad de session (ephemere, non conserve).
Requete source : `samples` ⋈ `qc_metrics` ⋈ `qc` sur `sample_id`, filtre
`sample_name LIKE 'Lung_Alc%' AND labo='CGFL'`, exclusion des `_rebasecalled_V5.0.0`.
Borne de Tukey reprise du doc (Q1 71,47 / Q3 74,62) → **66,745 %**, pas recalculee sur la cohorte.
