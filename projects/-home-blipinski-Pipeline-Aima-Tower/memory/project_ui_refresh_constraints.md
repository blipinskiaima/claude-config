---
name: Refonte UI Tower — contraintes et carte blanche
description: Contraintes de la refonte front-end Aima Tower (branche feat/ui-refresh), incluant la cohérence avec platform.aima-diagnostics.com et l'autorisation de réécriture totale.
type: project
originSessionId: e7cf4774-71b7-41ae-a4bc-9bc5a148a559
---
Refonte UI Aima Tower lancée le 2026-05-05 sur branche `feat/ui-refresh` (tag de retour : `pre-ui-refresh` sur commit `ed13d27`). Main reste l'app stable v2.2.0.

**Why:** Boris veut une UI moderne/sexy à la pointe, l'actuelle (Dash + dash-bootstrap-components) est jugée trop limitée visuellement. Tower est un spin-off de la plateforme principale https://platform.aima-diagnostics.com/ → cohérence visuelle attendue.

**Charte graphique parente (extraite du bundle Vite/CSS de platform.aima-diagnostics.com) :**
- Stack : Vite + React + Tailwind CSS
- Palette principale : Indigo (#4f46e5, #6366f1, #3730a3) + Emerald (#10b981)
- Accents : Pink/Rose, Purple, Amber
- Typo : system-ui, Avenir, Helvetica (pas de webfont custom)
- Dark mode natif, anti-FOUC via localStorage `theme-preference`
- Logo : `/aima-logo.png`

**Carte blanche utilisateur (2026-05-05) :**
- Aucune contrainte de temps ni de budget
- Réécriture totale autorisée si nécessaire (Dash → Vite/React/Tailwind + FastAPI backend)
- Comportement de l'app **strictement intact** (logique métier, callbacks, services DuckDB, accès aux 5 bases) — c'est la SEULE limite dure

**How to apply:**
- Privilégier les solutions qui rapprochent Tower de la stack platform.aima-diagnostics.com (Tailwind > custom CSS, palette Indigo/Emerald > random Plotly)
- Toute proposition de refonte doit garantir la non-régression fonctionnelle (tests cell-by-cell vs R, callbacks pattern-matching, services DuckDB read-only avec retry backoff)
- Travailler exclusivement sur `feat/ui-refresh`, ne jamais merger dans `main` sans validation explicite
- Possibilité d'une stratégie progressive (MVP visuel sur 1 page → migration page par page) ou big-bang (refonte totale) — à arbitrer avec Boris
