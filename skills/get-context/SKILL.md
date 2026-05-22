---
name: get-context
description: Charge le snapshot de contexte de tâche en cours sauvegardé par /save-context pour le projet courant. Affiche l'état mental précédent (où j'en étais, ce qui marche/foire, prochaine étape). Use when the user says "/get-context", "récupère le contexte", "où j'en étais", "load context", "snapshot précédent". Appelé automatiquement par agent-explore-quick au Session Start.
allowed-tools: Bash, Read
---

<objective>
Lire le snapshot `~/.claude/projects/-home-blipinski/memory/context/{projet}.md` (s'il existe) et l'afficher en début de session pour rappeler à Boris où il en était sur la tâche en cours.
</objective>

<workflow>

## Step 1 : Détecter le projet

`basename "$(pwd)"` (ou nom passé en argument optionnel).

## Step 2 : Vérifier l'existence du snapshot

```bash
CTX=~/.claude/projects/-home-blipinski/memory/context/{projet}.md
test -f "$CTX" || { echo "Aucun snapshot pour {projet}."; exit 0; }
```

Si absent → retourner « Aucun snapshot pour {projet}. » et s'arrêter.

## Step 3 : Vérifier la fraîcheur

```bash
AGE_DAYS=$(( ($(date +%s) - $(stat -c %Y "$CTX")) / 86400 ))
```

Si `AGE_DAYS > 7` → préfixer l'affichage avec « ⚠ Snapshot daté de {N} jours, probablement obsolète » mais afficher quand même (Boris décide s'il l'utilise).

## Step 4 : Afficher

Lire le contenu du fichier et l'afficher préfixé :

```
📌 État précédent (snapshot du {timestamp lu dans le fichier})

{contenu du fichier}
```

Si appelé depuis `agent-explore-quick`, intégrer en section dédiée du résumé de l'agent au lieu d'un bloc à part.

</workflow>

<notes>

- Un seul snapshot par projet — pas de gestion d'historique
- Last-writer-wins en cas de sessions parallèles (acceptable)
- Skill read-only : ne modifie jamais le snapshot

</notes>
