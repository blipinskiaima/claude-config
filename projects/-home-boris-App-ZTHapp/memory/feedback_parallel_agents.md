---
name: Parallélisation maximale via agent teams
description: Pour gros chantiers multi-fichiers, lancer plusieurs Agent en parallèle dès que les périmètres sont disjoints
type: feedback
originSessionId: 6e608394-4cbc-42d0-88d3-01a4274d2e76
---
Boris préfère que je parallélise le maximum de tâches en lançant plusieurs `Agent` en parallèle (même message, plusieurs tool calls) plutôt que d'exécuter séquentiellement.

**Why:** Boris a explicitement redirigé pendant le port ZTHapp2 ("oui mais parallélise le plus de tâche, utilise les agents teams"). Gros chantier = beaucoup de fichiers indépendants à créer/porter, le séquentiel serait perte de temps.

**How to apply:**
- Pour tout chantier impliquant >5 fichiers ou >3 modules indépendants : découper en vagues parallèles d'agents
- Une vague = N agents avec périmètres de fichiers disjoints, lancés dans un seul message avec plusieurs invocations Agent
- Entre les vagues : attendre les complétions, faire un point, lancer la vague suivante
- Ne paralléliser que ce qui est vraiment indépendant — sinon merge conflicts / race conditions
- Donner à chaque agent : (a) périmètre exact des fichiers à toucher, (b) paths absolus de sources à lire, (c) conventions imports/hooks à respecter, (d) contraintes critiques (ex: "ne pas toucher tel dossier")
