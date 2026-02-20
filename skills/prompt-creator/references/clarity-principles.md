# Clarity Principles

Core principles that apply to every prompt regardless of model or use case.

## Be Explicit, Not Implicit

Models follow literal instructions. Say exactly what you want.

```
# Bad
Create an analytics dashboard

# Good
Create an analytics dashboard with user growth, revenue trends, and churn rate charts. Include date range filtering and export to CSV.
```

## Explain WHY, Not Just WHAT

Context motivation helps the model generalize correctly (Anthropic).

```
# Bad
NEVER use ellipses

# Good
Your response will be read aloud by a text-to-speech engine, so never use ellipses since the engine cannot pronounce them.
```

## One Instruction Per Sentence

Compound instructions get partially ignored. Break them up.

```
# Bad
Summarize the article and extract key entities and classify sentiment

# Good
1. Summarize the article in 3 sentences.
2. Extract all named entities (people, companies, locations).
3. Classify the overall sentiment as positive, neutral, or negative.
```

## Tell What TO Do, Not Just What NOT To Do

Positive framing is more reliable than negative constraints alone.

```
# Bad
Do not use markdown in your response

# Good
Write your response as flowing prose paragraphs without any formatting.
```

## Use Concrete Constraints

Vague limits produce inconsistent results.

```
# Bad
Keep it concise

# Good
Maximum 5 bullet points, each under 15 words.
```

## Match Prompt Style to Output Style

The formatting you use in the prompt influences the response. If you want minimal markdown output, minimize markdown in your instructions. If you want prose, write your prompt in prose.
