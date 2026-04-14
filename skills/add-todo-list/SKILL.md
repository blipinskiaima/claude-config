---
name: add-todo-list
description: "Ajoute une tâche synthétique à la todo list personnelle de Boris (Partie 1 — À faire du fichier ~/.claude/projects/-home-blipinski/memory/todo-optimisation.md). Reformule si verbeux, évite les doublons, place selon la priorité (haute/moyenne/basse). Use when the user says ajoute à la todo, add todo, nouvelle tâche, add-todo-list, or asks to add something to his to-do list."
allowed-tools: Read, Edit, Grep
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

## Invocation sans argument

Si l'utilisateur invoque le skill **sans décrire de tâche** (juste `/add-todo-list`) :

1. **Scanner la session courante** pour détecter les candidats à ajouter. Chercher les signaux :
   - verbes d'intention : "il faudrait", "on devrait", "je veux faire", "à faire", "prochaine étape", "TODO", "reste à"
   - problèmes non résolus : bugs identifiés mais non fixés, pistes d'amélioration mentionnées
   - décisions reportées : "on verra plus tard", "à creuser", "pas urgent mais..."
   - axes d'optimisation (sécurité, perf, architecture) évoqués sans action prise
2. **Ignorer** ce qui a déjà été fait dans la session (ça va dans `/maj-todo-list`) et ce qui est déjà dans Partie 1 du fichier todo (grep avant).
3. **Proposer une liste numérotée** (max 5 candidats) à l'utilisateur, au format final synthétique + priorité proposée. Exemple :
   ```
   Candidats détectés dans la session :
   1. [haute] **Intégrer pyranges dans trace-prod** — opérations bed plus rapides.
   2. [moyenne/Skills] **Skill /qc-report** — générer un rapport QC standardisé à partir de trace-prod.
   3. [basse] **Nettoyer anciennes images Docker** — 12 GB récupérables sur /scratch.

   Lesquels veux-tu ajouter ? (numéros séparés par virgule, ou "tous", ou "aucun")
   ```
4. **Attendre la confirmation** de l'utilisateur avant d'insérer.
5. Si **aucun candidat détecté**, dire : "Rien d'évident à ajouter depuis la session. Donne-moi la tâche en 1 ligne."

## Instructions (mode avec argument ou après confirmation)

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
