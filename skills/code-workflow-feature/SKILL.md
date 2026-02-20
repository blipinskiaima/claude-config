---
name: code-workflow-feature
description: Workflow structure pour ajouter une feature a un projet en cours de developpement. Suit un processus en 4 etapes (Exploration, Planification, Execution, Verification) avec les Karpathy Guidelines. Use when the user wants to add a feature, implement a new functionality, or says "code-workflow-feature", "ajoute une feature", "implement", "nouvelle fonctionnalite", or any variation of adding a feature to an existing project.
---

<objective>
Workflow complet pour implementer une feature dans un projet existant. Chaque etape requiert confirmation utilisateur avant de passer a la suivante. Les Karpathy Guidelines s'appliquent a l'ensemble du processus.
</objective>

<rules>
- Demander confirmation a l'utilisateur a CHAQUE transition d'etape
- Demander question/detail/information au moindre doute a n'importe quelle etape
- Suivre les Karpathy Guidelines scrupuleusement (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution)
- Ne jamais supposer — toujours verifier
- Chaque ligne modifiee doit etre traceable a la demande utilisateur
</rules>

<workflow>

## Overview

```
Etape 1: EXPLORATION     → verify: contexte suffisant pour planifier
Etape 2: PLANIFICATION   → verify: plan approuve par l'utilisateur
Etape 3: EXECUTION       → verify: code compile, tests passent
Etape 4: VERIFICATION    → verify: recap valide, memoire sauvegardee
```

**Confirmation utilisateur requise entre chaque etape.**

---

## Etape 1: Exploration

Construire le contexte necessaire pour implementer la feature. Utilise les subagents en parallele.

| Need | Reference |
|---|---|
| Strategie d'exploration detaillee | [references/exploration.md](references/exploration.md) |

**Actions:**

1. **Explorer le codebase** — lancer `agent-explore` (ou `agent-explore-quick` si le projet est deja documente). Si quick est insuffisant, relancer une exploration profonde.

2. **Identifier les libraries** — si la feature utilise des libraries (existantes ou nouvelles), lancer `agent-docs` pour chercher la documentation via Context7.

3. **Rechercher sur le web** — si besoin d'informations complementaires (best practices, patterns, solutions connues), lancer `agent-websearch`.

4. **Synthese** — combiner les resultats des agents en une vue complete :
   - Architecture actuelle du code impacte
   - Fichiers a modifier/creer
   - APIs et patterns a utiliser
   - Contraintes et gotchas identifiees

**Presenter la synthese a l'utilisateur et demander confirmation avant de planifier.**

---

## Etape 2: Planification

Planifier l'implementation en 2 temps : creer un prompt de planification, puis executer en mode plan.

| Need | Reference |
|---|---|
| Workflow de planification detaille | [references/planning.md](references/planning.md) |

**Actions:**

1. **Creer le prompt de planification** — utiliser le skill `/prompt-creator` pour generer un prompt structure qui :
   - Decrit la feature a implementer
   - Inclut le contexte d'exploration (architecture, fichiers, patterns)
   - Definit les criteres de succes verifiables
   - Liste les contraintes (Karpathy Guidelines, style existant)

2. **Executer en mode plan** — utiliser `EnterPlanMode` pour :
   - Explorer les fichiers impactes
   - Designer l'approche d'implementation
   - Lister les fichiers a creer/modifier avec les changements prevus
   - Definir l'ordre d'implementation et les verifications intermediaires

3. **Presenter le plan** — utiliser `ExitPlanMode` pour soumettre le plan a l'utilisateur.

**Le plan doit etre approuve par l'utilisateur avant d'executer.**

---

## Etape 3: Execution

Implementer le plan approuve en suivant les Karpathy Guidelines.

| Need | Reference |
|---|---|
| Regles d'execution detaillees | [references/execution.md](references/execution.md) |

**Principes:**
- **Surgical Changes** — ne toucher que ce qui est necessaire
- **Simplicity First** — code minimal, pas d'abstractions speculatives
- **Goal-Driven** — verifier apres chaque etape du plan
- Suivre l'ordre d'implementation defini dans le plan
- Matcher le style existant du projet

**Si un obstacle survient pendant l'execution:**
1. Ne pas forcer — identifier la cause
2. Presenter le probleme a l'utilisateur
3. Proposer des alternatives
4. Attendre la decision avant de continuer

**Demander confirmation a l'utilisateur une fois l'execution terminee.**

---

## Etape 4: Verification

Verifier le code, recapituler les modifications, et sauvegarder le contexte.

| Need | Reference |
|---|---|
| Checklist de verification | [references/verification.md](references/verification.md) |

**Actions:**

1. **Verifier le code:**
   - Lancer les tests (`npm test`, `pytest`, etc.)
   - Verifier la compilation/build
   - Checker les diagnostics IDE (`mcp__ide__getDiagnostics`)
   - Lire les fichiers modifies pour revue rapide

2. **Recapituler les modifications:**
   - `git diff --stat` — vue d'ensemble
   - Liste des fichiers modifies/crees/supprimes
   - Resume fonctionnel de chaque changement
   - Erreurs rencontrees et comment elles ont ete resolues

3. **Presenter le recap a l'utilisateur.**

4. **Si tout est OK** — utiliser le skill `/claude-memory` pour sauvegarder les apprentissages de la session (patterns decouverts, decisions architecturales, gotchas).

</workflow>
