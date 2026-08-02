# Context — ZTHapp — 2026-08-02

**Branche** : main
**Dernier commit** : feb0e8c — Docs: CLAUDE.md à jour (état prod)
**Status** : clean (aucun code touché cette session)

## Où j'en suis
Semaine 1 du programme ZTH bouclée (27-31/07) : adhérence nutrition parfaite et
rampe sport S1 passée sur les 3 séances. Session consacrée au suivi, pas au code —
logs des 3 séances avec verdicts, 6 standards montés, correction du référentiel riz
sur étiquette réelle, remplacement des mollets par des dips, fixation du vocabulaire
« palier » et clarification du passage palier 1 → palier 2. Tout est écrit dans les
skills daily-diet et weekly-muscu (4 fichiers de références).

## Ce qui marche / ce qui foire
- ✓ Nutrition 5/5 jours conformes, zéro resto, zéro écart — 2015 kcal/j réels,
  déficit 286, ~0.26 kg de gras. Première semaine tenue intégralement.
- ✓ Rampe S1 complète (Upper A 27/07 · Lower 30/07 · Upper B 31/07). Standards montés :
  curl 12→14, RDL 16→18, oiseau 6→8, latérales S3 14→16, upright row Upper B →12/14/16.
- ✓ Quantités figées par Boris : riz 170 g / huile 5 g (a refusé la version 160/7).
  Passage au palier 2 = un seul chiffre bouge, riz 170 → 110 g.
- ✗ `app/lib/foods.ts` toujours sur le riz générique (340 kcal / L 1.2) au lieu de
  l'étiquette réelle Curti (349 / L 0) — chip de tâche en attente, non lancée.
- ✗ Absence 03 → 09/08 : aucune séance possible, Boris documente ses repas lui-même.
  Calories inchangées à 2001, aucune compensation au retour.
- ✗ Divergence PDF/Excel non tranchée : pour le P3, le PDF prescrit +100/+200 kcal en
  cas de stagnation, l'Excel offre −500 (palier 2). À arbitrer avant la décision.

## Prochaine étape
Dimanche 09/08 au retour — bilan de fin de palier 1 (J14) : récupérer le poids le plus
bas de la semaine + le tour de taille, puis décider entre maintien à 2001 et passage au
palier 2 (riz 170 → 110 g). Si les données du déplacement sont inexploitables, la
décision glisse au 23/08. Séances à reprendre le 10/08, un cran sous les standards sur
les polys pour la première séance.
