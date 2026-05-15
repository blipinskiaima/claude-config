---
name: reference-portfolio-page
description: "Page /portfolio (RSC) avec timeline annotée valeur vs investi, KPI bar, dots achats cliquables, événements marché en surimpression"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6d8f103e-07c2-4ff7-a6e0-8ebb434e76f3
---

Route `/portfolio` ajoutée le 2026-05-14 (commits 454b393 + e4fff24).

**Architecture** : RSC `app/portfolio/page.tsx` orchestre auth + résolution profil (URL searchParam, default = is_active) + Promise.allSettled fetch + appel `buildPortfolioTimeline` + props vers Client Components.

**Core lib** : `app/lib/portfolio-timeline.ts` expose `buildPortfolioTimeline`, `forwardFill`, `computeDrawdownRatio` (anchored 1.0), `isTradingDay`, `downsampleWeekly`. Fonctions pures, testées dans `app/lib/__tests__/portfolio-timeline.test.ts` (28 cases vitest). Réutilise `fetchJustETF` de `app/lib/justetf.ts` (pas de duplication).

**Décisions structurelles** : drawdown calculé sur ratio value/invested anchored à 1.0 (cf [[feedback-metric-rigor]]), Promise.allSettled pour résilience fetch 28 ETF, trading-day cadence (Mon-Fri), filtre SQL `shares NOT NULL` pour ignorer executions pre-mai 2026 incomplètes, downsample hebdo si plage "Tout" > 365j, popover détail achat inclut profileId+profileName pour mode "Tous profils".

**Pattern réutilisable** : RSC + Promise.allSettled + propagation `failedIsins[]` / `truncatedIsins[]` en warning UI = template pour toute page future qui fetche N ressources externes en parallèle.

**Design doc + test plan** archivés dans `~/.gstack/projects/Lipinski-B-DCATrack/boris-main-design-20260514-101154.md` et `boris-main-eng-review-test-plan-20260514-102710.md`.
