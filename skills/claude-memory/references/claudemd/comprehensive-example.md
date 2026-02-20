# Comprehensive CLAUDE.md Example

A complete, realistic example for a full-stack TypeScript project.

```markdown
# Acme Platform

## Overview
Acme Platform is a SaaS billing dashboard built with Next.js 15 (App Router) + tRPC + Prisma + PostgreSQL. Monorepo managed with Turborepo.

## Commands
- Install: `pnpm install`
- Dev: `pnpm dev` (starts Next.js + API on port 3000)
- Build: `pnpm build`
- Test: `pnpm test`
- Test single: `pnpm test -- --testPathPattern={path}`
- Lint: `pnpm lint`
- Type check: `pnpm typecheck`
- DB migrate: `pnpm db:migrate`
- DB seed: `pnpm db:seed`
- DB studio: `pnpm db:studio`

## Architecture
- `apps/web/` — Next.js frontend (App Router)
  - `app/` — Routes and layouts
  - `components/` — React components (colocated with routes when possible)
  - `lib/` — Client-side utilities and hooks
- `apps/api/` — tRPC API server
  - `routers/` — tRPC routers (one per domain)
  - `services/` — Business logic (pure functions, no framework deps)
  - `middleware/` — Auth, rate limiting, logging
- `packages/db/` — Prisma schema, migrations, client
- `packages/shared/` — Shared types, validation schemas (Zod)
- `packages/ui/` — Shared UI component library

## Code Style
- 2-space indentation, no semicolons
- Single quotes for strings
- Named exports only (no default exports)
- Imports ordered: external > @packages > relative
- Use `type` keyword for type-only imports
- Components: PascalCase files, one component per file
- Utilities: camelCase files and functions
- Constants: SCREAMING_SNAKE_CASE

## Patterns
- All business logic in services/ — routers are thin wrappers
- Validation with Zod schemas in packages/shared/ (shared client + server)
- Error handling: throw TRPCError with code and message
- DB queries: always use Prisma transactions for multi-step ops
- Auth: JWT in httpOnly cookie, validated in middleware
- Never use `any` — use `unknown` and narrow with type guards

## Testing
- Framework: Vitest
- Unit tests: `*.test.ts` colocated with source
- Integration tests: `tests/integration/`
- Use `createTestContext()` for DB fixtures
- Mock external services, never mock Prisma (use test DB)
- Min coverage: 80% for services/, not enforced elsewhere

## Git
- Branch: feature/JIRA-123-short-desc or fix/JIRA-456-short-desc
- Commit: feat(billing): add invoice generation
- Always rebase on main, squash in PR
- PR requires 1 approval + passing CI

## Important
- Never import from apps/api/ in apps/web/ — use packages/shared/
- The `billing` module has complex state machine logic — read services/billing/README.md first
- Legacy endpoints in apps/api/routers/v1/ are deprecated — don't add new ones
- Rate limiter uses Redis — ensure Redis is running for local dev (`docker compose up redis`)

## Environment
See @.env.example for required variables.
Local Postgres: port 5432 (docker compose up db)
Local Redis: port 6379 (docker compose up redis)
```
