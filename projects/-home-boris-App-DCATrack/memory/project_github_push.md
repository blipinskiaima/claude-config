---
name: DCATrack GitHub push procedure
description: Repo Lipinski-B/DCATrack push via HTTPS — nécessite gh auth switch vers Lipinski-B (compte AIMA blipinskiaima active par défaut)
type: project
originSessionId: d4e22a2f-03a6-4048-9576-70ff40157692
---
**Repo distant** : `https://github.com/Lipinski-B/DCATrack.git` (compte perso `Lipinski-B`)

**Auth setup** : Boris a 2 comptes GitHub loggués via `gh auth`, **`blipinskiaima` est actif par défaut** (compte AIMA). Le compte qui a accès au repo perso DCATrack est `Lipinski-B`, dormant. Sans switch, `git push` retourne "Repository not found" sur HTTPS.

**Why:** L'erreur trompe — c'est un problème d'auth (mauvais compte actif), pas un problème de clé SSH ou de repo. La précédente version de cette mémoire suggérait à tort une question de clé SSH.

**How to apply:**

Procédure standard pour push DCATrack :

```bash
gh auth switch --user Lipinski-B
git push origin main [<tag>]
gh auth switch --user blipinskiaima   # re-switch pour ne pas casser le contexte AIMA
```

Le compte actif est partagé globalement → toujours re-switcher après push pour ne pas affecter les autres projets AIMA (trace-prod, Bam2Beta, etc.) qui dépendent de `blipinskiaima` actif.

Vérifier avant push : `gh auth status 2>&1 | grep -E "Active account|Logged in"`.
