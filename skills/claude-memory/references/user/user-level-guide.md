# User-Level Configuration Guide

Personal preferences that apply across all your projects.

## User CLAUDE.md

Location: `~/.claude/CLAUDE.md`

This file contains your personal global preferences. Keep it lean — these tokens are consumed in every session.

### Example

```markdown
# Global Guidelines

## Coding Preferences
- Use functional style when possible
- Prefer composition over inheritance
- Always use strict TypeScript (no any)
- Use const assertions where applicable

## Communication
- Be concise, no preambles
- Use French for explanations unless code/comments
- Don't add emoji unless I ask

## Workflow
- Never commit without asking me first
- Always run tests before suggesting changes are done
- Use git rebase, never merge commits
```

## User Rules Directory

Location: `~/.claude/rules/`

Personal rules loaded before project rules (project rules override if conflict).

### Recommended Structure

```
~/.claude/rules/
├── preferences.md     # Coding style preferences
├── workflows.md       # Git, review, deployment habits
├── git.md             # Commit message and branch conventions
└── communication.md   # How you want Claude to communicate
```

### Example: preferences.md

```markdown
# Personal Coding Preferences

- Prefer early returns over deeply nested conditionals
- Use descriptive variable names (no single-letter vars except loop counters)
- Always destructure function parameters when 3+ properties
- Prefer const over let, never use var
- Use template literals over string concatenation
```

### Example: workflows.md

```markdown
# Workflow Preferences

- Always run the full test suite before declaring a task complete
- Use /compact when context is getting long
- When debugging, reproduce the issue first before fixing
- Prefer minimal diffs — don't refactor adjacent code
```

### Example: git.md

```markdown
# Git Preferences

- Commit message format: type(scope): description
- Branch naming: feature/short-desc, fix/short-desc
- Always rebase on main before creating PR
- Never force push to shared branches
- Squash commits when merging
```

## User Settings

Location: `~/.claude/settings.json`

Programmatic preferences (not natural language instructions):

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(pnpm *)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(git status)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)"
    ]
  },
  "env": {
    "EDITOR": "code"
  }
}
```

## Priority Order

When there's a conflict between user and project config:

1. Project settings override user settings
2. Project rules override user rules
3. Project CLAUDE.md overrides user CLAUDE.md
4. Local files (.local.md, settings.local.json) override shared project files

This means: set your defaults at user level, let projects override when needed.
