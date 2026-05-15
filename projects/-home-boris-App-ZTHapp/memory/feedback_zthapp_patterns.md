---
name: ZTHapp portage patterns
description: Patterns concrets portes de DCATrack vers ZTHapp et gotchas confirmes pendant la Phase 0
type: feedback
originSessionId: 11a5f17e-a3c3-4b9c-9c3e-d73b30335ac3
---
# ZTHapp — patterns de portage et gotchas (Phase 0 confirmes)

## Pattern : create-next-app + portage cible (preferable a clone direct)

Boris a explicitement choisi (B) `create-next-app` neuf + portage cible plutot que (A) `cp -r` de DCATrack.

**Why** : evite de trainer l'historique d'erreurs DCATrack et le code metier ETF. Le scaffold genere les configs Next 16 a jour automatiquement (tsconfig.json, eslint.config.mjs, postcss.config.mjs sont en fait identiques a DCATrack — pas besoin de les ecraser).

**How to apply** :
1. `cd /tmp && npx create-next-app@latest <name>-init --ts --tailwind --app --turbopack --no-src-dir --import-alias "@/*" --use-npm --eslint --yes` (le `-init` suffix evite le refus des majuscules)
2. `mv` selectif des fichiers vers le projet cible (jamais `cp -rT` qui ecrase silencieusement)
3. Porter UNIQUEMENT les composants generiques de DCATrack (sans logique metier ETF)
4. Ajouter manuellement `recharts` + `lucide-react` dans `package.json` (le scaffold ne les inclut pas)

## Pattern : sidebar desktop + BottomNav mobile (DCATrack-style)

DCATrack n'a PAS de "drawer overlay mobile + bouton hamburger flottant" comme la doc `dcatrack-template.md` le decrit. La realite : `SideDrawer.tsx` est `hidden lg:flex` (desktop only) et `BottomNav.tsx` prend le relais en `lg:hidden` (mobile).

**Why** : pattern moderne et plus ergonomique sur mobile (5 tabs visibles + Action sheet pour le secondaire) vs un drawer caché.

**How to apply** : pour ZTHapp, garder la meme separation. Sidebar 4 tabs principaux + 3 secondaires + Actions ; BottomNav 4 tabs + bouton "Plus" qui ouvre `ActionSheet` (Aide / Parametres / A propos / theme toggle).

## Pattern : bootstrap anti-flash inline dans `<head>`

Script inline lit `localStorage` (`zthapp-theme`, `zthapp-sidebar`) et applique `.dark` + CSS var `--sidebar-w` AVANT le rendu React.

**Why** : sans ce script, FOUC flash blanc + sidebar qui saute de 16rem a 4.5rem au mount.

**How to apply** : copier-coller le bootstrap depuis `app/layout.tsx` DCATrack en remplacant les keys `dcatrack-*` → `zthapp-*`. Le `suppressHydrationWarning` sur `<html>` est obligatoire car le script modifie le DOM avant React.

## Pattern : `RegisterSW` prod-only

Service worker registered uniquement si `process.env.NODE_ENV === "production"`. En dev, le SW casse le HMR.

## Pattern : Tailwind v4 dans `globals.css` (pas de tailwind.config.js)

Config via `@theme inline { --font-sans: ... }` + `@variant dark (&:where(.dark, .dark *));` directement dans `app/globals.css`. CSS vars Recharts (`--chart-tooltip-bg`, `--pie-stroke`) definies en bas du fichier pour les composants charts qui ne peuvent pas utiliser `dark:`.

## Pattern : theme color amber `#f59e0b`

Garder l'identite visuelle DCATrack (gradient amber `from-amber-400 to-orange-500` sur le brand, surfaces `text-amber-600 dark:text-amber-300` pour l'item actif). Boris n'a pas demande de change → on conserve.

## Gotcha confirme : `create-next-app` refuse les majuscules

`create-next-app zthapp` → init le projet `zthapp` ; mais `create-next-app ZTHapp` est rejete avec "name should be all lowercase". Workaround eprouve : init dans `/tmp/<lowercase>` puis `mv` vers `/home/boris/App/ZTHapp/`.

## Gotcha confirme : preserver les fichiers existants pendant le `mv`

Avant le portage, `/home/boris/App/ZTHapp/` contenait deja `CLAUDE.md`, `docs/`, `zth.pdf`, `Zero_to_Hero_Calculator.xlsx`. Faire `mv` fichier par fichier (pas `mv /tmp/zthapp-init/* .`) pour eviter les collisions silencieuses.

## Gotcha confirme Phase 1 : initial state d'un Client Component qui lit localStorage

**Faux pattern** (declenche un hydration mismatch) :
```ts
const [theme, setTheme] = useState<Theme>(() => {
  if (typeof window === "undefined") return "dark";
  return window.localStorage.getItem(THEME_KEY) ?? "dark";
});
```
Sur SSR retourne "dark", sur client retourne autre chose si localStorage existe. Mismatch React 19.

**Bon pattern** (utilise `mounted` + `useEffect`) :
```ts
const [theme, setTheme] = useState<Theme>("dark");
const [mounted, setMounted] = useState(false);
useEffect(() => {
  setTheme(window.localStorage.getItem(THEME_KEY) ?? defaultTheme);
  setMounted(true);
}, []);
useEffect(() => {
  if (!mounted) return;
  /* sync state -> DOM/localStorage */
}, [theme, mounted]);
```
SSR rend "dark" et premier client render aussi → match. useEffect post-mount applique la vraie valeur. La classe `.dark` est deja appliquee par le bootstrap inline du layout, donc pas de FOUC visible meme avec ce delai.

## Gotcha confirme Phase 1 : Recharts SSR warnings `width(-1)/height(-1)`

Genere a `npm run build` :
```
The width(-1) and height(-1) of chart should be greater than 0...
```
Non bloquant — le chart se rend post-hydration cote client via `<ResponsiveContainer>`. **A ignorer**, c'est attendu pour tout chart Recharts dans un Client Component.

## Gotcha confirme Phase 1 : turbopack cache stale apres edit important

Apres une grosse modif (ajout de plusieurs Client Components), `.next/` peut servir une version stale. Symptome : meme code sur disque mais browser execute l'ancien.

**Fix** : `pkill -f "next dev"` + `rm -rf .next/` + `npm run dev` relance.

## Gotcha confirme Phase 1 : warning `<script>` inline dans `<head>`

Le bootstrap anti-flash via `<script dangerouslySetInnerHTML={...} />` declenche en dev :
```
Encountered a script tag while rendering React component. Scripts inside React components are never executed when rendering on the client.
```
**Non bloquant** — le script s'execute pendant le SSR rendering (c'est ce qu'on veut), le warning concerne uniquement le re-render client (qui n'execute jamais le script, c'est OK). Garder le pattern tel quel.

## Pattern Phase 1 : cle localStorage par jour en local time

`dateKey(date: Date) → "YYYY-MM-DD"` construit depuis `getFullYear/getMonth/getDate` (pas `toISOString` qui sort en UTC). Evite les decalages de fuseau quand on passe minuit en France mais qu'il est encore le jour precedent en UTC.

## Pattern Phase 1 : donut Recharts coherent avec macroBars

Le donut affiche les **proportions** G/L/P calculees depuis `grams × kcal/g` (4·G + 9·L + 4·P), mais le total au centre = `totals.kcal` (somme directe des kcal des templates). Sinon mismatch visuel : le centre du donut differe de la barre Calories quand les macros sont approximatives.

## Gotcha confirme Phase 1.1 : Recharts `cx="50%"` ne dessine pas sans ResponsiveContainer

Symptome : `<PieChart width={...} height={...}>` avec `<Pie cx="50%" cy="50%">` produit un SVG `recharts-surface` correctement dimensionne mais avec **0 path enfant**. Le container existe, le donut est invisible.

**Why** : Sans ResponsiveContainer, Recharts ne resout pas les pourcentages — il faut donner cx/cy en pixels.

**Fix eprouve** : mesurer la largeur du parent via `useRef + ResizeObserver`, conditionner le rendu `{width > 0 && <PieChart width={width} ...>}`, et passer `cx={width / 2} cy={height / 2}` en pixels. Aussi `isAnimationActive={false}` pour eviter un flicker au mount.

```tsx
const ref = useRef<HTMLDivElement>(null);
const [width, setWidth] = useState(0);
useEffect(() => {
  if (!ref.current) return;
  const el = ref.current;
  const obs = new ResizeObserver(() => setWidth(el.clientWidth));
  obs.observe(el);
  return () => obs.disconnect();
}, []);

<div ref={ref} style={{ height: 200 }}>
  {width > 0 && (
    <PieChart width={width} height={200}>
      <Pie cx={width / 2} cy={100} innerRadius={55} outerRadius={90} ...>
```

Le warning `width(-1)/height(-1)` au build reste present — toujours non bloquant.

## Pattern Phase 1.1 : Entry polymorphe + retro-compat localStorage

`Entry` polymorphe : `{ type: "dish", dishSlug, ingredients? }` ou `{ type: "food", foodId, qty }`. Le retro-compat dans `migrateEntry` accepte l'ancien format `{ id, dishSlug, slot, ts }` (sans `type`) et le promeut en `type: "dish"`. Permet l'evolution du schema sans casser les donnees existantes.

## Pattern Phase 1.1 : sidebar collapsed sticky entre /pages

Le state du SideDrawer (`zthapp-sidebar`) persiste dans localStorage et est applique via le bootstrap inline avant le rendu React. Donc une navigation entre pages (`/nutrition` → `/parametres`) garde la sidebar replieie sans flash.

## Gotcha confirme Phase 2 : auto-fill sur onChange = pollution pendant le typing

**Faux pattern** : auto-fill des series 2-3 sur `onChange` du champ poids top set. Quand Boris tape "100", les 3 frappes "1", "0", "0" declenchent 3 onChange :
- "1" → auto-fills set2 a 0.9 (arrondi 1) et set3 a 0.81 (arrondi 1)
- "10" → set2 et set3 ont deja weight=1, condition `=== 0` fausse, pas d'overwrite
- "100" → idem, le top set affiche bien 100 mais les sets 2-3 restent a 1

**Bon pattern** : auto-fill sur `onBlur` du champ. Le user finit de taper, sort du champ, l'auto-fill se declenche une seule fois avec la valeur finale. Implementation :
```tsx
const onTopSetBlur = () => {
  if (exercise.technique !== "pyramidal") return;
  const top = value.sets[0].weight;
  if (top <= 0) return;
  const set2 = Math.round(top * 0.9 * 4) / 4;
  const set3 = Math.round(set2 * 0.9 * 4) / 4;
  // n'ecrase pas si Boris a deja saisi manuellement set2/set3
  ...
};

<input onChange={updateSet} onBlur={idx === 0 ? onTopSetBlur : undefined} />
```

Lecon generalisable : tout calcul derive d'un input controle qui modifie d'autres champs doit etre sur **onBlur**, pas onChange. Sinon le typing intermediaire pollue les autres champs.

## Pattern Phase 2 : 1 entite par jour (workout, vs entries multiples nutrition)

Nutrition : `Entry[]` par jour (plusieurs repas par jour) → cle `zthapp-entries-{date}` · valeur = array.

Sport : 1 `Workout` par jour max (Boris demande 1 seance/jour) → cle `zthapp-workout-{date}` · valeur = objet (pas array).

Choix de schema base sur la cardinalite. Plus simple : pas de tableau a iterer, pas de `id` par entry, le `Workout` lui-meme contient tout (5 exos × 3 series × {weight, reps} + RIR par exo).

## Pattern Phase 2 : suggestion contextuelle base sur l'historique

`findLastTopSet(exerciseId, beforeDate)` : itere `listAllWorkouts()` (sorted desc), retourne le top set du premier workout < date courante qui contient cet exo et a poids ou reps > 0. Affiche "↺ 80kg × 5 (12/03)" au-dessus de l'exo.

Pattern reutilisable Phase 3 (suggestion pas) et plus tard pour toute UI qui veut "rappeler la valeur precedente".

## Gotcha confirme Phase 4 : Supabase magic link rate-limited free tier

Le free tier Supabase limite a ~4 emails/heure pour les magic links / confirm email. Impossible de connecter PC + mobile en parallele dans la meme heure (chaque device demande un nouveau lien).

**Solution adoptee** : passer en **email + password** (`signInWithPassword` / `signUp`). Plus pratique pour multi-device : 1 mdp memorise → connexion sur N devices a volonte. Aussi disable "Confirm email" dans Supabase Auth → Providers pour eviter le rate limit lors du signup.

Le magic link reste utilisable si jamais on en a besoin (la route `/auth/callback` existe deja), mais les actions principales sont password-based.

## Pattern Phase 4 : cache-first read, fire-and-forget write-through

Pour le sync online-first multi-device sans bloquer l'UI :
- **Read** : lire localStorage immediatement (instant render), puis pull Supabase async, replace state quand reponse OK. UI repond < 50ms meme si Supabase lent.
- **Write** : update state + localStorage immediatement, puis push Supabase via `.catch(() => {})` (fire-and-forget). Si Supabase down/erreur → log silencieux, donnees safes en local. Ce sera resync au prochain pull.

Avantages : UI ultra-reactive, pas de blocage sur les saves, code simple. Inconvenients : si push silencieusement fail, on ne sait pas ; et 2 devices peuvent diverger temporairement (last-write-wins, OK pour solo). Pour multi-user / collab → faudrait realtime + CRDT (overkill pour Boris).

## Pattern Phase 4 : migration auto localStorage → Supabase via SyncBootstrap

Composant Client `<SyncBootstrap />` monte au layout uniquement si auth (`{email && <SyncBootstrap />}`). Au premier mount, check flag `zthapp-migrated-v1` localStorage. Si absent → push tout (profile + food_entries + workouts + daily_steps) vers Supabase, set flag. Idempotent (flag protege). Permet a Boris d'arriver avec ses donnees locales accumulees Phases 0-3 et de les retrouver en cloud sans saisie manuelle.

## Pattern Phase 4 : middleware redirect public-paths whitelist

`middleware.ts` racine appelle `updateSession(req)` qui :
1. Refresh la session via `auth.getUser()` (rafraichit le cookie)
2. Si pas de user ET path pas dans `PUBLIC_PATHS` (`/login`, `/auth/callback`) → redirect /login
3. Sinon → laisse passer

Le `matcher` exclut les assets statiques (`_next/static`, `manifest.json`, `sw.js`, icons) pour eviter le redirect sur ces ressources.

## Gotcha confirme Phase 4 : `<body className>` conditional sur user state

Quand non auth (`/login`), on ne veut pas appliquer le `padding-left: var(--sidebar-w)` du body (sinon contenu decale a gauche meme sans sidebar). Solution : layout async ajoute la classe `no-sidebar` conditionnellement, et `globals.css` override `body.no-sidebar { padding-left: 0 !important; padding-bottom: 0 !important; }`. Plus simple qu'un layout dedie `(auth)/layout.tsx`.

## Pattern Phase 1.1 : Server Component qui import un Client Component pour lire localStorage

Pour le dashboard `/` : la page reste Server, et la carte Nutrition est extraite en `DashboardNutritionCard` (Client) qui lit localStorage en `useEffect`. Plus efficace que tout passer en Client. Pattern reutilisable Phase 2/3 pour les cartes Sport et Pas.
