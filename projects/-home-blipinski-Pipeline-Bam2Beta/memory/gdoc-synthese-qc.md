---
name: gdoc-synthese-qc
description: "Onglet Synthese du Google Doc QC — les 5 QC liquid chiffres sur 1 324, seuil non-alignement 30 % sur A/(A+D), et les metriques ecartees pour apport net nul"
metadata:
  node_type: memory
  type: project
---

# Onglet « Synthèse » — 5 QC de la cohorte liquide (2026-08-19)

Onglet **`t.bw3qo6n8aizg`** du Google Doc QC (7 onglets depuis ce jour). Cree vide, rempli
integralement dans cette session : 6 parties, **11 tableaux**, 6 arbres ASCII (Courier New 9 pt),
~19 700 car. Plan impose par Boris, **identique pour chaque QC** : definition en 1 phrase, seuil,
tableau des cas, arbre de decision, liste des echantillons en defaut.

## Le perimetre 1 324 — definition exacte

`sample_type='liquid'` **∩** `qc.reads_unmapped IS NOT NULL`. Les 4 conditions candidates
(`reads_unmapped`, `n50_n75_ratio`, `pct_mass_removed`, ligne `qc`) donnent **le meme ensemble** —
verifie par intersection. 1 362 liquides en base → **1 324**, les **38 ecartes sont tous des
`Bladder_Urine_*` CGFL**. Composition **1 221 plasma / 81 urine / 22 Twist**.

⚠ Ne pas confondre avec les **1 332** de l'onglet « Nb reads mapped » partie 3 (= liquides avec
ligne `qc`, idxstats non requis). Boris a tranche : **c'est 1 324 partout**.

## Les 5 QC et leur colonne exacte

| QC | Colonne | Unite | Seuil | En defaut | % |
|---|---|---|---|---:|---:|
| Molecules generees (A+D) | `qc.reads_primary` | unites | ≥ 5 M | 72 | 5,4 % |
| Profondeur | `qc_metrics.depth` | X | ≥ 0,25× | 67 | 5,1 % |
| Ratio N50/N75 | `qc_metrics.n50_n75_ratio` | — | 1,26 / 1,43 | 32 + 65 | 2,4 / 4,9 % |
| Masse > 1 kb | `qc_metrics.pct_mass_removed` | % | ≤ 22 % | 46 | 3,5 % |
| Non-alignement | `reads_unmapped / reads_primary` | % | ≤ 30 % | 20 | 1,5 % |

**`nb_reads_aligned` = `reads_primary`, prouve 1332/1332** (tolerance 0,005 M). Le nom est faux
(il inclut les non alignees) mais la valeur est la bonne. Prendre `qc` (unites), pas `qc_metrics`
(millions, arrondi 2 decimales → 61/76 au lieu de 57/72 aux seuils).

## Le taux de non-alignement est passe au denominateur A+D

**Decision de Boris** : `reads_unmapped / reads_primary` (A+D), et non `reads_unmapped_pct`
(qui divise par `reads_total`, donc secondaires + supplementaires inclus). Mediane 10,96 → **13,00 %**.

| seuil | n | vide de la distribution |
|---|---:|---|
| 70 % (1re version) | 10 | **33,17 pts** entre 53,16 et 86,33 — milieu **69,75** |
| **30 % (retenu)** | **20** | 2,7 pts entre **28,97 et 31,65** |

Le changement de denominateur **ne reclasse personne** a 70 %. Les 20 en defaut a 30 % sont
**20 urines, 100 % CGFL**.

## Trois metriques a APPORT NET NUL — ne pas les reinstruire

1. **`reads_primary_mapped ≥ 4 M`** (le « QC contributif » de l'onglet Nb reads mapped) :
   73 en defaut, **0 apport net** — tous deja pris par 5 M ou 0,25×. **Ecarte du document.**
   ⚠ Contredit en apparence [[qc-deux-niveaux]] qui annoncait 6 : ce 6 etait mesure contre le
   **seul** 5 M, sans la profondeur.
2. **Le non-alignement a 70 %** : 0 apport net (les 10 sont a 0,00-0,06× de profondeur).
   A **30 %** il en gagne **3** : `Bladder_Urine_02_066` (0,92×), `02_119` (2,71×), `02_027` (1,09×).
3. Ecartes d'office : **MAD ichorCNA** et **`coverage_percent`** (voir
   [[qc-palier1-candidats-ecartes]]), **Fano** (pas en base), **28M/CpG** (en base, traites, mais
   aucun seuil etabli), **MITO** (pas de seuil, 1 095/1 324).

## Le levier de la profondeur est double — resultat etabli ici

Sur les **67** en defaut de profondeur : **60 sont aussi sous 5 M** (le resequencage corrige) et
les **7 autres depassent tous 30 % de non-alignement** (l'ADN n'est pas humain, resequencer est
inutile). L'arbre QC2 du document a donc **3 feuilles** la ou les autres en ont 2.

## Cascade d'ensemble (ordre 1-2-3-4-5)

1 324 → −72 → −7 → −48 → −6 → −1 = **1 190**, dont 22 en zone grise → **1 168 conformes (88,2 %)**,
**134 ecartes (10,1 %)**. Les 2 QC en vigueur en portent 79 sur 134.

**Les 329 Healthy sont 0 en defaut sur les QC 3, 4 et 5** (verifie en base). Les 22 Twist sont
tous conformes sur le ratio ; plasma 98,1 % / urine 8,6 %.

## Les listes en defaut sont des TABLEAUX segmentes

Format `Plage | Prelevements | dont urines | Echantillons`, paliers par gravite decroissante
(2 a 5 selon le QC). Regroupement par **prelevement** : rebasecalls et replicats fusionnes
(`Colon_22 ×6`, `Colon_20 ×4`, `Breast_6 ×2`, `Pancreas_6 ×2` — conforme au doc).

⚠ **Le regroupement doit etre ITERATIF et porter sur `(famille, labo)`** : les suffixes s'empilent
(`Colon_20_rep1_OK`) et **75 noms sont portes par 2 echantillons distincts** (1 CGFL + 1 HCL).
Regex : `(_rebasecalled(_V[\d.]+)?(_trimmed)?|_rep\d*|_moche(_\d+)?|_OK)$` appliquee jusqu'a
point fixe.

## Outillage d'ecriture — dans le scratchpad de session

`gdoc.py` (auth + garde-fous), `parse.py` (markdown → blocs), `write.py` (ecriture), `swap.py`
(remplacement liste → tableau), `check_intact.py`.

**Deux garde-fous a reproduire systematiquement** :
- `batch()` **leve une exception** sur tout type de requete destructrice, et sur toute
  `location`/`range` sans `tabId` (sans quoi l'ecriture part dans le 1er onglet).
  `deleteContentRange` n'est possible que sur **opt-in explicite**.
- Avant toute suppression : **comparer l'INTEGRALITE du texte de l'onglet** a ce qu'on croit y
  avoir ecrit. Egalite stricte = personne n'est passe. C'est ce qui manquait lors de l'incident
  du 2026-08-14 ([[feedback_gdoc_no_overwrite]]).

⚠ **Le `cwd` du shell revient a la racine du projet entre deux appels Bash** — un `cat > x.py`
sans `cd` prealable ecrit **dans le depot**. Toujours `cd <scratchpad> && ...`.

Voir [[n50-ratio-qc]] pour les seuils 1,26/1,43/22 %, [[qc-deux-niveaux]] pour l'architecture
primaire/contributif, [[unmapped-reads-urines]] pour la cause des 20 urines,
[[gdoc-qc-ratio-n50]] pour l'acces au document.
