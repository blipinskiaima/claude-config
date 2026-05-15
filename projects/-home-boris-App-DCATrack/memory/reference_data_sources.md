---
name: Data sources évalués (mai 2026)
description: Comparatif gratuit/légal pour prix d'ETF EU + verdict final pour DCATrack — Alpha Vantage = seule alternative légale viable, justETF accepté pour POC
type: reference
originSessionId: e464ea0f-682f-4446-bef2-c9cc5a8e2767
---
## Verdict final

| Source | Coût | Légal prog. | Couverture EU ETF | État DCATrack |
|---|---|---|---|---|
| **justETF** (actuel) | gratuit | ⚠️ zone grise (TOS interdit scraping) | excellente | **utilisé en prod** pour POC perso |
| **Alpha Vantage** free | gratuit | ✅ TOS OK | EU OK via `.PAR` / `.FRK` | **clé en .env.local**, prêt à basculer |
| Twelve Data free | gratuit | ✅ | ❌ EU gated derrière plan Grow $79/mo | disqualifié |
| EODHD All World | 19.99€/mo | ✅ | excellente | option payante future si projet grossit |
| Yahoo / yfinance | gratuit | ❌ TOS interdit explicitement | excellente | disqualifié |
| FMP / Tiingo / Polygon free | gratuit | ✅ | US only | disqualifiés |
| Marketstack free | gratuit | ✅ | EU OK | 100 req/mois — trop peu |

## Détails Alpha Vantage (validé sur les 9 ETF historiques)

- Free tier : **5 req/min, 25 req/jour**
- Suffix exchange : `.PAR` (Euronext Paris), `.FRK` (Frankfurt), `.LSE`, `.DEX` (Xetra)
- Endpoint catalogue : `SYMBOL_SEARCH?keywords=PUST` → `bestMatches[]`
- Endpoint prix : `TIME_SERIES_DAILY?symbol=PUST.PAR&outputsize=full` → 20+ ans d'historique en 1 call
- Validé sur PUST (FR0011871110) → `PUST.PAR` en EUR ✓ et 8 autres ETFs

**Stratégie d'usage si on bascule** : 1 call = full history d'1 ETF. Pour 28 ETF en daily refresh = bust le quota. Solution : refresh uniquement les ETF effectivement utilisés (~25 actifs), backfill on-demand quand un user en ajoute un nouveau.

## Détails justETF (encore utilisé)

- Endpoint : `https://www.justetf.com/api/etfs/{ISIN}/performance-chart`
- Headers nécessaires : User-Agent Chrome + Referer/Origin = justetf.com
- Cache Next.js `revalidate: 3600` + tags `etf-{isin}` (invalidable via Server Action `refreshETFs()`)
- `app/lib/justetf.ts` → `fetchJustETF(isin)` retourne `{ series, latestQuote, latestQuoteDate }`
- Validé pour les 28 ETF du catalogue (sauf EWLD FR0011869353 figé en 2024-03-15, probablement retiré)

## Décision Boris

Boris a explicitement demandé "100% légal et gratuit" mais après recherche a accepté de garder justETF pour ce POC perso. **À surveiller** : si l'app gagne des users hors cercle perso, basculer sur Alpha Vantage (gratuit) ou EODHD (20€/mo) pour rester clean.

## Catalogue ETF (métadonnées)

Pas d'API utilisée — les 28 ETF sont **hardcodés** dans `app/lib/etfs.ts:WATCHLIST`. Les sources publiques (issuers iShares/Amundi/BNP CSV, ESMA FIRDS) ont toutes été testées mais leurs API/CSV publics interdisent l'usage automatisé en TOS. Solution = curation manuelle.
