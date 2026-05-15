---
name: Règle d'affichage des allocations
description: Boris veut target % + real % + real € visible partout, mais PAS le target € (montant théorique)
type: feedback
originSessionId: e464ea0f-682f-4446-bef2-c9cc5a8e2767
---
Quand un % d'allocation apparaît dans l'UI (cartes ETF, bandeau DCA du mois, synthèse profil, badge, camembert…), montrer :

- ✅ **target %** — la cible voulue par l'utilisateur (ex `50 %`)
- ✅ **real %** — la vraie après arrondi en parts entières (ex `48 %`, en format `50 → 48 %` quand divergence ≥ 0.5 %)
- ✅ **real €** — le prix final = `shares × prix unitaire` (ex `243 €`)
- ❌ **target €** (le montant théorique = `budget × percent / 100`) — ne plus afficher

**Why:** Boris l'a explicitement formulé : *"il faudrait ne faire apparaître que le montant allouable et non plus le montant théorique en plus, on veut le pourcentage théorique voulu, le pourcentage alloué en conséquence et le prix final, non plus le prix théorique"*. Le target € créait du bruit visuel sans valeur ajoutée — le user connaît déjà la cible via le %.

**How to apply:**
- Format compact recommandé : `50 → 48 % · 243 €` (ou `50 % · 243 €` si pas de divergence)
- Tooltip peut détailler : `Cible 50.0 % → réel 48.6 % · 3 parts × 81 € = 243 €`
- Cas "trop cher" (target_eur < price/2) : afficher `50 % · trop cher`
- Cas "no-price" (chargement / custom ETF) : afficher juste `50 %` (gris, neutre)
- **Exception légitime** : la KPI globale "Allouable réel : X € / Y € budget" reste OK car le second nombre est le **budget** (référence max), pas un target théorique d'ETF.
- **Camembert** : parts dimensionnées par `real %` (pas target %), parts à 0 (too-expensive) filtrées pour éviter artefacts recharts. Centre affiche le real total avec sous-titre `N ETF · / Y € budget`.
