---
name: feedback-workflow-skills
description: "Pour features DCATrack non-triviales, enchaîner /office-hours → /plan-eng-review → code marche bien pour Boris"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6d8f103e-07c2-4ff7-a6e0-8ebb434e76f3
---

Pour une feature DCATrack qui touche plusieurs fichiers ou implique des décisions sémantiques (KPI, algo, structure data), proposer le workflow /office-hours → /plan-eng-review → implémentation.

**Why:** Validé 2× consécutivement le 2026-05-14 :
- Session /portfolio : office-hours a calé le scope, plan-eng-review a sorti 14 issues + outside voice 8 findings dont 3 P0 (drawdown loss-regime, range justETF, shares=null pré-migration). Boris a choisi "boil the lake D".
- Session /historique refonte : office-hours a calé l'angle (B+C compose + A+D narratif), plan-eng-review a sorti 1 finding scope (Step 0 variant prop) + outside voice 10 findings dont 5 P0 (doc stale, `<Link>` autour Recharts, fetch cost, `<colgroup>` pour bandes events, `<details>` perdu sur re-render RSC). Boris a re-choisi "boil the lake D".

**ROI confirmé** : outside voice = 2 min de CC pour 8-10 findings dont 3-5 P0 critiques par session. Sans ce workflow, ces bugs seraient découverts au moment du code (1h+ de debug par P0). Boris accepte systématiquement +20 min CC pour zéro trou connu.

**How to apply:** Avant d'attaquer une feature non-triviale, suggérer /office-hours. Une fois le design doc APPROVED, enchaîner /plan-eng-review (l'outside-voice via subagent en Phase finale est précieux — 8/8 findings utiles dans la session précédente). Pour fix simple ou refactor mineur, skip ce workflow et coder directement. Le pattern de décision via AskUserQuestion (1 décision = 1 AUQ avec recommendation+stakes+options) marche bien — Boris répond rapidement par lettre/numéro et interrompt si tour trop long.
