---
name: Todo list — routing par section
description: Quand Boris demande "en cours", "à faire", "stand-by", "fait" → afficher UNIQUEMENT la partie correspondante de todo-optimisation.md, pas la liste complète.
type: feedback
originSessionId: 6600d36d-c2d4-4ccc-87ac-ba3095f8db9b
---
La todo list `~/.claude/projects/-home-blipinski/memory/todo-optimisation.md` a 4 parties :
1. **Partie 1 — À faire** (par priorité : haute/moyenne/basse)
2. **Partie 2 — En cours** (tâches actives démarrées)
3. **Partie 3 — Complété** (historique par jour)
4. **Partie 4 — En stand-by** (bloquées)

**Routing des requêtes :**
- "à faire" / "todo" / "prochaine tâche" → Partie 1
- "en cours" / "qu'est-ce qui tourne" → Partie 2
- "complété" / "fait" / "historique" → Partie 3
- "stand-by" / "bloqué" / "en pause" → Partie 4
- "todo list" (sans précision) → Partie 1 + Partie 2 (actif uniquement)

**Why:** Boris a demandé cette séparation le 2026-04-15 pour éviter de scroller tout le fichier à chaque consultation.
**How to apply:** Ne jamais dumper le fichier complet si la question cible une section précise. Les skills `/add-todo-list`, `/maj-todo-list`, `/standby-todo-list` doivent respecter ces 4 parties.
