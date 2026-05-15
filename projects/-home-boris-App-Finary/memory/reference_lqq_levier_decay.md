---
name: LQQ levier 2x et volatility decay
description: Analyse du levier 2x quotidien du LQQ - ratio réel vs PUST, explication du decay, quand il se manifeste
type: reference
---

## LQQ = Nasdaq-100 x2 quotidien

Le LQQ (FR0010342592) réplique 2x le rendement QUOTIDIEN du Nasdaq-100. Ce n'est PAS 2x sur la période.

### Ratio LQQ/PUST observé au 27 mars 2026

| Fenêtre | PUST (x1) | LQQ (x2) | Ratio |
|---|---|---|---|
| vs High 52w | -10.2% | -21.8% | 2.1x |
| vs High 6m | -10.2% | -21.8% | 2.1x |
| vs High YTD | -8.6% | -18.8% | 2.2x |
| vs High 1m | -6.3% | -13.5% | 2.1x |

Au 27 mars 2026, le ratio est stable à ~2.1x → decay minime car le Nasdaq est en baisse directionnelle.

### Quand le decay se manifeste

| Scénario marché | Ratio réel | Decay ? |
|---|---|---|
| Baisse en ligne droite | ~2.0x | Non |
| Hausse en ligne droite | ~2.0x | Non |
| Allers-retours (volatilité) | 2.5-3x+ | Oui, perte sèche |
| Marché flat volatile | ∞ (perte sur LQQ, 0 sur PUST) | Oui, maximum |

### Exemple concret de decay
Jour 1 : Nasdaq -5% → PUST 95€, LQQ 90€
Jour 2 : Nasdaq +5% → PUST 99.75€, LQQ 94.50€
Bilan : PUST -0.25%, LQQ -5.50% → decay = -5.0 points

### Implication pour le DCA
- LQQ à 1,244€ l'unité → achat possible 1x tous les 2.5 mois avec un DCA 500€
- En phase de baisse directionnelle (comme actuellement), le ratio est propre ~2x
- En phase volatile, le decay va se creuser
- Prix unitaire élevé rend le DCA mensuel de 500€ compliqué
