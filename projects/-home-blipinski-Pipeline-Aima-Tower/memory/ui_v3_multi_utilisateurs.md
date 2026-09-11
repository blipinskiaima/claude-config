---
name: ui-v3-multi-utilisateurs
description: "Tower v3 n'est plus un dashboard perso : retrait des références personnelles et thème light par défaut."
metadata:
  node_type: memory
  type: project
  modified: 2026-05-07T00:00:00.000Z
---

# UI Tower v3 — multi-utilisateurs (2026-05-07)

La Tower n'est plus un dashboard personnel. Retrait des références « Boris », « Plan G »,
de la branche `feat/ui-refresh-g` et de la mention « Internal · v3 preview » dans la
Sidebar, Home et Exploration.

**Thème light par défaut** : le fallback de `getStoredTheme` passe de `"system"` à
`"light"`. ⚠ La clé `theme-preference` du localStorage est **préservée**, donc les
utilisateurs ayant déjà choisi gardent leur réglage. Le sélecteur dark/system reste
disponible dans la sidebar.
