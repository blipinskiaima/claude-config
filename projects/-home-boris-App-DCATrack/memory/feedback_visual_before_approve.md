---
name: feedback-visual-before-approve
description: "Pour DCATrack, générer un wireframe HTML visuel AVANT de demander l'approbation d'un design doc — pas juste un MD textuel"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6d8f103e-07c2-4ff7-a6e0-8ebb434e76f3
---

Pour toute session /office-hours ou /plan-design-review sur DCATrack qui touche à une vue UI, générer un wireframe HTML rough sketch (self-contained, inline CSS, ouvrable en navigateur) AVANT de demander "approuve le doc ?". Pas seulement écrire le design doc en MD.

**Why:** Confirmé le 2026-05-14 sur la refonte de /historique. Après 5 AUQ et un design doc APPROVED, Boris a réagi "je vois rien, c'est normal ?". Légitime : le doc MD était dans `~/.gstack/projects/` et le layout ASCII ne suffit pas pour juger la dispo réelle. Un wireframe HTML (généré en ~5 min) a immédiatement débloqué la validation finale ("PARFAIT"). Sur la session précédente /portfolio, j'avais lancé le dev server APRÈS le doc — workflow équivalent mais plus tardif. Le wireframe en amont aurait sauvé un tour.

**How to apply:** Quand le skill /office-hours arrive à Phase 5 (Design Doc) et que l'output touche une vue UI, faire le wireframe HTML AVANT la AUQ "Approve". Le skill a une section "Visual Sketch (UI ideas only)" qui le permet — ne pas la zapper. Style : rough sketch avec couleurs approximatives DCATrack (amber gradient, zinc backgrounds, mono pour chiffres) — pas un mockup polish, juste assez pour juger la disposition. Sauver dans `~/.gstack/projects/{slug}/` (pas /tmp/) pour référence future. Voir [[reference-portfolio-page]] et [[reference-historique-refonte]] pour exemples.
