# What NOT to Include in a Skill

A skill should contain only what another Claude instance needs to execute the task. Everything else is bloat — costs tokens, dilutes signal, creates confusion.

## Forbidden Files

| File | Why forbidden | What to do instead |
|---|---|---|
| README.md | User-facing docs ≠ skill behavior. Claude doesn't read it. | Put trigger info in frontmatter `description` |
| CHANGELOG.md | Version history is meta, not procedural | Use git log |
| INSTALLATION_GUIDE.md | Skills auto-load from filesystem | Nothing |
| QUICK_REFERENCE.md | Duplicates SKILL.md or references | Merge into existing reference file |
| CONTRIBUTING.md | Process meta, not skill behavior | Out of scope |
| TODO.md / NOTES.md | Ephemeral state | Use TaskCreate in conversation |
| .gitignore, .github/ | Skill isn't a standalone repo | None |
| LICENSE.txt | OK only if explicitly required by source | Skip unless redistributing |

## Forbidden Content in SKILL.md Body

| Anti-pattern | Why | Fix |
|---|---|---|
| "When to Use This Skill" section | The body loads AFTER trigger — triggers belong in frontmatter `description` | Move trigger phrases to description |
| "This skill helps you..." intro | Self-reference adds no procedural value | Delete |
| Author credits, version notes | Meta info, not behavior | Delete |
| Setup instructions for the user | Skills have no install step | Delete |
| Long Markdown intro paragraphs | Prose before action wastes tokens | Lead with workflow |

## Forbidden Content in Reference Files

- **General knowledge Claude already has**: Markdown syntax, basic Python, what HTTP is, etc.
- **Duplicated content**: one fact, one file. If two files explain the same thing, merge them.
- **Long prose explanations**: prefer tables, code blocks, bullet points.
- **Defensive caveats**: "It's important to note that...", "Don't worry if..." — delete.
- **Meta-narration**: "In the next section we will...", "As mentioned above..." — delete.

## The Three-Question Test

For each file in the skill, ask:

1. Does another Claude instance **need** this file to execute the skill correctly?
2. Is this info already available elsewhere (frontmatter, code comments, official docs)?
3. Would removing this file degrade Claude's behavior on the task?

If (1) is **no** OR (2) is **yes** OR (3) is **no** → delete it.

## Bloat Patterns to Strip

| Pattern | Symptom | Fix |
|---|---|---|
| Verbose explanations | Paragraphs of prose before each example | Show example first, 1-line context |
| Reassurance | "Don't worry if X happens" | Delete |
| Self-reference | "This skill will help you..." | Delete |
| Hedging | "You might want to consider possibly..." | Use imperative: "Use X" |
| Repeating frontmatter | Body restates the description | Delete from body |

## When in Doubt

Default to **deleting**. A leaner skill is almost always better than a thorough one. If Claude needs the info later, add it then — don't pre-emptively bundle it.
