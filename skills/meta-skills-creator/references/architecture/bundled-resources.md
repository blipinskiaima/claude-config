# Bundled Resources

A skill = SKILL.md + optional bundled resources. Three resource types, each with a specific role.

## The Three Types

| Type | Folder | Purpose | Loaded into context? |
|---|---|---|---|
| **Scripts** | `scripts/` | Executable code (Python, Bash) | No — executed directly |
| **References** | `references/` | Markdown docs read by Claude | Yes — on demand |
| **Assets** | `assets/` | Files used in output (templates, images, fonts) | No — copied or embedded |

## Decision Tree

```
Is the file executable code Claude runs?
├── Yes → scripts/
└── No
    ├── Will Claude read it as guidance?
    │   ├── Yes → references/
    │   └── No → assets/
```

## Scripts (`scripts/`)

### When to use
- Same code gets rewritten across invocations
- Deterministic reliability needed (parsing, validation, conversion)
- Operation is fragile and benefits from a tested implementation

### Examples
| Skill | Script | Why |
|---|---|---|
| skill-creator | `quick_validate.py` | Deterministic validation |
| pdf-editor | `rotate_pdf.py` | Same code each time |
| qc-report | `compute_metrics.py` | Reusable across samples |

### Conventions
- Shebang line (`#!/usr/bin/env python3`, `#!/usr/bin/env bash`)
- Executable bit (`chmod +x`)
- CLI args parsed (argparse, click, getopts)
- No interactive prompts (skills run autonomously)
- Test before bundling — buggy scripts waste retry loops

### Anti-patterns
- Wrapping a one-line bash command in a script
- Scripts that depend on user environment without checking
- Scripts that print to stdout verbosely (use stderr for logs)

## References (`references/`)

### When to use
- Schemas, API docs, domain knowledge
- Patterns and templates too detailed for SKILL.md
- Variant-specific content (per provider, per framework)

### Examples
| Skill | Reference | Content |
|---|---|---|
| big-query | `references/schema.md` | Table schemas, join keys |
| brand-kit | `references/colors.md` | Palette HEX codes |
| pipeline | `references/troubleshooting.md` | Known errors → fixes |

### Conventions
- 1 file = 1 topic
- <200 lines per file
- Table of Contents if >100 lines
- Linked from SKILL.md with description of when to load

See [file-structure.md](file-structure.md) for the modular sub-folder layout.

## Assets (`assets/`)

### When to use
- Templates copied or modified in Claude's output (HTML, PPTX, Typst)
- Binary files (images, fonts, icons, logos)
- Sample documents Claude adapts

### Examples
| Skill | Asset | Usage |
|---|---|---|
| frontend-builder | `assets/hello-world/` | React boilerplate, copied as-is |
| brand-kit | `assets/logo.png` | Embedded in generated docs |
| rapport | `assets/template.typ` | Typst template, modified per report |

### Conventions
- Group by output type (`assets/templates/`, `assets/images/`)
- Document expected usage in SKILL.md
- Keep small — large binaries bloat the skill package

## Quick Comparison

| Question | Scripts | References | Assets |
|---|---|---|---|
| Loaded into Claude's context? | No | Yes (on demand) | No |
| Token cost when used? | 0 (executed) | High (full read) | 0 (copied) |
| Can Claude read for patching? | Yes | Yes | Rarely |
| Best for fragile ops? | ✅ | ❌ | ❌ |
| Best for procedural guidance? | ❌ | ✅ | ❌ |
| Best for output materials? | ❌ | ❌ | ✅ |

## When NOT to Bundle

| Don't bundle | Reason |
|---|---|
| README, CHANGELOG, etc. | See [../quality/anti-patterns.md](../quality/anti-patterns.md) |
| Files specific to one user | Skills should be reusable across contexts |
| Sensitive data (tokens, API keys) | Skills are shareable artifacts |
| Anything Claude can derive cheaply | If `git log` or `--help` gives it, no need |

## Sizing Discipline

A bundled resource that's never loaded is overhead. Before adding any file:

1. **Will Claude actually load/run this** in the expected workflow?
2. Is there a smaller, simpler alternative?
3. Could it live in SKILL.md instead (if <30 lines)?

If "no/yes/yes" → don't bundle.
