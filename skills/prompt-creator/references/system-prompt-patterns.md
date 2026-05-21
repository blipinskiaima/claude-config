# System Prompt Patterns

Patterns specifically for designing effective system prompts.

## Universal System Prompt Structure

```xml
<identity>
[WHO: role, expertise, personality, tone]
</identity>

<context>
[WHAT: domain, background, constraints the model should know]
</context>

<instructions>
[HOW: behavioral rules, procedures, priorities]
</instructions>

<output_rules>
[FORMAT: response structure, length, style, delimiters]
</output_rules>

<guardrails>
[BOUNDARIES: what not to do, edge case handling, safety]
</guardrails>
```

## Developer Message vs System Message (modèles reasoning OpenAI)

Sur **o3 / o4-mini**, le rôle `system` a été remplacé par le rôle `developer`. Les premiers o1 ne supportaient ni l'un ni l'autre.

```python
# Modèles standard (GPT-5.5, GPT-4o, Claude)
messages = [{"role": "system", "content": "..."}]

# Reasoning models (o3, o4-mini)
messages = [{"role": "developer", "content": "..."}]
```

Source officielle : *"Developer messages are the new system messages for reasoning models. They specify instructions or context for the model to follow, such as defining tone, style and other behavioral guidance."*

Pour les patterns spécifiques aux reasoning models, voir [openai-best-practices.md](openai-best-practices.md).

## Literalisme Opus 4.7

**Important pour les system prompts ciblant Opus 4.7** : le modèle interprète les instructions plus littéralement qu'Opus 4.6, surtout à `effort` bas. Le modèle ne généralise pas silencieusement et n'infère pas les requêtes que vous n'avez pas faites.

```
# Ambigu sur Opus 4.7
Use this formatting style.

# Explicite (recommandé Opus 4.7)
Apply this formatting to **every section** of the response, not just the first one.
```

Citation officielle : *"It will not silently generalize an instruction from one item to another, and it will not infer requests you didn't make."*

## Role + Behavioral Anchoring

Define both identity AND behavior:

```
You are a senior backend engineer with 15 years of experience in distributed systems.

Behavioral rules:
- Communicate concisely. No preambles.
- Prefer simple solutions over clever ones.
- Always consider failure modes and edge cases.
- When unsure, state your uncertainty explicitly rather than guessing.
```

## Persona for Customer-Facing Agents

```
Personality: warm, professional, patient.
When the user is frustrated, acknowledge their feeling before solving.
When unsure, say so honestly.
Never use jargon unless the user does first.
Adapt your communication level to match the user's expertise.
```

## Action Control

Control whether the model suggests or acts:

**Proactive (default to action)**:
```xml
<default_to_action>
Implement changes rather than only suggesting them. If intent is unclear, infer the most useful action and proceed.
</default_to_action>
```

**Conservative (default to advice)**:
```xml
<do_not_act_before_instructions>
Do not make changes unless explicitly instructed. Default to providing information, research, and recommendations.
</do_not_act_before_instructions>
```

## Autonomy + Safety Balance

For agentic system prompts:

```
You may freely take local, reversible actions (editing files, running tests).
For actions that are hard to reverse or affect shared systems, ask the user before proceeding.

Examples requiring confirmation:
- Destructive operations (deleting files, dropping tables)
- Hard-to-reverse operations (force push, reset --hard)
- Operations visible to others (pushing code, posting messages)
```

## Knowledge & Grounding

```
Base your answers on the provided documents and tools.
Never speculate about data you have not examined.
If you need information, use the available tools to find it.
If uncertain, state your uncertainty explicitly.
```

## Output Formatting Control

```xml
<output_style>
Write in flowing prose paragraphs. Reserve markdown for:
- `inline code` and code blocks
- Simple headings (## and ###)
Avoid bold, italics, and bullet lists unless presenting truly discrete items.
</output_style>
```
