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
2. **Calibrate prescriptiveness** — pick degrees of freedom (high/medium/low) per area
3. **Group into sub-folders** — organize by function (fundamentals, operations, patterns, etc.)
4. **Decide bundled resources** — scripts/ for executables, assets/ for output materials
5. **One file per topic** — each file covers one focused subject
6. **Design SKILL.md** — lean workflow + navigation table to references

See [references/architecture/file-structure.md](references/architecture/file-structure.md) for structure patterns.
See [references/architecture/skillmd-template.md](references/architecture/skillmd-template.md) for the SKILL.md template.
See [references/architecture/degrees-of-freedom.md](references/architecture/degrees-of-freedom.md) to calibrate prescriptiveness.
See [references/architecture/bundled-resources.md](references/architecture/bundled-resources.md) for scripts/references/assets choices.

## Phase 4: Build

Execute in this order:

1. **Initialize** with `init_skill.py` from the skill-creator
2. **Clean up** example files (scripts/, assets/, example reference)
3. **Verify nothing forbidden** — no README, CHANGELOG, etc. (see anti-patterns)
4. **Create sub-folders** in references/
5. **Write SKILL.md** first (workflow + navigation table)
6. **Write all reference files** (in parallel when independent)
7. **Remove empty directories**

See [references/patterns/writing-guidelines.md](references/patterns/writing-guidelines.md) for content standards.
See [references/quality/anti-patterns.md](references/quality/anti-patterns.md) for what NOT to include.

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

Optional — package for distribution:
```bash
python3 {skill-creator-path}/scripts/package_skill.py {skill-path}
```
Use only if sharing with another machine or user (produces a `.skill` zip). Skills used locally don't need packaging.

## Phase 7: Iterate

Skills rarely land perfect on first build. Treat the first version as a draft.

After real usage:
1. **Observe** where Claude struggled, looped, or asked redundant questions
2. **Identify** the gap — missing reference, unclear workflow step, wrong degree of freedom
3. **Update** the affected file (SKILL.md or specific reference) — surgical, don't rewrite
4. **Re-validate** with `quick_validate.py`
5. **Re-test** on the failing case

Common iteration triggers:
- Claude loads a reference file that turns out unhelpful → tighten the description or remove
- Claude misses a constraint repeatedly → move it from a reference to SKILL.md
- Claude over-explains where it should act → reduce freedom in that section
- Claude is rigid where flexibility is needed → increase freedom

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
