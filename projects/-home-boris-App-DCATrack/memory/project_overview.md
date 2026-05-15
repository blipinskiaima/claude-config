---
name: DCATrack project overview
description: POC perso d'indicateur DCA timing — catalogue 28 ETF UCITS, allouable réel en parts entières, auth multi-user via Vercel + Supabase
type: project
originSessionId: e464ea0f-682f-4446-bef2-c9cc5a8e2767
---
**DCATrack** — POC perso multi-user (Boris + invités).

**Objectif** : Répondre à "Aujourd'hui, est-ce un bon jour pour faire mon DCA mensuel sur cet ETF ?" + planifier l'allocation en parts entières.

**Catalogue** : 28 ETF UCITS dans `WATCHLIST` (`app/lib/etfs.ts`).
- 9 marqués `favori: true` par défaut (les ETF historiques)
- 19 marqués `favori: false` (catalogue étendu : 6 du portefeuille perso de Boris + 13 du top Finary communauté)
- L'utilisateur curate ses favoris via `/favoris` (table Supabase `user_favorites`)

**Sources de données** :
- **justETF** pour les prix (zone grise légale, accepté pour POC perso)
- **Alpha Vantage free tier** validé (25 req/jour) comme alternative légale future
- Catalogue ETF métadonnées = hardcodé dans `etfs.ts` (pas de scraping)

**Backend** : Supabase (auth + tables `dca_profiles`, `dca_executions`, `user_favorites`).

**Stack** : Next.js 16 (App Router) + TypeScript + Tailwind v4 + Recharts + Supabase SSR + lucide-react.

**Auth** : double couche — Basic Auth HTTP (env `BASIC_AUTH_CREDS` format `user1:pass1,user2:pass2,...`) + session Supabase.

**Repo** : `/home/boris/App/DCATrack` → `git@github.com:Lipinski-B/DCATrack.git` → Vercel auto-deploy.

**Why:** Boris fait du DCA mensuel sur PEA + CTO, veut optimiser timing intra-mois ET planifier l'achat en parts entières (un % théorique 50% × 500€ = 250€ ne donne pas un montant achetable si l'ETF coûte 81€ → faut 3 ou 4 parts).

**How to apply:**
- Travailler dans `/home/boris/App/DCATrack`
- Respecter "indépendance des indicateurs par ETF"
- Le projet est un POC : pas de tests, pas de DB locale, pas de sur-ingénierie
- Toute migration Supabase = SQL à exécuter manuellement dans Dashboard
