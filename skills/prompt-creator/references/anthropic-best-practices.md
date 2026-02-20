# Anthropic Best Practices (Claude 4.6)

Techniques and recommendations specific to Claude Opus 4.6 and Sonnet 4.6.

## XML Tags Are First-Class

Claude excels with XML-structured prompts. Use descriptive tag names:
`<context>`, `<task>`, `<rules>`, `<examples>`, `<output_format>`, `<guardrails>`

## Context Motivation

Explain WHY a rule matters — Claude generalizes from the explanation better than from the rule alone.

## Remove Anti-Laziness Prompts

Claude 4.6 is already proactive. Instructions like "be thorough", "think carefully", "do not be lazy" cause over-execution and runaway thinking. Remove them.

## Soften Tool-Use Language

Replace "You MUST use [tool]" with "Use [tool] when it would enhance your understanding." Tools that under-triggered in older models now trigger appropriately.

## Don't Force Thinking

Remove "use the think tool to plan your approach" — Claude 4.6 thinks effectively without being told to. Forced thinking causes over-planning.

## Effort as Primary Control

If Claude is too aggressive after prompt cleanup, lower the `effort` parameter rather than adding prompt constraints.

## Parallel Tool Calling

Claude excels at parallel execution. Boost to ~100% with:
```xml
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the calls, make all independent calls in parallel.
</use_parallel_tool_calls>
```

## Overeagerness Prevention

Claude 4.6 tends to over-engineer. Add scope discipline:
```
Only make changes directly requested. No extra features, no refactoring, no "improvements" beyond what was asked.
```

## Hallucination Mitigation

```xml
<investigate_before_answering>
Never speculate about code you have not opened. Read the file before answering. Give grounded, hallucination-free answers.
</investigate_before_answering>
```

## Output Formatting

- Tell what to do instead of what not to do
- Use XML format indicators for output sections
- Match prompt style to desired output style

## No More Prefills

Claude 4.6 no longer supports prefilled assistant responses. Instead:
- Use direct instructions: "Respond directly without preamble."
- Use structured outputs or XML tags for format control
- Use tool calling for constrained outputs

## Vision

Give Claude a crop/zoom tool for image analysis — consistent uplift on image evaluations.
