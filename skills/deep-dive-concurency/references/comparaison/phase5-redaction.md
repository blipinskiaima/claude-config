# Phase 5 — Comparaison & rédaction des deux rapports

## Point de départ : le corpus vérifié de la Partie 2

Les deux rapports **dérivent** du corpus figé par le fact-check (Partie 2), confronté au
**profil AIMA** (`concurency/AIMA-POSITIONING.md`). Les deux sont structurés sur les mêmes axes :
la comparaison est un **diff axe par axe** (wet lab ↔ wet lab, perfs ↔ perfs, verrous concurrent
↔ §7 verrous AIMA…). Ne pas réextraire ni recomparer ce qui est déjà vérifié — la rédaction met
ce diff en récit pour deux publics.

## Règle d'or

**Synthétique mais complet.** Un rapport interminable ne sera pas lu. Viser 6-8 pages PDF par
partie. Densité maximale : tableaux pour les données énumérables, prose pour l'analyse.

Retirer sans regret : les redites entre sections, les listes de niveau de preuve en tableau
géant, les commentaires méthodologiques qui n'apportent pas de décision.

## Découpage — deux documents à écrire, deux générés

| Fichier | Public | Contenu | Qui l'écrit |
|---|---|---|---|
| `{SLUG}-P0-MAJEURS.md` | tous | les faits qui changent leur droit de vendre | `cli.py competitive-profil` |
| `{SLUG}-P1-TECHNIQUE.md` | bioinformaticiens, data scientists | wet lab, dry lab, features, modèle, performances, comparaison technique, verrous AIMA | **ce skill** |
| `{SLUG}-P2-MARCHE.md` | direction générale | commercial, réglementaire, remboursement, financement, essais, concurrence, marché, implications | **ce skill** |
| `{SLUG}-P3-TRAJECTOIRE.md` | tous | ce qui a bougé depuis la dernière révision, chronologie, questions ouvertes | `cli.py competitive-profil` |

Emplacement : `~/Pipeline/Aima-Survey/concurency/profils/` — **pas** `rapports/`, gelé depuis le
29/07/2026. PDF combiné dans `concurency/pdf/profils/{SLUG}.pdf`, produit par le cron du lundi
dès qu'un `P1-TECHNIQUE.md` existe : **sans P1, pas de PDF du tout**.

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
