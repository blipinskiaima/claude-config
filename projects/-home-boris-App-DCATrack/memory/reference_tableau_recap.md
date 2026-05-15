---
name: Tableau récap & tableau PEA
description: Vocabulaire Boris pour les tableaux d'ETF dans app/lib/etfs.ts — WATCHLIST = 28 ETF (catalogue complet), PEA_PRESET = 3 ISINs PEA actif
type: reference
originSessionId: e464ea0f-682f-4446-bef2-c9cc5a8e2767
---
Boris parle en **2 tableaux** dans `app/lib/etfs.ts` :

- **Tableau récap** = `WATCHLIST` — **28 ETF UCITS** au total :
  - 9 marqués `favori: true` par défaut (PUST, ETSZ, PAEEM, PSP5, CW8, WPEA, SPEA, LQQ, BNKE)
  - 19 marqués `favori: false` (catalogue étendu, hors favoris par défaut) :
    - 6 du portefeuille perso : PE500, CAC, EWLD, UST, VUSA, HMWO
    - 13 du top Finary communauté + variantes : ESE, DCAM, SXR8, MWRD, AEEM, AMUS, EUNL, CACC, EWLDD, WLD, PAASI, MAGR, PCEU
- **Tableau PEA** = `PEA_PRESET` (3 ISINs du PEA actif : PUST, ETSZ, PAEEM, hors CW8).
- **Favoris user-curated** = table Supabase `user_favorites` (PK user_id+isin), gérée via `/favoris` avec barre de recherche. La constante `FAVORITES_PRESET` (= ETF avec `favori: true`) sert seulement de défaut implicite.

Le reste (`DEFAULT_FAVORITES`, `ETFS`, `ETF_BY_ISIN`, `ETF_BY_TICKER`) = plomberie/alias.

**How to apply:** quand Boris parle de "tableau récap" → WATCHLIST (28 ETF) ; "tableau PEA" → PEA_PRESET (3 ISIN). "Favoris" peut signifier (a) le preset historique des 9 ETF, ou (b) la liste user-curated dans Supabase — préciser selon contexte.
