# Subagents Fundamentals

## What Are Subagents

Subagents are specialized AI instances that run in isolated context windows with:
- Custom system prompts (focused behavior)
- Specific tool access (security and focus)
- Independent permissions
- Separate context from main conversation

When Claude encounters a task matching a subagent's description, it delegates work to that subagent. The subagent works independently and returns results.

## Why Use Subagents

- **Preserve context**: keep exploration/implementation out of main conversation
- **Enforce constraints**: limit which tools a subagent can use
- **Specialize behavior**: focused prompts for specific domains
- **Control costs**: route to cheaper models (Haiku) for simple tasks
- **Parallel execution**: run multiple subagents simultaneously
- **Reuse configurations**: share across projects

## Built-in Subagents

### Explore
- **Model**: Haiku (fast, low-latency)
- **Tools**: Read-only (no Write, Edit)
- **Purpose**: file discovery, code search, codebase exploration
- **Thoroughness levels**: quick, medium, very thorough
- **When used**: Claude needs to search/understand codebase without changes

### Plan
- **Model**: Inherits from main conversation
- **Tools**: Read-only (no Write, Edit)
- **Purpose**: codebase research for planning
- **When used**: plan mode, gathering context before presenting a plan

### general-purpose
- **Model**: Inherits from main conversation
- **Tools**: All tools
- **Purpose**: complex research, multi-step operations, code modifications
- **When used**: task requires both exploration and modification

### Others
| Agent | Model | Purpose |
|---|---|---|
| Bash | Inherit | Terminal commands in separate context |
| statusline-setup | Sonnet | `/statusline` configuration |
| Claude Code Guide | Haiku | Questions about Claude Code features |

## Key Constraints

- **Subagents cannot spawn other subagents** (no nested delegation)
- **Subagents don't inherit skills** from parent (must list explicitly)
- **Subagents receive only their system prompt** (not the full Claude Code system prompt)
- **Background subagents auto-deny** unapproved permissions
- **MCP tools unavailable** in background subagents

## Subagents vs Agent Teams

| Subagents | Agent Teams |
|---|---|
| Work within single session | Coordinate across separate sessions |
| Return results to main context | Independent context per worker |
| No inter-agent communication | Agents communicate via messages |
| Good for focused tasks | Good for sustained parallel work |
| Context returns to main conversation | Each worker manages own context |
