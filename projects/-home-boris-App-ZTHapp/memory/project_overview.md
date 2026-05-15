---
name: ZTHapp project overview
description: App de suivi nutrition + sport + pas pour le programme ZTH (Zero To Hero) de Boris, basée sur le squelette DCATrack
type: project
originSessionId: 11a5f17e-a3c3-4b9c-9c3e-d73b30335ac3
---
# ZTHapp — Vue d'ensemble

## Objectif
App de suivi triple pour le programme **ZTH Protocole 3** :
- **Nutrition** : journal repas 1-clic (templates ZTH/MFP) + macros vs objectif jour (1994 kcal · 99g P · 61g L · 261g G calculés via `computeZth`)
- **Sport** : 3 séances/sem (Lundi Upper A · Mercredi Lower · Vendredi Upper B), saisie poids × reps + RPE, charts progression sur 7 lifts polyarticulaires clés
- **Pas** : saisie manuelle quotidienne, cible ZTH 10 000 pas/jour

**Why** : Boris suit le programme ZTH P3 (cut −300 kcal). Sources structurées disponibles : `zth.pdf` (182p, programme officiel), `Zero_to_Hero_Calculator.xlsx` (formules calcul kcal/macros), MCP MyFitnessPal `/home/boris/App/Myfitnesspal/` (backend lecture/écriture journal MFP, 9 tools).

**How to apply** : projet en 4 phases (voir `project_phasing.md`). Phase 0 livrée, Phases 1-3 itératives, persistance localStorage initiale + migration Supabase ultérieure.

## Stack
- Next.js 16.2.5 (App Router + Turbopack) + TypeScript strict
- Tailwind v4 (`@theme` inline dans `globals.css`, **pas** de `tailwind.config.js`)
- Recharts 3.8 pour donut macros (P1) + charts progression (P2/P3)
- lucide-react disponible (icônes — aussi des SVG inline pour la NAV)
- PWA : `manifest.json` + `sw.js` minimal pass-through + RegisterSW prod-only
- Persistance Phase 0-3 : `localStorage` (clé prefix `zthapp-*`)
- Persistance Phase 4 (futur) : Supabase + auth + RLS user_id

## Source de données ZTH
- `zth.pdf` : 4 protocoles, 3 séances Upper A/Lower/Upper B avec exos, 9 recettes étoilées, règle ajustement `−100 kcal = −25g glucides` (P et L lockés)
- `Zero_to_Hero_Calculator.xlsx` : 15 formules clé, BMR moyen Mifflin-St Jeor + Katch-McArdle, maintenance × 1.5
- Code TypeScript prêt à coller : `computeZth({age, height, weight, bodyfat, protocol})` dans `docs/zth-calculator.md` (Boris P3 Initiale = 1994.55 kcal / 99.2g P / 61.44g L / 261.2g G)

## Transposition DCATrack → ZTHapp (réf. `docs/transposition.md`)
| DCATrack (finance) | ZTHapp (multi) |
|---|---|
| ETF | Repas (P1) / Exo (P2) / Jour (P3) |
| WATCHLIST 28 ETF | 9 templates MFP + 7 lifts polyarticulaires |
| Score 0-100 composite | Score équilibre `100 − moy |écarts à 100%|` (P1) |
| `dca_executions` | `food_entries` (P1) + `workout_sets` (P2) + `daily_steps` (P3) |
| `refreshETFs()` Server Action | (retiré Phase 0 — pas de fetch externe) |

## État (2026-05-06)
- ✅ Phase 0 (Bootstrap) livrée : Next.js 16 scaffolde, 7 routes navigables, theme dark/light, sidebar collapse desktop + BottomNav mobile, PWA installable, dev server OK sur http://localhost:3000
- 📅 Phase 1 (Nutrition) : à planifier
- 📅 Phase 2 (Sport) : à planifier
- 📅 Phase 3 (Pas) : à planifier
- 📅 Phase 4 (Supabase) : futur

## Fichiers de référence dans le repo
- `/home/boris/App/ZTHapp/CLAUDE.md` — point d'entrée projet
- `/home/boris/App/ZTHapp/docs/transposition.md` — mapping concepts
- `/home/boris/App/ZTHapp/docs/dcatrack-template.md` — patterns réutilisables
- `/home/boris/App/ZTHapp/docs/nutrition-data.md` — templates repas + IDs MFP
- `/home/boris/App/ZTHapp/docs/zth-program.md` — synthèse PDF (135/182 pages)
- `/home/boris/App/ZTHapp/docs/zth-calculator.md` — formules xlsx + impl TypeScript
