# Prompting Techniques for CLAUDE.md

How to write effective instructions in memory files.

## Be Specific, Not Vague

```markdown
# Bad
- Format code properly
- Write good tests
- Handle errors

# Good
- Use 2-space indentation, max 100 char lines
- Every new function needs a unit test with at least 2 assertions
- Throw AppError with code and message, log with structured logger
```

## Use Bullet Points, Not Prose

Memory files are reference material, not documentation. Bullet points are faster to parse.

```markdown
# Bad
When writing code for this project, you should make sure to use TypeScript
and ensure that all types are properly defined. It's important that we
don't use the any type and instead prefer unknown with proper type guards.

# Good
- Use strict TypeScript (no `any`)
- Prefer `unknown` with type guards over `any`
- Define explicit return types on exported functions
```

## Group by Topic

```markdown
## Testing
- Framework: Vitest
- Run: `pnpm test`
- Coverage: min 80% for services/

## API Design
- REST, plural resource names
- Validate input with Zod at boundaries
- Return `{ data, meta, errors }` format
```

## Include Commands

Claude frequently needs to run commands. Put them where they're easy to find:

```markdown
## Commands
- Dev: `pnpm dev`
- Test: `pnpm test`
- Lint: `pnpm lint`
- Type check: `pnpm typecheck`
```

## Use Imports for Large Content

Don't bloat CLAUDE.md with content that's already documented elsewhere:

```markdown
## References
- API docs: @docs/api.md
- Database schema: @prisma/schema.prisma
- Architecture: @docs/architecture.md
```

## Explain WHY When It's Not Obvious

```markdown
## Conventions
- Always use cursor-based pagination
  (offset pagination breaks when data changes between pages)
- Never import from apps/api/ in apps/web/
  (creates circular dependency in monorepo build)
```

## Use Conditional Instructions

```markdown
## Error Handling
- In API routes: return structured error response with HTTP status
- In services: throw typed AppError (let route handle HTTP mapping)
- In utils: return null or throw — document which approach in JSDoc
```

## Keep Memory Files Updated

As your project evolves:
- Remove instructions for deprecated patterns
- Update commands when they change
- Add new conventions as they emerge
- Review periodically with `/memory`

## Token Budget Awareness

All loaded memory files share the same context window. Keep the total lean:
- CLAUDE.md: aim for under 100 lines
- Each rule file: aim for under 50 lines
- MEMORY.md: hard limit of 200 lines (only first 200 loaded)
- Total across all files: be mindful of cumulative impact
