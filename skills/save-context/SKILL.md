---
name: save-context
description: Sauvegarde un snapshot du contexte de tâche en cours (où j'en suis, ce qui marche/foire, prochaine étape) dans ~/.claude/projects/-home-blipinski/memory/context/{projet}.md. Complémentaire à MEMORY.md (long terme) — sert à reprendre une session interrompue. Use when the user says "/save-context", "sauve le contexte", "save context", "snapshot tâche", "où j'en suis". Appelé automatiquement par /end-session.
allowed-tools: Bash, Write, AskUserQuestion
---

<objective>
Écrire un snapshot court de l'état mental de la tâche en cours dans `~/.claude/projects/-home-blipinski/memory/context/{projet}.md`. Relu par `/get-context` ou `agent-explore-quick` au début de la prochaine session pour reprendre exactement où on en était.
</objective>

<workflow>

## Step 1 : Détecter le projet

`basename "$(pwd)"`. Si cwd = `~` ou dossier non-projet, demander à Boris quel nom utiliser (ou annuler).

## Step 2 : Récupérer le git context

```bash
git branch --show-current
git log -1 --oneline
git status --short
```

Si pas de repo git → "n/a" pour ces champs.

## Step 3 : Synthétiser depuis la conversation

Extraire de la session courante :
- **Où j'en suis** : 1-3 phrases (tâche actuelle + point d'arrêt)
- **Ce qui marche / ce qui foire** : 2-5 bullets ✓/✗
- **Prochaine étape** : 1 action concrète

## Step 4 : Valider avec Boris

Afficher le snapshot proposé entier. **Ne PAS écrire avant confirmation explicite.**

## Step 5 : Écrire

```bash
mkdir -p ~/.claude/projects/-home-blipinski/memory/context/
```

Écrire dans `~/.claude/projects/-home-blipinski/memory/context/{projet}.md` (écrase l'éventuel snapshot précédent — pas d'historique).

## Step 6 : Confirmer

Une phrase courte : « Snapshot écrit dans `{path}`. »

</workflow>

<format>

```markdown
# Context — {projet} — {ISO timestamp local}

**Branche** : {git branch}
**Dernier commit** : {sha court} — {message}
**Status** : {clean / N fichiers modifiés}

## Où j'en suis
{texte}

## Ce qui marche / ce qui foire
- ✓ ...
- ✗ ...

## Prochaine étape
{texte}
```

</format>
