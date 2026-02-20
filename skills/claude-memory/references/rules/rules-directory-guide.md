# Rules Directory Guide

## What Is .claude/rules/

A modular alternative to monolithic CLAUDE.md files. Each markdown file in `.claude/rules/` is automatically loaded with the **same high priority as CLAUDE.md**.

## When to Use Rules vs CLAUDE.md

| Use CLAUDE.md for | Use .claude/rules/ for |
|---|---|
| Project overview, key commands | Domain-specific guidelines |
| Quick-reference info needed every session | Rules that apply to specific file types |
| Team-wide conventions | Detailed standards per topic |
| Small projects with few rules | Large projects with many conventions |

## Basic Setup

```
your-project/
├── .claude/
│   ├── CLAUDE.md              # Lean: overview + commands
│   └── rules/
│       ├── code-style.md      # Naming, formatting
│       ├── testing.md         # Test conventions
│       ├── security.md        # Security requirements
│       └── git.md             # Git workflow
```

## Organized with Subdirectories

```
.claude/rules/
├── frontend/
│   ├── react.md               # Component patterns
│   ├── styles.md              # CSS/Tailwind conventions
│   └── accessibility.md       # A11y requirements
├── backend/
│   ├── api-design.md          # REST/GraphQL conventions
│   ├── database.md            # Query patterns, migrations
│   └── error-handling.md      # Error format, logging
├── infra/
│   ├── docker.md              # Container conventions
│   └── ci-cd.md               # Pipeline rules
└── general.md                 # Cross-cutting concerns
```

All `.md` files are discovered recursively.

## Path-Specific Rules

Rules can target specific files using YAML frontmatter:

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "src/api/**/*.test.ts"
---

# API Development Rules

- All endpoints must validate input with Zod
- Return standard error format: `{ code, message, details }`
- Include OpenAPI documentation comments
```

Without `paths` frontmatter: rule loads for all files (unconditional).
With `paths` frontmatter: rule loads only when Claude works on matching files.

### Glob Patterns

| Pattern | Matches |
|---|---|
| `**/*.ts` | All .ts files anywhere |
| `src/**/*` | Everything under src/ |
| `*.md` | Markdown in project root only |
| `src/components/*.tsx` | Direct children only |
| `src/**/*.{ts,tsx}` | Both .ts and .tsx (brace expansion) |
| `{src,lib}/**/*.ts` | .ts files in src/ or lib/ |

## Symlinks

Share rules across projects:
```bash
# Symlink shared directory
ln -s ~/shared-claude-rules .claude/rules/shared

# Symlink individual file
ln -s ~/company-standards/security.md .claude/rules/security.md
```

Circular symlinks are detected and handled safely.

## Best Practices

1. **One topic per file** — don't mix testing and security in one file
2. **Descriptive filenames** — `api-validation.md` not `rules2.md`
3. **Use path targeting sparingly** — only when rules truly apply to specific file types
4. **Keep rules focused** — each file should be scannable in 30 seconds
5. **Version control** — commit rules so the team shares the same standards
6. **Migrate gradually** — extract sections from CLAUDE.md into targeted rules over time
