# Context Management

Techniques for handling long documents, multiple sources, and context window limits.

## Long-Context Re-Grounding (OpenAI)

For inputs exceeding ~10k tokens, force the model to anchor to source material:

```
Before answering:
1. Summarize the relevant sections from the provided documents
2. Re-state the user's constraints
3. Anchor all claims to specific document sections with references
```

## Instruction Placement (OpenAI)

For long-context prompts, place critical instructions at BOTH the beginning AND end.

```
<critical_instructions>
Answer only based on the provided documents. Cite sources.
</critical_instructions>

<documents>
{...10k+ tokens of content...}
</documents>

<reminder>
Remember: answer only based on the documents above. Cite sources for every claim.
</reminder>
```

If only one placement: before context outperforms after.

## Progressive Disclosure (Anthropic)

Don't dump everything upfront. Structure context so the model loads detail as needed:

```
Start with <summary> for the overview.
Refer to <detailed_spec> only for implementation details.
Consult <edge_cases> only if the main path doesn't cover the scenario.
```

## Context Reliance Tuning (OpenAI)

Specify whether the model should stick to provided context or supplement with knowledge.

**Strict (closed-book)**:
```
Answer ONLY based on the documents provided. If the answer isn't in the documents, say "Not found in provided context."
```

**Flexible (open-book)**:
```
Use the provided documents as primary sources. Supplement with general knowledge only when documents are insufficient, and clearly mark which parts come from your knowledge.
```

## Document Formatting for Long Context

Performance by format (OpenAI research):
1. **XML tags** — best performance for long context
2. **Pipe-delimited** (`ID: 1 | TITLE: x | CONTENT: y`) — compact, good performance
3. **Markdown** — good general purpose
4. **JSON** — avoid for long context (degrades retrieval performance)

## Multi-Context Window Workflows (Anthropic)

For tasks spanning multiple sessions:

```
Before ending a session:
1. Save progress to progress.md
2. List remaining tasks in todo.md
3. Commit work with a descriptive message

When starting a new session:
1. Read progress.md and todo.md
2. Review recent git log
3. Run tests to verify current state
4. Continue from where you left off
```

## Bridging Phrases (Google)

When placing questions after long context, use explicit bridges:

```
Based on the information provided above, answer the following:
```
