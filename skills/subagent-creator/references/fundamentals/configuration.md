# Subagent Configuration

## File Format

Subagents are markdown files with YAML frontmatter + system prompt body.

```markdown
---
name: my-agent
description: Expert at doing X. Use proactively when Y happens.
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: default
maxTurns: 15
memory: user
skills:
  - relevant-skill
---

System prompt in markdown here.
```

## Scope and Priority

| Location | Scope | Priority | Use Case |
|---|---|---|---|
| `--agents` CLI flag | Current session only | 1 (highest) | Quick testing, automation |
| `.claude/agents/` | Current project | 2 | Project-specific agents |
| `~/.claude/agents/` | All your projects | 3 | Personal reusable agents |
| Plugin `agents/` | Where plugin enabled | 4 (lowest) | Distributed via plugins |

When multiple subagents share the same name, higher-priority location wins.

## Frontmatter Fields

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Unique ID, lowercase + hyphens |
| `description` | Yes | When Claude should delegate to this agent |
| `tools` | No | Allowed tools. Inherits all if omitted |
| `disallowedTools` | No | Tools to deny (removed from inherited list) |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` (default) |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `delegate`, `bypassPermissions`, `plan` |
| `maxTurns` | No | Max agentic turns before stopping |
| `skills` | No | Skills to inject into agent context |
| `mcpServers` | No | MCP servers available to this agent |
| `hooks` | No | Lifecycle hooks scoped to this agent |
| `memory` | No | Persistent memory: `user`, `project`, or `local` |

## Model Selection

| Model | Best For | Cost | Speed |
|---|---|---|---|
| `haiku` | Simple tasks, search, classification | Low | Fast |
| `sonnet` | Balanced analysis, code review | Medium | Medium |
| `opus` | Complex reasoning, architecture | High | Slow |
| `inherit` | Same as main conversation (default) | Varies | Varies |

## Permission Modes

| Mode | Behavior |
|---|---|
| `default` | Standard permission checking |
| `acceptEdits` | Auto-accept file edits |
| `dontAsk` | Auto-deny permission prompts |
| `delegate` | Coordination-only (agent teams) |
| `bypassPermissions` | Skip all checks (use with caution) |
| `plan` | Read-only exploration |

## Persistent Memory

Enable cross-session learning:

```yaml
memory: user      # ~/.claude/agent-memory/<name>/
memory: project   # .claude/agent-memory/<name>/ (git-tracked)
memory: local     # .claude/agent-memory-local/<name>/ (gitignored)
```

When enabled:
- Agent can read/write to its memory directory
- First 200 lines of MEMORY.md loaded at startup
- Read, Write, Edit tools auto-enabled

## CLI-Defined Agents (Session-Only)

```bash
claude --agents '{
  "reviewer": {
    "description": "Code reviewer",
    "prompt": "You are a senior code reviewer...",
    "tools": ["Read", "Grep", "Glob"],
    "model": "sonnet"
  }
}'
```

## Loading

- Agents loaded at session start
- Add file manually → restart session or use `/agents` to reload
- Use `/agents` command to create, edit, delete, and view agents
