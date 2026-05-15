---
name: Coach IA chatbot ZTH
description: Architecture du coach IA conversationnel (page /coach + FAB) — provider Gemini gratuit, Vercel AI SDK v6, contexte user 30j auto-injecté
type: project
originSessionId: 1475a4a7-d56a-4373-bc32-2df4b2f927e5
---
Feature ajoutée au commit `e4538a4` (mai 2026). Coach IA qui répond aux questions de Boris sur nutrition / sport / récupération / progression, avec accès à ses données réelles (profil + 30 derniers jours d'entries / workouts / steps / suppléments / phases).

**Why:** Boris voulait un assistant qui le guide concrètement (reprise après écart nutrition, décision aller au sport ou pas, stagnation, calibrage calories) plutôt que de chercher dans le PDF ZTH ou Claude.ai à la main.

**How to apply:** Toute évolution du coach IA doit respecter cette architecture. Toute nouvelle source de données utilisateur → l'ajouter dans `context-builder.ts`. Toute nouvelle source de connaissance ZTH → l'ajouter dans `scripts/build-knowledge.mjs`.

## Provider : Google Gemini (gratuit) — pas Anthropic

Boris a un abonnement Claude Pro/Max sur claude.ai mais **l'API Anthropic est un produit séparé** (facturation à l'usage). Boris a explicitement refusé tout coût supplémentaire → on est sur **Google Gemini Free Tier** via `@ai-sdk/google` :
- Modèles : `gemini-2.5-flash` (default, rapide) + `gemini-2.5-pro` (toggle UI "deep")
- Quota gratuit : 15 RPM / 1500 RPD — largement suffisant pour usage perso
- Clé API : créée sur https://aistudio.google.com (séparé d'aucun abonnement)
- Var env : `GOOGLE_GENERATIVE_AI_API_KEY` (convention SDK)

Si Boris veut switcher provider (ex: Anthropic API si budget débloqué), c'est trivial : remplacer `createGoogleGenerativeAI` par `createAnthropic` dans `app/api/chat/route.ts`. Le reste du code est provider-agnostic.

## Stack Vercel AI SDK v6 (pas v4 !)

L'API a changé en v6 — les patterns v4 trouvés sur le web ne marchent pas :
- `ai` v6.x · `@ai-sdk/react` v3.x (séparé) · `@ai-sdk/google` v3.x
- Côté server : `streamText({ model: provider(id), system, messages: await convertToModelMessages(uiMessages), onFinish })` — `convertToModelMessages` est **async** (Promise) en v6.
- Côté client : `useChat({ transport: new DefaultChatTransport({ api, prepareSendMessagesRequest }) })` — `transport` est obligatoire, plus de `api: '/...'` direct.
- Plus de `input` / `handleInputChange` / `handleSubmit` auto. État input géré soi-même + `sendMessage({ text })`.
- `onFinish` ne reçoit plus `response` (donc pas accès aux response headers côté client). Pour passer du data du server vers le client : utiliser custom data parts ou un endpoint séparé.
- `messages` côté client = `UIMessage[]` avec `parts: Array<{type: 'text', text: string}>` (pas `content` direct).

## Architecture

**Backend** :
- `app/api/chat/route.ts` (Edge runtime, maxDuration 60) — auth Supabase, build user context, streamText, persist messages onFinish.
- `app/lib/coach/system-prompt.ts` — identité + ton + référentiel ZTH concaténé.
- `app/lib/coach/context-builder.ts` — `buildUserContext(supabase, userId)` async qui agrège profil + 30j toutes les tables en markdown structuré (~3-5k tokens).
- `app/lib/coach/zth-knowledge.generated.ts` — fichier **généré** par `scripts/build-knowledge.mjs` (lit `docs/*.md` au prebuild). Gitignored. ~16k tokens.
- `app/lib/chat-storage.ts` — CRUD conversations + messages.
- `supabase/migrations/0005_chat.sql` — tables `chat_conversations` + `chat_messages` + RLS auth.uid() = user_id + trigger updated_at.

**Frontend** :
- `app/coach/page.tsx` (server) → auth check → render `<CoachView />`.
- `app/coach/CoachView.tsx` (client) → `<PageHero>` + `<ChatPanel>` pleine hauteur.
- `app/components/CoachFab.tsx` (client) → bouton flottant `fixed bottom-20 right-4` ouvrant un `Drawer.Root` vaul avec `<ChatPanel showModelToggle={false} />` compact. Caché sur `/login` et `/coach`.
- `app/components/coach/ChatPanel.tsx` — logique partagée entre /coach et FAB. `useChat` + state input + scroll auto + welcome state (4 suggestions cliquables si messages vides).
- `app/components/coach/{CoachMessage, ModelToggle, SuggestionChip}.tsx` — sous-composants UI.
- `app/lib/coach/welcome.ts` — message d'accueil + 4 suggestions (j'ai sauté 2j de nut / mal aux épaules / je stagne au DC / calibrage calories).

**Nav** : `<CoachFab />` ajouté dans `app/layout.tsx` après `<BottomNav>` (uniquement si email). Lien Coach IA ajouté dans NAV principal `SideDrawer` + en première position de l'ActionSheet "Plus" du `BottomNav`.

## Knowledge base — pattern prebuild

Pas de RAG vectoriel : on stuffe les ~16k tokens des docs en system prompt à chaque requête. Le SDK Gemini gère ça sans broncher (1M context window).

Le pipeline :
1. `docs/zth-program.md` + `zth-calculator.md` + `zth-exercices-detail.md` + `nutrition-data.md` (sources Boris-friendly à éditer)
2. `scripts/build-knowledge.mjs` lance via `npm run prebuild` → concatène tout dans `app/lib/coach/zth-knowledge.generated.ts` exportant `export const ZTH_KNOWLEDGE: string`
3. `system-prompt.ts` import et l'injecte
4. `.gitignore` exclut le `.generated.ts`

**Pour étendre** : ajouter une entrée dans `SOURCES` du script + un nouveau `.md` dans `docs/`. Le prebuild auto-régénère.

## User context — pattern Supabase server

`buildUserContext()` fait 6 requêtes Supabase en parallèle (`Promise.all`) sur profile + food_entries + workouts + daily_steps + daily_supplements + phase_events. Filtre 30j via `.gte("date", cutoff)`. Calcule les agrégats côté JS (moyennes, plats récurrents, top sets par exercice, streaks).

Pas de cache — recompute à chaque message, ce qui est OK car requêtes rapides (<300ms total) et données fraîches obligatoires pour conseils contextuels.

## Coût observé

Avec Gemini Free Tier : 0€/mois pour usage Boris (30 msg/jour). Quotas larges (15 RPM, 1500 RPD).

Si bascule Anthropic future : ~10-15€/mois (Haiku 4.5 + prompt caching ephemeral via `providerOptions.anthropic.cacheControl`).

## Piège : check constraints SQL vs valeurs code

Lors du swap de provider (Anthropic → Google) la check constraint SQL `chat_conversations_model_check` est restée sur `IN ('haiku', 'sonnet')` alors que le code envoie `'flash'` / `'pro'`. Symptôme : `create_conversation_failed` avec code Postgres `23514`. Fix manuel via `ALTER TABLE … DROP CONSTRAINT … ; ADD CONSTRAINT … CHECK (model IN ('flash', 'pro'))`. Si on rechange de provider plus tard, **toujours** auditer `0005_chat.sql` (ou écrire une nouvelle migration corrective) en même temps que `MODEL_ID` dans `route.ts`.

## Sécurité

- Clés API **jamais** dans le code commité. `.env.local` gitignored.
- Boris a appris à la dure (clé sk-ant-... postée en clair → révoquée). Toujours rappeler de coller dans le fichier directement, pas dans le chat.
- Auth Supabase obligatoire sur `/api/chat` (401 si pas connecté).
- RLS Supabase sur `chat_messages` : un user ne peut pas lire les conversations d'un autre.
