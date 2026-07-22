---
name: combined-suspect-tab
description: "Page /combined onglet Suspects : dotplot des 25 imageries suspectes (scores.csv unité 'suspect'), sans vérité-terrain. Contrat de lecture, calibration du seuil, gotchas."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1ac897e3-ecbe-4991-b748-6a6308a81fb3
  modified: 2026-07-20T07:55:18.118Z
---

# Page `/combined` — onglet Suspects (2026-06-25, commits `e76f3c3`→`040e515`)

4ᵉ onglet du panneau Résultat, à côté de Dilution. Dotplot des **25 imageries suspectes**
(`unit == 'suspect'` dans `scores.csv`) scorées par le combo sélectionné, avec la ligne de
seuil et un compteur « N au-dessus ». Même architecture reader-only que Dilution : le
pipeline `~/Pipeline/Feature` produit les scores, Tower ne fait que lire.

## Le point structurant : pas de vérité-terrain

Les suspects ont **`label` NULL** — ce sont des imageries en attente de statut, pas une
cohorte annotée. Conséquence directe sur ce qu'on a le droit d'afficher :

```
Dilution / Initial          Suspects
  label connu                 label NULL
  → Se / Sp calculables       → NI sensibilité NI spécificité
                              → seulement : combien passent le seuil
```

Ne jamais ajouter de KPI Se/Sp à cet onglet : il n'y a rien pour les calculer. Le seul
chiffre légitime est `n_above / n_total`. C'est le même parti pris que pour la dilution.

## Contrat de lecture (`src/dilution_service.py::get_suspect_scores`)

Source unique `result/speedvac_{no,yes}/scores.csv`, même fichier que Dilution, un seul
passage `csv.reader` qui remplit deux collections en parallèle :

| | Filtre ligne | Usage |
|---|---|---|
| Points affichés | `unit == 'suspect'` | dotplot (25 pts) |
| Calibration seuil | `eval_cohort == 'train'` ET `is_healthy == TRUE` ET **`label` parsable en float** | `quantile_type1(healthy, target_spec)` |

Le garde `float(row[i_label])` est là pour que **les lignes sans vérité-terrain ne
polluent jamais la calibration** — sans lui, un suspect flaggé healthy entrerait dans le
quantile qui sert à le juger. Ne pas le retirer en croyant simplifier.

Lookup colonne = `features.replace(",", "+")`, identique à Dilution (clé Combined en `,`,
colonnes du CSV en `+`). Combo absent du CSV → `found: False`, l'UI affiche « absent du
benchmark » au lieu de planter.

## Frontend

- `useCombinedSuspect(features, speedvac, spec, enabled)` — TanStack Query, `staleTime` 60 s,
  **lazy** : `enabled = resultTab === "suspect"`, donc aucun fetch tant que l'onglet n'est
  pas ouvert (même pattern que `useCombinedDilution`).
- `SuspectChart.tsx` — scatter Plotly, rouge `#dc2626` au-dessus du seuil / violet `#5b5bd6`
  en dessous, ligne de seuil pointillée en `xref: "paper"`, axes `fixedrange` (pas de zoom).
- **Jitter X déterministe** : suite de Weyl (`(i * 0.618...) % 1`), **pas `Math.random()`** —
  sinon les points sautent à chaque re-render React. Pattern réutilisable pour tout dotplot.
- Le seuil hérite des paramètres d'évaluation de la page (`targetSpec` + `speedvac`), comme
  Dilution — pas de contrôle dédié.

## Tests

`tests/test_suspect.py` — 4 tests, verts au 2026-07-20 : found + n_total == 25, forme des
points, cohérence `n_above` vs recomptage, combo inexistant → `found: False`.
Ils tapent le **vrai** `scores.csv` (pas de fixture), donc `n_total == 25` cassera si la
cohorte suspecte bouge côté Feature — c'est voulu, ça sert de canari.

Voir aussi : [[combined_dilution_tab]] (même contrat scores.csv), [[feature_pipeline_integration]] (archi reader-only).
