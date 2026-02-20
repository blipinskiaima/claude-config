---
name: prompt-creator
description: Expert prompt engineering for creating effective prompts for Claude, GPT, Gemini, and other LLMs. Use when writing system prompts, user prompts, agent prompts, few-shot examples, or optimizing existing prompts for better performance. Covers all major prompting methodologies including clarity, structure, XML tags, examples, reasoning, chaining, and advanced patterns.
---

<objective>
Create highly effective prompts using proven techniques from Anthropic (Claude 4.6), OpenAI (GPT-5.2), and Google (Gemini 3) research. Every prompt created should be clear, specific, and optimized for the target model.

This skill covers all major prompting methodologies: clarity, structure, examples, reasoning, and advanced patterns.
</objective>

<workflow>

## Step 1: Gather Requirements

Before writing, clarify with the user:
- **Target model**: Claude, GPT, Gemini, or model-agnostic?
- **Use case**: system prompt, user prompt, agent prompt, chain, or template?
- **Goal**: what should the prompt accomplish?
- **Constraints**: length, format, tone, language?

If the user hasn't specified, ask 1-2 focused questions. Don't over-ask.

## Step 2: Select Structure & Techniques

Choose the right scaffold and techniques based on the use case. Consult the appropriate reference files:

| Need | Reference File |
|---|---|
| Core writing principles | [clarity-principles.md](references/clarity-principles.md) |
| XML tag patterns | [xml-structure.md](references/xml-structure.md) |
| Few-shot examples | [few-shot-patterns.md](references/few-shot-patterns.md) |
| Chain-of-thought, reasoning | [reasoning-techniques.md](references/reasoning-techniques.md) |
| Long context, grounding | [context-management.md](references/context-management.md) |
| System prompt design | [system-prompt-patterns.md](references/system-prompt-patterns.md) |
| Ready-to-use scaffolds | [prompt-templates.md](references/prompt-templates.md) |
| Claude-specific tips | [anthropic-best-practices.md](references/anthropic-best-practices.md) |
| GPT-specific tips | [openai-best-practices.md](references/openai-best-practices.md) |
| Gemini-specific tips | [google-best-practices.md](references/google-best-practices.md) |
| What to avoid | [anti-patterns.md](references/anti-patterns.md) |

## Step 3: Build the Prompt

Apply these universal principles (always):
- Be explicit and specific — never assume the model will infer intent
- Use clear delimiters (XML tags or markdown headings) to separate sections
- Match prompt formatting style to desired output style
- Define success criteria in the prompt itself

Apply these selectively (when relevant):
- **Few-shot examples** for classification, extraction, formatting
- **Chain-of-thought** for reasoning, math, multi-step logic
- **Self-check loops** for high-stakes outputs
- **Scope discipline** to prevent over-engineering
- **Persona anchoring** for consistent tone

## Step 4: Review & Refine

Self-check before delivering:

1. **Clarity**: Could someone unfamiliar with the task follow these instructions?
2. **Ambiguity**: Are there instructions that could be interpreted multiple ways?
3. **Completeness**: Does the prompt define success criteria?
4. **Conciseness**: Can any section be cut without losing meaning?
5. **Example alignment**: Do examples demonstrate ALL the rules stated?

## Step 5: Deliver

Present to the user:
- The complete prompt, ready to copy-paste
- A brief note on which techniques were applied and why
- Suggestions for iteration if relevant

</workflow>
