---
name: Patterns TanStack Start + Convex (gotchas découverts)
description: Patterns et gotchas appris en bootstrappant ZTHapp2 (TanStack Start + Convex Auth)
type: feedback
originSessionId: 6e608394-4cbc-42d0-88d3-01a4274d2e76
---
Patterns et gotchas découverts pendant le bootstrap de ZTHapp2 :

**Why:** Future itérations sur ZTHapp2 ou nouveau projet TanStack/Convex — éviter de retomber sur les mêmes pièges (1h de débuggage économisée).

**How to apply:** consulter avant de bootstrap un nouveau projet TanStack/Convex ou de débugger ZTHapp2.

### Bootstrap

- Commande officielle (2026-05) : `npm create convex@latest -- <NAME> -t tanstack-start`. Elle est **interactive** et plante en sandbox sans TTY.
- **Workaround** : `yes "" | npm create convex@latest -- <NAME> -t tanstack-start` pour auto-accepter les prompts par défaut.
- Le template installé bootstrappe : TanStack Start + Convex + `@convex-dev/react-query` + intégration SSR via `routerWithQueryClient`.
- Convex Auth n'est PAS inclus — installer après : `npm install @convex-dev/auth @auth/core`. Les fichiers `auth.ts`/`auth.config.ts`/`http.ts` peuvent être créés à la main, MAIS il faut **impérativement** lancer `npx @convex-dev/auth` (ou `yes "" | npx @convex-dev/auth` en non-interactif) pour générer les variables d'env `JWT_PRIVATE_KEY`, `JWKS`, `SITE_URL` sur le deployment Convex. Sans elles, le signUp crée un compte mais le signIn final plante avec `Missing environment variable JWT_PRIVATE_KEY` ; et tout compte créé avant la génération des keys est **corrompu** (signIn ultérieur → `InvalidSecret`) — il faut supprimer les lignes `users` + `authAccounts` + `authSessions` via le dashboard Convex (`http://127.0.0.1:6790/?d=anonymous-<project>` → Data) avant de ré-inscrire.

### Imports à connaître

- `import { Password } from "@convex-dev/auth/providers/Password";` — **named import**, pas default (la doc montre default mais c'est obsolète dans les versions récentes).
- `import { convexAuth } from "@convex-dev/auth/server";`
- `import { useAuthActions, useConvexAuth } from "@convex-dev/auth/react";`
- Pattern data : `useQuery(convexQuery(api.X.Y, args))` depuis `@tanstack/react-query` + `@convex-dev/react-query`. Mutations : `useMutation(api.X.Y)` depuis `convex/react`.

### tsconfig

- Le tsconfig racine généré inclut `**/*.ts` ce qui catch `convex/` (qui a son propre tsconfig). Ajouter `"exclude": ["node_modules", "dist", ".output", "convex"]` au tsconfig racine pour éviter des erreurs de type sur `process.env` (Convex tourne sous Node, le frontend non).

### Codegen Convex

- `convex/_generated/api.d.ts` est **stale tant que `npx convex dev` n'a pas été lancé avec un deployment Convex**. Tant qu'il n'est pas régénéré, tous les `api.X.Y` retournent `any`.
- Workaround pour build : écrire manuellement un stub `api.d.ts` qui référence les modules (`import type * as foodEntries from "../foodEntries.js"` puis `ApiFromModules<{...}>`). Stub remplacé automatiquement au premier `npx convex dev`.

### Schema Convex

- `userId: v.id("users")` (pas `v.string()`) — les tables `authTables` du module `@convex-dev/auth/server` créent une table `users` dont les IDs sont typés.
- Spread `...authTables` dans `defineSchema({...})` pour inclure users/sessions/accounts/verificationCodes auto.
- Pattern guard systématique dans queries/mutations : helper `requireUserId(ctx)` qui throw "Unauthorized" si pas auth. Toutes les queries DB scopent via `withIndex("by_userId..", q => q.eq("userId", userId)...)`.

### Provider Convex Auth (CRITIQUE)

- Dans `src/router.tsx`, le `Wrap` doit utiliser **`ConvexAuthProvider`** depuis `@convex-dev/auth/react`, PAS `ConvexProvider` depuis `convex/react`. Le second ne fournit pas le contexte `ConvexProviderWithAuth` qu'attend `useConvexAuth()` → runtime error "Could not find ConvexProviderWithAuth as an ancestor component". Le template bootstrap met `ConvexProvider` par défaut, c'est faux si on utilise Convex Auth.

### Routing

- Pas de `app.config.ts` (training data obsolète) — tout dans `vite.config.ts` avec le plugin `tanstackStart()`.
- File-based routing : `src/routes/__root.tsx` (shell HTML) + groupes `(auth)/` (invisibles dans URL) + layout `_authenticated/` (underscore = layout sans segment URL).
- Auth guard : dans `_authenticated/route.tsx`, utiliser `useConvexAuth()` + `useEffect` + `useNavigate` pour rediriger vers `/login` si pas auth (le SSR ne connaît pas l'auth Convex côté serveur sans setup additionnel).
- Suppression du `index.tsx` racine : le dashboard vit dans `_authenticated/index.tsx` qui matche `/` automatiquement.

### Build

- `npm run build` enchaîne `vite build && tsc --noEmit`. Le typecheck strict fait planter le build si une seule erreur de type — d'où l'importance de fixer ts ET de stub `api.d.ts`.
- Pas besoin de `npm run dev` (incompatible avec workflow Boris). Push Vercel après build OK.

### Pièges Next.js → TanStack

- `next/link` → `@tanstack/react-router` `Link` avec `to=` (pas `href=`)
- `next/navigation` `usePathname` → `useLocation`. `useSearchParams` → `useSearch`. `useRouter` → `useNavigate`.
- `next/image` → `<img>` standard (props `fill` → classes `absolute inset-0 h-full w-full object-cover`)
- `"use client"` → supprimer (TanStack Start n'a pas de RSC, tout est client React classique)
