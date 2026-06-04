---
name: explore-projet
description: Recharge INLINE le contexte du projet courant directement dans la fenêtre principale (pas via subagent) — snapshot de tâche (get-context), MEMORY.md ET ses topic files détaillés, plus un git scan léger. Use when the user says "/explore-projet", "explore le projet", "relance l'exploration", "refresh contexte", "recharge le projet", "recharge la mémoire", "explore-projet", or wants to actually reload full project context/memory into the active session.
allowed-tools: Bash, Read
---

<objective>
Recharger **réellement** le contexte du projet courant dans la fenêtre de la session principale. Contrairement au routing Session Start (qui délègue à `agent-explore-quick` en background pour économiser des tokens), ce skill **lit lui-même** les fichiers — le contenu entre donc directement dans le contexte actif, sans compression par un subagent.

Charge, dans l'ordre :
1. Le **snapshot de tâche** (`get-context`) — l'état mental de la dernière session
2. **MEMORY.md ET ses topic files détaillés** — pas seulement l'index 200 lignes auto-chargé, mais le contenu réel des fichiers liés
3. Un **git scan léger** pour situer l'état courant

**Pourquoi inline** : un subagent lit dans SA propre fenêtre et ne renvoie qu'un résumé compressé. Les topic files détaillés (schemas, patterns) et le snapshot ne sont jamais réellement présents dans la session principale. Ce skill corrige ça en lisant directement.
</objective>

<workflow>

## Step 1: Résoudre les chemins (un seul bloc Bash)

```bash
PROJ=$(basename "$(pwd)")
MEMDIR="$HOME/.claude/projects/$(pwd | sed 's#/#-#g')/memory"
CTX="$HOME/.claude/projects/-home-blipinski/memory/context/$PROJ.md"

echo "=== PROJET: $PROJ ==="
echo "=== MEMDIR: $MEMDIR ==="

# Snapshot de tâche (get-context)
if [ -f "$CTX" ]; then
  AGE_DAYS=$(( ($(date +%s) - $(stat -c %Y "$CTX")) / 86400 ))
  echo "=== SNAPSHOT: $CTX (âge ${AGE_DAYS}j) ==="
else
  echo "=== SNAPSHOT: aucun ==="
fi

# Liste des topic files de mémoire (hors MEMORY.md)
echo "=== TOPIC FILES ==="
ls -1 "$MEMDIR"/*.md 2>/dev/null | grep -v '/MEMORY.md$' || echo "(aucun)"

# Git scan léger
echo "=== GIT ==="
git branch --show-current 2>/dev/null
git log --oneline -10 2>/dev/null
git status --short 2>/dev/null
```

Si cwd = `~` ou dossier non-code → demander confirmation à Boris avant de continuer.

## Step 2: Charger le snapshot de tâche

Si le snapshot existe (`$CTX`), le **lire avec Read** et l'afficher préfixé `📌 État précédent`.
- Si âge > 7 jours → préfixer « ⚠ Snapshot daté de {N}j, possiblement obsolète » mais l'afficher quand même (Boris décide).
- Si absent → le noter en une ligne, continuer.

## Step 3: Charger la mémoire détaillée (cœur du skill)

1. **Read `$MEMDIR/MEMORY.md`** — l'index (déjà partiellement auto-chargé, on le relit pour la fraîcheur).
2. **Read CHAQUE topic file** listé au Step 1, intégralement. C'est le point clé : le contenu réel des schemas/patterns/feedback entre dans la fenêtre, pas seulement leurs titres dans l'index.
   - S'il y a > 15 topic files, charger en priorité ceux dont le `name`/`description` matchent l'intent du premier message de Boris ; sinon tous.

## Step 4: git scan léger

Déjà récupéré au Step 1 (branch / log -10 / status --short). Ne PAS charger le diff complet sauf si Boris le demande.

## Step 5: Synthèse à Boris

Restituer en français, concis, structuré :
- **Tâche en cours** (depuis le snapshot, si présent) + prochaine étape
- **Contexte mémoire** : 3-6 points saillants tirés des topic files réellement lus (pas de paraphrase de l'index)
- **État git** : branche, dernier commit, fichiers modifiés

Pas de subagent lancé. Si une exploration **code-level profonde** est nécessaire (traces d'exécution, architecture), le signaler et proposer de lancer `agent-explore` deep — mais ne pas le lancer automatiquement (décision de Boris).

</workflow>

<quick_reference>

## Quand utiliser ce skill

| Cas | Pourquoi |
|---|---|
| Nouvelle session où le contexte auto-chargé ne suffit pas | Charge le snapshot + les topic files détaillés (jamais auto-chargés) |
| Reprise d'un projet après une pause | Recharge l'état mental précédent + git récent |
| Sortie de compaction | Rebase complet sur la mémoire documentée réelle |
| Tu sens que Claude « a oublié » un schema/pattern documenté | Force la lecture intégrale des topic files |

## Quand NE PAS utiliser

- Pour une exploration **code-level profonde** (architecture, traces) → `agent-explore` deep
- Si tu veux juste économiser des tokens au Session Start → le routing auto (`agent-explore-quick`) suffit

## Inline vs subagent — la distinction clé

| Mécanisme | Lit dans quelle fenêtre | Résultat |
|---|---|---|
| **Session Start auto** (`agent-explore-quick`, Haiku, background) | Fenêtre du subagent | Résumé compressé (<100 lignes) renvoyé à la session principale |
| **`/explore-projet`** (ce skill, inline) | **Fenêtre principale directement** | Contenu réel (snapshot + topic files) présent en contexte, non compressé |

Le subagent **protège** la fenêtre principale ; `/explore-projet` la **remplit**. C'est l'inverse, par dessein.

## Coût indicatif

- Une invocation = lecture inline de ~5-20k tokens (snapshot + MEMORY.md + topic files) dans la fenêtre principale.
- Plus cher qu'un `agent-explore-quick` délégué (~$0.02), mais c'est le prix d'avoir le contexte **réellement en tête** au lieu d'un digest.

</quick_reference>
