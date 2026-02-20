# CLAUDE.md Structure Guide

## File Locations

| File | Location | Shared? | Purpose |
|---|---|---|---|
| Project CLAUDE.md | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team (git) | Project-wide instructions |
| Local CLAUDE.md | `./CLAUDE.local.md` | No (gitignored) | Personal project prefs |
| User CLAUDE.md | `~/.claude/CLAUDE.md` | No | Global personal prefs |

## Recommended Section Order

```markdown
# Project Name

## Project Overview
Brief description of what the project does, the stack, and key architecture decisions.

## Tech Stack
- Language/Framework versions
- Key dependencies
- Database / infrastructure

## Commands
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`
- Dev server: `npm run dev`

## Architecture
- Key directories and what they contain
- Important patterns (MVC, hexagonal, etc.)
- Module relationships

## Code Style
- Naming conventions
- Import ordering
- Formatting rules (indentation, line length)

## Git Conventions
- Branch naming: feature/xxx, fix/xxx
- Commit message format
- PR requirements

## Important Notes
- Known gotchas or quirks
- Things to never do
- Security considerations
```

## Key Principles

### Keep It Concise
Every line consumes tokens. Ask: "Does Claude need this in every session?" If no, put it in a rules file or reference doc instead.

### Be Specific
```
# Bad
Format code properly

# Good
- Use 2-space indentation
- Max line length: 100 characters
- Use single quotes for strings
```

### Use Imports for Large Content
Don't duplicate content. Reference other files:
```markdown
See @README.md for project overview.
See @docs/api.md for API documentation.
Git workflow: @docs/git-instructions.md
```

Imports support:
- Relative paths (resolved from the importing file)
- Absolute paths
- Home directory: `@~/.claude/my-instructions.md`
- Max recursion depth: 5 hops

### Group Related Instructions
```markdown
## Testing
- Run tests: `pytest tests/`
- Always run tests before committing
- Minimum coverage: 80%
- Use fixtures for database tests
```

### Include the WHY
```markdown
## API Design
- Always return pagination metadata
  (our mobile clients require total count for infinite scroll)
- Use snake_case for JSON keys
  (legacy system compatibility, cannot change)
```

## What NOT to Put in CLAUDE.md

- Long documentation (use @imports or .claude/rules/ instead)
- Information Claude already knows (language syntax, framework basics)
- Temporary task-specific context (belongs in conversation, not memory)
- Secrets, tokens, passwords (security risk if committed)
