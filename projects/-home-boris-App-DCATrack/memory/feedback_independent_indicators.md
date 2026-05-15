---
name: DCATrack indicators are independent per ETF
description: Pas de verdict global ni de pondération - chaque ETF a son propre indicateur autonome
type: feedback
---

**Règle : Chaque ETF est évalué INDÉPENDAMMENT. Pas de verdict global, pas de score agrégé.**

**Why:** Boris échelonne ses achats DCA dans le mois en fonction des signaux propres à chaque ETF. Exemple concret donné par Boris : "le J3 du mois je mets 50% sur un ETF, le J7 je mets 35% sur un autre et le J21 je mets le reste sur le dernier ETF car mes indicateurs m'ont indiqué que pour les ETF en question, les JX ont été les meilleurs au moment donné."

**How to apply:**
- Chaque carte ETF dans le dashboard contient son propre score + son propre verdict 🟢🟡🔴
- Ne PAS ajouter un bandeau "verdict global moyen" en haut de la page
- Si une fonctionnalité de pondération par capital DCA est demandée, garder les signaux indépendants — la pondération sert juste au calcul des montants à investir, pas au signal
- Le seul élément global du dashboard est le bouton "Actualiser" (refresh des 3 fetchs en cache)
- Si Boris demande un suivi du portefeuille agrégé, c'est une autre app (pas DCATrack — voir mémoire Finary)
