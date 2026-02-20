# Phase 1: Understand the Skill

## Inputs to Gather

Before creating any skill, collect:

### From the User
- **Name**: what should the skill be called?
- **Purpose**: what does it do? (1-2 sentences)
- **Triggers**: when should Claude invoke it? (specific scenarios)
- **Scope**: what does it cover? What does it NOT cover?
- **References**: any examples, screenshots, URLs, or existing skills to learn from?

### From Analysis
- **Domain mapping**: what are the distinct sub-topics?
- **Existing knowledge**: what does Claude already know about this domain?
- **Gap analysis**: what procedural knowledge must be provided?
- **Target audience**: who will use this skill? (developer, PM, designer?)

## User Input Strategy

Ask maximum 1-2 questions. Don't over-ask.

```
Good: "What's the core purpose, and should it cover X or Y too?"
Bad: 10 separate questions about edge cases
```

If the user provides examples (screenshots, URLs):
1. Extract the structure pattern (file organization)
2. Note the section naming conventions
3. Identify what content is included vs. referenced
4. Adopt what works, improve what doesn't

## When to Skip Research

Skip Phase 2 (research) when:
- The skill codifies a process you just executed (like this meta-skill)
- The domain is well-known and doesn't require official docs
- The user provides complete reference material

## Output of Phase 1

A mental model of:
- The skill's identity (name, description, triggers)
- The domain map (list of topics to cover)
- The research plan (what to search for in Phase 2)
