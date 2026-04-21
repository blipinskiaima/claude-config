---
name: Claude Pro auth pattern (subprocess CLI)
description: Pattern pour router un script Python headless (cron) sur l'abonnement Claude Pro/Max plutôt que sur crédit API facturé — aucun pont officiel SDK, solution = subprocess sur le CLI `claude -p`
type: reference
originSessionId: 2436002f-1dc1-46c9-9d7b-0cb1a41488d6
---
## TL;DR

Le SDK Python `anthropic` ne peut PAS utiliser un abonnement Claude Pro/Max — il nécessite une clé API facturée. Le seul chemin pour exploiter l'abonnement depuis un script headless passe par un **subprocess sur le CLI `claude -p`** avec une variable d'env `CLAUDE_CODE_OAUTH_TOKEN` générée via `claude setup-token`.

## Fichiers canoniques

- **Référence originale** : `~/Pipeline/Aima-Tower/src/claude_cli.py` (~62 lignes)
- **Réplication** : `~/Pipeline/Aima-Survey/lib/claude_cli.py`

Les deux exposent une fonction simple :
```python
call_claude(user_content: str, system_prompt: str,
            *, model="claude-haiku-4-5", timeout=60) -> str
```

## Recette

1. **Token OAuth** : `claude setup-token` sur le poste local → colle dans `.env` :
   ```
   CLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat01-...
   ```
2. **HOME isolé** pour chaque projet (évite que le CLI pollue `~/.claude` interactif) :
   ```python
   env = os.environ.copy()
   env["HOME"] = str(Path.home() / ".aima-<project>-claude-home")
   ```
3. **Flags subprocess obligatoires** :
   ```python
   ["claude", "-p",
    "--model", model,
    "--system-prompt", system_prompt,
    "--output-format", "text",
    "--disable-slash-commands",
    "--tools", "",              # interdit tous les outils
    "--no-session-persistence",
    "--permission-mode", "bypassPermissions",
    "--setting-sources", "",
   ]
   ```
4. **Input** passé via stdin (`input=user_content`), **output** via `result.stdout.strip()`.

## PIÈGE CRITIQUE

Si `ANTHROPIC_API_KEY` ET `CLAUDE_CODE_OAUTH_TOKEN` sont tous deux définis, le CLI **priorise silencieusement la clé API** et bypasse l'abonnement → facturation inattendue. Toujours retirer `ANTHROPIC_API_KEY` du `.env` quand on veut l'abonnement.

## Tests

Les tests mockent directement `call_claude` via `monkeypatch.setattr(module, "call_claude", lambda *a, **k: response_text)`. Pas de MagicMock sur un client SDK.

## Pré-requis environnement

- CLI `claude` installé (`npm install -g @anthropic-ai/claude-code` ou binaire) — sur Boris : `/home/blipinski/.local/bin/claude` v2.1.116+
- Token OAuth valide (survit indéfiniment sauf révocation)
- Pas de SDK Python `anthropic` nécessaire — peut être retiré de `requirements.txt` si utilisé uniquement pour ce flux
