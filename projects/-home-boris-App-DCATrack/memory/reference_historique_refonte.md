---
name: reference-historique-refonte
description: Page /historique refondue (2026-05-14) — narratif mois-par-mois + mini-embed /portfolio + grille events + accordéon allocation
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6d8f103e-07c2-4ff7-a6e0-8ebb434e76f3
---

Route `/historique` refondue (commits `e34233a` + `03ce2ce`).

**Architecture** : RSC `app/historique/page.tsx` orchestre auth + fetch profil actif (`is_active`) + fetch dca_executions + Promise.allSettled `fetchJustETF` + `buildPortfolioTimeline` pour la mini-série, puis passe tout à `ExecutionHistory` (Server Component) qui compose 5 sections.

**Composition visuelle (top→bottom)** :
1. Sub-header compact (profil + budget + fenêtre)
2. Mini-chart /portfolio embedded (`<PortfolioChart variant="mini">` wrapped dans `MiniChartLink` Client qui fait `router.push("/portfolio?range=1y")` au clic — pas `<Link>` à cause conflit prefetch + Recharts handlers)
3. 2 KPI cards : "N/12 mois tenus" (cf `countMonthsHeld`) + "Investi cumulé" (target € retiré, cf [[feedback-allocation-display]])
4. Calendrier ETF×12 mois enrichi : bandes events marché via `<colgroup><col style={{background}}>` + label event au-dessus de la colonne. Conserve `shares×prix` sous chaque coche (parts entières arrondies).
5. Journal narratif déroulé (`MonthlyJournal` + `MonthlyEntry` Client Components avec `useState` expand). Bouton "Tout déplier" en haut.
6. Accordéon `<details>` "Détail par ETF" (`AllocationAccordion`) collapsé par défaut — l'ancien tableau Allocation, déplacé hors du chemin principal.

**Composants nouveaux** :
- `app/components/MiniChartLink.tsx` (Client) — wrapper navigation router.push
- `app/components/MonthlyEntry.tsx` (Client) — card collapsible 1 mois
- `app/components/MonthlyJournal.tsx` (Client) — déroule N MonthlyEntry + tout déplier
- `app/components/AllocationAccordion.tsx` (Server) — `<details>` wrapper du tableau

**Lib étendue** : `app/lib/executions.ts` gagne `monthKey`, `groupExecutionsByMonth`, `countMonthsHeld`. 10 tests vitest dans `app/lib/__tests__/executions.test.ts` (edge cases multi-mois, multi-ETF, hors-fenêtre).

**Composant existant modifié** : `app/portfolio/PortfolioChart.tsx` gagne prop `variant?: "full"|"mini"` (DRY au lieu d'extract un nouveau MiniPortfolioChart). En mode `"mini"` : `dot={false}`, pas de Tooltip, pas de légende, pas de warnings, pas de popover modal (variant guard sur le `useState selected`).

**Drop** : `app/components/ExecutionsJournal.tsx` (remplacé par MonthlyJournal).

**Design doc + test plan** : `~/.gstack/projects/Lipinski-B-DCATrack/boris-main-design-20260514-110412.md` + `boris-main-eng-review-test-plan-20260514-112810.md`.

**Pattern réutilisable** : `variant` prop sur un composant existant > extraire un nouveau composant. DRY préservée. À garder en tête pour les futures réutilisations cross-page.
