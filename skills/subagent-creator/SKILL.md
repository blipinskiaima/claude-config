---
name: subagent-creator
description: Expert en creation, configuration et orchestration de sous-agents Claude Code. Use when the user wants to create custom subagents, configure .claude/agents/ files, design multi-agent workflows, use the Task tool effectively, set up agent teams, or optimize agent delegation patterns. Also use when asked about subagent best practices, debugging agents, or writing agent system prompts.
---

<objective>
Create, configure, and orchestrate Claude Code subagents. This skill covers:
- Custom subagent creation (.claude/agents/ files)
- Built-in subagent types (Explore, Plan, general-purpose)
- System prompt writing for agents
- Tool access configuration and permissions
- Multi-agent orchestration patterns
- Agent teams for parallel workflows
- Context management and persistent memory
- Debugging and error recovery

Subagents are specialized AI instances with isolated context, custom prompts, specific tool access, and independent permissions. They delegate focused tasks, preserve main context, and enable parallel execution.
</objective>

<workflow>

## Step 1: Assess the Need

Before creating a subagent, determine if one is needed:

| Use main conversation when | Use subagent when |
|---|---|
| Frequent back-and-forth needed | Task is self-contained |
| Multiple phases share context | Task produces verbose output |
| Quick, targeted change | Need tool restrictions |
| Latency matters | Want isolated context |

Also consider: **Skills** for reusable prompts in main context, **Agent teams** for parallel work with inter-agent communication.

## Step 2: Design the Subagent

Consult references based on need:

| Need | Reference |
|---|---|
| Core concepts and built-in types | [references/fundamentals/subagents.md](references/fundamentals/subagents.md) |
| File format and configuration | [references/fundamentals/configuration.md](references/fundamentals/configuration.md) |
| Writing effective agent prompts | [references/prompts/writing-subagent-prompts.md](references/prompts/writing-subagent-prompts.md) |
| Multi-agent patterns | [references/orchestration/orchestration-patterns.md](references/orchestration/orchestration-patterns.md) |
| Context and memory management | [references/operations/context-management.md](references/operations/context-management.md) |
| Debugging and error recovery | [references/operations/debugging-agents.md](references/operations/debugging-agents.md) |

## Step 3: Create the Subagent

1. Choose scope: project (`.claude/agents/`) or user (`~/.claude/agents/`)
2. Write the markdown file with YAML frontmatter
3. Craft the system prompt (focused, actionable, structured)
4. Configure tools (minimal set needed)
5. Select model (haiku for speed, sonnet for balance, opus for complexity)

## Step 4: Test and Iterate

1. Invoke the subagent with a representative task
2. Verify tool usage is appropriate
3. Check output quality and format
4. Adjust prompt, tools, or model as needed
5. Consider adding persistent memory for learning agents

</workflow>

<quick_reference>

## Subagent File Format

```yaml
---
name: agent-name
description: When Claude should use this agent
tools: Read, Grep, Glob
model: sonnet
permissionMode: default
maxTurns: 10
memory: user
skills:
  - skill-name
---

System prompt goes here in markdown.
```

## Built-in Agent Types

| Type | Model | Tools | Purpose |
|---|---|---|---|
| Explore | Haiku | Read-only | Fast codebase search |
| Plan | Inherit | Read-only | Research for planning |
| general-purpose | Inherit | All | Complex multi-step tasks |

## Common Tool Combinations

| Use Case | Tools |
|---|---|
| Read-only analysis | `Read, Grep, Glob` |
| Test execution | `Bash, Read, Grep` |
| Code modification | `Read, Edit, Write, Grep, Glob` |
| Full access | Omit `tools` (inherits all) |

</quick_reference>
