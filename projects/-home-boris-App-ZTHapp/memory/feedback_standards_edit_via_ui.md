---
name: feedback-standards-edit-via-ui
description: "Pour modifier les standards sport (poids/reps cibles), preferer l'UI /parametres/standards au SQL UPDATE direct"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4575925d-af2f-47b9-840a-66c5a182f66d
---

Pour modifier les standards de programme sport (poids/reps cibles par exercice), editer via l'UI `/parametres/standards` plutot que generer du SQL UPDATE manuel.

**Why:** L'UI `StandardsView` (`app/parametres/standards/StandardsView.tsx`) offre l'edition formulaire (kilos x reps x variante) avec save direct vers Supabase (push + sync localStorage). Boris a confirme prefere cette voie le 2026-05-13. Le SQL cible ajoute friction (Supabase Studio, copier/coller du JSONB, risque de typo) et n'a de valeur qu'en backup.

**How to apply:** Quand Boris veut changer un poids/rep cible : pointer vers `/parametres/standards` et indiquer l'exo concerne. Le seed `scripts/seed-program-standards.sql` reste la source de verite initiale (cycle demarre, fichier docs/programme-actuel.md). Ne proposer du SQL UPDATE qu'en backup explicite : bootstrap initial, sync forcee apres corruption locale, ou si Boris demande explicitement.

Voir aussi : [[project_programme_actuel]] (tableau formate actuel).
