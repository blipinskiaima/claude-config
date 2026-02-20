# CLAUDE.md Section Templates

Copy and adapt the sections relevant to your project.

## Project Overview

```markdown
## Project Overview
{Project name} is a {type of app} built with {stack}.
It {main purpose} for {target users}.
Architecture: {pattern} (e.g., monorepo, microservices, monolith).
```

## Commands

```markdown
## Commands
- Install: `{package_manager} install`
- Dev: `{package_manager} run dev`
- Build: `{package_manager} run build`
- Test all: `{package_manager} test`
- Test single: `{package_manager} test -- {path}`
- Lint: `{package_manager} run lint`
- Lint fix: `{package_manager} run lint:fix`
- Type check: `{package_manager} run typecheck`
- DB migrate: `{command}`
- DB seed: `{command}`
```

## Architecture

```markdown
## Architecture
- `src/` — Application source code
  - `api/` — API routes and controllers
  - `services/` — Business logic
  - `models/` — Data models / entities
  - `utils/` — Shared utilities
- `tests/` — Test files (mirror src/ structure)
- `docs/` — Documentation
- `scripts/` — Build and deployment scripts
```

## Code Style

```markdown
## Code Style
- Indentation: {n} spaces
- Max line length: {n} characters
- Quotes: {single/double}
- Semicolons: {yes/no}
- Naming: {camelCase/snake_case} for variables, {PascalCase} for classes
- Imports: {ordering rules}
- No default exports (use named exports)
```

## Git Conventions

```markdown
## Git Conventions
- Branch format: {type}/{description} (e.g., feature/add-auth, fix/login-bug)
- Commit format: {type}({scope}): {description}
  Types: feat, fix, docs, refactor, test, chore
- Always rebase on main before merging
- Squash commits in PR
- Never force push to main
```

## Testing

```markdown
## Testing
- Framework: {jest/pytest/vitest/etc.}
- Run: `{command}`
- Naming: `{pattern}` (e.g., describe/it blocks, test_ prefix)
- Coverage minimum: {n}%
- Always write tests for new features
- Test edge cases and error paths
```

## Error Handling

```markdown
## Error Handling
- Use custom error classes extending {BaseError}
- Always include error code, message, and context
- Log errors with structured logging ({logger})
- Return consistent error format: `{ error: { code, message, details } }`
- Never expose internal errors to clients
```

## API Conventions

```markdown
## API Conventions
- RESTful endpoints: `/{resource}` (plural nouns)
- Versioning: {/api/v1/ prefix | header-based}
- Auth: {JWT/OAuth/API key} in {header/cookie}
- Response format: `{ data, meta, errors }`
- Pagination: cursor-based with `limit` and `after` params
- Rate limiting: {n} req/min per user
```

## Security

```markdown
## Security
- Never commit secrets — use environment variables
- Validate all user input at system boundaries
- Sanitize output to prevent XSS
- Use parameterized queries (no string concatenation for SQL)
- CORS: only allow {origins}
- Authentication required for all non-public endpoints
```

## Environment

```markdown
## Environment
- Node: {version} (see .nvmrc)
- Package manager: {npm/pnpm/yarn/bun}
- Required env vars: see .env.example
- Local DB: {postgres/mysql/sqlite} on port {n}
- Redis: port {n} (required for {feature})
```
