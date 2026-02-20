---
name: save-code
description: Workflow complet de fin de session pour sauvegarder le travail. Met a jour README.md, CLAUDE.md, et la memoire de Claude avec les modifications de la session, puis commit et push. Use when the user wants to save, commit, push their work, or when they say "save", "save-code", "commit and push", "je veux sauvegarder", "on commit", or any variation of saving/committing their modifications.
---

<objective>
Automatise le workflow de fin de session : analyse les changements, met à jour la documentation (README.md, CLAUDE.md, auto memory), puis commit et push. Chaque étape nécessite une confirmation utilisateur avant de passer à la suivante.
</objective>

<workflow>

## Step 1: Analyze Changes

Comprendre ce qui a changé pendant la session.

**Actions:**
1. `git diff --stat` — fichiers modifiés et ampleur des changements
2. `git diff` — contenu détaillé des modifications
3. `git status` — fichiers non-suivis
4. `git log --oneline -5` — derniers commits pour contexte

Produire un résumé clair des modifications :
- Quels fichiers ont été modifiés/créés/supprimés
- Quel est le but fonctionnel des changements
- Quelle est l'ampleur (petit fix, nouvelle feature, refactoring)

**Présenter le résumé à l'utilisateur pour confirmation avant de continuer.**

## Step 2: Update README.md

Mettre à jour le README du projet si les changements l'impactent.

| Need | Reference |
|---|---|
| Quand et comment mettre à jour le README | [references/updates/readme-update.md](references/updates/readme-update.md) |

**Actions:**
1. Lire le README.md existant
2. Déterminer si les changements impactent le README (nouvelle feature, API modifiée, setup changé)
3. Si oui, proposer les modifications au README
4. Si non, informer l'utilisateur et passer à l'étape suivante

**Demander confirmation avant d'appliquer les modifications au README.**

## Step 3: Update CLAUDE.md & Memory (via /claude-memory)

Utiliser le skill `/claude-memory` pour mettre à jour le CLAUDE.md du projet ET la mémoire de Claude de façon optimisée. Ce skill connaît la hiérarchie mémoire, les bonnes pratiques de structuration, et les limites de tokens.

| Need | Reference |
|---|---|
| Patterns de mise à jour CLAUDE.md | [references/updates/claudemd-update.md](references/updates/claudemd-update.md) |
| Patterns de mise à jour mémoire | [references/updates/memory-update.md](references/updates/memory-update.md) |

**Actions:**
1. Invoquer le skill `/claude-memory` avec le contexte des modifications de la session
2. Le skill gère : CLAUDE.md (conventions, commandes, architecture) + MEMORY.md (apprentissages, patterns, debugging) + topic files si nécessaire
3. Proposer les modifications à l'utilisateur pour confirmation

**Demander confirmation avant d'appliquer les modifications.**

## Step 4: Commit & Push

Commit et push des modifications.

| Need | Reference |
|---|---|
| Workflow git sécurisé | [references/git/commit-workflow.md](references/git/commit-workflow.md) |

**Actions:**
1. `git add` — ajouter les fichiers modifiés (spécifiques, pas `git add .`)
2. Proposer un message de commit descriptif
3. **Demander confirmation du message à l'utilisateur**
4. `git commit`
5. `git push`
6. Confirmer le succès avec `git status`

**Ne JAMAIS push sans confirmation explicite de l'utilisateur.**

</workflow>

<quick_reference>

## Checklist Rapide

- [ ] Changements analysés et résumés
- [ ] README.md mis à jour (si nécessaire)
- [ ] CLAUDE.md mis à jour (si nécessaire)
- [ ] Auto memory mise à jour
- [ ] Commit avec message descriptif
- [ ] Push effectué
- [ ] Tout confirmé par l'utilisateur à chaque étape

</quick_reference>
