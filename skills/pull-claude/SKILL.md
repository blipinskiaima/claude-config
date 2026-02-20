---
name: pull-claude
description: Pull la configuration Claude (~/.claude) depuis le repo git claude-config. Use when the user wants to sync, pull, or update their Claude config from the remote repo, or when they say "pull-claude", "sync claude", "pull config", "update claude", or any variation of pulling their Claude Code configuration.
---

<objective>
Pull les dernières modifications de ~/.claude depuis le repo git (github.com/blipinskiaima/claude-config.git). Rapide et direct.
</objective>

<workflow>

## Step 1: Pull

**Actions:**
1. `cd ~/.claude && git pull --ff-only`
2. Si conflit, informer l'utilisateur et proposer `git pull --rebase`
3. Afficher le résumé des fichiers mis à jour

</workflow>

<quick_reference>

## Repo Info
- **Local:** `~/.claude/`
- **Remote:** `github.com/blipinskiaima/claude-config.git`
- **Branch:** `main`

</quick_reference>
