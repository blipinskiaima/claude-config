# Orchestration Patterns

## Pattern 1: Sequential Chain

One subagent's output feeds the next.

```
User → "Review code, then fix issues"
Claude:
  1. code-reviewer → list of issues
  2. fixer → fixes applied
  3. Returns summary
```

Best for: dependent multi-step workflows.

## Pattern 2: Parallel Research

Spawn multiple subagents simultaneously for independent tasks.

```
User → "Analyze auth, database, and API modules"
Claude spawns 3 Explore agents in parallel:
  - Explore (auth) → findings
  - Explore (database) → findings
  - Explore (API) → findings
Claude synthesizes all findings
```

Best for: independent investigations. Warning: each result consumes main context.

## Pattern 3: Isolate Verbose Operations

Delegate high-output tasks to keep main context clean.

```
User → "Run the full test suite"
test-runner subagent:
  - Runs 500 tests internally
  - Returns: "498 passed, 2 failed: test_auth, test_payment"
```

Best for: test execution, log analysis, documentation scanning.

## Pattern 4: Specialist Delegation

Domain-specific agents auto-invoked by description match.

```
.claude/agents/
├── security-reviewer.md
├── performance-analyzer.md
├── api-designer.md
└── test-writer.md
```

## Pattern 5: Coordinator Agent

Main agent orchestrating specialized sub-agents (`claude --agent`):

```yaml
---
name: coordinator
tools: Task(worker, researcher, tester), Read, Bash
---

Workflow:
1. researcher → understand the task
2. worker → implement changes
3. tester → verify results
```

## Pattern 6: Agent Teams

For sustained parallel work with inter-agent communication:

```
TeamCreate → creates team + task list
TaskCreate → defines tasks
Task → spawn teammates (own sessions)
SendMessage → agents communicate
TaskUpdate → track progress
```

## Foreground vs Background

| Foreground | Background |
|---|---|
| Blocks main conversation | Runs concurrently |
| Permission prompts pass through | Pre-approved permissions only |
| Can ask clarifying questions | Questions auto-fail |
| MCP tools available | MCP tools unavailable |

Press **Ctrl+B** to background a running task.

## Model Assignment Strategy

| Role | Model | Why |
|---|---|---|
| Lead/Coordinator | Opus | Complex reasoning |
| Specialized worker | Sonnet | Balanced capability/cost |
| Fast search/lookup | Haiku | Speed, low latency |

## SDK Orchestration

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async for message in query(
    prompt="Review and fix the auth module",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Grep", "Glob", "Task"],
        agents={
            "reviewer": AgentDefinition(
                description="Code reviewer",
                prompt="You are a security reviewer...",
                tools=["Read", "Grep", "Glob"],
                model="sonnet",
            ),
        },
    ),
):
    if hasattr(message, "result"):
        print(message.result)
```
