---
name: Cascade cohorte /exploration — intégrée (v3.0.0, 2026-05-07)
description: Cascade des 7 étapes de filtrage (1300+ → ~454 samples) implémentée dans Tower v3 /exploration. Backend `compute_cohort_cascade()` + frontend `useCohortCascade` (TanStack Query lazy + debounce 250ms). Spec d'origine venait du projet Feature/.
type: project
originSessionId: ea114ee1-d89c-4b61-860a-ddba8a365c05
---
# Cascade cohorte /exploration — intégrée (v3.0.0)

Spec d'origine venait du projet `~/Pipeline/Feature/` (cohort-filters-cascade.md, target-specificity.md). Implémentée le 2026-05-07 sur main.

## Implémentation

| Couche | Fichier | Élément |
|---|---|---|
| Backend compute | `src/exploratory_compute.py` | `ExploratoryAnalysisService.compute_cohort_cascade()` `@lru_cache(64)` (+313 lignes) |
| Backend API | `backend/routers/exploration.py` | endpoint `/api/exploration/cohort-cascade` (+59 lignes) |
| Frontend hook | `frontend/src/lib/exploration.ts` | `useCohortCascade()` TanStack Query, fetch lazy `enabled` au premier open du panneau |
| Frontend hook | `frontend/src/lib/use-debounced-value.ts` | `useDebouncedValue(value, 250ms)` — pour ne refetch qu'après inactivité slider |
| Frontend UI | `frontend/src/pages/Exploration.tsx` | composant `CohortAlert` étendu avec dropdown cascade + KPI inline (target_spec, spec_realized, threshold) |

## Flow

```
Slider/filtre change
    │
    ▼
useDebouncedValue (250ms inactivity)
    │
    ▼
useCohortCascade (TanStack Query, enabled=open && mode==tables)
    │
    ▼
GET /api/exploration/cohort-cascade?centre=...&target_specificity=...&...
    │
    ▼
ExploratoryAnalysisService.compute_cohort_cascade() @lru_cache(64)
    │
    ▼
{ steps: [{label, count, delta}], n_model, n_healthy, n_cancer }
```

## Décisions / écarts vs spec d'origine

- **Lazy fetch** : la cascade ne fetch que si le panneau est ouvert ET en mode `tables` (pas `graphs`) — évite les calls inutiles. Spec d'origine ne précisait pas.
- **Debounce 250ms** : évite le bombardement quand on glisse un slider. Slider continu côté UI, fetch retardé.
- **Layout** : intégré dans `CohortAlert` (haut de page) plutôt qu'en bas de sidebar — meilleure visibilité dans la v3 React.
- **`@lru_cache(64)`** réutilise le pattern existant de `compute()` — caches par tuple d'arguments (centre, target_specificity, indications frozenset, …).

## Réutilisation pour Feature/

Si Feature/ veut un jour partager les 7 étapes côté Python plutôt que R, `compute_cohort_cascade()` est le point d'entrée canonique. Mais pour l'instant Feature/ reste sur R (validé bit-exact contre Michael).
