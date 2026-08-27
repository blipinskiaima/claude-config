# Grille des pièges chiffrés

Tous constatés sur cas réels. À passer en revue systématiquement en phase 4.

## 1. Les trois jeux de chiffres d'un même test

Toute validation clinique produit au moins trois valeurs différentes pour la « sensibilité ».
Les confondre est l'erreur la plus fréquente **et la plus grave**.

| Niveau | Ce que c'est | Marqueur |
|---|---|---|
| **Observé** | mesuré sur la cohorte de validation | `[SOURCÉ]` |
| **Repondéré** | réestimé sur une population de référence (stades, âge) | `[PONDÉRÉ]` |
| **Validation croisée** | mesuré sur l'entraînement, **toujours meilleur** | ⚠ ne jamais citer comme performance |
| **Marketing** | plaquette, souvent sans publication | `[MARKETING]` |

**Cas réel DELFI** : observé 84 % / 53 % · repondéré 80 % / 58 % · validation croisée 84 %
pondéré avec spécificité 50 % · plaquette NNS 79 quand le papier dit 76.

Erreur commise : avoir présenté le repondéré comme observé — et donc reproché à l'industriel de
cacher une spécificité de 58 % alors que la vraie valeur observée, **pire**, était 53 %.

## 2. Une sensibilité sans sa spécificité ne veut rien dire

```
AIMA   53,8 % stade I @ spécificité 96,2 %   (n = 13)
DELFI  71 %   stade I @ spécificité 53 %     (n = 248)
GRAIL  18 %   stade I @ spécificité > 99 %
```

Ces trois nombres ne sont **pas comparables**. Toujours ramener à spécificité équivalente, ou
refuser la comparaison.

## 3. Performance combinée présentée comme celle du test seul

Vérifier ce qui entre dans le modèle qui produit le chiffre.

**Cas réels** : les 94 % de Mathios 2021 combinent fragmentation **+ facteurs de risque
cliniques + CEA + scanner**. Les « > 90 % » de Bruhm 2023 combinent mutations **+ autres
features + scanner**. Aucun n'est la performance d'un test sanguin autonome.

## 4. Effectifs insuffisants

Un pourcentage par stade repose souvent sur une poignée de patients. Toujours exiger le
dénominateur.

**Cas réel AIMA** : 100 % au stade II sur **4 patients**, 100 % au stade III sur **3**.
Statistiquement vide — et si on cite ces chiffres, on s'expose exactement à la critique qu'on
adresse aux concurrents.

Seuil de prudence : en dessous de ~30 cas, ne pas citer en comparaison externe.

## 5. Attribution méthodologique croisée

Quand plusieurs papiers d'une même équipe sont lus ensemble, leurs paramètres se mélangent.

**Cas réel** : les paramètres fins de correction GC et de Z-scores attribués au produit
commercial venaient en réalité du papier fondateur de 5 ans antérieur, le papier de validation
se contentant d'un « as previously described ».

Toujours nommer la source de chaque paramètre, et signaler l'héritage quand il y en a un.

## 6. Métriques renvoyant à des données non publiées

Repérer les appels de note. « Unpublished data on file » signifie invérifiable — et souvent en
écart avec les valeurs publiées.

## 7. Ne pas confondre statut réglementaire et approbation

**Breakthrough Device Designation ≠ approbation FDA.** C'est un statut d'examen accéléré. De
même, LDT sous CLIA n'est pas une autorisation de mise sur le marché.

## 8. Accusations non vérifiées sur nos propres outils

**Cas réel** : affirmation que notre requête de veille ratait les publications du concurrent
« parce que l'équipe publie sous affiliation académique ». Faux — le papier de validation est
bien indexé sous le nom de la société. La vraie cause était l'antériorité des publications.

Rejouer la requête avant d'affirmer qu'elle est défaillante.

## 9. Courbes non monotones = bruit probable

Une performance qui ne varie pas régulièrement avec un paramètre continu (profondeur, dose)
signale du bruit d'échantillonnage plutôt qu'un effet réel.

**Cas réel AIMA** : 87,7 % à 0,25x, 80,2 % à 0,5x, 90,5 % à 1x, 84,8 % à 2x. Ne pas bâtir
d'argument « robuste à basse couverture » là-dessus sans investigation.
