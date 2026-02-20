---
name: claude-memory
description: Expert en creation et optimisation du systeme de memoire de Claude Code. Initialise ou met a jour CLAUDE.md, auto memory (MEMORY.md), et les regles modulaires (.claude/rules/). Use when the user wants to set up Claude memory for a new project, optimize an existing CLAUDE.md, create modular rules, manage auto memory, or review and improve their Claude Code configuration. Also use when the user invokes /claude-memory or asks about memory best practices.
---

<objective>
Master Claude Code's memory system to initialize, update, and optimize project configurations. This skill covers:
- CLAUDE.md files (project, user, local)
- Auto memory (MEMORY.md + topic files)
- Modular rules (.claude/rules/)
- Settings configuration (settings.json)

Goal: ensure Claude always has the right context, loaded efficiently, for the current project.
</objective>

<workflow>

## Step 1: Assess Current State

Before making changes, analyze the existing memory configuration:

1. Check for existing CLAUDE.md files (project root, .claude/, parent dirs)
2. Check for .claude/rules/ directory and existing rules
3. Check auto memory at ~/.claude/projects/<project>/memory/
4. Check user-level config at ~/.claude/CLAUDE.md and ~/.claude/rules/
5. Identify the project type, stack, and conventions

Ask the user: **Initialize** (new project) or **Update** (existing project)?

## Step 2: Choose the Right Approach

### For Initialization
Consult references by project need:

| Need | Reference |
|---|---|
| CLAUDE.md structure | [references/claudemd/structure.md](references/claudemd/structure.md) |
| Section templates | [references/claudemd/section-templates.md](references/claudemd/section-templates.md) |
| Complete examples | [references/claudemd/comprehensive-example.md](references/claudemd/comprehensive-example.md) |
| Modular rules setup | [references/rules/rules-directory-guide.md](references/rules/rules-directory-guide.md) |
| Rules by domain | [references/rules/domain-rules.md](references/rules/domain-rules.md) |
| User-level config | [references/user/user-level-guide.md](references/user/user-level-guide.md) |
| Auto memory setup | [references/memory/auto-memory-guide.md](references/memory/auto-memory-guide.md) |
| Writing techniques | [references/techniques/prompting-techniques.md](references/techniques/prompting-techniques.md) |

### For Update
1. Read existing CLAUDE.md and rules
2. Analyze the current project (stack, patterns, conventions)
3. Identify gaps and outdated instructions
4. Apply updates surgically — don't rewrite what works

## Step 3: Build or Update

### CLAUDE.md Principles
- **Be specific**: "Use 2-space indentation" not "Format code properly"
- **Be concise**: every line must earn its token cost
- **Use structure**: bullet points, grouped under descriptive headings
- **Include commands**: build, test, lint, deploy commands the project uses
- **Document patterns**: architecture decisions, naming conventions, key abstractions
- **Use imports**: `@path/to/file` for referencing other docs instead of duplicating

### Rules Directory Principles
- **One topic per file**: `testing.md`, `security.md`, `api-design.md`
- **Use path targeting** when rules apply only to specific files
- **Organize with subdirectories**: `frontend/`, `backend/`, `infra/`
- **Descriptive filenames**: the name should indicate the content

### Auto Memory Principles
- **Keep MEMORY.md under 200 lines** (only first 200 lines are loaded)
- **Use topic files** for detailed notes (debugging.md, patterns.md)
- **MEMORY.md is an index**, not a dump — link to topic files

## Step 4: Verify

After creating/updating:
1. Check total token budget impact (all loaded files combined)
2. Verify no contradictions between memory files
3. Confirm rules have correct path targeting
4. Test with a sample query to verify Claude picks up the new instructions

</workflow>

<memory_hierarchy>
Priority order (highest first):
1. Managed policy (/etc/claude-code/CLAUDE.md)
2. Project rules (.claude/rules/*.md) — same priority as CLAUDE.md
3. Project CLAUDE.md (./CLAUDE.md or ./.claude/CLAUDE.md)
4. CLAUDE.local.md (personal, gitignored)
5. User CLAUDE.md (~/.claude/CLAUDE.md)
6. User rules (~/.claude/rules/*.md)
7. Auto memory (~/.claude/projects/<project>/memory/MEMORY.md — first 200 lines)

More specific instructions always take precedence over broader ones.
</memory_hierarchy>
