# Context — Aima-Tower — 2026-08-12 (clôture session)

**Branche** : main (poussé, origin/main = f591749)
**Dernier commit** : f591749 — docs: README + CLAUDE.md v5.2.0, versions réalignées
**Status** : clean (hors untracked `.claude/worktrees/` et `Exis 1.1.pdf`, hors scope
depuis le 24/07)

## Où j'en suis
Session close via /end-session. Deux features livrées et déployées : le bloc
« Performance des produits » sur le Tableau de bord, et le passage de mVAF v1.4 au
seuil Exis 0,0042 sur /reproductibilite. La prod a été rebuildée en dernier, elle est
alignée sur main (API en 5.2.0).

En début de session, ~740 lignes de ton travail des 29-31/07 traînaient non commitées
(page /profil-aima, compute_mrd_postop, plafonnement de comparabilité, slider 0,999) —
commitées en 32c91bc avant de commencer, tag pre-bloc-synthese-dashboard.

## Ce qui marche / ce qui foire
- ✓ Bloc Tableau de bord : 5 lignes (Exis global + CRC/Lung/Pancreas + THEMELIO),
  décompte 485/1471. Aucun recalcul — même endpoint et même pct() que le Profil AIMA.
  Rendu vérifié en 1440 px et 800 px.
- ✓ Seuil 0,0042 sur /reproductibilite. 100 tests passés / 4 skipped, tsc exit 0.
- ⚠ Le seuil déplace AUSSI le taux d'accord : cohorte pure 93,8 % → 85,4 %. Colon_22
  perd son unanimité à cause d'un run à 0,0041. Assumé, mais à savoir si quelqu'un
  s'étonne de la baisse.
- ⚠ Piège consigné : la ligne Exis GLOBALE du Tableau de bord affiche 82,0 % là où
  /exploration montre 76,2 % (exclusion vessie/TNE/Nuclear) ; les 3 lignes par
  indication, elles, correspondent exactement.
- ✗ tests/test_dilution.py échoue à la COLLECTE : `ImportError: cannot import name
  'mvaf_threshold' from 'dilution_service'`. Panne PRÉ-EXISTANTE (déjà là sur 159633a),
  non traitée — elle masque tout le module de tests dilution.
- ℹ Non fait faute de demande : ligne de seuil + mention « > 0,0042 » dans la légende
  de /reproductibilite (à l'échelle linéaire le seuil est invisible) ; lien « voir le
  Profil AIMA » depuis le bloc du Tableau de bord ; préchauffage du cache comparaison
  (5,5 s au premier chargement de la Home après redémarrage).

## Prochaine étape
Réparer tests/test_dilution.py — c'est la seule chose cassée du repo, et elle masque
un module entier. Vérifier ce qu'est devenu `mvaf_threshold` dans dilution_service.py
(renommé ou supprimé lors de l'ajout de l'onglet Suspects ?) et remettre le test en
phase, ou le retirer s'il n'a plus d'objet.
