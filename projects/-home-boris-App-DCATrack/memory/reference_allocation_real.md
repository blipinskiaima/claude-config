---
name: Allouable réel (parts entières)
description: Algo computeAllocations() qui transforme les % cibles en parts entières + contrainte budget — display target % + real % + real € partout
type: reference
originSessionId: e464ea0f-682f-4446-bef2-c9cc5a8e2767
---
## Le problème résolu

L'utilisateur saisit un `Allocation.percent` (% cible) mais on ne peut acheter que des parts entières d'ETF. Avec budget=500€, target=50% (=250€) et prix=81€ → 3 parts (243€, 48.6%) plutôt que 4 parts (324€, 64.8%).

## L'algo

`app/lib/allocation.ts` → `computeAllocations(targets[], budget)` retourne `{ items, totalActualEur, remainingEur, ... }`.

3 étapes :
1. **Closest indépendant** : `shares = round(targetEur / price)` par ETF
2. **Contrainte budget** : si `Σ shares×price > budget`, demote greedy l'ETF avec coût d'arrondi minimal (ré-itère jusqu'à ≤ budget)
3. **Cas limites** : `targetEur < price/2` → `status: "too-expensive"` ; pas de prix → `status: "no-price"`

Validé sur cas math : `500€/50%/81€ → 3 parts, 243€, 48.6%` ✓

## Règle d'affichage (validée par Boris)

Partout où une allocation apparaît, on montre :
- **target %** (ce que l'user voulait)
- **real %** (résultat après arrondi, divergence ≥ 0.5% → format `50 → 48 %`)
- **real €** (prix final = shares × price)

**On ne montre PAS le target €** (le prix théorique). Boris l'a explicitement retiré : "ne faire apparaître que le montant allouable et non plus le montant théorique en plus".

## Flux de propagation des prix

- **Pages serveur** (`/vue`, `/favoris`) : fetch les prix server-side via `fetchJustETF()`, construit `priceByIsin: Record<string, number>`, passe en prop aux Client Components.
- **Pages client** (`/profil`) : hook `usePrices(isins)` (`app/lib/usePrices.ts`) qui appelle `/api/price/[isin]` (route légère qui wrappe `fetchJustETF` et retourne juste `latestQuote`).

## Composants qui utilisent l'algo

- `MonthlyExecutionsCard` (vue /vue) — bandeau "Allouable réel" + détail par ligne
- `StrategySummary` (vue /vue) — KPI "Allouable réel" + colonne real % avec divergence
- `StrategySynthesis` (page /profil) — KPI enrichi + tableau de répartition
- `DCAAmountBadge` (cartes ETF) — badge `50 → 48 % · 243 €`
- `AllocationPie` — parts dimensionnées par real %, centre affiche real total
- `ExecutionHistory` (/historique) — utilise `shares × price_at_execution` capturés à l'exécution

## Capture des vraies valeurs à l'exécution (Option B)

À chaque clic "Exécuté" dans `MonthlyExecutionsCard`, on stocke dans `dca_executions` :
- `shares: integer NULL` (nb de parts entières du moment)
- `price_at_execution: NUMERIC(12,4) NULL` (prix unitaire EUR)

Pré-migration les colonnes étaient inexistantes → les exécutions antérieures ont ces 2 champs à NULL → fallback sur target € théorique dans `/historique`.

**Migration appliquée le 2026-05-05** :
```sql
ALTER TABLE dca_executions
  ADD COLUMN IF NOT EXISTS shares INTEGER,
  ADD COLUMN IF NOT EXISTS price_at_execution NUMERIC(12, 4);
```
