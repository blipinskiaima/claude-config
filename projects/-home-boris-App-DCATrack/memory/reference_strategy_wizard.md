---
name: DCATrack Strategy Wizard
description: Wizard 7 étapes pour créer un profil DCA, catalogue 28 ETF, 7 marchés (US/Europe/France/Emerging/Asia/World/Sectoriel), filtrage strict par support
type: reference
originSessionId: e464ea0f-682f-4446-bef2-c9cc5a8e2767
---
**Wizard de création** : alternative guidée au formulaire manuel. Actif depuis "+ Nouvelle stratégie" dans `ProfileList`.

**Fichiers** :
- `app/components/StrategyWizard.tsx` — state machine 7 steps + `Step1Markets` (boutons multi avec ordre de préférence) + `ChoiceGrid` générique
- `app/lib/wizard.ts` — types, MARKETS/RISKS/EXPERIENCES/SUPPORTS/BUDGETS/WEIGHTINGS, `filterWatchlist`, `preselectFromPool`, `buildDraftProfile`
- `app/lib/etfs.ts` — `ETFConfig` (markets, riskLevel, complexity, supports, favori, pea), `WATCHLIST` à 28 ETF

**7 marchés (depuis 2026-05-05)** :

| value | label | count | exemples |
|---|---|---|---|
| US | USA | 10 | PSP5, SXR8, VUSA, PUST |
| Europe | Europe | 5 | ETSZ, BNKE, PCEU |
| **France** | France | 2 | CAC, CACC (CAC 40 pur) |
| Emerging | Émergents | 3 | PAEEM, AEEM |
| **Asia** | Asie | 1 | PAASI (Asie émergente) |
| World | Monde | 10 | CW8, WPEA, EUNL |
| Sectoriel | Sectoriel | 4 | PUST, LQQ, BNKE |

**Tags ETF** : codés en dur dans WATCHLIST. CAC/CACC ont `["Europe", "France"]`, PAASI a `["Emerging", "Asia"]` — l'ETF apparaît si l'user choisit l'un OU l'autre.

**Filtrage cumulatif** (`filterWatchlist`) : intersection markets ∩ + rank risk ≤ + rank complexity ≤ + support strict.

**Pondération** (étape 7) :
- `equal` — équirépartition simple
- `conviction` — buckets dégressifs par marché préféré : 1 marché=[100], 2=[65,35], 3=[50,30,20], 4=[40,30,20,10], 5+=[35,25,20,12,8]

**buildDraftProfile** retourne un `DCAProfile` avec `id`, `name = "Stratégie {support}"`, `budget`, `allocations` (% qui somment à 100), `riskProfile`, `support`.

**preselectFromPool** : à l'étape 6, pré-coche `suggestedEtfCount(budget)` ETF en round-robin sur les marchés préférés (favori=true en priorité).
