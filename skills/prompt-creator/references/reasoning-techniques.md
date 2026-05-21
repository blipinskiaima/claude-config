# Reasoning Techniques

Techniques to improve model reasoning quality on complex tasks.

## Chain-of-Thought (CoT)

Ask the model to reason step by step before answering.

```
Analyze this problem step by step:
1. Identify the key variables
2. Consider edge cases
3. Formulate your solution
4. Verify against the requirements
Then provide your final answer.
```

**When to use**: complex reasoning, math, multi-step logic, debugging.
**When to skip**: simple lookups, factual questions, models with built-in reasoning (GPT o-series, Claude with adaptive thinking).

## Adaptive Thinking + Effort Param (Claude 4.6+)

Sur Claude Sonnet 4.6 et Opus 4.7, le raisonnement interne est contrôlé par le paramètre `effort` plutôt que par des prompts CoT explicites.

```python
# Au lieu d'écrire "think step by step" dans le prompt :
output_config={"effort": "high"}    # max | xhigh | high | medium | low
thinking={"type": "adaptive"}
```

Valeurs `effort` :
- `max` — pas de contrainte sur la profondeur
- `xhigh` — exploration étendue (Opus 4.7 uniquement)
- `high` — raisonnement profond (défaut, recommandé pour code/agentic)
- `medium` — équilibré, skip thinking sur queries simples
- `low` — rapide, skip thinking sur tâches simples

Pour les détails complets, voir [anthropic-best-practices.md](anthropic-best-practices.md).

## Scratchpad (Anthropic)

Give the model a workspace for intermediate reasoning:

```
Use a <scratchpad> to work through your analysis. Show your intermediate steps there, then provide the final answer outside the scratchpad.
```

## Planning Before Action (OpenAI)

For agentic workflows, require the model to plan explicitly:

```
Before each action, briefly state:
1. What you know so far
2. What you need to find out next
3. Your planned next step and why
```

## Self-Critique (Google)

Ask the model to evaluate and revise its own output:

```
After drafting your response:
1. Check for unstated assumptions
2. Verify claims are grounded in provided data
3. Look for gaps or missing perspectives
Revise if needed, then deliver the final version.
```

## Self-Check Loop (OpenAI)

For high-stakes domains (legal, financial, medical):

```
Before finalizing your answer:
1. Scan for unstated assumptions
2. Check for ungrounded numbers or statistics
3. Verify claims against the provided sources
4. Soften overly strong language where appropriate
```

## Structured Reasoning (Google)

Three-phase approach for research and analysis tasks:

```
Phase 1 — Query Analysis: Break down what's being asked
Phase 2 — Evidence Gathering: Rate each source as [high/medium/low/none] relevance
Phase 3 — Synthesis: Combine findings into a coherent answer with citations
```

## When NOT to Force Reasoning

**Pas de "think step by step" sur ces modèles** :
- **OpenAI o-series** (o3, o4-mini) — raisonnement interne natif. Recommandation officielle : *"prompting them to 'think step by step' is unnecessary."*
- **Claude avec adaptive thinking** — utiliser `effort: high` (ou `xhigh` sur Opus 4.7) plutôt que des instructions CoT manuelles.

**Pas de CoT non plus pour** :
- Classification ou lookup simples — ajoute de la latence sans bénéfice
- Tâches déjà bien définies — Claude 4.6+ et GPT-5.x raisonnent déjà efficacement par défaut

Voir [openai-best-practices.md](openai-best-practices.md) pour la distinction reasoning vs standard models et [anthropic-best-practices.md](anthropic-best-practices.md) pour l'utilisation détaillée du paramètre `effort`.
