---
name: end-session
description: Workflow complet de cloture de session — execute successivement les 3 skills /save-code, /commit-claude et /maj-todo-list, dans l'ordre, jusqu'au bout. Use when the user types /end-session.
disable-model-invocation: true
---

# Skill : End Session

Orchestre la cloture complete d'une session de travail en enchainant les 3 skills de sauvegarde dans un ordre strict.

## Objectif

Reproduire exactement l'effet de taper successivement `/save-code`, puis `/commit-claude`, puis `/maj-todo-list` dans le prompt — sans intervention de Boris pour declencher chaque skill individuellement.

## Sequence d'execution (stricte)

### Step 1 : `/save-code`

Invoquer le skill via le tool `Skill` :

```
Skill({ skill: "save-code" })
```

Ce skill prend en charge :
- Analyse des changements du repo projet (`git diff`, `git status`)
- Mise a jour README.md (si impacte)
- Mise a jour CLAUDE.md + MEMORY.md (si impacte)
- Commit + push avec message descriptif

**Boris confirme chaque etape** (analyse, README, CLAUDE.md/memory, commit message).

**Ne pas passer a Step 2 tant que Step 1 n'est pas termine** (commit pushe, working tree clean).

### Step 2 : `/commit-claude`

Invoquer le skill via le tool `Skill` :

```
Skill({ skill: "commit-claude" })
```

Ce skill prend en charge :
- Verification des changements dans `~/.claude/`
- Commit + push vers `github.com/blipinskiaima/claude-config.git`

Skill rapide et direct — pas de confirmation requise sauf si changements inhabituels.

**Ne pas passer a Step 3 tant que Step 2 n'est pas termine.**

### Step 3 : `/maj-todo-list`

Invoquer le skill via le tool `Skill` (sans argument) :

```
Skill({ skill: "maj-todo-list" })
```

Ce skill prend en charge :
- Detection des taches realisees dans la session
- Matching contre la Partie 1 du fichier `~/.claude/projects/-home-blipinski/memory/todo-optimisation.md`
- Proposition de candidats a marquer done OU nouvelle entree done si la tache n'etait pas dans la todo
- Insertion en Partie 3 sous la date du jour, apres confirmation Boris

## Regles importantes

- **Sequence stricte** : Step 1 → Step 2 → Step 3, dans cet ordre, jamais en parallele
- **Aller jusqu'au bout de chaque skill** : ne pas tronquer, ne pas sauter d'etapes internes
- **Respecter les confirmations utilisateur** : chaque skill enfant peut demander des validations a Boris, attendre sa reponse avant de continuer
- **Stop en cas d'echec** : si un skill echoue (push rejete, hook qui bloque, etc.), s'arreter immediatement et ne pas executer les suivants. Reporter l'erreur a Boris.
- **Aucune action en arriere-plan** : tous les commits/push sont synchrones et visibles

## Anti-patterns

- ❌ Ne pas paralleliser les 3 skills — l'ordre est important (les commits doivent etre propres avant la mise a jour de la todo)
- ❌ Ne pas inventer des etapes intermediaires non prevues par les skills enfants
- ❌ Ne pas modifier le comportement des skills enfants — `/end-session` est un orchestrateur, pas un skill autonome
