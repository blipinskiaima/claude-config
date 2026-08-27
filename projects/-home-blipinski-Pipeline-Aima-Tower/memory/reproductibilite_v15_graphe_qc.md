---
name: reproductibilite-v15-graphe-qc
description: "/reproductibilite : mVAF v1.5 au seuil reporté de v1.4, seuils tracés, filtre de conformité QC, et les deux pièges Plotly de l'échelle log."
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-27T14:01:59.124Z
  originSessionId: 680b13e5-33bd-46c2-bf4f-44728c518e18
---

# `/reproductibilite` — mVAF v1.5, seuils tracés, filtre QC (2026-08-27)

## mVAF v1.5 : le seuil est REPORTÉ, pas calibré

`mvaf_v15` existait déjà en base (`retd_suivis`, schéma v26, backfill 100 % — 1362 samples,
0 KO résiduel), même fichier source et même `format_mvaf4` que v1.4. **Aucun seuil publié**
pour elle : rien dans Exis 1.1, rien dans le doc QARA.

Décision Boris : **réutiliser 0,0042**, le seuil v1.4. `_category()` fait donc
`if model in ("mvaf_v14", "mvaf_v15")`.

⚠ Ce n'est **pas** un seuil « à 95 % » pour v1.5. Mesuré avant de trancher : la recette Exis
(quantile type 1, 224 sains de la cohorte Exis, 95 %) reproduit exactement `0,0042` sur v1.4
— elle est donc valide — et donne **`0,0025`** sur v1.5. Comme v1.5 est **inférieure ou égale
à v1.4 partout** sur ces 224 sains, à seuil égal sa spécificité réelle **dépasse** les 95 %
visés. À dire avant de commenter un chiffre de spécificité v1.5.

⚠ Le raisonnement « propre à v1.4 » de [[reproductibilite_seuil_exis]] visait l'**échelle**,
pas le numéro de version : v1.0 sort de `qc_metrics` (autre échelle) et reste binaire ; v1.5
partage la colonne et le format de v1.4, d'où le report possible.

Effet mesuré : cohorte pure, accord 85,4 % (v1.4) → 87,5 % (v1.5) ; un seul verdict bascule,
`Colon_21_moche_2_rebasecalled_V5.0.0_trimmed` (détection → négatif).

## Les deux pièges Plotly de l'échelle log — vérifiés dans la page, pas déduits

C'est le cœur technique de la session. Boris signalait « une diagonale dans le graphe ».

**1. Le range est retenu d'un rendu à l'autre.** En basculant linéaire → log, Plotly conserve
le range calculé précédemment et le réinterprète comme des **exposants** : l'axe descendait à
`1e-48`, écrasant tous les points contre le haut du cadre. `autorange: true` **ne suffit pas**
— un `relayout` post-rendu corrigeait, le rendu lui-même non. Fix : le range log est calculé
(`logRange()`) et passé **explicitement** ; une borne explicite gagne toujours sur la retenue.
Axe passé de `[2,5e-49 ; 1,6e5]` à `[2,87e-7 ; 82,2]`.

**2. Les `shapes` prennent la valeur BRUTE, même sur l'axe log.** Plotly convertit lui-même.
J'avais « corrigé » l'inverse en croyant à un bug pré-existant sur themelio — c'était faux, le
code d'origine était juste. Mesuré sur le SVG rendu, cadre `[8 ; 364]` px :

```
y0 = 0,0042            → M56,188.65   ✓ dans le cadre
y0 = log10(0,0042)     → M56,3746     ✗ hors cadre (Plotly rejette le négatif)
```

⚠ Méthode à retenir : ces deux points étaient **indémontrables par lecture de code**. Ce qui
a tranché, c'est de lire `_fullLayout.yaxis.range` et l'attribut `d` du path SVG dans la page,
et de comparer les deux conventions par `Plotly.relayout`. Une shape à `y0 === y1` ne peut pas
être diagonale — j'ai perdu du temps à théoriser avant d'aller regarder.

## Zéros en échelle log : plancher + marqueur creux

Un axe log ne peut pas placer 0. Ils étaient passés en `null` donc **invisibles** ; sur ces
cohortes le zéro est pourtant le résultat le plus fréquent. Ils sont maintenant posés sur un
plancher une décade sous la plus petite valeur positive, en **marqueur creux** (`-open`) pour
ne pas se lire comme une mesure à cette hauteur, le survol donnant le vrai 0 via `customdata`
(`[nom, valeur réelle]`, sinon le hover afficherait la valeur du plancher).

## Seuils tracés : `thresholds` accepte désormais `s2: null`

La coloration **dépendait déjà** du seuil (`pointColor(p.category)` ← `_category()`), mais
rien à l'écran ne le montrait : `thresholds` valait `None` pour les mVAF, donc ni ligne ni
valeur en légende. Ce qui bloquait, c'est que la forme du champ (`s1`/`s2`/3 libellés) était
taillée pour themelio. Généralisée : `s2: null` = une seule coupure, légende à 2 catégories.
v1.0 reste sans ligne — sa règle est « > 0 », pas un seuil calibré, et une ligne à zéro se
confondrait avec l'axe.

## Filtre « Conformes uniquement » : il RECALCULE

`qc_only` garde les runs à `nb_reads_total >= 5` M **et** `depth >= 0,25×` (`nb_reads_total`
est **déjà en millions** en base). Métrique absente = **non conforme** (on ne peut pas prouver
la conformité). Mêmes valeurs que la pastille de `/sample/:id`.

⚠ Le filtre ne masque pas des points, il **refait** CV / accord / unanimité sur le
sous-ensemble — sinon le tableau décrirait une cohorte que le graphe n'affiche plus.
Cohorte pure : 85,4 % (41/48) → 87,2 % (34/39).

⚠ **Il écarte 11 runs, soit exactement le « n = 11 aliquots removed » publié en QARA §2.5**
(`depth` est le critère mordant ; `reads` n'en retire aucun de plus). Coïncidence vérifiée,
pas supposée — c'est un argument de traçabilité réglementaire, la page reproduit la méthode
publiée.

⚠ **8 de ces 11 sont des partiels `_OK`**, déjà hors statistiques et décochés par défaut : le
bandeau annonçait 11 disparitions pour 3 visibles. D'où `n_qc_excluded_partial` et le
décompte en deux parties. Piège général : un décompte au niveau cohorte ne se lit pas comme
un décompte à l'écran quand un autre filtre est déjà actif.

Voir aussi : [[reproducibilite_page]], [[reproductibilite_seuil_exis]], [[exis_alignment]],
[[qara_page]].
