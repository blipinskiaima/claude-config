---
name: Docker compose Tower main — project name figé à `aima-tower`
description: Le docker-compose.yml de Aima-Tower fixe le project name à `aima-tower` (sans suffixe `-main`). Sans cela, compose dérive du nom du dossier et taggue une image fantôme.
type: feedback
originSessionId: c43652e0-b0c5-4c6d-8cd9-e05ec94930e4
---
Le `docker-compose.yml` de `~/Pipeline/Aima-Tower/` contient `name: aima-tower` en tête. Sans ce override, Docker Compose dérive le project name du nom du dossier (`Aima-Tower` → `aima-tower-main`) et taggue les images comme `aima-tower-main-mini-tower:latest`, alors que les containers historiques utilisent `aima-tower-mini-tower:latest`. Résultat : `compose build` produit une image fantôme et `compose up` recrée des containers basés sur la vieille image.

Symptôme typique : on modifie `src/compute.py`, on rebuild, mais le container tourne toujours avec l'ancien code (les hashes md5 entre `/app/src/compute.py` et le fichier host divergent).

**Why:** Héritage du cutover v3.0.0 (mai 2026). Le project name `aima-tower` a été figé pendant le passage Dash → React, et changer le nom du dossier après coup aurait cassé les volumes / réseaux nommés.
**How to apply:** Le fix est permanent depuis 2026-05-09 (`name: aima-tower` dans le compose). Si tu travailles sur une vieille checkout sans ce override, ajoute `-p aima-tower` à toutes les commandes : `docker compose -p aima-tower {build,up,down,logs}`. Vérifie aussi avec `docker inspect <container> --format '{{.Image}}'` vs `docker images aima-tower-mini-tower` si tu suspectes un container qui tourne avec une vieille image.
