---
name: survey-competitors-tab
description: "Onglet Concurrence de /survey : le match se fait aussi sur l'affiliation du dernier auteur."
metadata:
  node_type: memory
  type: project
  modified: 2026-04-22T00:00:00.000Z
---

# Onglet Concurrence Survey étendu

`is_competitor_article(a)` matche désormais `a.org_name` **OR** `a.last_author_affiliation`
contre `competitors.json` (23 entreprises, tiers 1/2/3 avec alias). IMBdx ajouté en tier_2
MOYENNE.

Effet : l'onglet passe de **11 à 29** articles concurrents.

Une reclassification Haiku ciblée était en cours côté Aima-Survey au moment de l'écriture
(script `reclassify_competitors.py`) — état à revérifier avant de s'appuyer dessus.
