---
name: feedback-no-market-timing
description: "DCATrack n'est plus une app de timing — c'est un pur tracker DCA avec encouragement à la régularité"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d7bd71ce-6a16-4e5f-a225-1a237559f1fb
---

DCATrack abandonne définitivement le rôle de "timer de marché". Plus de score DCA composite (drawdown + mean reversion), plus de verdicts "Acheter / Attendre / Au plus haut", plus de conseil sur le bon moment d'exécution.

**Why:** Boris a explicitement repositionné le produit (session 2026-05-20) : "L'objectif de l'application va être avant tout d'aider l'utilisateur à tracer au mieux son DCA, sans essayer de donner des conseils financiers de déterminer si oui ou non c'est le bon moment, je ne veux plus ça." Évite la responsabilité de conseil financier, recentre sur la valeur réelle : la discipline.

**How to apply:**
- Quand tu vois "score DCA", "badge buy/wait/hold", "au plus haut", "mean reversion" → c'est à retirer ou remplacer par une feature de **suivi de régularité** (streaks, % de mois respectés, versement cumulé, prochain DCA prévu, etc.).
- Le nouveau ton est **gamification positive** : féliciter l'utilisateur qui tient son DCA, l'inciter à exécuter régulièrement. Inspirations : Duolingo streaks, Strava récap, habit trackers.
- La memory `feedback_independent_indicators.md` ("chaque ETF est évalué indépendamment") devient obsolète — elle parlait du score, qui disparaît.
- Pages impactées : `/vue` (badges score retirés), `/etf/[isin]` (section "Décomposition du score" à supprimer ou remplacer), `/tracker` (ne plus trier par score), lib/score.ts (à retirer).
- Lib à conserver : `lib/allocation.ts`, `lib/portfolio-timeline.ts`, `lib/executions.ts`, `lib/strategy.ts` — c'est de la mécanique DCA pure, indépendante du timing.
