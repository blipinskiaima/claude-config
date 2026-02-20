# Few-Shot Patterns

Providing examples is one of the most effective techniques across all models. Google explicitly recommends always including few-shot examples.

## Basic Pattern (2-3 examples)

```xml
<examples>
<example>
<input>I can't log in to my account</input>
<output>
Category: Account Access
Priority: High
Action: Reset password link sent, escalate if MFA issue
</output>
</example>
<example>
<input>The dashboard loads slowly</input>
<output>
Category: Performance
Priority: Medium
Action: Check server load, clear cache, monitor response times
</output>
</example>
</examples>

Now process this input:
<input>{user_message}</input>
```

## Key Rules

1. **Use 2-3 examples** — enough to show the pattern, not so many the model overfits
2. **Show only positive examples** — negative examples ("don't do this") can confuse the model (Google research)
3. **Every rule must appear in an example** — if a rule isn't demonstrated, the model may ignore it (OpenAI)
4. **Vary your examples** — cover different categories/edge cases, not just the easy path
5. **Keep formatting consistent** — all examples should use identical structure

## With Prefixes (Google Pattern)

Useful for translation, transformation, and classification tasks:

```
English: How are you?
French: Comment allez-vous?

English: What time is it?
French: Quelle heure est-il?

English: {input}
French:
```

## Complex Output Format

When the output is structured, show the full expected structure:

```xml
<example>
<input>
Company: Acme Corp
Revenue: $50M (2024)
Growth: 15% YoY
</input>
<output>
{
  "company": "Acme Corp",
  "revenue_usd": 50000000,
  "year": 2024,
  "growth_rate": 0.15,
  "assessment": "Strong growth trajectory, above industry average"
}
</output>
</example>
```

## Edge Case Examples

Include at least one example showing how to handle missing or ambiguous data:

```xml
<example>
<input>Some company mentioned revenue growth</input>
<output>
{
  "company": null,
  "revenue_usd": null,
  "year": null,
  "growth_rate": null,
  "assessment": "Insufficient data to extract structured fields"
}
</output>
</example>
```
