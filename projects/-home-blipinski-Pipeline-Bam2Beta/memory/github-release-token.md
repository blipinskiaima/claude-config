---
name: github-release-token
description: gh release create echoue en 403 avec le GITHUB_TOKEN de github.sh — fallback env -u GITHUB_TOKEN
metadata: 
  node_type: memory
  type: reference
  originSessionId: 291a35d1-00d1-415e-87ca-5f791e66f227
---

Sur Bam2Beta (repo `aima-dx/Bam2Beta`), `gh release create` échoue avec **HTTP 403 "Resource not accessible by personal access token"** quand `GITHUB_TOKEN` est chargé via `source /home/blipinski/Pipeline/export/github.sh`.

**Cause** : `github.sh` exporte un PAT fine-grained (`github_pat_11...`) qui a la permission push (git) mais **pas** la permission *releases*. Cette var d'env est prioritaire sur le token stocké par `gh`.

**Fix** : neutraliser la var pour forcer le fallback vers le token de `~/.config/gh/hosts.yml` (`gho_...`, scope classique `repo` → couvre les releases) :
```bash
env -u GITHUB_TOKEN -u GH_TOKEN gh release create V<x> --title ... --notes ...
```
Le `git push origin main --tags`, lui, marche avec le PAT (permission contents/push OK). Seule la création de release nécessite le fallback.

Vérifié le 2026-07-06 lors de la release V2.0.0. Voir la skill [[maj-bam2beta]].
