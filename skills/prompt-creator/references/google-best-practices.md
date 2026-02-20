# Google Best Practices (Gemini 3)

Techniques and recommendations specific to Gemini 3.x models.

## Directness Over Verbosity

Gemini 3 favors direct, concise prompts. Short prompts that state a clear goal outperform verbose ones.

## Always Include Few-Shot Examples

Google's own recommendation: always provide few-shot examples. 2-3 varied examples is the sweet spot. Too many causes overfitting.

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

## Temperature Settings

- Keep default 1.0 for Gemini 3 (recommended by Google)
- Lower (near 0) for deterministic/factual tasks only
- Higher for creative tasks

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

## Agentic Patterns (Gemini 3)

- Logical decomposition: analyze prerequisites and operation order
- Problem diagnosis: encourage abductive reasoning
- Risk assessment: distinguish exploratory vs state-change actions
- Adaptability: determine when to pivot vs persist
