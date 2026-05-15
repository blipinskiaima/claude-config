---
name: justETF performance chart endpoint
description: Endpoint JSON non documenté justETF utilisé par DCATrack pour récupérer l'historique de prix
type: reference
---

**Endpoint** :
```
GET https://www.justetf.com/api/etfs/{ISIN}/performance-chart
   ?locale=en
   &valuesType=MARKET_VALUE
   &reduceData=false
   &includeDividends=false
   &features=DIVIDENDS
   &currency=EUR
```

**Headers REQUIS** (sinon bloqué) :
```
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ...
Accept: application/json, text/plain, */*
Referer: https://www.justetf.com/
```

**Shape de la réponse** :
```json
{
  "latestQuote": {"raw": 93.2, "localized": "93.20"},
  "latestQuoteDate": "2026-04-29",
  "series": [
    {"date": "2014-05-20", "value": {"raw": 10, "localized": "10.00"}},
    ...
  ],
  "performance": {...},
  "features": {...}
}
```

⚠️ **`value` est wrappé en `{raw, localized}`** — pas un nombre brut. La fonction `unwrap()` dans `app/lib/justetf.ts` gère les deux formats.

**Volume de données** : ~4000+ jours d'historique journalier depuis l'inception de l'ETF (10+ ans pour les vieux). Filtrer côté client si besoin.

**Rate limit observé** : 1 req par ETF par heure (cache ISR Next.js) suffit largement, aucun ban observé.

**Fallback prêt si bannissement** : Yahoo Finance avec ticker Euronext `.PA` (`PUST.PA`, `ETSZ.PA`, `PAEEM.PA`) via `https://query1.finance.yahoo.com/v8/finance/chart/{ticker}`.

**Sources** :
- Reverse-engineered depuis `https://github.com/druzsan/justetf-scraping`
- Stable depuis plusieurs années dans plusieurs projets open source
