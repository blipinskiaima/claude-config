# Context — ZTHapp — 2026-07-27

**Branche** : main
**Dernier commit** : feb0e8c — Docs: CLAUDE.md à jour (état prod)
**Status** : clean

## Où j'en suis
Recalibrage post-pause terminé et déployé : audit PDF ZTH complet (182 p.), plan de reprise validé — déficit direct 2001 kcal dès AUJOURD'HUI 27/07 (= JOUR 1), repas verrouillés Raptor Club + Riz Œuf (riz 170 g, huile 5 g), rampe sport S1 cette semaine (tops un cran sous les standards), re-test standards S2. App enrichie en prod : page /mesures (poids bas hebdo + tour de taille, migration 0008 appliquée), Coach IA réparé, backup v2, base de connaissance coach 9 docs. 2 skills user créés : daily-diet (journal + arbre de décision nutrition) et weekly-muscu (séances + progression).

## Ce qui marche / ce qui foire
- ✓ 6 commits poussés, build vert, Vercel déployé, migration passée en prod
- ✓ Skills daily-diet / weekly-muscu opérationnels, journal actif depuis le 25/07
- ✓ Coach IA voit désormais phases + compléments (requêtes corrigées)
- ✗ Boris doit encore faire /parametres : poids 64.5 · âge 30 · offset → 0
- ✗ Refeed à surveiller ~27/09 (compteur 2 mois de déficit)

## Prochaine étape
Dimanche 02/08 : premier bilan — /daily-diet (poids bas hebdo + tour de taille → arbre de décision) et /weekly-muscu (perfs rampe S1 → verdicts).
