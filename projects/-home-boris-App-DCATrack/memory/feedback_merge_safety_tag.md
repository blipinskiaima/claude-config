---
name: Safety tag before merging UI-global features
description: Boris veut un filet de rollback (tag pre-X) avant de merger des features qui touchent layout/nav/globalCSS dans DCATrack
type: feedback
originSessionId: d4e22a2f-03a6-4048-9576-70ff40157692
---
Pour les merges dans DCATrack qui touchent `app/layout.tsx`, `app/globals.css`,
la nav (SidePanel, BottomNav) ou tout composant racine global : créer un tag
git `pre-<feature>` sur main AVANT le merge, fast-forward le merge (style du
repo, pas de --no-ff).

**Why:** Boris a explicitement demandé "merger mais je veux pouvoir revenir
en arrière si ça casse l'app" sur la feature page-fade-in transitions
(2026-05-15). Vercel auto-deploy depuis main → un layout cassé = downtime
immédiat sur dcatrack.

**How to apply:**
- Avant merge feature UI-globale : `git tag pre-<feature-name> main`
- Merge en `--ff-only` (préserve l'historique propre du repo, pas de merge commits)
- Donner les 2 commandes de rollback explicites à Boris dans le récap final :
  - Soft : `git revert <commit>` (ou plage de commits)
  - Hard : `git reset --hard pre-<feature-name>`
- Pas nécessaire pour features non-UI (lib/, scripts/, supabase migrations).
