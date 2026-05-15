---
name: No credentials leak
description: Never expose passwords, API keys, tokens, or any credentials in code, config, logs, or conversation
type: feedback
---

NEVER leak any credentials (passwords, emails, API keys, tokens, session cookies) in code, config files, logs, or conversation output.

**Why:** User's explicit golden rule for this project. Finary credentials are sensitive financial data.

**How to apply:**
- Always use environment variables or secure credential stores for auth
- Never hardcode credentials in source files
- Never print/log credentials
- Use .env files with .gitignore protection
- Review all code before committing for accidental credential exposure
