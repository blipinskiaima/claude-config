---
name: Supabase schema (3 tables)
description: État du schéma Supabase au 2026-05-05 — dca_profiles, dca_executions (étendu shares/price), user_favorites (nouveau)
type: reference
originSessionId: e464ea0f-682f-4446-bef2-c9cc5a8e2767
---
Schéma DB Supabase (toutes les tables ont RLS activée, accès par `auth.uid()`).

## `dca_profiles`

Profils DCA de l'utilisateur. 1 trigger SQL `enforce_single_active_profile` désactive les autres au passage `is_active = true`.

```
id, user_id, name, budget (NUMERIC), allocations (JSONB),
risk_profile, support, is_active, created_at, updated_at
```

`allocations` = `[{ isin: string, percent: number }, ...]`.

## `dca_executions`

1 ligne = 1 ETF coché un mois donné. Toggle = INSERT / DELETE.

**Schéma actuel après migration 2026-05-05** :
```
id, user_id, profile_id, isin,
period_year, period_month, executed_at, created_at,
shares INTEGER NULL,                    -- depuis 2026-05-05
price_at_execution NUMERIC(12,4) NULL   -- depuis 2026-05-05
```

Les colonnes `shares` + `price_at_execution` sont capturées à chaque clic "Exécuté" dans `MonthlyExecutionsCard` (depuis `realByIsin.get(isin)` calculé via `computeAllocations`). NULL pour les exécutions antérieures à la migration → fallback sur target théorique dans `/historique`.

Migration SQL appliquée :
```sql
ALTER TABLE dca_executions
  ADD COLUMN IF NOT EXISTS shares INTEGER,
  ADD COLUMN IF NOT EXISTS price_at_execution NUMERIC(12, 4);
```

## `user_favorites` (nouveau 2026-05-05)

Liste curated par utilisateur des ETF affichés sur `/favoris` (recherche WATCHLIST + ISIN libre, bouton × pour retirer).

```sql
CREATE TABLE user_favorites (
  user_id    UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  isin       TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, isin)
);

ALTER TABLE user_favorites ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users manage their own favorites"
  ON user_favorites FOR ALL
  USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
```

Server actions dans `app/favoris/actions.ts` : `addFavorite(formData)` (normalise ISIN avec regex puis upsert) et `removeFavorite(formData)` (delete par PK).

## Migrations versionnées

Dans `supabase/migrations/` (créé 2026-05-05) :
- `20260505_add_shares_price_to_dca_executions.sql`
- `20260505_add_user_favorites.sql`

**Pas de runner automatique** : SQL à exécuter manuellement dans Supabase Dashboard → SQL Editor. Les 2 migrations ci-dessus ont été appliquées.

## Tables/concepts NON utilisés Supabase

Les **prix** ne sont PAS stockés. Pas de table `etf_prices`. Le catalogue d'ETF (28 entrées) est hardcodé dans `app/lib/etfs.ts:WATCHLIST`, pas en BDD.
