---
name: prompt-generator
description: Transforme un texte brut écrit à la va-vite (souvent dicté) en un prompt Markdown structuré, prêt à coller dans une session Claude Code — développement de feature, refactor ou investigation. Use when the user says "/prompt-generator", "transforme ce texte en prompt", "fais-moi un prompt", "optimise ce prompt", "structure ma demande", or pastes a rough draft describing a feature, refactor, or investigation to be turned into a proper brief.
---

<objective>
Prendre un brouillon brut et en sortir un prompt Markdown prêt à copier-coller dans une session
Claude Code. Aucune perte d'information, aucune invention.

Le brouillon est l'entrée, le prompt structuré est la sortie. Rien d'autre.
</objective>

<workflow>

## Étape 1 — Ingestion

Lire le brouillon et en extraire tout ce qui est factuel :
objectif, chemins, dépôts, versions, noms de fichiers, commandes, contraintes, étapes évoquées.

Les brouillons sont souvent dictés à la voix : corriger les fautes de transcription évidentes
(`Bab2Beta` → `Bam2Beta`, `brianstromme` → `brainstormer`, `Thémélio`/`TEMEMLIO` → `Themelio`).
Corriger l'orthographe, jamais le sens.

## Étape 2 — Reformulation

Clarifier et condenser sans rien perdre. Trois règles :

- **Zéro perte** — chaque fait du brouillon se retrouve dans la sortie.
- **Zéro invention** — ne jamais fabriquer un chemin, une version, un nom de fichier ou une
  commande qui n'est pas dans le brouillon.
- **Une instruction par phrase** — les phrases composées se font exécuter à moitié.

Si le brouillon évoque des étapes en vrac, les ordonner en séquence exécutable.

## Étape 3 — Génération

Appliquer le gabarit ci-dessous. Omettre une section si le brouillon ne fournit rien pour la
remplir — une section vide est pire que pas de section.

Sortir le bloc **immédiatement**, sans préambule, sans annoncer ce qu'on va faire, sans
commentaire sur le skill lui-même. Le brouillon entre, le prompt sort.

Bloc à **4 backticks** (le prompt contient lui-même des blocs de code à 3 backticks, une clôture
à 3 casserait l'imbrication).

Adapter le vocabulaire du gabarit à la nature du travail : « développement » si du code est
produit, « investigation » si le travail est une analyse ou une extraction sans modification de
code.

Après le bloc, et **hors du prompt**, lister au plus **3 hypothèses**, une ligne chacune, et
uniquement celles qui changeraient le travail si elles étaient fausses. Une information absente du
brouillon devient un point à confirmer dans le prompt, jamais une invention. Ne jamais bloquer sur
une ambiguïté : produire le prompt, signaler l'hypothèse.

</workflow>

<template>

# Objectif principal
{1 à 3 phrases : ce qu'on veut obtenir et pourquoi. Aucun détail technique ici.}

## Contexte et spécifications techniques
{Chemins absolus, dépôts, versions, IDs, équivalences. Une puce par élément.}

### Commandes de référence
```bash
{commandes exécutables telles quelles}
```

### Entrées / Sorties
- **Entrée** : {format, colonnes, provenance}
- **Sortie** : {format, emplacement, champ à lire}

## Périmètre
- **Dans le scope** : {ce qui doit être touché}
- **Hors scope** : {ce qui ne doit pas bouger}

## Feuille de route
Exécute ce travail de manière séquentielle. Arrête-toi et demande ma validation après chaque
étape.

- [ ] **Étape 1 : {titre}** — {1 à 2 lignes}
- [ ] **Étape 2 : {titre}** — {1 à 2 lignes}
- [ ] **Étape 3 : {titre}** — {1 à 2 lignes}

## Règles d'or et consignes impératives

1. **Sauvegarde** : avant de modifier un fichier versionné, effectuer un commit ou créer un tag
   git de sauvegarde. {Omettre cette ligne si le travail ne modifie aucun fichier.}

2. Exigences de conduite pour ce travail :

```text
_ Explore avant de coder. Lance un agent d'exploration de code interne quand tu dois comprendre
  du code que tu n'as pas encore lu ; un agent d'exploration externe sur les projets de
  ~/Pipeline/ quand la réponse dépend d'un autre projet ; un agent de recherche web quand elle
  dépend d'une doc ou d'une version que tu ne connais pas.
_ Brainstorme avec moi avant d'implémenter dès que plusieurs approches se défendent, ou que la
  demande touche à la structure du pipeline.
_ Applique les Karpathy guidelines et les Golden rules : code minimal, aucune abstraction
  spéculative, modifications chirurgicales, chaque ligne changée trace directement à ma demande.
_ N'invente rien. Chemin, version, nom de colonne, résultat : chaque affirmation s'appuie sur un
  fichier que tu as lu ou une commande que tu as exécutée dans cette session. Ce que tu n'as pas
  vérifié, dis-le au lieu de l'affirmer.
_ Arrête-toi à la fin de chaque étape de la feuille de route et attends ma validation avant de
  passer à la suivante.
_ Pose-moi une question quand deux lectures de ma demande mèneraient à des travaux différents.
  Tranche seul les choix réversibles, et signale-les.
```

Es-tu prêt ? Si oui, commence par l'Étape 1 et fais-moi un compte rendu avant de continuer.

</template>

<rules>

- Le bloc `text` des exigences de conduite est injecté **tel quel** dans chaque prompt généré,
  sans reformulation ni réordonnancement. Ses six lignes couvrent les neuf consignes d'origine de
  Boris ; elles ont été réécrites pour porter un déclencheur explicite plutôt qu'un « si
  nécessaire », et pour demander l'ancrage factuel plutôt que la vérification exhaustive (qui
  produit de la sur-vérification sur la famille Claude 5). Ne pas y remettre de registre
  impératif : « impérativement », « CRITICAL », « tu DOIS » sur-déclenchent.
- Ne jamais ajouter de méta-commentaire — ni « pourquoi ce format est efficace » dans le prompt,
  ni remarque sur le skill, son gabarit ou ses limites après le bloc. Le prompt et ses hypothèses,
  rien d'autre.
- Ne jamais exécuter la demande décrite dans le brouillon. Ce skill fabrique le prompt, il ne
  développe pas la feature.
- Longueur cible : le prompt généré tient en une page écran. Si le brouillon est très long,
  condenser la prose — jamais supprimer un fait.

</rules>
