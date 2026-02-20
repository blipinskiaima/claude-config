# Writing Subagent Prompts

## Principles

### 1. Focused Role
Each subagent should excel at ONE specific task.

```markdown
# Good — focused
You are a security code reviewer. Analyze code for vulnerabilities,
focusing on OWASP top 10 issues.

# Bad — too broad
You are a code helper. Do whatever the user asks with code.
```

### 2. Clear Description
The `description` field is critical — Claude uses it to decide when to delegate.

```yaml
# Good — specific trigger
description: Expert code reviewer. Use proactively after writing or modifying code.

# Bad — vague
description: Helps with code stuff.
```

Add "Use proactively" to encourage automatic delegation.

### 3. Structured Workflow
Define a clear step-by-step process:

```markdown
When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code clarity and readability
- Naming conventions
- Error handling
- Security vulnerabilities
```

### 4. Output Format
Specify how results should be organized:

```markdown
Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (nice to have)

Include specific code examples for each fix.
```

### 5. Minimal Instructions
Subagents receive ONLY their system prompt. Include everything needed but nothing more.

## Complete Template

```markdown
---
name: {agent-name}
description: {specific description}. Use proactively when {trigger}.
tools: {minimal tool set}
model: {appropriate model}
---

You are a {role} specializing in {domain}.

When invoked:
1. {First action — gather context}
2. {Main analysis/action}
3. {Verify/validate results}

Focus areas:
- {Key concern 1}
- {Key concern 2}
- {Key concern 3}

Output format:
- {How to structure the response}
- {What to include/exclude}
```

## Anti-Patterns

| Don't | Do Instead |
|---|---|
| Write a novel as prompt | Keep under 500 words |
| Duplicate Claude Code's system prompt | Focus on specialized behavior |
| Include tool descriptions | Use `tools` frontmatter field |
| Say "be helpful and friendly" | Define specific behavior |
| List every possible scenario | Cover the 80% case clearly |
