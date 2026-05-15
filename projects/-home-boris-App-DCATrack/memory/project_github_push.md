---
name: DCATrack GitHub push status
description: Repo lié à git@github.com:Lipinski-B/DCATrack.git mais push manuel requis (auth)
type: project
---

**Repo distant** : `git@github.com:Lipinski-B/DCATrack.git` (compte perso `Lipinski-B`)

**État au 1er mai 2026** : commit local prêt mais **non poussé** — la clé SSH locale `~/.ssh/id_ed25519` est associée à l'email pro AIMA (`boris.lipinski@aima-diagnostics.com`) qui n'est pas lié au compte GitHub perso.

**Why:** Boris a dit "je push manuellement après" — il choisira entre :
- Ajouter cette clé SSH à son GitHub perso (https://github.com/settings/ssh/new)
- Générer une 2ᵉ clé SSH dédiée perso (`ssh-keygen -f ~/.ssh/id_github_perso`)
- Personal Access Token via HTTPS
- `gh` CLI (`sudo apt install gh && gh auth login`)

**How to apply:**
- Ne PAS tenter `git push` automatique sur ce repo tant que l'auth n'est pas configurée
- Si Boris demande "tu peux push DCATrack ?", vérifier d'abord `ssh -T git@github.com` ou `gh auth status`
- Une fois résolu, mettre à jour cette mémoire (supprimer le warning) ou la supprimer
