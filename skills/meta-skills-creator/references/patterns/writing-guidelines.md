# Writing Guidelines for Reference Files

## Content Standards

### Be Actionable
Every section should answer: "What should Claude DO with this information?"

```markdown
# Bad — descriptive
XML tags are a feature of Claude that allows structured prompting.

# Good — actionable
Use XML tags to separate logical sections:
<context>background info</context>
<task>what to do</task>
<rules>constraints</rules>
```

### Be Specific
```markdown
# Bad
Keep files small

# Good
Each reference file: 50-150 lines (max 200)
SKILL.md: 80-150 lines (max 500)
MEMORY.md: hard limit of 200 lines (only first 200 loaded)
```

### Use Tables for Comparisons
```markdown
| Use X when | Use Y when |
|---|---|
| Task is simple | Task is complex |
| Speed matters | Quality matters |
```

### Use Code Blocks for Examples
Always show concrete examples, not just descriptions:

```markdown
## Template
\`\`\`yaml
---
name: example
description: Does X when Y happens
tools: Read, Grep
---

System prompt here.
\`\`\`
```

### Include Anti-Patterns
Every reference should have a "Don't" section or anti-pattern table.

## File Organization

### Table of Contents
For files >100 lines, include a ToC at the top:

```markdown
## Table of Contents
1. [Section A](#section-a)
2. [Section B](#section-b)
3. [Section C](#section-c)
```

### Section Ordering
1. Core concepts first
2. How-to / practical usage second
3. Examples third
4. Anti-patterns / gotchas last

### Heading Levels
- `#` — file title (one per file)
- `##` — major sections
- `###` — sub-sections
- Don't go deeper than `###` in reference files

## Tone and Style

- **Imperative mood**: "Use XML tags" not "You should use XML tags"
- **No filler**: every sentence must earn its token cost
- **Bullet points over prose**: faster to parse
- **Show, don't tell**: examples > explanations
- **English for technical content**: even if SKILL.md description is multilingual

## Quality Checklist Per File

- [ ] Title matches filename
- [ ] Under 200 lines
- [ ] Has at least one concrete example
- [ ] Has anti-patterns or "don't" section
- [ ] No duplicate content from other reference files
- [ ] No information Claude already knows (language basics, etc.)
- [ ] All code blocks have syntax highlighting
