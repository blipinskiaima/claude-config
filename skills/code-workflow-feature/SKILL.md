---
name: code-workflow-feature
description: Workflow structure pour ajouter une feature a un projet en cours de developpement. Suit un processus en 5 etapes (Brainstorming conditionnel, Exploration, Planification, Execution, Verification) avec les Karpathy Guidelines et l'integration des skills superpowers. Use when the user wants to add a feature, implement a new functionality, or says "code-workflow-feature", "ajoute une feature", "implement", "nouvelle fonctionnalite", or any variation of adding a feature to an existing project.
effort: xhigh
allowed-tools: Agent Skill Read EnterPlanMode ExitPlanMode mcp__ide__getDiagnostics
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
- Discipline Read-before-Edit absolue (cf. Etape 3)
</rules>

<workflow>

## Overview

```
Etape 0: BRAINSTORMING   (CONDITIONNEL)  → verify: spec design ecrite et validee
Etape 1: EXPLORATION                     → verify: contexte suffisant pour planifier
Etape 2: PLANIFICATION   (4 branches)    → verify: plan approuve par l'utilisateur
Etape 3: EXECUTION                       → verify: code compile, tests passent
Etape 4: VERIFICATION                    → verify: recap valide, memoire sauvegardee
```

**Confirmation utilisateur requise entre chaque etape.**

---

## Etape 0: Brainstorming (CONDITIONNEL)

Raffiner une idee vague en design doc avant toute exploration ou code.

**Skip si** : idee triviale, scope ≤ 3 fichiers, fix bug cible, typo, rename, ajout simple de log/colonne/parametre.

**Utiliser si** :
- Feature strategique (architecture, nouveau pipeline)
- Refactor lourd (> 5 fichiers modifies)
- Code ISO 15189 (Bam2Beta, trace-prod release)
- Multi-projets impactes
- Idee floue ou non specifiee
- > 15 fichiers impactes

**Action** : invoquer `superpowers:brainstorming`.

Le skill :
- Pose des questions une-a-une (multiple choice quand possible)
- Propose 2-3 approches avec trade-offs
- Presente le design par sections, validation incrementale
- Produit `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` (committe)

**Output** : design doc valide → input direct de l'Etape 2 (branche D).

---

## Etape 1: Exploration

Construire le contexte necessaire pour implementer la feature. Utilise les subagents en parallele.

| Need | Reference |
|---|---|
| Strategie d'exploration detaillee | [references/exploration.md](references/exploration.md) |

**Actions** :

1. **Explorer le codebase** — lancer `agent-explore` deep en background (ou `agent-explore-quick` si le projet est deja documente). Si quick est insuffisant, relancer une exploration profonde.

2. **Exploration architecturale approfondie** — si codebase large (> 50 fichiers) ou question architecturale transverse : lancer `agent-explore` deep avec un prompt focalisé sur le data flow et les dépendances inter-modules. Pertinent pour trace-prod, Bam2Beta, Aima-Tower.

3. **Identifier les libraries** — si la feature utilise des libraries (existantes ou nouvelles), lancer `agent-docs` pour chercher la documentation via Context7.

4. **Rechercher sur le web** — si besoin d'informations complementaires (best practices, patterns, solutions connues), lancer `agent-websearch`.

5. **Isolation worktree** — si la modification est risquee (refactor, migration, code production critique) : invoquer `superpowers:using-git-worktrees` pour creer un worktree isole.

6. **Synthese** — combiner les resultats des agents en une vue complete :
   - Architecture actuelle du code impacte
   - Fichiers a modifier/creer
   - APIs et patterns a utiliser
   - Contraintes et gotchas identifiees

**Presenter la synthese a l'utilisateur et demander confirmation avant de planifier.**

---

## Etape 2: Planification (4 branches)

Choisir UNE branche selon la taille et le contexte de la feature.

| Need | Reference |
|---|---|
| Workflow de planification detaille | [references/planning.md](references/planning.md) |

### Branche A — Trivial (≤ 3 fichiers, fix simple)

Skip la planification formelle. Creer une TodoList synthetique avec `TodoWrite` puis aller directement a l'Etape 3.

### Branche B — Standard (4-15 fichiers, AIMA quotidien)

Workflow par defaut :

1. **Creer le prompt de planification** via `/prompt-creator` qui :
   - Decrit la feature a implementer
   - Inclut le contexte d'exploration
   - Definit les criteres de succes verifiables
   - Liste les contraintes (Karpathy Guidelines, style existant)

2. **Executer en mode plan** via `EnterPlanMode` :
   - Explorer les fichiers impactes
   - Designer l'approche
   - Lister les fichiers a creer/modifier avec les changements prevus
   - Definir l'ordre d'implementation et les verifications intermediaires

3. **Presenter le plan** via `ExitPlanMode`.

### Branche C — Complexe (> 15 fichiers, multi-projets, ISO 15189)

Utiliser `/ultraplan` (cloud, review par sections avec inline comments) :
- Limite les abandons de Plan mode local
- Revue dediee par sections dans le browser
- Approuver pour executer en cloud OU teleporter le plan dans le terminal

**Limitation** : `/ultraplan` deconnecte Remote Control si actif.

### Branche D — Spec deja ecrit (output Etape 0)

Si l'Etape 0 a produit un design doc :

1. Invoquer `superpowers:writing-plans` → produit un plan d'implementation detaille
2. Passer a l'Etape 3 avec `superpowers:executing-plans`

**Le plan doit etre approuve par l'utilisateur avant d'executer.**

---

## Etape 3: Execution

Implementer le plan approuve en suivant les Karpathy Guidelines.

| Need | Reference |
|---|---|
| Regles d'execution detaillees | [references/execution.md](references/execution.md) |

**Principes Karpathy** :
- **Surgical Changes** — ne toucher que ce qui est necessaire
- **Simplicity First** — code minimal, pas d'abstractions speculatives
- **Goal-Driven** — verifier apres chaque etape du plan
- Suivre l'ordre d'implementation defini dans le plan
- Matcher le style existant du projet

**Discipline Read-before-Edit (obligatoire)** :
- Toujours `Read` un fichier AVANT `Edit`/`Write`
- Re-`Read` apres tout outil externe qui peut modifier le fichier (linter, formatter, autre session)
- `Edit` avec ≥ 3 lignes de contexte unique pour eviter les "String to replace not found"
- Si `Edit` echoue avec "File has been modified" : re-`Read` puis re-`Edit`

**Branche TDD (recommandee pour code ISO 15189)** :

Si la feature touche Bam2Beta, trace-prod, ou tout code soumis a la qualification ISO 15189 :
- Invoquer `superpowers:test-driven-development` AVANT le code
- Ecrire le test qui echoue, puis le code qui le fait passer
- Refactorer en gardant les tests verts

**Branche parallele** :

Si la feature contient 2+ taches independantes (pas d'etat partage, pas de dependances sequentielles) :
- Invoquer `superpowers:dispatching-parallel-agents`
- Ou `superpowers:subagent-driven-development` pour executer des sous-taches independantes dans la session courante

**Si un obstacle survient pendant l'execution** :
1. Ne pas forcer — identifier la cause
2. Presenter le probleme a l'utilisateur
3. Proposer des alternatives
4. Attendre la decision avant de continuer

**Demander confirmation a l'utilisateur une fois l'execution terminee.**

---

## Etape 4: Verification

Verifier le code, recapituler les modifications, sauvegarder le contexte.

| Need | Reference |
|---|---|
| Checklist de verification | [references/verification.md](references/verification.md) |

**Actions** :

1. **Gate "evidence before assertions"** — invoquer `superpowers:verification-before-completion` AVANT toute affirmation que le code est "fini" ou "passe les tests".
   Exige l'output reel des commandes (pas "should work").

2. **Verifier le code** :
   - Lancer les tests (`npm test`, `pytest`, `nextflow run` selon le projet)
   - Verifier la compilation/build
   - Checker les diagnostics IDE (`mcp__ide__getDiagnostics`)
   - Lire les fichiers modifies pour revue rapide

3. **Recapituler les modifications** :
   - `git diff --stat` — vue d'ensemble
   - Liste des fichiers modifies/crees/supprimes
   - Resume fonctionnel de chaque changement
   - Erreurs rencontrees et comment elles ont ete resolues

4. **Code review (au choix)** :
   - Rapide local : `superpowers:requesting-code-review` (gratuit, dans la session)
   - Approfondi cloud : `/ultrareview` (paye apres 3 free runs Pro, ~$5-20/run)
   - Si UI Aima-Tower : `impeccable` + `web-design-guidelines`
   - Si changement securite : `/security-review`

5. **Presenter le recap a l'utilisateur.**

6. **Si tout est OK** — invoquer `/claude-memory` pour sauvegarder les apprentissages de la session (patterns decouverts, decisions architecturales, gotchas).

7. **Finalisation de branche** (si feature sur branche dediee) — invoquer `superpowers:finishing-a-development-branch` pour decider merge / PR / cleanup.

</workflow>

---

## Conflits et overrides avec d'autres skills

- **`superpowers:brainstorming`** est invoque automatiquement avant ce skill (description "MUST use this before any creative work"). Pour les features triviales, indiquer explicitement "skip brainstorming, use code-workflow-feature directement".

- **`superpowers:using-superpowers`** (hook SessionStart) force l'invocation de skills process avant ce skill. Compatible — ce workflow respecte la chaine brainstorming → writing-plans → executing-plans dans la branche D.

- **`using-superpowers`** documente explicitement : *user instructions > skills*. Le `CLAUDE.md` global de Boris (francais, schemas avec fleches, comprendre avant implementer, ISO 15189 -> Boris garde la main) reste prioritaire sur ce workflow.

- **`/ultraplan`** (branche C) deconnecte Remote Control si actif. Choisir B au lieu de C si tu travailles depuis mobile.

- **`superpowers:test-driven-development`** : rigide, ne pas l'adapter (sauf override CLAUDE.md). Suit strictement red-green-refactor.

- **Pour les projets sans CLAUDE.md** (Pod2Bam, methylseq, basecall, IA, short-read) : faire `/init` avant l'Etape 1 pour que l'exploration ait un contexte stable.
