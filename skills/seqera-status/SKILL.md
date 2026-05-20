---
name: seqera-status
description: Vérifie l'état du MCP seqera (auth + connectivité), liste les workflows Tower récents via l'API Seqera Platform. Use when the user says "seqera-status", "tower status", "où en sont mes runs", "seqera status", "workflows seqera", or wants to check his Seqera Tower workflows from terminal.
allowed-tools: Bash(claude:*), Bash(tw:*), Bash(curl:*), Read
---

# Skill : Seqera Status

Vérifie l'état du MCP seqera et liste les workflows Tower récents.

## Phase 1 — Vérifier l'auth MCP seqera

```bash
claude mcp list 2>&1 | grep -i seqera
```

**Si `! Needs authentication`** → procédure 2026-04 (paste OAuth direct sur SSH) :

```bash
claude auth login
# Suivre l'URL affichée, copier le code OAuth, le coller dans le prompt
# (la procédure paste-code SSH résout le callback localhost qui échoue)
```

Puis re-vérifier :

```bash
claude mcp list 2>&1 | grep -i seqera
# doit afficher : ✓ Connected
```

## Phase 2 — Lister les workflows récents

**Si MCP seqera connecté** → utiliser les tools `mcp__seqera__*` directement (préférer cette voie).

**Fallback CLI** (si MCP indispo) :

```bash
# Workflows AIMA récents (workspace community/aima)
tw workflows list --workspace community/aima --limit 10

# Ou via curl direct (sans tw CLI)
curl -H "Authorization: Bearer $TOWER_ACCESS_TOKEN" \
     -H "Accept: application/json" \
     "https://api.cloud.seqera.io/workflow?workspaceId=$WORKSPACE_ID&max=10" \
     | jq '.workflows[] | {id, runName, status, dateCreated, projectName}'
```

## Phase 3 — Reporter

Format tableau markdown :

| Run ID | Name | Status | Duration | Tasks OK/Total |
|---|---|---|---|---|

**Mises en évidence (à signaler dans le rapport)** :
- ❌ **FAILED** (rouge) → proposer `/debug-nf` sur le run pour analyse
- ⚠️ **RUNNING > 24h** (warning) → possible hang, vérifier process
- ✅ **SUCCEEDED** récents (vert) → OK

## Cas d'usage AIMA

- Vérifier l'état des runs Bam2Beta lancés depuis ~/Run ou ~/Run2
- Tracker les workflows en parallèle (NANO basecalling + Bam2Beta)
- Détecter les hang avant que Boris ne le remarque manuellement

## Référence

- Doc API Seqera : https://docs.seqera.io/platform/24.2/api/
- Skill complémentaire : `/seqera` (CLI Seqera AI général)
- Source todo : `~/.claude/projects/-home-blipinski/memory/todo-optimisation.md`
  → « Seqera AI — finir la prise en main du CLI et de l'API » (priorité demain)
- MCP server : `https://mcp.seqera.io/mcp` (HTTP), auth OAuth
