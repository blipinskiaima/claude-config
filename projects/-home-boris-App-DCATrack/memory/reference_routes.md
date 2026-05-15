---
name: DCATrack routes & UX
description: Architecture des pages, sélecteur d'ETF, vue détaillée, persistance d'état
type: reference
---

**Routes** :
- `/` — Vue standard. Affiche les ETF de la sélection courante (3 favoris par défaut).
- `/etf/[isin]` — Vue détaillée pour un seul ETF. Statiquement pré-rendue pour les 9 ISIN de la watchlist (`generateStaticParams`).

**État de sélection (vue standard)** :
- URL param `?selection=PUST,ETSZ,PAEEM,LQQ` (tickers, ISIN connus, ou ISIN custom). Si absent → preset PEA par défaut.
- Server Component lit `searchParams` → fetch parallèle des ETF correspondants → rendu des cards.
- `parseSelection(raw)` (dans `app/lib/etfs.ts`) accepte tickers, ISIN connus ET ISIN libres matchant le format standard.
- `selectionToParam(isins)` reconvertit en tickers (si connus) pour une URL plus lisible.

**3 presets** dans `app/lib/etfs.ts` :
- `PEA_PRESET` (3 ETF actifs : PUST, ETSZ, PAEEM) — par défaut
- `FAVORITES_PRESET` (9 ETF de la watchlist complète)
- "custom" = sélection ne matchant ni l'un ni l'autre (détecté par `detectPreset`)

`isValidIsin(s)` valide le format ISIN standard (2 lettres + 9 alphanum + 1 chiffre).
`customEtfConfig(isin)` génère un ETFConfig minimal pour un ISIN libre (catégorie "Custom", non-PEA).

**Sélecteur d'ETF (`ETFSelector.tsx`)** :
- En haut : switcher de presets PEA / Favoris / Custom (auto-détecté).
  Click "Custom" ouvre directement le dropdown sans toucher la sélection.
- Pills horizontaux des ETF actifs avec ✕ pour retirer (dernier ETF non retirable).
- Bouton "+ Ajouter un ETF" → dropdown avec barre de recherche.
- Search filtre sur ticker, name, shortName, category, ISIN (case-insensitive).
- Si la query matche `isValidIsin` mais n'est pas dans la watchlist → suggestion "Ajouter cet ISIN custom" en haut du dropdown (badge `CUSTOM` orange dans la pill).
- Click sur une option → ajoute, vide le query, dropdown reste ouvert pour ajouts multiples.
- Bouton "Fermer" en footer du dropdown (garde-fou mobile).
- Outside click / Escape → ferme le dropdown. **Important** : `pointerdown` + `touchstart` (pas `mousedown`) sinon Android tactile ne ferme pas.
- Z-index 40 sur le container, 50 sur le dropdown — nécessaire car les cards en `backdrop-blur` créent des stacking contexts qui passent au-dessus de z-30.

**Watchlist (9 ETF)** dans `app/lib/etfs.ts` → constant `WATCHLIST` :
- Favoris : PUST, ETSZ, PAEEM
- PEA non-favoris : PSP5, WPEA, SPEA
- CTO (non-PEA) : CW8, LQQ, BNKE
- Source : alignée sur `reference_tableau_recap.md` du projet Finary

**Vue détaillée (`/etf/[isin]/page.tsx`)** :
- Header avec ticker, badges (catégorie + PEA/CTO), nom complet, ISIN, prix actuel, perfs YTD + 1 an
- `ETFSwitcher` : bouton horizontal pour basculer vers un autre ETF de la watchlist (ticker compact + dot couleur)
- `DetailChart` : AreaChart Recharts 1 an avec SMA200 superposée + lignes ATH 52w/6m/1m + tooltip date FR + axes labellés
- Card verdict (🟢🟡🔴 + score + 3 dips)
- `ScoreBreakdown` : par composant (dip_1m, dip_6m, dip_52w, meanReversion) avec valeur × poids = contribution + barre de progression
- 4 KPIs : ATH 52w/6m/1m + z-score commenté

**Couleurs des ETF** : map `ETF_COLORS` dans `app/lib/colors.ts`. Chaque ETF a sa couleur d'accent (orange pour PUST, bleu pour ETSZ, violet pour PAEEM, etc.). Réutilisable partout via `colorFor(ticker)`.

**Cards cliquables** :
- `ETFCard` est wrappé en `<Link href="/etf/${isin}">`.
- Indicateur visuel : flèche → apparaît au hover du header.
- Pas de nested anchors (la card entière est le lien).
