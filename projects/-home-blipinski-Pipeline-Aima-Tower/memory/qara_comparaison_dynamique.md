---
name: qara-comparaison-dynamique
description: "Vue dynamique de /qara (v5.7.0) : trois régimes de mesure distincts, Themelio non comparable par construction, et pourquoi la cohorte CUP du doc n'est pas reproductible."
metadata: 
  node_type: memory
  type: project
  modified: 2026-09-11T14:48:22.582Z
  originSessionId: 8caa8c85-cc3c-48c2-b136-83f5dc4b6a95
---

# `/qara` — comparaison au point figé (2026-09-11, v5.7.0)

Un interrupteur sous les trois cartes de la vue d'ensemble déplie une seconde rangée,
mesurée sur trace-prod. **Les cartes publiées ne bougent pas.** Premier appel réseau de
la page, qui était jusque-là 100 % statique : `GET /api/qara/live`, déclenché seulement
par le toggle (≈ 5 s à froid, 0,4 s ensuite).

## L'alignement est structurel, pas réglé à la main

Demande explicite de Boris : *« il faut que les éléments soient au même endroit
verticalement, sinon on va vite se perdre »*. La solution retenue n'est pas de recopier
des marges : la carte dynamique **réutilise le composant `Kpi`** de la carte figée et
itère sur **`p.kpis`**, donc elle affiche par construction les deux mêmes métriques,
avec les mêmes libellés et périmètres. Seules les valeurs changent.

`Kpi` a gagné un emplacement optionnel `middle` (entre la mesure et sa désignation) où
la rangée dynamique place l'écart. Les cartes figées ne le passent pas.

⚠ **L'écart n'est jamais coloré** : `=`, `↑/↓ x,x pt`, `+n éch.`, empilés, en gris.
« +1 cancer au dénominateur » n'est ni bon ni mauvais. Le teinter en magenta reproduirait
le piège rencontré deux fois au passage à la charte ([[charte_site_tokens]]).

## Trois régimes de mesure, volontairement différents

| Produit | Régime | Pourquoi |
|---|---|---|
| **Exis** | `exploratory_service.compute()` aux réglages Exis figés | **Aucun calcul maison** — mêmes réglages que [[qara_tower_skill]]. La sortie est lue telle quelle (chaînes `« 95.1% (213/224) »`, champ `Sens_Cancer_AI` et **non** `Sens_AI`) |
| **CUP** | comptage de `too_final_decision` | La strate est **déjà décidée par le pipeline** ; `max_p` n'est pas en base, donc **aucun seuil n'est ré-appliqué** |
| **Themelio** | seuils s1/s2 du bundle sur `themelio_score` | Mesuré et affiché, mais marqué `comparable: False` |

## ⚠ Themelio : l'écart mesure la méthode, pas les données

C'est le point le plus important de la session, et il a demandé une longue enquête.
`clinical_config.rds` du bundle `themelio_1_0` le dit lui-même :

```
calibration : "5-fold OOF"                        ← ce que publie le document
production  : "transfer (full model, not OOF)"    ← ce que stocke trace-prod
```

Sur les **mêmes 301 échantillons** (77 cancers + 224 sains) : sensibilité **54,5 % au doc,
62,3 % en base**. Le modèle de production a vu ces cancers à l'entraînement, donc il les
reconnaît mieux. Les deux chiffres sont justes ; leur différence ne décrit pas les données.

⚠ **Le même bundle est utilisé des deux côtés** : Bam2Beta est épinglé sur
`themelio_1_0.rds` et `run_themelio.R` refuse de tourner si `bundle$themelio_version`
n'est pas `"1.0.0"`. Ce n'est donc pas un problème de version de modèle.

**Source des chiffres publiés, trouvée par élimination** :
`screening_top10_xgb/releases/themelio_1_0/results/oof_predictions.csv`, filtré sur
`scoring_method == "5-fold OOF"`. Il reproduit le doc exactement : sains 1 au-dessus de
s1 et 4 au-dessus de s2, cancers Detection 24 / Suspicious 18 / Negative 35.
⚠ Ne **pas** utiliser `screening_top10_xgb/results/screening_top10_xgb_predictions.csv` :
il donne 0 sain au-dessus des deux seuils et 119 cancers — c'est un autre entraînement.
Je m'y suis trompé et j'ai conclu à tort que le score avait été recalculé.

## ⚠ La cohorte CUP du document n'est pas reproductible

`n = 284` est un **jeu de développement figé** au moment de l'entraînement, pas un filtre.
Le plus proche équivalent mesurable aujourd'hui (« active cancer, mVAF v1.4 > 0 »,
restreint aux 5 classes, réplicats dédupliqués) en compte **522**. Les effectifs de
strates comparent donc des populations de tailles différentes — dit dans le README.

En revanche `tumor_of_origin/regulatory/output/tables/oof_predictions.csv` contient les
284 **avec leur `max_p`**, et **284/284 mVAF v1.4 sont identiques** à aujourd'hui : la
cohorte CUP elle-même n'a pas bougé d'un chiffre.

## La divergence 94/95 du document CUP est résolue

Un seul échantillon, `CGFL_Bladder_Blood_02_094`, a un `max_p` **exactement égal** au
seuil `0,825743846152373`.

```
max_p >= seuil   →  (ii) 94, (iii) 95            = les tableaux §4/§5 du doc
max_p >  seuil   →  (ii) 95, (iii) 94, 47,4 % / 90,4 %   = le pipeline, la figure, la phrase
```

Le document ne contient donc pas une erreur de chiffres : il décrit la même cohorte avec
deux conventions de seuil. Les pourcentages publiés viennent du `>` strict.
⚠ L'encart de [[qara_page]] reste valable, mais sa cause est maintenant connue.

## Pièges techniques rencontrés

- ⚠ **`samples.sample_name` n'est pas unique** (1531 lignes / 1456 noms). Toute jointure
  avec un fichier du pipeline doit passer par `unique_id` = `labo` + nom débarrassé des
  suffixes techniques. Une jointure par nom fabrique des lignes et des valeurs fausses —
  piège déjà documenté dans [[endpoints_exploration_casses_preexistants]], j'y suis
  retombé quand même.
- ⚠ `_get_prepared` prend le **frozenset dorado** en `version_mode`, pas une chaîne.
  Avec `"v5.0.0"` on obtient 148 sains au lieu de 224.
- ⚠ `samples` n'a **pas** de colonne `indication` : elle est dérivée du nom par
  `_extract_indication`.
- Les trois documents ont **trois dates d'émission différentes** (Exis 06/07, CUP 13/07,
  Themelio 16/07) — chaque carte figée porte la sienne, il n'y a pas de date unique.

Voir aussi : [[qara_page]], [[qara_refonte_vitrine]], [[qara_tower_skill]],
[[charte_site_tokens]].
