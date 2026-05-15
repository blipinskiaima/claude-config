---
name: DCATrack score formula
description: Formule du score "Soldes" 0-100 et seuils des verdicts
type: reference
---

**Formule du score "Soldes" — V2 percentile-based** (dans `app/lib/score.ts`) :

```typescript
score = dip_1m × 0.40  +  dip_6m × 0.25  +  dip_52w × 0.15  +  meanReversion × 0.20
// puis clamp 0..100, arrondi
```

**Variables** (toutes 0-100) :
- `dip_X` = rang percentile inversé du prix actuel dans la fenêtre X jours.
  - 100 = prix actuel = plus bas de la fenêtre
  - 0 = prix actuel = plus haut de la fenêtre
  - 50 = médiane
- `meanReversion = min(100, max(0, -zScore_200) × 50)` — bonus quand on est sous la SMA200, sature à z=-2

**Pourquoi V2 (changement clé du 1er mai 2026)** :
La V1 utilisait `drawdown × poids` (écart absolu au plus haut). En marché haussier proche de l'ATH 52w, un dip relatif récent de 2-3% donnait un score proche de 0 — indistinguable d'un ETF au plus haut absolu. Boris a observé que ETSZ avait chuté sur 2 semaines mais ressortait avec score 2 (vs PUST score 0 pourtant à l'ATH absolu).

Le percentile rank capture la position **relative** dans la fenêtre, peu importe la magnitude absolue. Il différencie correctement les 3 ETF même quand tous sont à <3% de leur ATH 52w.

**Pondération** :
- 40% dip_1m → signal principal "dip local sur 1 mois"
- 25% dip_6m → contexte semestriel
- 15% dip_52w → position annuelle
- 20% mean reversion → signal statistique sous SMA200

**Seuils des verdicts** :
- `score >= 50` → 🟢 **buy** — "DCA recommandé" — "C'est les soldes"
- `20 <= score < 50` → 🟡 **wait** — "Moment correct" — "Tu peux y aller, sans plus"
- `score < 20` → 🔴 **hold-off** — "Au plus haut" — "Mieux vaut attendre"

Note : en marché haussier (zScore positif, dip_52w < 20), le score plafonne ~30-45. Donc 🟢 nécessite soit une vraie correction, soit un retour sous la SMA200. C'est volontaire — les soldes existent vraiment quand le marché baisse.

**Validation V2 au 1er mai 2026** :
| ETF | dip_1m | dip_6m | dip_52w | zScore | Score | Verdict |
|---|---|---|---|---|---|---|
| PUST | 16 | 3 | 1 | +2.78 | 7 | 🔴 |
| ETSZ | 48 | 21 | 11 | +1.04 | **26** | 🟡 |
| PAEEM | 6 | 1 | 1 | +2.06 | 3 | 🔴 |

ETSZ ressort comme "moment correct" grâce à son dip récent (dip_1m=48 = médiane du dernier mois), conforme à l'intuition de Boris ("Europe a chuté 2 semaines, mieux que les autres").

**Référence académique** (de la recherche initiale) : "Proximity to the 52-week high and the risk-return trade-off" (ScienceDirect 2026) — la distance au 52w high prédit les retours futurs (anchoring effect mean reversion).
