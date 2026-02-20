# SKILL.md Template

## The Template

Every SKILL.md follows this structure:

```markdown
---
name: {skill-name}
description: {what it does + when to use it}. Use when {trigger 1}, {trigger 2}, or {trigger 3}. Also use when asked to {trigger 4}.
---

<objective>
{1-3 sentences explaining the skill's purpose and scope.}
{List the key areas covered.}
</objective>

<workflow>

## Step 1: {Assess / Gather / Understand}
{Initial analysis of what the user needs.}
{Questions to ask (1-2 max).}

## Step 2: {Design / Select / Plan}
{Decision-making phase.}

Navigation table to references:
| Need | Reference |
|---|---|
| {topic} | [references/{area}/{file}.md](references/{area}/{file}.md) |

## Step 3: {Build / Execute / Apply}
{Main action phase.}
{Key principles to follow.}

## Step 4: {Verify / Review / Test}
{Quality check before delivery.}

</workflow>

<quick_reference>
{Optional: key facts, formats, or cheat sheets that are useful inline.}
</quick_reference>
```

## Frontmatter Rules

### name
- Lowercase + hyphens
- Descriptive, 2-3 words max
- Examples: `prompt-creator`, `claude-memory`, `subagent-creator`

### description
- MOST IMPORTANT FIELD — Claude uses this to decide when to invoke
- Include BOTH what it does AND when to use it
- List specific triggers and scenarios
- Write in English (even if skill content is in another language)

```yaml
# Good — specific triggers listed
description: Expert prompt engineering for creating effective prompts for Claude, GPT, Gemini. Use when writing system prompts, user prompts, agent prompts, few-shot examples, or optimizing existing prompts.

# Bad — vague
description: Helps with prompts.
```

## Body Rules

### Use XML Tags
- `<objective>` — what the skill does (always present)
- `<workflow>` — step-by-step process (always present)
- `<quick_reference>` — inline cheat sheet (optional)
- `<tools>` — available scripts/commands (optional)

### Navigation Table
Link to every reference file with a descriptive "Need" label:

```markdown
| Need | Reference |
|---|---|
| Core concepts | [references/fundamentals/basics.md](...) |
| Configuration | [references/fundamentals/config.md](...) |
```

This is the KEY mechanism for progressive disclosure — Claude reads the table and loads only the relevant file.

### Keep It Lean
- SKILL.md should be 80-150 lines
- No detailed content — that goes in reference files
- Include only: workflow steps, navigation, quick reference
- If SKILL.md exceeds 200 lines, extract content to references

## Common Mistakes

| Mistake | Fix |
|---|---|
| Putting all content in SKILL.md | Extract to reference files |
| Vague description field | List specific triggers |
| No navigation table | Add a table linking to every reference |
| Missing `<objective>` tag | Always start with objective |
| Workflow steps too detailed | Keep high-level, link to refs |
