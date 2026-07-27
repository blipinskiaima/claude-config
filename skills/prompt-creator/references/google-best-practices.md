# Google Best Practices (Gemini 3.x)

Techniques and recommendations specific to Gemini 3.x models.

## Directness Over Verbosity

Gemini 3 favors direct, concise prompts. Short prompts that state a clear goal outperform verbose ones.

## Always Include Few-Shot Examples

Google's own recommendation: always provide few-shot examples. 2-3 varied examples is the sweet spot. Too many causes overfitting.

**Spécificité Gemini — divergence assumée.** Google maintient explicitement *"we recommend to always include
few-shot examples in your prompts"* (doc `prompting-strategies`, juin 2026), là où Anthropic et OpenAI ont réduit
le poids du few-shot sur leurs modèles à raisonnement. Ne pas généraliser la doctrine « moins d'exemples » à Gemini.

## Verbosité

Gemini 3 est **moins verbeux par défaut** que la génération précédente. Si un ton conversationnel ou développé est
souhaité, il faut le demander explicitement — l'inverse du réflexe « demander d'être concis » utile ailleurs.

## Input/Output Prefixes

Label semantic parts explicitly for transformation tasks:

```
English: How are you?
French: Comment allez-vous?

English: {input}
French:
```

## Prompt Component Order

Google's recommended ordering:
1. Examples first
2. Context second
3. Input/question last

For long context: place all context first, questions at the end. Use bridging phrases: "Based on the information above..."

## Use Consistent Delimiters

Pick one structural format (XML tags, markdown) and stick with it throughout. Mixing formats confuses the model.

## Thinking Level (Gemini 3.x)

Gemini 3 remplace le budget de tokens de raisonnement par `thinking_level` : `minimal` / `low` / `medium` / `high`.
Défaut `high` sur Gemini 3.1 Pro et 3 Flash.

**Migration CoT → thinking_level.** Recommandation officielle : un prompt qui portait un échafaudage chain-of-thought
élaboré sur Gemini 2.5 doit être **simplifié** et confié à `thinking_level: high` — *"elaborate step-by-step
scaffolding often just adds noise"*. Même doctrine que chez Anthropic et OpenAI.

## Temperature Settings

⚠️ **Sur Gemini 3, garder la température à 1.0 et ne pas y toucher.** Descendre en dessous de 1.0 peut produire des
comportements inattendus — bouclage, performance dégradée. Retirer explicitement tout réglage de température hérité
d'un prompt Gemini 2.x, y compris sur les tâches factuelles ou déterministes où baisser la température était
auparavant le réflexe.

Source : [Gemini 3 Developer Guide](https://ai.google.dev/gemini-api/docs/gemini-3) — *"Changing the temperature
(setting it below 1.0) may lead to unexpected behavior, such as looping or degraded performance"*.

## Enhanced Reasoning

Request explicit planning:
```
Before answering, plan your approach. Then execute step by step. After drafting, self-critique and revise if needed.
```

## Structured Output

Specify format explicitly:
```
Return your answer as a JSON object with the following fields: ...
```

## Rephrase and Iterate

If results aren't good:
1. Try different wording for the same intent
2. Switch task analogies (e.g., reformulate as multiple-choice)
3. Reorder content (examples, context, input) and observe impact

## Grounding

- Add current date for time-sensitive queries
- State knowledge cutoff explicitly
- Restrict responses to provided context when needed

## Agentic Patterns (Gemini 3.x)

- Logical decomposition: analyze prerequisites and operation order
- Problem diagnosis: encourage abductive reasoning
- Risk assessment: distinguish exploratory vs state-change actions
- Adaptability: determine when to pivot vs persist
