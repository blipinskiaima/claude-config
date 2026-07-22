---
name: cross-project-claude-cli-auth-pattern
description: Pattern réutilisé entre Aima-Tower et Aima-Survey pour appeler Claude via l'abonnement Pro/Max plutôt que l'API pay-as-you-go
metadata:
  type: project
---

Boris réutilise le même pattern `lib/claude_cli.py` (subprocess `claude -p` headless) dans plusieurs projets internes (Aima-Tower en premier, repris tel quel dans Aima-Survey) pour router les appels IA sur l'abonnement Claude Pro/Max via `CLAUDE_CODE_OAUTH_TOKEN` au lieu de facturer en pay-as-you-go sur `ANTHROPIC_API_KEY`.

Éléments stables du pattern (à réutiliser si un nouveau projet a besoin d'appels Claude légers/batch) :
- `HOME` isolé (répertoire dédié type `~/.aima-<projet>-claude-home`) pour ne pas polluer `~/.claude` interactif de Boris.
- Flags CLI : `--model`, `--system-prompt`, `--output-format text`, `--disable-slash-commands`, `--tools ""`, `--no-session-persistence`, `--permission-mode bypassPermissions`, `--setting-sources ""`.
- Piège connu (documenté dans chaque projet) : si `ANTHROPIC_API_KEY` est défini en plus de `CLAUDE_CODE_OAUTH_TOKEN`, le CLI priorise la clé API et bypass l'abonnement → facturation inattendue. Toujours vérifier qu'un seul des deux est présent dans l'env.

**Why** : éviter de payer des crédits API alors que Boris a déjà un abonnement Pro/Max qui couvre ces usages internes (scoring, classification, synthèse).
**How to apply** : si un futur projet `~/Pipeline/*` a besoin d'un scoring/classification IA léger et récurrent, proposer de reprendre `lib/claude_cli.py` (Aima-Survey) ou `src/claude_cli.py` (Aima-Tower) plutôt que du SDK `anthropic` + clé API.
