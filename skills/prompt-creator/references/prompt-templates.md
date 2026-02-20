# Prompt Templates

Ready-to-use scaffolds for common prompt types. Copy and adapt.

## Template 1: Classification / Extraction

```xml
<role>You are a {domain} specialist.</role>

<task>Classify the following input into one of these categories: {categories}.</task>

<rules>
- Choose exactly one category
- If uncertain, pick the closest match and note your confidence
- If the input doesn't fit any category, use "Other" and explain
</rules>

<examples>
<example>
<input>{example_input_1}</input>
<output>{expected_output_1}</output>
</example>
<example>
<input>{example_input_2}</input>
<output>{expected_output_2}</output>
</example>
</examples>

<input>{actual_input}</input>
```

## Template 2: Analysis / Research

```xml
<role>You are a {domain} analyst.</role>

<context>{background_information}</context>

<task>{specific_analysis_question}</task>

<instructions>
1. Analyze the provided data step by step
2. Identify key findings
3. Note any limitations or gaps in the data
4. Provide actionable recommendations
</instructions>

<output_format>
## Summary (2-3 sentences)
## Key Findings (max 5 bullets)
## Limitations
## Recommendations
</output_format>

<data>{input_data}</data>
```

## Template 3: Code Generation

```xml
<role>You are a senior {language} developer.</role>

<context>
Codebase: {framework/stack}
Style: {conventions, patterns}
</context>

<task>{what_to_build_or_fix}</task>

<constraints>
- Follow existing codebase conventions
- No unnecessary abstractions
- Only change what's needed
- Include error handling at system boundaries only
</constraints>

<output_format>
Provide the code with brief inline comments only where logic isn't self-evident.
</output_format>
```

## Template 4: Agent System Prompt

```xml
<identity>
You are {agent_role}. You {key_behavior}.
</identity>

<tools>
You have access to: {tool_list}
Always use tools to gather information. Never guess.
</tools>

<workflow>
1. Understand the user's request
2. Plan your approach (state it briefly)
3. Execute using available tools
4. Verify results
5. Report outcome concisely
</workflow>

<rules>
- Keep working until the task is fully resolved
- If blocked, try alternative approaches before asking the user
- Make independent tool calls in parallel when possible
- Provide 1-2 sentence status updates only at major milestones
</rules>

<guardrails>
- Ask before destructive or irreversible actions
- Never fabricate data or tool outputs
- State uncertainty explicitly when applicable
</guardrails>
```

## Template 5: Content Generation

```xml
<role>You are a {content_type} writer with expertise in {domain}.</role>

<task>Write a {content_type} about {topic}.</task>

<audience>{target_audience}</audience>

<tone>{desired_tone}: {2-3 adjectives}</tone>

<constraints>
- Length: {word/sentence count}
- Style: {specific style requirements}
- Avoid: {things to not include}
</constraints>

<structure>
{expected_sections_or_format}
</structure>
```

## Template 6: Data Extraction (Structured Output)

```xml
<task>Extract structured data from the following text.</task>

<schema>
{
  "field_name": "type | null",
  "other_field": "type"
}
</schema>

<rules>
- Set missing fields to null. Never guess values.
- Include "source_text" field with the exact sentence each value was extracted from.
- If the text contains no extractable data, return an empty object with null fields.
</rules>

<examples>
<example>
<input>{example_text}</input>
<output>{example_json}</output>
</example>
</examples>

<input>{actual_text}</input>
```
