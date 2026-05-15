---
name: DCATrack stack and key files
description: Architecture technique, libs, fichiers cœur du projet DCATrack
type: reference
---

**Stack** :
- Next.js 16 App Router (Turbopack), TypeScript strict
- Tailwind CSS v4 (config dans CSS via `@theme`, pas de tailwind.config.js)
- Recharts pour les mini-charts (AreaChart + ReferenceLine)
- PWA via manifest.json + service worker minimal (`public/sw.js`) + `RegisterSW.tsx` Client Component
- Node v24.15.0 LTS via nvm
- Pas de shadcn/ui (POC : Tailwind raw suffit)
- Pas de @serwist/next (POC : SW minimal suffit pour installabilité)

**Fichiers cœur** :
- `app/lib/etfs.ts` — Constantes des 3 ETF (ISIN, ticker, nom, catégorie). Source de vérité.
- `app/lib/justetf.ts` — `fetchJustETF(isin)` avec headers navigateur + ISR cache 1h, tags `etf` et `etf-${isin}`.
- `app/lib/score.ts` — `analyze(series)` calcule drawdowns 52w/6m/YTD/1m, SMA200, std200, z-score, perfYTD, perf1y, score 0-100, verdict. `verdictMeta(v)` retourne emoji+label+couleurs Tailwind.
- `app/api/etf/[isin]/route.ts` — Route handler debug : GET → JSON `{etf, analysis}`.
- `app/actions/refresh.ts` — Server Action `refreshETFs()` qui appelle `updateTag("etf")` (Next.js 16 — pas `revalidateTag` qui demande maintenant un profil).
- `app/page.tsx` — Server Component : `loadAll()` → 3 cards en parallèle, gère erreurs par ETF (ErrorCard fallback).
- `app/components/ETFCard.tsx` — Card autonome (header, chart, verdict, ScoreBar, drawdown stats).
- `app/components/PriceChart.tsx` — Client Component Recharts.
- `app/components/RefreshButton.tsx` — Client Component avec useTransition.
- `app/components/RegisterSW.tsx` — Client Component qui register `/sw.js` en prod uniquement.

**PWA** :
- `public/manifest.json` — `display: standalone`, theme `#f59e0b`, icons 192+512 maskable
- `public/sw.js` — SW minimal pass-through (juste pour passer l'audit installability)
- `public/icon-192.png` + `icon-512.png` — Générés depuis SVG via ImageMagick

**Gotchas** :
- `revalidateTag` en Next.js 16 demande 2 args (`tag`, `profile`) — utiliser `updateTag(tag)` à la place dans Server Actions
- Recharts émet des warnings SSR `width(-1)/height(-1)` non bloquants — le chart se rend correctement après hydration
- `cp -rT` écrase `.git` — toujours re-add le remote après copie depuis tmp
- `create-next-app` refuse les noms avec majuscules — créer en `/tmp/dcatrack` puis copier dans `DCATrack/`
