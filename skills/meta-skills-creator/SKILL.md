---
name: meta-skills-creator
description: Expert en creation de skills Claude Code de qualite professionnelle. Suit un processus rigoureux en 6 etapes incluant la recherche sur les docs officielles, la conception modulaire avec sous-dossiers, et la validation. Use when the user wants to create a new skill from scratch, design a skill architecture, research best practices for a skill topic, or build a comprehensive skill with modular reference files. Also use when asked to build a skill following the proven methodology.
---

<objective>
Create production-grade Claude Code skills using a proven, repeatable methodology. This meta-skill codifies the exact process used to build high-quality skills like prompt-creator, claude-memory, and subagent-creator.

Every skill created with this process follows these principles:
- Research-driven: built on official documentation, not assumptions
- Modular architecture: sub-folders and topic files, not monoliths
- Progressive disclosure: SKILL.md is lean, references load on demand
- XML-structured: uses `<objective>`, `<workflow>` tags for clarity
- Validated: passes the skill-creator validation before delivery
</objective>

<workflow>

## Phase 1: Understand the Skill

Before writing anything, deeply understand what the skill should do.

Ask the user (1-2 questions max):
- What is the skill's core purpose?
- What triggers should invoke it?

If the user provides examples or references (screenshots, URLs, existing skills), analyze them for: structure patterns, reference file organization, and scope.

See [references/process/phase1-research.md](references/process/phase1-research.md) for the full research methodology.

## Phase 2: Research

Gather authoritative knowledge on the skill's domain:

1. **Search** official documentation (3+ parallel web searches)
2. **Fetch** the most relevant pages for detailed extraction
3. **Synthesize** findings into organized notes
4. **Identify** what Claude already knows vs. what must be in references

Rule: every reference file must contain information Claude does NOT already have. Don't repeat general knowledge.

See [references/process/phase2-research-methodology.md](references/process/phase2-research-methodology.md) for search strategies.

## Phase 3: Design Architecture

Choose the reference file structure based on the skill's domain:

1. **Identify topics** — list every distinct area the skill covers
2. **Group into sub-folders** — organize by function (fundamentals, operations, patterns, etc.)
3. **One file per topic** — each file covers one focused subject
4. **Design SKILL.md** — lean workflow + navigation table to references

See [references/architecture/file-structure.md](references/architecture/file-structure.md) for structure patterns.
See [references/architecture/skillmd-template.md](references/architecture/skillmd-template.md) for the SKILL.md template.

## Phase 4: Build

Execute in this order:

1. **Initialize** with `init_skill.py` from the skill-creator
2. **Clean up** example files (scripts/, assets/, example reference)
3. **Create sub-folders** in references/
4. **Write SKILL.md** first (workflow + navigation table)
5. **Write all reference files** (in parallel when independent)
6. **Remove empty directories**

See [references/patterns/writing-guidelines.md](references/patterns/writing-guidelines.md) for content standards.

## Phase 5: Validate

Run the validator:
```bash
python3 {skill-creator-path}/scripts/quick_validate.py {skill-path}
```

Check:
- Skill is valid (passes validation)
- All referenced files exist
- No empty directories remain
- SKILL.md under 500 lines
- Each reference file under 200 lines

## Phase 6: Deliver

Present to the user:
- **File tree** showing the complete structure
- **Summary** of what each sub-folder covers
- **Source list** (official docs used for research)
- **Invocation command** (`/skill-name`)

</workflow>

<tools>

## Skill Creator Scripts

Located in the skill-creator plugin cache. Find with:
```bash
find ~/.claude/plugins -name "init_skill.py" -path "*/skill-creator/*"
```

| Script | Purpose |
|---|---|
| `init_skill.py <name> --path <dir>` | Initialize a new skill directory |
| `quick_validate.py <skill-path>` | Validate skill structure |
| `package_skill.py <skill-path>` | Package into distributable .skill file |

</tools>
