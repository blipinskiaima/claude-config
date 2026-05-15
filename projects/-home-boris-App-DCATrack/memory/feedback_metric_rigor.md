---
name: feedback-metric-rigor
description: Métriques financières dans DCATrack doivent être honnêtes — préférer le chiffre rigoureux qui révèle la réalité au chiffre naïf qui flatte
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6d8f103e-07c2-4ff7-a6e0-8ebb434e76f3
---

Pour tout KPI financier ajouté à DCATrack, choisir la formule qui mesure honnêtement la réalité DCA, pas la version naïve textbook qui ment dans le contexte de versements mensuels.

**Why:** Lors de la session du 2026-05-14 sur la page /portfolio, Boris a choisi B sur D-A2 (drawdown ratio value/invested anchored à 1.0) plutôt que A (drawdown sur value brute). Raison : un drawdown calculé sur la valeur brute ment en DCA — un gros versement post-krach efface artificiellement le creux. Pareil pour la formule anchored 1.0 (décision outside-voice P0 #4) : si user n'est jamais remonté > 1.0, peak = ratio[0] sous-estime massivement le drawdown depuis break-even.

**How to apply:** Quand on ajoute un KPI à DCATrack (rendement annualisé, Sharpe, etc.), penser au cas pathologique (DCA en cours, période courte, série underwater, gros versement récent) et choisir la formule qui ne ment pas dans ces cas. Documenter la sémantique exposée à l'user dans le tooltip du KPI. Voir [[reference-portfolio-page]] pour exemple concret avec drawdown anchored.
