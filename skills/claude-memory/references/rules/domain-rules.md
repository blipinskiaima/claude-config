# Domain Rules Examples

Ready-to-use rule file templates organized by domain.

## Frontend: React

```markdown
---
paths:
  - "src/components/**/*.tsx"
  - "src/app/**/*.tsx"
---

# React Component Rules

- One component per file, named export matching filename
- Use functional components with hooks (no class components)
- Props interface named {ComponentName}Props
- Colocate styles with component
- Extract hooks into src/hooks/ when reused
- Use React.memo only for measured performance bottlenecks
- Event handlers: handle{Event} naming (handleClick, handleSubmit)
```

## Frontend: Styles

```markdown
---
paths:
  - "**/*.css"
  - "**/*.scss"
  - "**/*.module.css"
---

# CSS / Styling Rules

- Use CSS Modules for component styles
- Tailwind for utility classes, custom CSS for complex layouts
- No inline styles except dynamic values
- Mobile-first responsive design
- Use CSS variables for theme values (--color-primary, --spacing-md)
```

## Backend: API

```markdown
---
paths:
  - "src/api/**/*"
  - "src/routes/**/*"
---

# API Rules

- RESTful resource naming: plural nouns (/users, /invoices)
- Always validate request input at the boundary
- Return consistent response format: { data, meta, errors }
- Use HTTP status codes correctly (201 for create, 204 for delete)
- Log all errors with request context (requestId, userId)
- Rate limit all public endpoints
```

## Backend: Database

```markdown
---
paths:
  - "src/models/**/*"
  - "prisma/**/*"
  - "src/db/**/*"
---

# Database Rules

- Always use migrations (never modify DB schema manually)
- Use transactions for multi-step operations
- Index foreign keys and frequently queried columns
- Soft delete by default (deletedAt column)
- Never use raw SQL without parameterized queries
- Name migrations descriptively: add_invoice_status_column
```

## Testing

```markdown
---
paths:
  - "**/*.test.*"
  - "**/*.spec.*"
  - "tests/**/*"
---

# Testing Rules

- Test behavior, not implementation details
- One assertion per test when possible
- Use descriptive test names: "should return 404 when user not found"
- Arrange-Act-Assert pattern
- Mock external dependencies, not internal modules
- Clean up test data after each test
```

## Security

```markdown
# Security Rules (no paths — applies everywhere)

- Never commit secrets, tokens, or passwords
- Never log sensitive data (passwords, tokens, PII)
- Validate and sanitize all user input
- Use parameterized queries for all database operations
- Escape output to prevent XSS
- Set secure headers (CSP, HSTS, X-Frame-Options)
- Never use eval() or Function() with user input
```

## Git

```markdown
# Git Rules (no paths — applies everywhere)

- Branch format: {type}/{ticket}-{description}
- Commit format: {type}({scope}): {description}
- Types: feat, fix, docs, refactor, test, chore, perf
- Never force push to main/master
- Always rebase on main before creating PR
- Squash commits when merging PR
- Delete branch after merge
```
