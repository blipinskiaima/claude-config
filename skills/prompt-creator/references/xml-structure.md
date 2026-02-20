# XML Structure Patterns

XML tags are the most effective way to structure prompts, especially for Claude. They create clear boundaries between sections and prevent instruction bleed.

## Basic Section Tags

```xml
<role>You are a senior security engineer specializing in web applications.</role>

<context>
The user is submitting code for a production deployment.
The codebase uses Python 3.12 with FastAPI.
</context>

<task>Review the code for security vulnerabilities, focusing on OWASP top 10.</task>

<rules>
- Flag every vulnerability with severity (Critical/High/Medium/Low)
- Provide a fix for each issue
- If no vulnerabilities found, state that explicitly
</rules>
```

## Input/Output Wrapping

Clearly separate user data from instructions:

```xml
<input>{user_provided_content}</input>

<output_format>
Return a JSON object with fields: summary, findings[], recommendation
</output_format>
```

## Examples in XML

```xml
<examples>
<example>
<user_input>The app crashes on login</user_input>
<expected_output>Category: Bug | Priority: High | Component: Auth</expected_output>
</example>
<example>
<user_input>Add dark mode support</user_input>
<expected_output>Category: Feature | Priority: Medium | Component: UI</expected_output>
</example>
</examples>
```

## Document Embedding

For long-context prompts with multiple documents:

```xml
<documents>
<doc id="1" title="Q3 Report" source="finance">
{document_content}
</doc>
<doc id="2" title="Product Roadmap" source="engineering">
{document_content}
</doc>
</documents>

<task>Based on the documents above, identify alignment gaps between finance goals and product roadmap.</task>
```

## Nesting for Complex Prompts

```xml
<system>
<identity>You are a code review assistant.</identity>
<constraints>
<scope>Only review the changed files</scope>
<style>Match existing codebase conventions</style>
<forbidden>Do not refactor unchanged code</forbidden>
</constraints>
</system>
```

## When to Use XML vs Markdown vs JSON

| Format | Best For | Avoid For |
|---|---|---|
| XML tags | Claude, long context, nested structure | Short simple prompts |
| Markdown headings | GPT models, hierarchical docs | Deep nesting |
| JSON | Structured output schemas | Wrapping long documents (degrades perf) |
