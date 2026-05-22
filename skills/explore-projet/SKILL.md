---
name: explore-projet
description: Raccourci pour relancer manuellement l'exploration standard (light, Haiku) sur le projet courant — équivaut au routing automatique du Session Start. Utile pour rafraîchir le contexte en cours de session sans rouvrir Claude. Use when the user says "/explore-projet", "explore le projet", "relance l'exploration", "refresh contexte", "recharge le projet", "explore-projet", or wants to manually trigger a lightweight project context reload during an active session.
allowed-tools: Agent, Bash(pwd:*), Bash(basename:*)
---

<objective>
Lancer immédiatement le subagent `agent-explore-quick` (Haiku, ~30s, ~5-10k tokens) en background sur le projet correspondant au cwd courant. Permet de **rafraîchir le contexte standard** à tout moment de la session, sans rouvrir Claude. Aligné sur le comportement par défaut du routing Session Start (CLAUDE.md).

**Note** : pour forcer une exploration profonde (Sonnet, deep), il faut soit invoquer un workflow qui le justifie (`/code-workflow-feature`, `/clean-skill`), soit utiliser les mots-clés feature/refactor en langage naturel.
</objective>

<workflow>

## Step 1: Identifier le projet courant

**Actions:**
1. `pwd` — récupérer le répertoire courant
2. `basename "$(pwd)"` — nom court du projet pour la description de l'agent

Si le cwd n'est pas dans un projet (ex: `~` directement) ou est un dossier non-code, demander confirmation à Boris avant de lancer.

## Step 2: Lancer agent-explore-quick en background

**Actions:**
1. Invoquer le tool `Agent` avec :
   - `subagent_type: "agent-explore-quick"`
   - `run_in_background: true`
   - `description: "Quick refresh {project name}"` (≤ 5 mots)
   - `prompt:` — instruction d'exploration light selon le workflow standard de l'agent (voir bloc ci-dessous)

**Prompt à passer à l'agent :**
```
Effectue un rafraîchissement rapide du contexte projet à {cwd}.

Suis ton workflow standard light en 3 étapes :
1. Lis la documentation existante (CLAUDE.md, MEMORY.md, .claude/rules/*.md, topic files de la mémoire)
2. Light git scan (git log --oneline -10, git status --short, git branch --show-current)
3. Quick structure check uniquement si la doc est incomplète

Retourne ton résumé concis (sous 100 lignes) avec le signal d'escalation à la fin :
- "→ Context sufficient for this task" si la doc charge suffit
- "→ Recommend agent-explore deep for this task" si du code-level deep est nécessaire
```

## Step 3: Confirmer à Boris

**Actions:**
1. Une phrase courte : « Rafraîchissement du contexte lancé en background sur **{nom projet}** (Haiku, ~30s, ~$0.02). »
2. Ne **pas** attendre la fin de l'agent — rendre la main immédiatement à Boris

## Step 4: Intégration différée

**Actions:**
1. Quand l'agent termine (notification système), intégrer son résumé dans le contexte de la conversation
2. Si l'agent retourne `→ Recommend agent-explore deep for this task`, en informer Boris brièvement (sans lancer le deep automatiquement — c'est sa décision)

</workflow>

<quick_reference>

## Quand utiliser ce skill

| Cas | Pourquoi |
|---|---|
| Reprise d'un projet après quelques heures de pause | Recharger CLAUDE.md, MEMORY.md, git status récents |
| Tu as switché de projet et veux le contexte à jour | Skip le redémarrage de session |
| Tu as fait des commits/modifs et veux que Claude « voie » l'état actuel | Refresh git log et status |
| Tu sors d'une compaction et veux le contexte propre | Rebase rapide sur la doc |

## Quand NE PAS utiliser

- Au tout début d'une session → le routing Session Start auto le fait déjà
- Pour une exploration **profonde** (deep architecture, traces d'exécution) → utiliser plutôt `/code-workflow-feature` ou taper "implémente / refactor X" pour déclencher le deep via routing

## Différence avec le routing automatique

| Mécanisme | Quand | Agent lancé |
|---|---|---|
| **Session Start auto** (CLAUDE.md) | 1er message Boris, intent question/brainstorm | `agent-explore-quick` |
| **Session Start auto** (CLAUDE.md) | 1er message Boris, intent feature/refactor | `agent-explore-quick` + `agent-explore` deep |
| **`/explore-projet`** (ce skill) | À tout moment en cours de session | `agent-explore-quick` seul |
| **`/code-workflow-feature`** | Pour implémenter une feature | déclenche le deep via routing |

## Coût indicatif

- Une invocation `/explore-projet` = **~$0.02** (Haiku, ~5-10k tokens, ~30s)
- À comparer aux ~$0.30-0.80 d'un `agent-explore` deep
- Pas de hausse de coût si tu invoques le skill plusieurs fois dans la même session — c'est précisément son rôle

</quick_reference>
