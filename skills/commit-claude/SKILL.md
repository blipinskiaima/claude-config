---
name: commit-claude
description: Commit et push la configuration Claude (~/.claude) vers le repo git claude-config. Use when the user wants to sync, backup, or push their Claude config, or when they say "commit-claude", "sync claude", "push config", "backup claude", or any variation of saving their Claude Code configuration.
---

<objective>
Commit et push les modifications de ~/.claude vers le repo git (github.com/blipinskiaima/claude-config.git). Rapide et direct — pas de mise à jour de docs, juste git add/commit/push.
</objective>

<workflow>

## Step 1: Check Changes

**Actions:**
1. `cd ~/.claude && git status` — voir ce qui a changé
2. `cd ~/.claude && git diff --stat` — résumé des modifications

Si rien n'a changé, informer l'utilisateur et s'arrêter.

Sinon, présenter un résumé court des fichiers modifiés/ajoutés/supprimés.

## Step 2: Commit & Push

**Actions:**
1. `cd ~/.claude && git add -A` — stager tous les changements (le .gitignore filtre déjà les fichiers sensibles/éphémères)
2. Générer un message de commit concis décrivant les changements (ex: "update skills", "add new agent", "update project memory")
3. `cd ~/.claude && git commit -m "message"`
4. `cd ~/.claude && git push`
5. Confirmer le succès

**Ne PAS demander confirmation sauf si les changements semblent inhabituels (suppression massive, fichiers sensibles).**

</workflow>

<quick_reference>

## Repo Info
- **Local:** `~/.claude/`
- **Remote:** `github.com/blipinskiaima/claude-config.git`
- **Branch:** `main`

## What's Tracked
- `CLAUDE.md`, `settings.json`
- `skills/`, `agents/`
- `projects/*/memory/` (MEMORY.md et topic files uniquement)

## What's Ignored (.gitignore)
- `.credentials.json`
- `history.jsonl`, `cache/`, `debug/`, `session-env/`, `file-history/`
- `*.jsonl` dans projects (session logs)
- `settings.local.json`

</quick_reference>
