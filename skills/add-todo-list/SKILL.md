---
name: add-todo-list
description: "Ajoute une tâche à la todo list personnelle de Boris (Partie 1 — À faire). Use when the user says \"ajoute à la todo\", \"add todo\", \"nouvelle tâche\", \"add-todo-list\", or asks to add something to his to-do list."
argument-hint: "<description tâche> [--prio haute|moyenne|basse] [--section <nom>]"
allowed-tools: Read, Edit
---

# Skill : Add Todo

Ajoute une tâche synthétique à la todo list personnelle.

## Fichier cible

`~/.claude/projects/-home-blipinski/memory/todo-optimisation.md`

Structure fixe : **Partie 1 — À faire** (par priorité : Haute / Moyenne / Basse), **Partie 2 — Complété** (par jour).

## Format strict d'un bullet

```
- [ ] **Titre court (4-8 mots)** — 1 phrase de contexte : pourquoi ou effort/gain. Dépendance ou prérequis si pertinent.
```

Règles :
- **Max 2 phrases** après le tiret cadratin `—`.
- Jamais de liste imbriquée sauf si la tâche a de vrais sous-items actionnables.
- Pas de verbosité : supprimer adverbes, conditionnels, préambules.
- Mots-clés en gras : nom du projet, chiffres clés, dépendances humaines.
- Ordre de priorité interne : P0 > P1 > P2.

## Instructions

1. **Lire** le fichier todo pour voir la structure actuelle et éviter les doublons.
2. **Déterminer la priorité** :
   - Si l'utilisateur la donne (`--prio` ou dans le texte : "urgent", "quick win", "long terme"), respecter.
   - Sinon demander : `haute` / `moyenne` / `basse`.
3. **Déterminer la section** (pour moyenne priorité, choisir entre "Skills bioinformatiques" / "Projets bioinformatiques" ou créer une sous-section si aucune ne correspond). Pour haute/basse, pas de sous-section.
4. **Reformuler en format strict** (titre court + 1 phrase). Proposer à l'utilisateur la version synthétique avant d'insérer s'il a fourni un texte long.
5. **Insérer** le bullet au bon endroit via `Edit` :
   - Haute prio : à la fin de `## Haute priorité`
   - Moyenne : à la fin de la sous-section correspondante
   - Basse : à la fin de `## Basse priorité`
6. **Confirmer** brièvement à l'utilisateur : la ligne ajoutée + son emplacement.

## Exemples

### Entrée verbeuse → bullet synthétique

Utilisateur : "ajoute à la todo qu'il faudrait que je regarde comment intégrer pyranges dans trace-prod pour faire des opérations sur les bed files plus vite, c'est pas urgent"

Bullet inséré (basse prio) :
```
- [ ] **Intégrer pyranges dans trace-prod** — opérations bed plus rapides. Pas urgent.
```

### Entrée déjà courte

Utilisateur : "add-todo: bench Fastq2Bam vs Methylseq, prio haute"

Bullet inséré :
```
- [ ] **Bench Fastq2Bam vs Methylseq** — comparer performance/précision alignement. Prérequis décision stack short-read.
```

## Anti-patterns

- ❌ Bullet avec plus de 2 phrases ou plusieurs paragraphes
- ❌ Explication historique détaillée (appartient à la mémoire, pas à la todo)
- ❌ Conditionnel flou ("il faudrait peut-être voir si...") → reformuler en action
- ❌ Doublon : toujours grep le titre avant insertion
