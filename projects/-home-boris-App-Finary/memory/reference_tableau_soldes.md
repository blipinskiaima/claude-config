---
name: Tableau des soldes ETF
description: Comparaison des ETF PEA vs leur plus haut sur 4 fenêtres temporelles - données croisées justETF + stockanalysis
type: reference
---

## Tableau des soldes — 27 mars 2026

| ETF | Prix 27/3 | vs High 52w | vs High 6m | vs High YTD | vs High 1m |
|---|---|---|---|---|---|
| Amundi Nasdaq-100 2x Lev (LQQ) | 1,244€ | -21.8% | -21.8% | -18.8% | -13.5% |
| Amundi Euro Stoxx Banks (BNKE) | 289€ | -16.4% | -16.4% | -16.4% | -14.9% |
| Amundi PEA Nasdaq-100 (PUST) | 81€ | -10.2% | -10.2% | -8.6% | -6.3% |
| Amundi PEA Emerging (PAEEM) | 29€ | -9.9% | -9.9% | -9.9% | -9.9% |
| BNP STOXX Europe 600 (ETZ) | 19€ | -9.0% | -9.0% | -9.0% | -9.0% |
| Amundi PEA S&P 500 (PSP5) | 49€ | -6.4% | -6.4% | -6.4% | -3.8% |
| Amundi MSCI World (CW8) | 585€ | -6.3% | -6.3% | -6.3% | -5.3% |

Méthode : prix cours bourse (stockanalysis) vs plus haut de chaque fenêtre (justETF NAV).

### Sources et fiabilité
- **justETF** : NAV (valeur liquidative), 2 jours de retard, meilleur pour les pics historiques
- **stockanalysis.com** : cours bourse temps réel, meilleur pour le prix actuel
- Croiser les deux donne les données les plus fiables
- Librairie Python `justetf-scraping` installée dans le venv pour accès programmatique
