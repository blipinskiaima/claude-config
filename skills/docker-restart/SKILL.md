---
name: docker-restart
description: Redémarre proprement la stack docker compose d'un projet AIMA. Sequence stricte down → build → up -d → logs -f. Use when the user says "restart tower", "redémarre aima-tower", "docker-restart", "rebuild and restart", "redéploie", or is in a directory with docker-compose.yml and wants to redeploy after code changes.
allowed-tools: Bash(docker:*), Bash(cd:*), Bash(pwd:*), Bash(ls:*), Read
---

# Skill : Docker Compose Restart

Redémarre une stack docker-compose en suivant la séquence éprouvée sur Aima-Tower (pattern observé 10× verbatim sur 30j).

## Détection du contexte

1. Si l'utilisateur précise un projet (ex: « restart aima-tower »), `cd ~/Pipeline/Aima-Tower`
2. Sinon, vérifier `pwd` :
   - Si présence de `docker-compose.yml` ou `compose.yaml` → utiliser le cwd courant
   - Sinon, demander à Boris quel projet

## Séquence d'exécution (stricte, dans cet ordre)

```bash
cd $PROJECT_DIR

# Phase 1 : arrêt propre
docker compose down

# Phase 2 : rebuild (capture les modifs du code et du Dockerfile)
docker compose build

# Phase 3 : redémarrage en background
docker compose up -d

# Phase 4 : suivi des logs en foreground
docker compose logs -f
```

## Variantes (à proposer selon contexte)

- **Sans rebuild** (« restart sans rebuild ») → skip phase 2, séquence devient `down → up -d → logs -f`
- **Service unique** (« restart tower api ») → ajouter le nom du service à chaque commande, ex: `docker compose build api && docker compose up -d api && docker compose logs -f api`

## Validation post-restart

Avant de rendre la main, vérifier dans les 30 premières lignes de logs :
- Pas d'erreur fatale (`ERROR`, `FATAL`, `Exception`, `Traceback`)
- Présence d'une ligne de readiness (`ready`, `listening`, `started`, `running on`)
- Si erreur détectée : afficher les logs problématiques et demander à Boris s'il veut investiguer

## Golden rules

- **NEVER** `docker compose down -v` (supprime les volumes → perte de données persistées dans /app/data/)
- **NEVER** lancer en parallèle depuis plusieurs sessions Claude (race condition sur les ports exposés)
- **NEVER** `docker system prune -a` sans confirmation (supprime images encore utilisées)

## Référence

- Audit 2026-05-09 : pattern verbatim 10× sur Aima-Tower
- Projets concernés : Aima-Tower (V3 et antérieures), trace-platform, Aima-Survey
