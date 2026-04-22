---
name: Backend IA Tower via CLI claude -p
description: Architecture de la migration des 5 appels API Anthropic vers le CLI `claude -p` + abonnement Claude Pro/Max (2026-04-22)
type: project
originSessionId: 03964086-3177-42f8-b0e9-9c017f24ad77
---
# Backend IA Tower — CLI `claude -p` (2026-04-22)

## Pourquoi

Les 5 appels IA de Tower (Survey synthesis + Analytics chat + DB Q&A) consommaient des crédits API Anthropic via le SDK `anthropic.Anthropic()`. Migration vers le CLI `claude -p` + `CLAUDE_CODE_OAUTH_TOKEN` pour facturer sur l'abonnement Claude Max.

## Architecture

```
Tower callback
  └─> claude_cli.call_claude(user_content, system_prompt)
        └─> subprocess.run(["claude", "-p", ...],
                          env={..., HOME=/app/data/claude-home},
                          input=user_content, timeout=120)
              └─> /usr/bin/claude (npm @anthropic-ai/claude-code dans Docker)
                    └─> auth via CLAUDE_CODE_OAUTH_TOKEN (abonnement Max)
```

## Fichiers clés

- `src/claude_cli.py` — `call_claude()` + `flatten_history()` + `PIPELINE_CONTEXT` (14 CLAUDE.md chargés au module import)
- `src/survey_service.py:generate_article_synthesis` — Survey (1 user message)
- `src/callbacks.py:run_ai_chat` — Analytics main chat + describe (flatten history)
- `src/callbacks.py:run_db_qa` — DB Q&A SQL gen + answer (flatten history)
- `Dockerfile` — install Node.js 20 + `@anthropic-ai/claude-code` global
- `docker-compose.yml` — `CLAUDE_CODE_OAUTH_TOKEN` env + volume `/pipeline:ro`

## Gotchas critiques

### 1. `ANTHROPIC_API_KEY` interdit dans le container
Le CLI priorise `ANTHROPIC_API_KEY` sur `CLAUDE_CODE_OAUTH_TOKEN` quand les deux sont présents → bypass silencieux de l'abonnement, facturation API inattendue. `ANTHROPIC_API_KEY` est explicitement retiré du `environment:` de docker-compose.

### 2. HOME isolé
`/home/blipinski/` dans le container est owned by root → UID 1005 ne peut pas y écrire son `history.jsonl`, `.claude.json`. Fix : `subprocess.run(env={HOME: "/app/data/claude-home"})`. Ce dossier est dans le volume `./data:/app/data` writable. Le `~/.claude` du host est **jamais** monté.

### 3. Flags `--system-prompt` vs `--append-system-prompt`
`--append` laisse active l'auto-discovery CLAUDE.md (y compris `~/.claude/CLAUDE.md` global). `--system-prompt` remplace complètement → aucun CLAUDE.md auto-injecté. On utilise `--system-prompt` + injection manuelle du `PIPELINE_CONTEXT`.

### 4. Tool-off obligatoire
`--tools ""` + `--disable-slash-commands` + `--setting-sources ""` — sinon le modèle pourrait déclencher des skills ou tenter Read/Bash/Grep sur `/pipeline`.

### 5. Subprocess stdin pour injection
Le `user_content` passé via `input=` (stdin) évite toute interprétation shell des caractères spéciaux (`$`, `"`, backslash).

## Contexte Pipeline injecté

Au module import, `_load_pipeline_context()` glob `/pipeline/*/CLAUDE.md` (14 fichiers, ~66KB = ~20K tokens). Concaténé dans `<pipeline_context>...</pipeline_context>` et append au system prompt métier. Permet à Claude de connaître l'écosystème AIMA sans auto-discovery.

Trade-off : +2-3s latence par appel, quota Max consommé plus vite. Acceptable.

## Setup (une fois)

```bash
# 1. Créer le token OAuth sur l'hôte (session Claude Code active)
claude setup-token

# 2. Copier le token dans .env
echo "CLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat01-..." >> .env

# 3. Rebuild le container (Dockerfile ajoute Node.js + CLI)
docker compose down && docker compose build && docker compose up -d
```

## Vérification

```bash
docker compose exec mini-tower python3 -c "
import sys; sys.path.insert(0,'/app/src')
from claude_cli import call_claude, PIPELINE_CONTEXT
print(f'PIPELINE_CONTEXT={len(PIPELINE_CONTEXT)} chars')
print(call_claude('dis bonjour en 2 mots', 'Réponds concis.'))
"
```
Attendu : ~60K chars de contexte + réponse Claude.

Logs : `docker compose logs mini-tower | grep api.anthropic` → doit être vide (aucun appel API).
