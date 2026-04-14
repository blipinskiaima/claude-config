---
name: standby-todo-list
description: "Déplace une tâche bloquée de la Partie 1 (À faire) vers la Partie 3 (En stand-by) du fichier todo-optimisation.md, avec mention explicite de la raison du blocage et de la condition de déblocage. Peut aussi faire l'inverse (reprendre une tâche stand-by vers À faire). Use when the user says standby, stand-by, mettre en pause, bloqué, standby-todo-list, sandby, reprendre standby, or asks to park/pause/unpark a task in his to-do list."
allowed-tools: Read, Edit, Grep
---

# Skill : Standby Todo

Gère la **Partie 3 — En stand-by** du fichier todo : déplace une tâche bloquée depuis Partie 1 (À faire) ou la ramène vers Partie 1 quand débloquée.

## Fichier cible

`~/.claude/projects/-home-blipinski/memory/todo-optimisation.md`

Structure à 3 parties :
- **Partie 1 — À faire** (haute/moyenne/basse)
- **Partie 2 — Complété** (par jour)
- **Partie 3 — En stand-by** (tâches bloquées)

## Format strict d'un bullet stand-by

```
- [ ] **Titre court (4-8 mots)** — raison du blocage (1 phrase). **Débloquer quand :** condition concrète et observable.
```

Règles :
- La raison doit être **spécifique** : dépendance humaine (qui ?), info manquante (quoi ?), décision en attente (par qui ?), prérequis technique (lequel ?).
- La condition de déblocage doit être **observable** ("quand Florian disponible", "quand Dorado 1.1 sort", "quand décision ISO validée par Michael"), pas floue ("quand on aura le temps").
- Ne PAS mettre en stand-by les tâches simplement "basse priorité" — elles restent en Partie 1.

## Modes d'utilisation

### Mode A — Mettre en stand-by (Partie 1 → Partie 3)

C'est le mode par défaut.

1. **Identifier la tâche** dans Partie 1 (argument explicite ou fuzzy match).
2. **Demander la raison du blocage** si non fournie : dépendance / info manquante / décision / technique.
3. **Demander la condition de déblocage** si non fournie.
4. **Reformuler** au format stand-by strict.
5. **Retirer** le bullet de Partie 1 et **insérer** à la fin de Partie 3.
6. **Confirmer** : titre + raison + condition.

### Mode B — Reprendre (Partie 3 → Partie 1)

Déclenché par "reprendre", "débloquer", "unstandby", ou si l'utilisateur dit que la condition est remplie.

1. **Identifier la tâche** dans Partie 3.
2. **Demander la priorité** de reprise (haute/moyenne/basse).
3. **Reformuler** au format todo strict (retirer la raison/condition, garder le titre + contexte pertinent).
4. **Retirer** de Partie 3 et **insérer** dans la bonne section de Partie 1.

## Invocation sans argument

Si l'utilisateur invoque `/standby-todo-list` **sans nommer de tâche** :

1. **Scanner la session** pour détecter les signaux de blocage :
   - mentions explicites : "bloqué par", "en attente de", "dépend de", "pas avant que", "tant que X pas fait"
   - dépendances humaines : "nécessite Florian", "à valider avec Michael", "attendre Fred"
   - blocages techniques : "attend release X", "besoin GPU libre", "manque données Y"
2. **Lire Partie 1** et matcher les tâches évoquées comme bloquées.
3. **Proposer** max 5 candidats au format :
   ```
   Candidats stand-by détectés :
   1. Todo : **Ré-entraîner raima V1** (haute prio)
      → Raison : nécessite Florian. Débloquer quand : Florian disponible.
   2. Todo : **Expérience Apostle vs Maxwell** (haute prio)
      → Raison : prérequis wet-lab Romain. Débloquer quand : Romain a les aliquotes préparées.

   Lesquels mettre en stand-by ? (numéros, "tous", ou "aucun")
   ```
4. **Détecter aussi** les tâches en Partie 3 dont la condition semble levée dans la session → proposer reprise vers Partie 1.
5. **Attendre confirmation** avant édition.
6. Si aucun candidat : "Rien de bloqué détecté. Dis-moi quelle tâche mettre en stand-by ou reprendre."

## Exemples

### Mise en stand-by

Utilisateur : "standby-todo expérience Apostle vs Maxwell, Romain dispo que dans 3 semaines"

Action :
- Retire de Partie 1 / Haute priorité
- Ajoute à Partie 3 :
  ```
  - [ ] **Expérience Apostle vs Maxwell** — prérequis préparation aliquotes par Romain (indispo 3 semaines). **Débloquer quand :** Romain a les aliquotes prêtes.
  ```

### Reprise

Utilisateur : "reprendre l'expérience Apostle vs Maxwell, Romain a fini les préparations"

Action :
- Retire de Partie 3
- Ajoute à Partie 1 / Haute priorité :
  ```
  - [ ] **Expérience Apostle vs Maxwell** — même plasma sain, 2 aliquotes, comparer scores raima pour trancher le driver du batch effect.
  ```

## Anti-patterns

- ❌ Utiliser stand-by comme "basse priorité bis" → si ce n'est pas **bloqué**, ça reste en Partie 1
- ❌ Raison floue ("c'est compliqué", "à voir") → toujours nommer la dépendance
- ❌ Condition non observable ("quand on sera prêts") → toujours un événement concret
- ❌ Oublier de retirer le bullet de Partie 1 / Partie 3 (doublon)
