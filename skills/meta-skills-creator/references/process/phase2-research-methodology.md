# Phase 2: Research Methodology

## Search Strategy

### Parallel Searches (3+ simultaneous)
Launch multiple web searches in parallel to maximize coverage:

```
Search 1: "{topic} official documentation best practices 2025 2026"
Search 2: "{topic} guide techniques {provider} 2026"
Search 3: "{topic} configuration setup {tool/framework}"
```

### Source Priority
1. **Official documentation** (always primary source)
2. **Official engineering blogs** (Anthropic, OpenAI, Google engineering posts)
3. **Official cookbooks/guides** (GitHub repos from the provider)
4. **Community guides** (only for patterns not in official docs)

### Fetch Strategy
After search results arrive:
1. Identify the 3-4 most authoritative URLs
2. Fetch them in parallel with targeted prompts
3. Extract specific techniques, configurations, examples
4. Handle redirects (301/308) by re-fetching the new URL

## Extraction Prompts

Use specific extraction prompts when fetching:

```
Good: "Extract ALL configuration fields with their types and descriptions"
Bad: "Tell me about this page"
```

The more specific the extraction prompt, the better the data quality.

## Synthesis

After collecting data:

1. **Deduplicate** — remove overlapping information across sources
2. **Organize by topic** — group findings by the sub-folders identified in Phase 1
3. **Verify completeness** — check each planned reference file has enough material
4. **Identify gaps** — if a topic lacks sufficient official docs, note it

## What to Include vs. Exclude

### Include in References
- Specific configurations, fields, syntax (Claude doesn't memorize these)
- Official best practices and recommendations
- Patterns with concrete examples
- Anti-patterns and common mistakes
- Version-specific behavior (model-specific tips)

### Exclude from References
- General programming knowledge (Claude already knows)
- Framework basics (unless project-specific)
- Obvious advice ("be clear", "test your code")
- Long theoretical explanations without actionable content

## Research Quality Checklist

- [ ] Used 3+ parallel searches
- [ ] Consulted official documentation (not just blog posts)
- [ ] Fetched and extracted from primary sources
- [ ] All claimed best practices traceable to a source
- [ ] No speculative or unverified content
