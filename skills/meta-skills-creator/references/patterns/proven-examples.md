# Proven Examples

Real skills built with this methodology, showing the input-to-output pattern.

## Example 1: prompt-creator

### Input
"Create a skill for designing powerful prompts, research best practices from Anthropic, Google, OpenAI."

### Process
1. **Research**: 3 parallel searches (one per provider), 4 official doc fetches
2. **Architecture**: 11 flat reference files (no sub-folders needed — all same level)
3. **Build**: SKILL.md with `<objective>` + `<workflow>` + model-specific tips
4. **Validate**: passed on first attempt

### Output
```
prompt-creator/ (12 files)
├── SKILL.md (113 lines)
└── references/ (11 files, 50-150 lines each)
    ├── anthropic-best-practices.md
    ├── openai-best-practices.md
    ├── google-best-practices.md
    ├── clarity-principles.md
    ├── xml-structure.md
    ├── few-shot-patterns.md
    ├── reasoning-techniques.md
    ├── context-management.md
    ├── system-prompt-patterns.md
    ├── prompt-templates.md
    └── anti-patterns.md
```

### Key Decision
Flat structure because all 11 topics are peer-level (no natural hierarchy).

---

## Example 2: claude-memory

### Input
"Create a skill for initializing and managing Claude memory, based on official docs."

### Process
1. **Research**: 3 searches + 3 official doc fetches (memory page, rules page, settings page)
2. **Architecture**: 5 sub-folders organized by artifact type (claudemd, rules, memory, user, techniques)
3. **Build**: SKILL.md with `<objective>` + `<workflow>` + `<memory_hierarchy>`
4. **Validate**: passed on first attempt

### Output
```
claude-memory/ (9 files)
├── SKILL.md (105 lines)
└── references/
    ├── claudemd/ (structure, templates, example)
    ├── rules/ (guide, domain templates)
    ├── memory/ (auto-memory guide)
    ├── user/ (user-level config)
    └── techniques/ (writing guidelines)
```

### Key Decision
Sub-folders by artifact type because the skill manages distinct file types (CLAUDE.md, rules/, memory/).

---

## Example 3: subagent-creator

### Input
"Create a skill for creating and orchestrating Claude Code subagents."

### Process
1. **Research**: 3 searches + 2 official doc fetches (Claude Code + SDK docs)
2. **Architecture**: 4 sub-folders by lifecycle (fundamentals, prompts, orchestration, operations)
3. **Build**: SKILL.md with `<objective>` + `<workflow>` + `<quick_reference>`
4. **Validate**: passed on first attempt

### Output
```
subagent-creator/ (7 files)
├── SKILL.md (120 lines)
└── references/
    ├── fundamentals/ (concepts, configuration)
    ├── prompts/ (writing agent prompts)
    ├── orchestration/ (6 patterns + SDK)
    └── operations/ (context, debugging)
```

### Key Decision
Sub-folders by lifecycle phase because the skill follows a natural progression: understand → design → orchestrate → operate.

---

## Pattern Summary

| Skill | Files | Sub-folders | Organization |
|---|---|---|---|
| prompt-creator | 12 | 0 (flat) | By topic (peer-level) |
| claude-memory | 9 | 5 | By artifact type |
| subagent-creator | 7 | 4 | By lifecycle phase |

Choose the organization that matches the skill's natural structure.
