# Phase 5 — Comparaison & rédaction des deux rapports

## Point de départ : la fiche concurrent structurée

Les deux rapports **dérivent** de `concurency/competitors/{NOM}-PROFIL.md` (produite en Partie 2,
figée par le fact-check) confrontée au **profil AIMA** (`concurency/AIMA-POSITIONING.md`). Les deux ont
les mêmes axes : la comparaison est un **diff axe par axe** (§2 wet lab ↔ §2, §5 perfs ↔ §5,
§6 verrous ↔ §7 verrous AIMA…). Ne pas réextraire ni recomparer à la main ce qui est déjà dans
la fiche — la rédaction met en récit ce diff pour deux publics.

## Règle d'or

**Synthétique mais complet.** Un rapport interminable ne sera pas lu. Viser 6-8 pages PDF par
partie. Densité maximale : tableaux pour les données énumérables, prose pour l'analyse.

Retirer sans regret : les redites entre sections, les listes de niveau de preuve en tableau
géant, les commentaires méthodologiques qui n'apportent pas de décision.

## Découpage — toujours deux documents

| Fichier | Public | Contenu |
|---|---|---|
| `{CIBLE}-P1-TECHNIQUE.md` | bioinformaticiens, data scientists | wet lab, dry lab, features, modèle, performances, comparaison technique, perspectives |
| `{CIBLE}-P2-MARCHE.md` | direction générale | commercial, réglementaire, remboursement, financement, essais, concurrence, marché, implications |

Emplacement : `~/Pipeline/Aima-Survey/concurency/rapports/`. PDF combiné dans
`~/Pipeline/Aima-Survey/concurency/pdf/` via `scripts/md2pdf.py`.

Plan détaillé : [../templates/structure-rapports.md](../templates/structure-rapports.md).

## Marqueurs de niveau de preuve

Chaque affirmation chiffrée en porte un. Convention :
[../quality/niveaux-preuve.md](../quality/niveaux-preuve.md).

En-tête de chaque rapport : rappel compact de la convention, en 2 lignes, pas en tableau.

## Section obligatoire : positionnement vs AIMA

Dans **les deux** rapports, une section de comparaison explicite avec la fiche AIMA.

Dans P1 — comparaison technique :

| Axe | Concurrent | AIMA |
|---|---|---|
| Plateforme, chimie, amplification | | |
| Couverture | | |
| Signaux mesurés | | |
| Modalités par run | | |
| Modèle et sortie | | |
| Performances (à spécificité comparable) | | |

Dans P2 — positionnement stratégique : sur quel segment ils nous croisent, où ils ont une
avance, ce que leur trajectoire nous apprend, ce qui doit nous alerter.

## Ton et honnêteté

- Nommer ce qui est **favorable au concurrent** aussi clairement que ce qui l'est à AIMA.
- Écrire explicitement quand un espace stratégique est **déjà occupé** — ne pas présenter comme
  une opportunité ouverte ce qu'un concurrent fait déjà.
- Quand l'inoccupation d'un créneau peut refléter une **difficulté non résolue** plutôt qu'un
  angle mort du marché, le dire.
- Terminer chaque rapport par une section « à vérifier / incertitudes », jamais par une
  conclusion triomphale.

## Erreurs de rédaction à éviter

- Citer un chiffre sans son effectif ni sa spécificité
- Présenter une estimation repondérée comme une mesure
- Construire une critique du marketing d'un concurrent sur un chiffre mal lu
- Comparer une performance AIMA en cohorte de laboratoire à une performance concurrente en
  population de dépistage sans le signaler
