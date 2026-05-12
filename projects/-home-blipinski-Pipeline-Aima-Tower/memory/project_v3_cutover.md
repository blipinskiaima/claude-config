---
name: Tower v3.0.0 cutover (2026-05-07)
description: Refonte UI Plan G mise en prod, Tower main archivée v2.3.0, branches/worktrees/rollback
type: project
originSessionId: e7cf4774-71b7-41ae-a4bc-9bc5a148a559
---
## Stack v3.0.0 (en prod sur tower.aima-diagnostics.com)

- **Frontend** : Vite + React 18 + TypeScript + Tailwind v4 + AG Grid v35 + Lucide
- **Backend** : FastAPI + uvicorn (réutilise services Python services.py / compute.py / exploratory_compute.py / claude_cli.py / survey_service.py tels quels)
- **Container** : multi-stage Dockerfile (Node 20 build → Python 3.12 runtime, 1.6 GB)
- **Reverse proxy** : Caddy + basic auth bcrypt (inchangé vs v2.x)
- Frontend buildé statique servi par FastAPI (1 process), SPA fallback pour React Router

## Tags git

| Tag | Commit | Rôle |
|---|---|---|
| v2.3.0 | ed13d27 | Dernière Dash, point de retour |
| v3.0.0 | d91f80b | Refonte Plan G mergée sur main |

## Worktree

Un seul worktree depuis le 2026-05-11 (Plan C et Plan G nettoyés) :

```
~/Pipeline/Aima-Tower → main v3.0.0 (= source du container prod actif)
```

Le container `aima-tower-dashboard` est buildé depuis ce dossier. `.env` et `data/` sont des **vrais fichiers** dans ce dossier (plus de symlinks inter-worktrees).

## Why

Boris a validé la refonte UI complète après comparaison cell-by-cell : Plan G ≡ Tower main (266 cancers / 192 healthy / Sens AI 84.6% / Spec AI 89.1%). Plan C jamais utilisé en prod → supprimé. Plan G mergé dans main → supprimé. Tag `v2.3.0` sert de parachute en cas de besoin (Dash mono-stack).

## How to apply

- Pour modifier le code prod : éditer dans `~/Pipeline/Aima-Tower` → `docker compose build mini-tower && docker compose up -d`
- Pour rollback v2.3.0 :
  ```
  cd ~/Pipeline/Aima-Tower
  git stash && git checkout v2.3.0 -- .
  docker compose down
  docker compose build mini-tower
  docker compose up -d
  ```
- L'image `aima-tower-mini-tower:v3.0.0` est taguée pour identification (latest = v3 actuelle)
- Le project name `aima-tower` est figé dans le compose (override `name:`) → préserve volumes Caddy nommés (caddy_data, caddy_config = certificats Let's Encrypt) même si le worktree est renommé.

## v3.1.0 prévue : passer en systemd (sans Docker)

Boris a explicitement choisi de garder Docker pour v3.0.0, et de migrer vers systemd + venv en v3.1.0 plus tard pour simplifier le cycle de dev.
