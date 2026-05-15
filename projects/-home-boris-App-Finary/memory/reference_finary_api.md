---
name: Finary API setup
description: How to connect to Finary API - MCP server config, auth method, available endpoints
type: reference
---

## Finary API Access

**Base URL:** https://api.finary.com
**Auth:** Email/password + TOTP MFA (via finary_uapi library)
**Credentials:** Stored in /home/boris/App/Finary/.env (FINARY_EMAIL, FINARY_PASSWORD)
**Session:** Cached in JWT file after signin, re-auth needed if expired

## MCP Server
- Located: /home/boris/App/Finary/finary_mcp/mcp_server.py
- Config: /home/boris/.mcp.json and /home/boris/App/Finary/.mcp.json
- Venv: /home/boris/App/Finary/.venv/
- Dependencies: fastmcp, finary-uapi, docopt, fuzzywuzzy, curl-cffi
- Note: MCP server may not auto-load in Claude Code — fallback to direct Python API calls

## Direct API usage (fallback)
```python
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path('/home/boris/App/Finary/.env'))
from finary_uapi.signin import signin
from finary_uapi.auth import prepare_session
result = signin(otp_code='CODE_TOTP')
session = prepare_session()
```

## Available endpoints (read-only):
- get_holdings_accounts(session) — all accounts
- get_portfolio_investments(session) — investment details with securities
- get_portfolio_cryptos(session) — crypto holdings
- get_user_real_estates(session) — real estate
- get_user_scpis(session) — SCPI
- get_user_fonds_euro(session) — euro funds

## NOT available via API:
- Budget/dépenses (web-only, not reverse-engineered)
- Community top ETFs (web-only)
- Security performance data for non-held securities
