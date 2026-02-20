# File Structure Patterns

## The Golden Rule

**1 file = 1 topic. 1 sub-folder = 1 functional area.**

Claude loads only the reference file it needs. A monolithic file forces loading everything.

## Standard Structure

```
skill-name/
├── SKILL.md                        # Workflow + navigation (lean, <150 lines)
└── references/
    ├── {area-1}/                   # Functional area
    │   ├── {topic-a}.md           # Focused topic (<200 lines)
    │   └── {topic-b}.md
    ├── {area-2}/
    │   └── {topic-c}.md
    └── {area-3}/
        ├── {topic-d}.md
        └── {topic-e}.md
```

## Sub-Folder Naming Patterns

Choose names that describe the FUNCTION of the content:

| Pattern | Good Names | Use When |
|---|---|---|
| By lifecycle phase | `fundamentals/`, `operations/`, `advanced/` | Skill has progressive depth |
| By domain | `frontend/`, `backend/`, `infra/` | Skill spans multiple domains |
| By activity | `process/`, `architecture/`, `patterns/` | Skill is a methodology |
| By provider | `anthropic/`, `openai/`, `google/` | Skill covers multiple providers |
| By artifact | `claudemd/`, `rules/`, `memory/` | Skill manages multiple file types |

## Real Examples from Proven Skills

### prompt-creator (12 files)
```
references/
├── anthropic-best-practices.md     # Provider-specific
├── openai-best-practices.md
├── google-best-practices.md
├── clarity-principles.md           # Universal technique
├── xml-structure.md
├── few-shot-patterns.md
├── reasoning-techniques.md
├── context-management.md
├── system-prompt-patterns.md
├── prompt-templates.md             # Ready-to-use scaffolds
└── anti-patterns.md                # What to avoid
```

### claude-memory (8 files, 5 sub-folders)
```
references/
├── claudemd/                       # By artifact type
│   ├── structure.md
│   ├── section-templates.md
│   └── comprehensive-example.md
├── rules/
│   ├── rules-directory-guide.md
│   └── domain-rules.md
├── memory/
│   └── auto-memory-guide.md
├── user/
│   └── user-level-guide.md
└── techniques/
    └── prompting-techniques.md
```

### subagent-creator (6 files, 4 sub-folders)
```
references/
├── fundamentals/                   # By lifecycle phase
│   ├── subagents.md
│   └── configuration.md
├── prompts/
│   └── writing-subagent-prompts.md
├── orchestration/
│   └── orchestration-patterns.md
└── operations/
    ├── context-management.md
    └── debugging-agents.md
```

## Sizing Guidelines

| Component | Target | Max |
|---|---|---|
| SKILL.md | 80-150 lines | 500 lines |
| Reference file | 50-150 lines | 200 lines |
| Reference files per skill | 5-12 | 15 |
| Sub-folders | 2-5 | 7 |
| Total skill files | 6-13 | 16 |

## When NOT to Use Sub-Folders

If the skill has <=4 reference files, flat structure is fine:
```
references/
├── technique-a.md
├── technique-b.md
├── examples.md
└── anti-patterns.md
```

Sub-folders add value starting at 5+ reference files.
