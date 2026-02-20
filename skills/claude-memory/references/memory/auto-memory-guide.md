# Auto Memory Guide

## What Is Auto Memory

Auto memory is a persistent directory where Claude records learnings, patterns, and insights. Unlike CLAUDE.md (instructions you write), auto memory contains notes Claude writes for itself.

## Where It Lives

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Index file — first 200 lines loaded every session
├── debugging.md       # Detailed debugging notes
├── patterns.md        # Discovered code patterns
├── api-conventions.md # API design decisions
└── ...                # Any topic files Claude creates
```

The `<project>` path derives from the git repository root. All subdirectories within the same repo share one memory directory.

## How It Works

- **MEMORY.md**: first 200 lines loaded into system prompt every session
- **Topic files**: NOT loaded at startup, read on-demand by Claude when needed
- **MEMORY.md is an index**: keep it concise, link to topic files for details

## What Claude Remembers

- Project patterns: build commands, test conventions, code style
- Debugging insights: solutions to tricky problems, common error causes
- Architecture notes: key files, module relationships, abstractions
- User preferences: communication style, workflow habits, tool choices

## Managing Auto Memory

### Ask Claude to Remember
```
"Remember that we use pnpm, not npm"
"Save to memory that the API tests require a local Redis instance"
"Note that the billing module has a complex state machine — read README first"
```

### Edit Manually
Use `/memory` command to open any memory file in your editor.

### Force On/Off
```bash
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=0  # Force on
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1  # Force off
```

## Best Practices for MEMORY.md

### Keep It Under 200 Lines
Only the first 200 lines are loaded. Content beyond that is invisible to Claude.

### Use It as an Index
```markdown
# Project Memory

## Key Patterns
- Uses pnpm as package manager
- 2-space indentation, no semicolons
- Named exports only

## Debugging Notes
See [debugging.md](debugging.md) for detailed debugging patterns.

## Architecture
See [architecture.md](architecture.md) for module relationships.
```

### What Belongs in MEMORY.md vs Topic Files

| MEMORY.md (loaded every session) | Topic files (loaded on demand) |
|---|---|
| Essential patterns needed every session | Detailed debugging notes |
| Key commands and shortcuts | Architecture deep dives |
| Critical gotchas and warnings | Historical decisions |
| Links to topic files | Specific problem solutions |

### What Belongs in MEMORY.md vs CLAUDE.md

| MEMORY.md (auto, personal) | CLAUDE.md (manual, shared) |
|---|---|
| Claude's own learnings | Your instructions to Claude |
| Per-user, per-project | Team-shared conventions |
| Discovered patterns | Prescribed rules |
| Debugging insights | Required practices |
| Not version controlled | Version controlled |

## What NOT to Save

- Session-specific context (current task, in-progress work)
- Unverified guesses from reading a single file
- Anything that duplicates CLAUDE.md instructions
- Speculative or temporary information
