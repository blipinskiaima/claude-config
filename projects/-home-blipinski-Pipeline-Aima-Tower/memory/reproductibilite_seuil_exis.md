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

## Le seuil ne s'étend pas à v1.0 (mais bien à v1.5)

⚠ L'argument porte sur l'**échelle**, pas sur le numéro de version : `mvaf_v15` partage la
colonne et le format de v1.4 et a donc reçu ce seuil en report le 2026-08-27.

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

## Limite visuelle — RÉSOLUE le 2026-08-27

À l'échelle linéaire, tout ce qui est sous 0,0042 est collé à zéro : **les points changeaient
de couleur sans qu'on voie pourquoi**. C'est exactement ce que Boris a fini par signaler
(« la coloration n'est pas dépendante du seuil alors qu'elle devrait l'être ») — elle l'était,
mais rien ne le montrait.

⚠ Ce paragraphe disait qu'aucune ligne de seuil n'avait été ajoutée et que le champ
`thresholds` ne s'y prêtait pas. **Les deux ont changé** : `thresholds` accepte désormais
`s2: null` (une coupure, légende à 2 catégories) et la ligne est tracée pour v1.4 et v1.5,
valeur affichée en légende. Voir [[reproductibilite_v15_graphe_qc]].

## Tests

`test_mvaf_is_binary` figeait l'ancienne règle (`0,0001 → detection`). Remplacé par
`test_mvaf_v14_uses_exis_threshold` (bornes comprises : `0,0042` exactement → négatif,
la règle étant strictement supérieur) et `test_mvaf_v1_stays_binary`, qui verrouille le
fait que v1.0 ne bouge pas.

Voir aussi : [[reproducibilite_page]], [[exis_alignment]], [[dashboard_bloc_produits]].
