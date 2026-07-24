# Convention des marqueurs de niveau de preuve

Chaque affirmation chiffrée d'un rapport porte un marqueur. C'est ce qui permet à Boris de
savoir, d'un coup d'œil, ce sur quoi il peut s'appuyer.

| Marqueur | Signification | Usage |
|---|---|---|
| `[MESURÉ]` | valeur observée dans une cohorte, citée verbatim de la publication | le seul niveau citable sans réserve |
| `[PONDÉRÉ]` | estimation modélisée, repondérée sur une population de référence | toujours préciser sur quoi la repondération porte |
| `[MARKETING]` | chiffre de communication industrielle sans publication à l'appui | signaler l'écart avec les valeurs publiées s'il y en a un |
| `[PRÉPRINT]` | non revu par les pairs | utilisable pour la tendance, pas pour une décision |
| `[INFÉRENCE]` | extrapolation de notre part | doit être explicitement présentée comme une hypothèse à tester |
| `[NON VÉRIFIÉ]` | recherché sans résultat concluant | **afficher plutôt que combler** |
| `[CODE]` | extrait du code ou de la config d'un projet AIMA | pour la fiche de positionnement |
| `[VALIDÉ]` | confirmé explicitement par Boris | |

## Règles d'emploi

1. **Un chiffre sans marqueur est un défaut de rédaction.** Si le niveau est incertain, c'est
   `[NON VÉRIFIÉ]`.
2. **Ne jamais promouvoir un marqueur** pour rendre un argument plus fort. Un `[PONDÉRÉ]` ne
   devient pas `[MESURÉ]` parce qu'il arrange.
3. **Afficher les `[NON VÉRIFIÉ]`.** Un rapport avec huit champs non vérifiés assumés est plus
   utile qu'un rapport qui les comble par déduction. Ils indiquent aussi où creuser.
4. **`[INFÉRENCE]` engage.** Toute hypothèse de notre part doit être formulée comme telle et
   accompagnée de la manière de la tester.

## Rappel compact à mettre en en-tête de rapport

> Marqueurs : `[MESURÉ]` observé/cité verbatim · `[PONDÉRÉ]` estimation repondérée ·
> `[MARKETING]` sans publication · `[PRÉPRINT]` non relu · `[INFÉRENCE]` extrapolation nôtre ·
> `[NON VÉRIFIÉ]` cherché sans résultat
