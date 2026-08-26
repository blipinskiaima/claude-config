# Phase 4 — Fact-check adversarial ⛔ BLOQUANT

## Pourquoi cette phase existe

Lors de l'analyse DELFI de juillet 2026, le rapport a été rédigé **avant** la vérification. Le
fact-check a ensuite trouvé deux erreurs majeures, dont une qui invalidait l'argument central,
et tout a dû être réécrit.

**Ne jamais rédiger avant d'avoir les verdicts.**

## Protocole

Lancer un agent `general-purpose` **indépendant** — il ne doit pas avoir participé à la collecte.
Son rôle est de **challenger**, pas de valider.

Lui fournir :
- la liste numérotée de **toutes** les affirmations chiffrées à vérifier
- les chemins des textes intégraux déjà téléchargés
- les outils MCP PubMed (via `ToolSearch`)
- les pièges connus, listés explicitement dans le prompt

Lui demander un verdict par affirmation :

| Verdict | Sens |
|---|---|
| **CONFIRMÉ** | citation exacte de la source à l'appui |
| **INEXACT** | donner la valeur correcte |
| **TROMPEUR** | techniquement vrai, mal contextualisé |
| **NON VÉRIFIABLE** | dire pourquoi |

Formule qui marche : « Sois impitoyable sur les nuances. Une sensibilité pondérée par le stade
n'est pas une sensibilité brute ; un chiffre de validation croisée n'est pas un chiffre de
validation clinique. Signale toute confusion entre les deux. »

## Ce qu'il faut lui faire vérifier en priorité

1. **Toutes les métriques de performance** — avec leur cohorte, leur effectif, leur spécificité
2. **L'attribution des détails méthodologiques** : quel papier pour quel paramètre ?
3. **Les chiffres de la plaquette** vs ceux des publications
4. **Nos propres affirmations** sur nos outils — nos requêtes, notre base, nos manques supposés
5. Les effectifs derrière chaque pourcentage

## Vérifier soi-même ce que l'agent ne peut pas atteindre

L'agent n'a pas accès à la plaquette locale (ni web, ni PubMed). Vérifier soi-même en parallèle :
- présence/absence des termes techniques
- origine des appels de note des métriques
- nature des références citées

## Traiter les verdicts

- **INEXACT** → corriger la valeur, et vérifier si l'argument construit dessus tient encore
- **TROMPEUR** → reformuler avec le contexte manquant, ne pas supprimer
- **NON VÉRIFIABLE** → conserver avec le marqueur `[NON VÉRIFIÉ]`, ne jamais deviner
- Une erreur trouvée dans un raisonnement invalide **tout ce qui en découle** — relire la chaîne

## Rapporter honnêtement à Boris

Lui donner les corrections **avant** la réécriture, en nommant les erreurs sans les noyer.
S'il s'agit d'erreurs de l'analyse précédente, le dire simplement et passer à la suite.

## Sortie de phase

Une liste de verdicts et de corrections appliquées, **consolidées dans le corpus** structuré sur
les axes du profil AIMA, chaque chiffre portant son marqueur de preuve et son verdict de
fact-check. C'est ce matériau figé, et non des notes éparses, qui entre en Partie 3.
**Alors seulement**, comparer et rédiger.
