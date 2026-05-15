---
name: project-programme-actuel
description: "Le tableau programme musculation à jour de Boris (15 exos × 3 sessions, kilos × reps + alternatives choisies) vit dans /home/boris/App/ZTHapp/docs/programme-actuel.md. Quand Boris demande \"tableau programme\" → lire ce fichier et le restituer."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6a81153f-c59d-435a-98a9-cd1b5d113665
---

Le **tableau programme à jour** de Boris est maintenu dans `/home/boris/App/ZTHapp/docs/programme-actuel.md`.

Quand Boris demande **"tableau programme"**, **"mon programme"**, **"où en est mon programme"** → lire ce fichier et le restituer formaté.

**Why:** Boris veut un endroit unique et stable pour son programme courant, qu'il peut consulter à tout moment via Claude. Tient compte des alternatives choisies (variantId) et des dernières mises à jour kilos/reps.

**How to apply:**
- Source de vérité applicative : table Supabase `program_standards` (cf. [[reference-program-standards-app]]).
- Source de vérité documentaire : `docs/programme-actuel.md` (formaté lisible).
- Seed reproductible : `scripts/seed-program-standards.sql`.
- **Quand les standards changent**, mettre à jour les **3 fichiers** dans cet ordre : (1) doc programme-actuel.md, (2) seed-program-standards.sql, (3) push à l'app via UI ou via Supabase Studio.
- L'app a une page d'édition à `/parametres/standards` qui pousse vers Supabase via `pushUserProgram()` ; le seed reste utile pour reseed à zéro.

Liens : [[project-overview]] · [[project-phasing]] · [[feedback-paliers-haltere]]
