---
name: explore-projet
description: Raccourci pour lancer agent-explore deep en background sur le projet courant. Équivaut à demander verbalement "explore en profondeur le projet en background" — force le mode deep sans passer par le routing automatique du Session Start. Use when the user says "/explore-projet", "explore le projet", "explore en profondeur", "exploration profonde", "deep explore", "explore deep", "explore-projet", or wants to manually trigger a full codebase deep dive on the current project.
allowed-tools: Agent, Bash(pwd:*), Bash(basename:*)
---

<objective>
Lancer immédiatement le subagent `agent-explore` (Sonnet, deep) en background sur le projet correspondant au cwd courant. Court-circuite le routing automatique Session Start qui aurait sinon lancé `agent-explore-quick` (Haiku). Utilisé quand Boris a explicitement besoin de la profondeur deep, indépendamment de l'intent inféré.
</objective>

<workflow>

## Step 1: Identifier le projet courant

**Actions:**
1. `pwd` — récupérer le répertoire courant
2. `basename "$(pwd)"` — nom court du projet pour la description de l'agent

Si le cwd n'est pas dans un projet (ex: `~` directement) ou est un dossier non-code, demander confirmation à Boris avant de lancer.

## Step 2: Lancer agent-explore en background

**Actions:**
1. Invoquer le tool `Agent` avec :
   - `subagent_type: "agent-explore"`
   - `run_in_background: true`
   - `description: "Deep explore {project name}"` (≤ 5 mots)
   - `prompt:` — instruction d'exploration deep selon le workflow standard de l'agent (voir bloc ci-dessous)

**Prompt à passer à l'agent :**
```
Effectue une exploration profonde du projet à {cwd}.

Suis ton workflow standard en 6 phases :
1. Load existing context (CLAUDE.md, MEMORY.md, rules, git log)
2. Map project structure
3. Detect project type (bioinfo AIMA si applicable) & find entry points
4. Analyze architecture
5. Identify patterns & conventions
6. (Si bioinfo) Pipeline context AIMA — position dans le flow, Docker containers, S3 paths, Nextflow processes, dépendances inter-projets

Retourne le résumé structuré complet selon ton template (Project Overview, Architecture, Entry Points, Key Files, Patterns, Data Flow, Commands, Gotchas, Pipeline Context si bioinfo).
```

## Step 3: Confirmer à Boris

**Actions:**
1. Une phrase courte : « Exploration profonde lancée en background sur **{nom projet}** (Sonnet, ~5-15 min, ~50-100k tokens). Tu peux continuer à travailler — j'intégrerai le résumé quand l'agent termine. »
2. Ne **pas** attendre la fin de l'agent — rendre la main immédiatement à Boris

## Step 4: Intégration différée

**Actions:**
1. Quand l'agent termine (notification système), intégrer son résumé dans le contexte de la conversation
2. Si Boris est en train de travailler sur autre chose, ne pas l'interrompre — mentionner brièvement que l'exploration est terminée et le résumé disponible

</workflow>

<quick_reference>

## Quand utiliser ce skill

| Cas | Pourquoi |
|---|---|
| Nouveau projet récemment cloné ou récupéré | Pas de contexte mémorisé, le quick serait insuffisant |
| Reprise d'un projet après une longue absence | Vérifier que la mémoire reste alignée avec le code actuel |
| Override volontaire du routing Session Start | Le quick a démarré par défaut mais Boris veut le deep |
| Préparation d'un gros refactor ou ajout structurel | Avoir le contexte complet avant d'attaquer |
| Quand `agent-explore-quick` a signalé "→ Recommend agent-explore deep" | Suivre la recommandation explicite |

## Quand NE PAS utiliser

- Question simple ou status check → laisser le routing auto faire `agent-explore-quick`
- Debug ponctuel → lecture ciblée des logs/code, pas d'exploration
- Si un `agent-explore` deep est déjà en cours dans la session courante → inutile de relancer

## Différence avec le routing automatique

| Mécanisme | Déclencheur | Agent lancé |
|---|---|---|
| **Session Start auto** (CLAUDE.md) | 1er message Boris avec intent feature/refactor | `agent-explore-quick` + `agent-explore` deep |
| **Session Start auto** (CLAUDE.md) | 1er message Boris avec intent question/brainstorm | `agent-explore-quick` seul |
| **`/explore-projet`** (ce skill) | Invocation explicite, à tout moment | `agent-explore` deep **directement** |

## Coût indicatif

- Une invocation `/explore-projet` = **~$0.30-0.80** (Sonnet, ~50-100k tokens)
- À comparer aux ~$0.02 d'un `agent-explore-quick`
- À utiliser quand le bénéfice (compréhension architecture complète) justifie le coût

</quick_reference>
