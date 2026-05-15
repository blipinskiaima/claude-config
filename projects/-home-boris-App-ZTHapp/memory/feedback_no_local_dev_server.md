---
name: Pas de dev server local sur ZTHapp
description: Ne jamais lancer `npm run dev` sur ZTHapp — utiliser build + Vercel pour tester
type: feedback
originSessionId: 1475a4a7-d56a-4373-bc32-2df4b2f927e5
---
Sur ZTHapp, **ne pas lancer `npm run dev` en local** (ni background ni foreground).

**Why:** Ça fait planter l'ordinateur de Boris (Turbopack + ressources limitées). Boris l'a explicitement signalé après le checkpoint Phase A de la refonte UI où j'avais démarré un dev server en arrière-plan.

**How to apply:**
- Pour vérifier la compilation : `npm run build` (one-shot, ne reste pas en mémoire) — suffisant pour valider TypeScript/lint/bundling.
- Pour validation visuelle : commit + push → Vercel déploie automatiquement → Boris teste sur l'URL de preview/prod.
- Workflow checkpoint : build local OK → confirmer commit/push avec Boris → Vercel preview → Boris valide visuellement → on continue.
- Si test de rendu avant push : MCP claude-in-chrome sur l'URL Vercel, jamais sur localhost.
