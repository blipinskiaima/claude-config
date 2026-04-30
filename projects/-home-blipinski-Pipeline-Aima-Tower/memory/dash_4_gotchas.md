---
name: Dash 4.1+ gotchas Tower
description: Pièges Dash 4.1+ rencontrés sur Tower (allow_direct_input, persistence, conditional components)
type: project
originSessionId: 5bfbec5e-fc97-4d4e-a697-549503f02ef9
---
# Dash 4.1+ — Gotchas Tower

## `allow_direct_input` par défaut True (Slider/RangeSlider)

Depuis Dash 4.1, `dcc.Slider` et `dcc.RangeSlider` ajoutent un **input numérique éditable** à côté du curseur (default `allow_direct_input=True`). Si tu veux slider-only (pas de saisie manuelle) :
```python
dcc.Slider(..., allow_direct_input=False, ...)
dcc.RangeSlider(..., allow_direct_input=False, ...)
```

**Why:** comportement nouveau Dash 4 qui n'existait pas dans 2.x. **How to apply:** par défaut `allow_direct_input=False` sur tous les sliders d'Exploration (et idéalement Qualité).

## Persistence ID bumping pour invalider le cache navigateur

Quand on change la valeur par défaut d'un Dropdown / Slider avec `persistence=True`, l'ancienne valeur reste cachée dans la session storage du navigateur → l'utilisateur ne voit jamais la nouvelle default.

**Solution** : changer `persistence=True` en `persistence="version-key"` (string unique). Quand la string change, Dash invalide tous les anciens caches.

Exemples Tower :
- `exploration-indications` : `persistence="explv3-healthy"` (bump quand on ajoute Healthy au défaut)
- multi-select dynamiques : `persistence="explv2"`

**Why:** sans bump, les modifications de défaut sont invisibles pour l'utilisateur (cache stale). **How to apply:** systématiquement bumper la string quand on touche au `value=` initial d'un composant persistent.

## Composants rendus conditionnellement → callbacks plantent

Erreur courante : référencer dans `Input(...)` un composant qui n'est pas TOUJOURS dans le DOM. Exemple :
```python
# Tab Avancé dans /exploration > Graphiques
dbc.Tab(html.Div([dbc.Button(id="exploration-graph-adv-apply", ...)]))
```
Le bouton existe SEULEMENT quand `_build_graphics_section` est appelé (sub_tab="sub-graphs"). Quand l'utilisateur est sur Tableaux, le bouton n'existe pas dans le DOM.

Si on fait :
```python
@app.callback(
    Output("exploration-cohort-alert", "children"),
    Input("exploration-graph-adv-apply", "n_clicks"),  # ← n'existe pas en Tableaux !
    ...
)
```
Le callback plante au render → page vide.

**Solution** : utiliser un `dcc.Store(id="...", storage_type="session")` toujours présent dans le layout principal comme **relais**. Le bouton conditionnel met à jour le Store, les callbacks panel-wide écoutent le Store.

**Why:** Dash exige que tous les composants Input/Output existent dans le layout au moment du callback. Composants conditionnels = source de bugs cachés. **How to apply:** Inputs cross-tab → toujours via un Store relais permanent.

## tooltip `transform` peut casser le rendu (RangeSlider)

Dash 4.1 accepte `tooltip={"transform": "fmtMyFunction"}` qui référence une fonction JS globale. **Mais** si la prop n'est pas reconnue par le composant, le slider entier ne se rend plus (page blanche du slider). Pas de message d'erreur clair côté serveur.

Si besoin de format custom du tooltip, vérifier d'abord la doc précise du composant via `help(dcc.Slider)` et tester progressivement.

## Pattern-matching State avec `ALL` est OK

`State({"type": "exploration-adv-filter", "full": ALL}, "value")` fonctionne même si certains composants matching ne sont pas dans le DOM (Dash retourne juste une liste vide). Pas le même problème que les Inputs/Outputs nommés.

## Imports tardifs pour éviter les cycles

Dans Tower, les callbacks dans `callbacks.py` importent `pages._filter_label` ou `pages._build_exploration_content` à l'intérieur des fonctions (pas en haut du fichier) car `pages.py` importe lui-même des choses de `callbacks.py` indirectement.

```python
def update_exploration_advanced_graph(...):
    from pages import _filter_label  # noqa: E402
    ...
```

**Why:** import circulaire au module load. **How to apply:** garder les imports tardifs pour les fonctions de pages.py utilisées dans callbacks.py.
