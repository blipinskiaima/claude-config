# Debugging Agents

## Common Issues and Fixes

### Claude Not Delegating
- Ensure `Task` tool is available (not denied)
- Make description more specific, add "Use proactively"
- Mention agent by name: "Use the code-reviewer agent to..."
- Check if another agent with same name has higher priority

### Agent Not Loading
- Agents load at session start — restart or use `/agents`
- Check file is in `.claude/agents/` or `~/.claude/agents/`
- Verify YAML frontmatter has no syntax errors
- Check `name` uses lowercase + hyphens only

### Permission Errors
- Check `tools` field includes needed tools
- Check `disallowedTools` isn't blocking needed tools
- Background agents: permissions must be pre-approved
- Resume failed background agent in foreground for interactive prompts

### Agent Over/Under-Acting
- **Over-acting**: restrict `tools`, add `maxTurns`, tighten prompt
- **Under-acting**: expand `tools`, increase `maxTurns`, make prompt more explicit

### Long Prompt Failures (Windows)
- Windows command line limit: 8191 chars
- Keep prompts concise or use filesystem-based agents

## Diagnostic Steps

1. Run `/agents` to list all agents
2. Check priority conflicts (same name, different locations)
3. Verify `settings.json` doesn't deny the agent
4. Review transcripts: `~/.claude/projects/{project}/{session}/subagents/`
5. Test explicitly: "Use the {name} agent to {simple task}"

## Monitoring Hooks

```json
{
  "hooks": {
    "SubagentStart": [{
      "matcher": "my-agent",
      "hooks": [{ "type": "command", "command": "echo 'started'" }]
    }],
    "SubagentStop": [{
      "hooks": [{ "type": "command", "command": "echo 'stopped'" }]
    }]
  }
}
```

## PreToolUse Validation

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
```

Exit codes: `0` = allow, `2` = block (error via stderr).

## Performance Optimization

| Issue | Solution |
|---|---|
| Agent too slow | Use `haiku` for simple tasks |
| Too much context consumed | Ask for summaries only |
| Agent over-explores | Add `maxTurns` limit |
| Re-discovers same info | Enable `memory` |
| Too many parallel agents | Limit concurrency, use sequential for dependencies |
