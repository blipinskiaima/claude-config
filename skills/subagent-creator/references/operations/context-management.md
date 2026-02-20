# Context Management

## How Subagent Context Works

Each subagent runs in its own isolated context window:
- Receives ONLY its system prompt + environment details
- Does NOT receive the full Claude Code system prompt
- Does NOT inherit parent conversation history
- Results return to parent's context when complete

## Minimize Context Impact

Every subagent result consumes main context. Strategies:

- Ask subagents to return summaries, not raw data
- Isolate verbose operations (tests, logs, docs scanning)
- Use background agents for concurrent work
- For sustained parallelism, use agent teams instead

## Auto-Compaction

Subagents support automatic compaction:
- Triggers at ~95% capacity by default
- Configure via `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`
- Compaction events logged in transcripts

## Persistent Memory

```yaml
memory: user      # Remembers across all projects
memory: project   # Project-specific, git-tracked
memory: local     # Project-specific, gitignored
```

Memory directory:
```
~/.claude/agent-memory/<agent-name>/
├── MEMORY.md          # Index (first 200 lines loaded)
├── patterns.md        # Discovered patterns
└── decisions.md       # Key decisions
```

Tips:
- Include memory instructions in system prompt
- Ask agent to consult memory before work
- Ask agent to update memory after completing
- Use `user` scope as default

## Resuming Subagents

Resume to continue where agent left off:
- Full history preserved (tool calls, results, reasoning)
- Ask Claude to "continue that review"
- Transcripts at: `~/.claude/projects/{project}/{session}/subagents/`

## Skills Injection

```yaml
skills:
  - api-conventions
  - error-handling-patterns
```

- Full skill content injected at startup
- Subagents don't inherit parent's skills — list explicitly
