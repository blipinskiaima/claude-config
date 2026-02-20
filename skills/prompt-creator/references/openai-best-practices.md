# OpenAI Best Practices (GPT-5.2)

Techniques and recommendations specific to GPT-5.x models.

## CTCO Pattern

The most reliable structure for GPT prompts:
- **Context**: who is the model, background state
- **Task**: single, atomic action required
- **Constraints**: negative constraints, scope limits
- **Output**: exact format expected

## Recommended Prompt Structure

```markdown
# Role and Objective
# Instructions
## Sub-categories for detail
# Reasoning Steps
# Output Format
# Examples
# Context
# Final instructions (reminder)
```

## Instruction Placement

Place critical instructions at BOTH the beginning AND end of long contexts. If only one: before context outperforms after.

## Explicit Length Constraints

GPT-5.2 responds best to concrete limits:
- Simple questions: 1-2 sentences
- Standard answers: 3-6 sentences
- Detailed analysis: 1 overview paragraph + max 5 bullets

## Markdown as Primary Delimiter

Use H1-H4 headings for hierarchy. Inline backticks and code blocks for technical content. Lists for enumerated rules.

## Instruction-Following Precision

GPT-5.2 follows instructions more literally than predecessors:
- Make instructions literal and explicit
- Don't rely on implicit intent
- Don't overuse ALL CAPS, bribes, or penalties
- Demonstrate important behavior in examples AND cite it in rules

## Tool-Calling Best Practices

- Use the API `tools` field, don't inject tool descriptions manually
- Name tools clearly with detailed descriptions
- Put usage examples in the system prompt, not in tool descriptions

## Agentic Persistence

```
Keep working until the task is fully resolved. Do not yield control back until done or genuinely blocked.
```

## Self-Check for High-Stakes

```
Before finalizing, scan your answer for unstated assumptions, ungrounded numbers, and overly strong language. Soften or qualify as needed.
```

## Reasoning Effort Control

Use `reasoning_effort` parameter (none → low → medium → high) to balance quality vs latency. Lower effort for simple tasks, higher for complex reasoning.

## Scope Discipline

```
No extra features, no added components, no UX embellishments beyond what was specified.
```

## File Diff Format

GPT models trained on V4A diff format. Use 3-line context, `@@` operators, never line numbers.
