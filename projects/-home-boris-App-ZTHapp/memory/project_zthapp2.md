---
name: ZTHapp2 — Port sister-project sur TanStack Start + Convex
description: ZTHapp2 est un fork de ZTHapp dans /home/boris/App/ZTHapp2/ avec stack TanStack Start + Convex au lieu de Next.js + Supabase
type: project
originSessionId: 6e608394-4cbc-42d0-88d3-01a4274d2e76
---
`/home/boris/App/ZTHapp2/` est un fork expérimental de ZTHapp créé le 2026-05-11 pour tester la stack TanStack Start + Convex.

**Why:** Boris voulait expérimenter une stack alternative à Next.js + Supabase tout en gardant les features ZTHapp. Le port a été fait via agent teams parallèles (Wave 1/2/3) en respectant intégralement ZTHapp (lecture seule).

**How to apply:**
- Travailler dans ZTHapp2 quand Boris parle du projet "TanStack/Convex" ou "ZTHapp2"
- ZTHapp et ZTHapp2 sont en parallèle, indépendants (chacun son git, son backend)
- Hors scope du port initial : Coach IA, PWA, sync localStorage (Convex temps réel rend ce dernier inutile)
- ZTHapp2 a Convex Auth Password (email/password seul, pas d'OAuth)
- Compte Supabase ZTHapp (`boris.lipinski83@gmail.com`) ne s'applique pas à ZTHapp2 (Convex a son propre auth interne)
- Bootstrap commit : `8fcb0ac` sur branche `master`

**Stack ZTHapp2** :
- `@tanstack/react-start` 1.x + Vite + Vinxi
- `convex` 1.36 + `@convex-dev/auth` + `@convex-dev/react-query`
- `@tanstack/react-router` (file-based) + `@tanstack/react-query`
- Tailwind v4 (tokens identiques à ZTHapp)
- 10 modules Convex : auth, http, foodEntries, workouts, profile, dailySteps, dailySupplements, phaseEvents, programStandards, restDays
- 7 routes : `/login` + `_authenticated/{index,nutrition,sport,pas,complements,parametres}`
- Auth flow : guard client-side via `useConvexAuth()` dans `_authenticated/route.tsx`
