---
name: Data sources for ETF analysis
description: How to cross-reference ETF data - justETF for historical, stockanalysis for real-time, avoid single source
type: feedback
---

Toujours croiser les sources pour les données ETF. justETF a 2 jours de retard sur la NAV, ce qui peut fausser les calculs de solde.

**Why:** On a eu un ratio LQQ/PUST de 3x (faux) à cause du prix PUST de justETF qui avait 2 jours de retard (83.79€ au lieu de 81.17€). Le ratio réel était 2.1x.

**How to apply:**
- **Prix actuel** → stockanalysis.com (cours bourse temps réel)
- **Pics historiques / NAV** → justETF (librairie `justetf-scraping`)
- **Perf annualisée** → stockanalysis.com
- **Boursorama / Bourse Direct** → JS-rendered, souvent inaccessible par WebFetch
- Toujours vérifier la date des données justETF avant de conclure
