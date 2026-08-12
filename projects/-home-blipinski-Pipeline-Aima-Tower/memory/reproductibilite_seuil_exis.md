---
name: reproductibilite-seuil-exis
description: "/reproductibilite : mVAF v1.4 passe du binaire au seuil Exis 0,0042 — et pourquoi ça déplace aussi le taux d'accord des réplicats."
metadata: 
  node_type: memory
  type: project
  originSessionId: 77ec5d89-9e21-4626-81f9-57f4f990b853
  modified: 2026-08-12T15:30:20.880Z
---

# Seuil Exis 0,0042 sur /reproductibilite (2026-08-12)

Demande de Boris : « si supérieur à 0,0042 alors c'est positif, sinon négatif ».
Un seul point de code touché — `_category()` dans `src/reproducibility_service.py`.

```python
MVAF_V14_SEUIL = 0.0042      # quantile type 1 des 224 sains à 95 % — valeur Exis 1.1 / QARA

if model == "mvaf_v14":
    return "detection" if score > MVAF_V14_SEUIL else "negatif"
```

## Le seuil est propre à v1.4 — ne pas l'étendre à v1.0

`mvaf_v1` sort de `qc_metrics` (float), `mvaf_v14` de `retd_suivis` (VARCHAR virgule FR).
Échelles différentes, et aucun seuil n'a été calibré pour v1.0 : lui appliquer 0,0042
inventerait un nombre. v1.0 **reste binaire**. themelio garde ses deux seuils cliniques.

## Ce n'est pas qu'une couleur — le taux d'accord bouge

`_category()` est le point **unique** de décision, et `_family_stats` réutilise le verdict
pour `_pairwise_agreement`. Il n'existe qu'une définition du positif dans la page, donc
déplacer le seuil déplace la statistique. Mesuré avant/après :

```
REPRODUCTIBILITÉ PURE          avant     après
  Colon_21                      3/6   →   2/6
  Colon_22                      6/6   →   3/6    ← perd son unanimité
  GLOBAL                       93,8 %  → 85,4 %  (−8,4 pts)

MÉTHODES D'EXTRACTION
  Colon_62  2/6 → 3/6 ; Colon_63  3/6 → 2/6
  GLOBAL                       76,7 %  → 76,7 %  (se compense)
```

5 points sur 60 basculent. Le cas qui pèse est **Colon_22 Run 2 = 0,0041** — un
dix-millième sous le seuil, et une famille unanime devient discordante. La métrique
d'accord est désormais **sensible au voisinage immédiat de 0,0042**, ce que l'ancienne
règle (`> 0`) n'était pas. À dire quand on commente une baisse d'accord.

## Limite visuelle connue

À l'échelle linéaire, tout ce qui est sous 0,0042 est collé à zéro : **les points changent
de couleur sans qu'on voie pourquoi**. La case « Échelle logarithmique » le rend lisible.
Aucune ligne de seuil ni mention « > 0,0042 » n'a été ajoutée à la légende — pas demandé.
Le champ `thresholds` de `MODELS` ne convient pas tel quel : sa forme (`s1`/`s2`/3 labels)
est spécifique à themelio et ferait rendre une légende à 3 catégories.

## Tests

`test_mvaf_is_binary` figeait l'ancienne règle (`0,0001 → detection`). Remplacé par
`test_mvaf_v14_uses_exis_threshold` (bornes comprises : `0,0042` exactement → négatif,
la règle étant strictement supérieur) et `test_mvaf_v1_stays_binary`, qui verrouille le
fait que v1.0 ne bouge pas.

Voir aussi : [[reproducibilite_page]], [[exis_alignment]], [[dashboard_bloc_produits]].
