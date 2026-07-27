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

## Adaptive Thinking + Effort Param (famille Claude 5)

Sur la famille Claude 5, le raisonnement interne est contrôlé par le paramètre `effort` plutôt que par des prompts CoT explicites. `budget_tokens` est **supprimé** (erreur 400).

```python
# Au lieu d'écrire "think step by step" dans le prompt :
output_config={"effort": "high"}    # max | xhigh | high | medium | low
thinking={"type": "adaptive"}       # actif par défaut si omis sur Opus 5 / Fable 5
```

Valeurs `effort` (les cinq niveaux sont disponibles sur toute la famille 5) :
- `max` — pas de contrainte sur la profondeur, réservé au correctness-over-cost
- `xhigh` — coding et agentic les plus durs
- `high` — défaut de l'API, minimum pour tout travail intelligence-sensitive
- `medium` — compromis coût/qualité
- `low` — sous-agents, tâches courtes et cadrées

⚠️ **Sur Opus 5, `low` et `medium` sont anormalement forts** — souvent au niveau du `xhigh` des générations précédentes. Démarrer haut puis balayer vers le bas sur ses propres evals ; les valeurs héritées d'un modèle antérieur ne se transposent pas.

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

> ⚠️ **Ne PAS appliquer à la famille Claude 5.** Opus 5 vérifie déjà son propre travail spontanément ; lui demander de se relire produit de la **sur-vérification** sans gain de capacité. C'est une inversion assumée d'une best practice par ailleurs saine — voir [anthropic-best-practices.md](anthropic-best-practices.md) § « Supprimer les instructions de vérification ». Les deux sections ci-dessous restent valables sur Gemini et GPT.

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
- **Famille Claude 5** — le thinking est adaptatif et actif par défaut (toujours actif sur Fable 5). Utiliser `effort` plutôt que des instructions CoT manuelles.

**Pas de CoT non plus pour** :
- Classification ou lookup simples — ajoute de la latence sans bénéfice
- Tâches déjà bien définies — la famille Claude 5 et GPT-5.x raisonnent déjà efficacement par défaut

**Cas particulier — Claude 5 avec thinking désactivé** : ne pas écrire « ne raisonne pas » / « ne réfléchis pas » pour limiter la sortie. Sur Opus 5 cette consigne **augmente** la fuite de balises `<thinking>` dans la réponse visible. Préférer thinking activé à `low`/`medium`.

Voir [openai-best-practices.md](openai-best-practices.md) pour la distinction reasoning vs standard models et [anthropic-best-practices.md](anthropic-best-practices.md) pour l'utilisation détaillée du paramètre `effort`.
