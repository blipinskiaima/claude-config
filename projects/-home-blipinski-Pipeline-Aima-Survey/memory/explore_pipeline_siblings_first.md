---
name: Explorer les projets jumeaux Pipeline avant de proposer une solution
description: Pour toute nouvelle tâche dans ~/Pipeline/, vérifier d'abord si un autre projet AIMA a déjà résolu le même problème — l'écosystème Boris est cohérent et les patterns se répliquent
type: feedback
originSessionId: 2436002f-1dc1-46c9-9d7b-0cb1a41488d6
---
Avant de proposer un design face à une tâche "comment faire X sur projet AIMA Y", **explorer d'abord les projets jumeaux** dans `~/Pipeline/` (`Aima-Tower`, `Aima-Survey`, `trace-prod`, `trace-platform`, `trace-workflow`, `email-hub`, etc.). Si un pattern similaire existe déjà, le copier tel quel plutôt que concevoir une solution from-scratch.

**Why :** Le 2026-04-21, Boris a demandé comment router le scoring Haiku d'Aima-Survey sur son abonnement Pro/Max. Première réaction : lancer un agent de recherche web qui a conclu "impossible, il faut racheter du crédit API". Deuxième réaction (sur correction de Boris) : explorer Aima-Tower où le pattern existait déjà en production (`src/claude_cli.py`, subprocess `claude -p` avec `CLAUDE_CODE_OAUTH_TOKEN`). La copie prit 30 minutes, la recherche web avait coûté un aller-retour inutile. Boris entretient intentionnellement la cohérence de son écosystème — proposer des solutions ad-hoc le décoiffe.

**How to apply :**
1. À toute tâche type "je veux faire X sur projet Y", commencer par `ls ~/Pipeline/` puis `grep -rln "<pattern-pertinent>" ~/Pipeline/*/src/ ~/Pipeline/*/lib/`
2. Si un fichier pertinent existe chez un jumeau, le lire en priorité et proposer directement la réplication comme solution canonique
3. Ne partir sur une approche from-scratch ou une recherche web UNIQUEMENT si l'exploration jumelle revient vide
4. Cas typiques où la réplication s'applique : auth (Claude, Redis, Scaleway S3), DuckDB UPSERT patterns, subprocess wrappers, email sending, Dockerfile conventions, tests fixtures
