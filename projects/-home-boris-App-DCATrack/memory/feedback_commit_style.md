---
name: feedback-commit-style
description: "Sur DCATrack, splitter chore/feat en commits séparés plutôt que de bundler — git log doit raconter l'histoire"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6d8f103e-07c2-4ff7-a6e0-8ebb434e76f3
---

Préférer plusieurs commits ciblés (1 par type chore/feat/fix) plutôt qu'un commit unique qui mélange. Granularité = 1 sujet par commit.

**Why:** Confirmé le 2026-05-14 : pour la feature /portfolio, Boris a choisi B (commit `chore(test): setup vitest` séparé du commit `feat(portfolio): ...`) au lieu de A (commit bundled "feat + setup test"). Argument retenu : git log lisible = chacun raconte une chose, on retrouve facilement pourquoi vitest a été ajouté indépendamment de la feature qui l'a justifié.

**How to apply:** Avant de commit, examiner les fichiers staged et splitter par intention. Setup tooling → `chore(...)`. Nouvelle feature → `feat(...)`. Fix → `fix(...)`. Migration data → `chore(migration): ...`. Si la même session touche plusieurs intentions, faire N commits dans l'ordre logique (setup avant feature, feature avant docs). Format français OK pour le sujet (cf [[feedback-git-author]] pour identité).
