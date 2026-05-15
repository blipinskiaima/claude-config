---
name: ZTHapp phasing
description: Decoupage en 4 phases livrables (0 Bootstrap → 1 Nutrition → 2 Sport → 3 Pas → 4 Supabase), avec statut courant
type: project
originSessionId: 11a5f17e-a3c3-4b9c-9c3e-d73b30335ac3
---
# Phasage ZTHapp

Decoupage approuve par Boris (2026-05-06) pour livrer en increments testables.

**Why** : projet massif (3 vues + dashboard + PWA + persistance) qui aurait ete instable en monobloc. Le phasage fait que chaque livraison est une app utilisable, et chaque phase debloque la suivante.

**How to apply** : ne pas planifier la phase N+1 avant la fin de la phase N. Avant chaque phase : `EnterPlanMode` pour soumettre un plan a l'utilisateur.

## Phase 0 — Bootstrap ✅ (2026-05-06)
- `create-next-app@latest` Next 16.2.5 + Tailwind v4, scaffold dans `/tmp/zthapp-init` puis `mv` vers `/home/boris/App/ZTHapp/` (preserve `docs/`, `CLAUDE.md`, `zth.pdf`, `Zero_to_Hero_Calculator.xlsx`)
- Portage cible depuis DCATrack : `app/{layout.tsx, globals.css}` + `app/components/{SideDrawer, BottomNav, ThemeToggle, RegisterSW, ScoreBar}.tsx`
- Adaptations : NAV (Tableau de bord / Nutrition / Sport / Pas + Aide / Parametres / A propos), retire Supabase + RefreshETFs + AccountBlock, localStorage prefix `zthapp-*`
- 7 routes, theme dark/light persistant, sidebar collapse, PWA `manifest.json` + `sw.js`
- Verifie : `npx tsc --noEmit` OK, `npm run build` OK (10 pages statiques), dev server + 4 screenshots browser_batch sans erreur

## Phase 1 — Nutrition ✅ (2026-05-06)
- 4 libs : `dishes.ts` (9 templates avec macros approximatives), `zth-calc.ts` (paste `computeZth` + `BORIS_TARGET = 1994/261/61/99`), `score.ts` (formule equilibre + verdictMeta), `storage.ts` (wrapper localStorage avec validation type)
- 6 composants : `DateNav` (picker ◀ Aujourd'hui ▶), `DishGrid` (9 templates avec hover accent + bouton "Ajouter au {slot}"), `DayJournal` (entries groupees par slot midi/soir/snack), `MacroBars` (4 barres kcal/G/L/P avec over flag), `MacrosDonut` (Recharts PieChart, kcal-total au centre = somme dishes pour coherence), `DashboardNutritionCard` (Client, lit le meme localStorage que `/nutrition`, affiche kcal/cible)
- Orchestrateur `nutrition/NutritionView.tsx` (Client) + page wrapper Server
- Persistance localStorage `zthapp-entries-{YYYY-MM-DD}` en local time (pas UTC)
- Dashboard `/` : carte Nutrition synchronisee, montre `kcal cumul / 1994`
- Cible Boris hardcoded en Phase 1 (P3 Initiale = 1994 kcal · 99g P · 61g L · 261g G) — futur ecran `/parametres` pour saisir age/taille/poids/BF

## Phase 1.1 — Ajustements nutrition ✅ (2026-05-06)

5 ajustements demandes par Boris, livres en parallele :

1. **Macros approximatives + relation lineaire** par aliment :
   - Nouveau `app/lib/foods.ts` : table FOODS unitaires (28 aliments avec kcal/P/L/G par g/item/ml)
   - `dishes.ts` repense : templates = `ingredients: [{foodId, qty}]`. `dishMacros()` calcule lineairement
   - Boris peut modifier la quantite de chaque aliment et les macros se recalculent

2. **Edition des quantites a la saisie ET apres** :
   - `DishGrid` : click card → expand inline avec `IngredientEditor` (inputs qty par ingredient + 3 boutons +Midi/+Soir/+Snack)
   - `EditEntryModal` : click sur entry du journal → modal d'edition (slot + ingredients/qty + supprimer)
   - `IngredientEditor` reutilisable

3. **Aliments libres** :
   - `FoodPicker` : bouton "+ Aliment libre" → modal recherche FOODS + qty + slot. Stocke `Entry { type: "food", foodId, qty }`
   - 19 aliments libres dispos (banane, chocolat, whey, kefir, skyr, etc.)
   - Custom foods (Boris definit ses propres aliments) → Phase 1.5 si besoin

4. **Auto-add Raptor Club au midi** :
   - Toggle dans `/parametres` (default **on**)
   - `NutritionView` useEffect : si `profile.autoRaptor && !midiEntry` → ajoute Raptor Club par defaut

5. **Ecran `/parametres` etendu** :
   - Profil : age/taille/poids/BF saisissables
   - Protocole P1/P2/P3/P4 + Phase courante (Maintenance / Initiale / Etape 1 / Etape 2)
   - Cible journaliere recomputee dynamiquement via `computeZth`
   - Toggle auto Raptor Club
   - Zone dangereuse : reset profil + vider tous les journaux
   - Stockage `localStorage zthapp-profile`
   - Nouveau lib `app/lib/profile.ts` : `Profile` + `computeTarget(profile)` + load/save

## Phase 2 — Sport ✅ (2026-05-06)
- `app/lib/exercises.ts` : 15 exos hardcoded ZTH P3 (Upper A / Lower / Upper B), avec technique (pyramidal/classic/raptorSet/dropSet/superset), reps ranges (typed), notes
- `app/lib/sport-storage.ts` : `Workout = { date, session, exercises }` (1/jour) · localStorage `zthapp-workout-{YYYY-MM-DD}` · helpers `findLastTopSet`, `getProgressionHistory`, `countFilledSets`, `clearAllWorkouts`
- 5 composants : `SessionPicker` (3 cartes Upper A / Lower / Upper B avec badge "Aujourd'hui" base sur jour de semaine), `SessionView` (header + liste ExerciseRow), `ExerciseRow` (3 series fixes poids×reps + RIR 0-5 + auto -10% sur **onBlur** du top set pyramidal + suggestion historique "↺ 80kg×5"), `ProgressionChart` (mini line Recharts top set sur 12 dernieres seances), `DashboardSportCard` (sync localStorage)
- `SportView` : onglets "Saisir" / "Progression" · DateNav · gestion workout courant
- Auto-suggestion top set : badge ↺ "Derniere fois : 80kg × 5 (12/03)" en haut de chaque exo si historique trouve via `findLastTopSet`
- Cible Boris : suivre les 15 exos · charts pour les 15 (3 sections accordeon par session)
- Auto -10% : declenche sur **onBlur** du champ poids serie 1 (pas onChange — sinon "1" remplit set2/set3 a 0.9/0.81 → arrondi 1). Calcul : `set2 = round(top × 0.9 × 4) / 4` (arrondi 0.25kg), `set3 = round(set2 × 0.9 × 4) / 4`.
- Reset `/parametres` : ajout bouton "Vider tous les workouts"

## Phase 3 — Pas ✅ (2026-05-06)
- `app/lib/steps-storage.ts` : 1 valeur scalaire par date · localStorage `zthapp-steps-{date}` · helpers `getRange(N)` (complete dates manquantes a count=0), `avgLastNDays`, `streakAboveTarget`, `bestDay`, `clearAllSteps`
- `app/components/StepsChart.tsx` : Recharts BarChart avec `<ReferenceLine y={10000}>` · couleur barres conditionnelle (emerald si >= cible, amber sinon) via `<Cell>` · pattern ResizeObserver
- `app/pas/PasView.tsx` : input grand format · progress bar dynamique · sous-texte "Cible atteinte (+X)" / "X pas restants" · toggle 7j/30j/90j · stats Moyenne 7j / Meilleur jour / Streak
- `app/components/DashboardPasCard.tsx` : sync localStorage · couleur conditionnelle violet/emerald
- Reset `/parametres` : ajout bouton "Vider tous les pas"
- Cleanup `app/page.tsx` : retire le composant interne `DashboardCard` placeholder devenu inutile, les 3 cartes sont maintenant des Client Components dedies

## Phase 4 — Supabase + Auth + Vercel ✅ (2026-05-07)

Decoupage en 4 sous-phases livrees :

### Phase 4.1 — Auth + login UI
- `@supabase/ssr` + `@supabase/supabase-js`
- `app/lib/supabase/{client,server,middleware}.ts` (browser, server, session refresh)
- `middleware.ts` : redirect /login si non auth (sauf /login, /auth/callback)
- `/login` + `/auth/callback` (route handler) + `/signout` (POST)
- Layout async qui lit user via `auth.getUser()` ; SidePanel + BottomNav reçoivent email
- Body class `no-sidebar` quand non auth → CSS override padding-left
- **Auth finale = email + password** (pas magic link). Magic link essaye initialement, abandonné car free tier Supabase rate-limite a ~4 emails/heure → impossible de connecter PC + mobile en parallele rapidement.

### Phase 4.2 — Schema Supabase + sync nutrition
- `supabase/migrations/0001_init.sql` : 4 tables (`profile`, `food_entries`, `workouts`, `daily_steps`) + RLS `auth.uid() = user_id`
- `app/lib/storage.ts` enrichi : `pullEntries`, `pushEntry`, `deleteEntryRemote`, `migrateLocalEntriesToSupabase`, `clearAllEntriesRemote`
- `app/lib/profile.ts` enrichi : `pullProfile`, `pushProfile`, `clearProfileRemote`
- Pattern : **cache-first read, fire-and-forget write-through**. UI lit localStorage instant, pull Supabase async, replace state. Save = local + push Supabase (catch silent → online-first).

### Phase 4.3 — Sync sport + steps
- `app/lib/sport-storage.ts` : `pullWorkout`, `pushWorkout`, `pullAllWorkouts`, `migrateLocalWorkoutsToSupabase`, `clearAllWorkoutsRemote`
- `app/lib/steps-storage.ts` : `pullAllSteps`, `pushSteps`, `migrateLocalStepsToSupabase`, `clearAllStepsRemote`
- SportView : pull workout au mount + push at change ; pullAllWorkouts au switch tab Progression + bump `progressKey` pour re-mount des charts
- PasView + DashboardPasCard : pullAllSteps au mount

### Phase 4.4 — Backup + Deploy
- `app/lib/backup.ts` : `exportAll` (pull all 4 tables) + `downloadJson` + `readBackupFile` + `importAll` (upsert idempotent)
- `/parametres` SettingsView : section Backup (exporter .json / importer .json) + reset Supabase pour profile + entries + workouts + steps
- `app/components/SyncBootstrap.tsx` (Client, monte uniquement si auth) : migration auto localStorage → Supabase au premier login (idempotent via flag `zthapp-migrated-v1`)
- Deploy : repo GitHub `https://github.com/Lipinski-B/ZTHapp` + Vercel auto-deploy a chaque push
- URL prod : `https://zt-happ.vercel.app`
- Env vars Vercel : `NEXT_PUBLIC_SUPABASE_URL` + `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Supabase Auth → URL Configuration : Site URL = Vercel URL, Redirect URLs incluent localhost et Vercel
