---
name: DCATrack Profil DCA feature
description: Page /profil pour configurer la stratégie DCA (budget + allocations %), donut chart, persistance localStorage
type: reference
---

**Route** : `/profil` — vue avec onglets, structure prête pour ajouter plus tard "Historique", "Préférences", etc.

**Onglet "Stratégie"** : 2 états gérés par `ProfileTabs.tsx` (Client Component) selon `loadStrategy()` :
- Pas de stratégie → `StrategyForm` (mode création)
- Stratégie sauvegardée → `StrategySynthesis` (vue) + bouton "Modifier" qui revient au `StrategyForm` (mode édition)

**Modèle** (V2 multi-profils) dans `app/lib/strategy.ts` :
```ts
type Allocation = { isin: string; percent: number }; // 0..100

type DCAProfile = {
  id: string;                 // uuid
  name: string;               // "PEA", "CTO", "Crypto"...
  budget: number;             // EUR / mois
  allocations: Allocation[];
  updatedAt: string;          // ISO
};

type DCAProfilesState = {
  profiles: DCAProfile[];
  activeId: string | null;
};
```

**Persistance** : localStorage clé `dcatrack-profiles`. Migration auto depuis l'ancienne clé `dcatrack-strategy` (single profile) → premier profil nommé "PEA" + actif. La clé legacy est supprimée après migration.

**Helpers** : `loadProfiles`, `saveProfiles`, `getActiveProfile`, `setActiveProfile`, `upsertProfile`, `deleteProfile`, `genProfileId`, `isProfileValid`. Compat ascendante : `loadStrategy`/`saveStrategy`/`clearStrategy`/`DCAStrategy` continuent de fonctionner et opèrent sur le profil actif.

**Hook `useStrategy()`** (`app/lib/useStrategy.ts`) : Client hook qui expose `{ strategy, mounted }`. Écoute :
- l'event `storage` (modifs cross-tab)
- un custom event `dcatrack-strategy-updated` émis par `notifyStrategyChange()` après save/clear (même tab — l'event `storage` ne fire pas dans le même tab).
ProfileTabs appelle `notifyStrategyChange()` après save/clear pour que tous les hooks de la page se rafraîchissent.

**Connexion Profil ↔ Tracker** :
- `StrategySummary` Client Component sur la home (`/`). Si stratégie définie → mini donut (conic-gradient SVG-free, ultra léger), liste compacte d'ETF avec %, montant mensuel, CTA "↓ Voir les indicateurs de cette stratégie" qui charge la sélection dans le tracker via URL params (`router.replace`).
- `DCAAmountBadge` Client Component sur chaque `ETFCard` → affiche `↻ DCA X €` si l'ISIN est dans la stratégie.
- `ETFSelector` ajoute un preset "Stratégie" (premier dans la barre) si une stratégie existe. `detectPreset(isins, strategyIsins?)` reconnaît ce preset.
- Toutes ces connexions se font côté client (localStorage) — le Server Component (la page) ne connaît pas la stratégie.

**StrategyForm.tsx** :
- Input budget (number, step=10)
- Liste d'ETF avec, pour chaque : slider 0-100 + input numérique step="any" + bouton "→100" (fill remaining) + bouton ✕ (retirer) + montant calculé "≈ X € / mois"
- Picker d'ETF (réutilise la même UX que ETFSelector : dropdown avec recherche + ISIN libre + bouton Fermer + pointerdown listener pour Android)
- Bouton "⚖ Équilibrer" : répartit 100% équitablement, **arrondi à 0.1** pour éviter `33.33 + 0.01 = 33.339999999999996` (floating-point JS)
- Validation live : indicateur "Total: 100% ✓" vert OU "Total: X% (à ajuster pour atteindre 100%)" orange
- `Sauvegarder` disabled tant que `isStrategyValid()` est false
- En mode édition : bouton Annuler en plus

**StrategySynthesis.tsx** :
- `AllocationPie` : donut Recharts (innerRadius 55%, outerRadius 95%, paddingAngle 2, stroke = `var(--pie-stroke)` qui s'adapte au thème). Centre = montant total + nb ETF.
- KPIs : Budget mensuel, Part la + grosse, Part la + petite, Annualisé (×12), Mise à jour
- Tableau détail : 1 ligne par ETF triées par % décroissant, avec ticker (Link vers `/etf/[isin]`), badges PEA / custom, ISIN, %, montant €, mini-bar de couleur
- Boutons : "Réinitialiser" (avec `window.confirm`) + "Modifier la stratégie"

**Nav** : `ProfileLink.tsx` (icône utilisateur) ajouté dans le header de la home et de la page détail. Click → `/profil`.

**Gotchas / patterns** :
- Server Component shell pour la route, Client Component pour la logique (localStorage = browser-only)
- Le composant Tabs est extensible : changer `Tab = "strategie"` en `"strategie" | "historique"` quand on ajoute le 2ème onglet
- Les couleurs des slices viennent de `colorFor(ticker)` (lib/colors.ts) — cohérent avec le reste de l'app
- Le donut central utilise `pointer-events-none` sur l'overlay text pour ne pas bloquer les hovers Recharts
