# Signal pack — audit Claude Code Boris (2026-04-09 → 2026-05-09)

> Toutes les commandes ci-dessous sont reproductibles. `TR=$(find ~/.claude/projects -name '*.jsonl' -mtime -30 -type f -not -path '*/subagents/*')` sauf indication contraire.

## 1. Volume

| Métrique | Valeur | Commande |
|---|---|---|
| Sessions principales (jsonl top-level) | **100** | `find . -name "*.jsonl" -mtime -30 -not -path "*/subagents/*" \| wc -l` |
| Transcripts subagent | **133** | `find . -name "*.jsonl" -mtime -30 -path "*/subagents/*" \| wc -l` |
| Volume total transcripts | 8.4 MB | `find ... -printf "%s\n" \| awk '{s+=$1}END{print s/1024/1024}'` |
| User messages (string) | **2 254** | `jq 'select(.type=="user" and (.message.content\|type=="string"))'` |
| Assistant messages | **17 873** | `jq 'select(.type=="assistant")'` |
| Tool calls totaux | **8 839** | `jq 'select(...tool_use)' \| wc -l` |
| Tool calls / user turn | **3.92** | calculé |
| Jours actifs (stats-cache) | **16/22** | `stats-cache.json` window 04-09→05-05 |
| Sessions / jour (médiane) | 4 | stats-cache |
| Pic msgs/jour | 4 178 (2026-04-29) | stats-cache |
| Médiane durée session | **31 min** | premier→dernier user.timestamp |
| p95 durée session | 1 437 min | idem (sessions Cursor IDE persistantes) |
| Mean turns/session | 25.6 | idem |
| p95 turns/session | 87 | idem |
| Sessions parallèles max (1h) | **8** (2026-04-13T15h) | groupBy hour, count distinct sessionId |
| Plage horaire dominante | 8h-15h UTC | `jq .timestamp \| hour histogram` |

## 2. Coût / modèles / cache

| Métrique | Valeur |
|---|---|
| Opus 4.7 invocations | 12 498 |
| Opus 4.6 invocations | 5 341 |
| Sonnet 4.6 invocations | **1** |
| Haiku 4.5 invocations | **0** |
| Cache hit rate | **97.86 %** |
| Cache read tokens | 4.38 G |
| Cache create tokens | 96.0 M |
| Output tokens | 17.3 M |
| Coût retail équivalent (Opus 4.7) | ~$9 676 / 30j (Boris est sur sub flat) |

## 3. Top tools (top 30)

```
4472 Bash      1845 Edit      1069 Read      380 Write     369 TaskUpdate
208 TaskCreate 138 Agent      110 Grep        80 ToolSearch 70 Skill
68 TaskOutput   43 AskUserQuestion 20 ScheduleWakeup 14 WebSearch
14 Monitor      13 ExitPlanMode 11 Glob         7 TaskList   6 WebFetch
5 TaskStop       5 EnterPlanMode  2 SendMessage   1 mcp__ide__getDiagnostics
```

## 4. Top Bash verbes (premier token, ≥150)

```
2620 echo  | 937 cd  | 757 for  | 696 python3  | 661 grep  | 607 docker
601 import | 536 git | 442 if   | 375 ls       | 313 from | 272 cat
254 curl   | 224 print() | 220 AWS_PROFILE=scw | 219 EOF | 193 sleep | 191 tail
```

Anti-patterns Bash :
- **3 030 cat/head/tail** (≈ 19 % des Bash) — règle système préconise `Read`
- **674 commandes commencent par cat/head/tail** précédés d'un séparateur
- **193 `sleep N`** — détail : `sleep 2` ×102, `sleep 3` ×93, `sleep 5` ×53, `sleep 300` ×6
- nextflow : seulement **122 hits** (Boris lance manuellement hors Claude)
- gh CLI : **2 hits** seulement

## 5. Skills (31 définies, 12 invoquées)

| Skill | Inv. | Skill | Inv. |
|---|---|---|---|
| save-code | 17 | maj-todo-list | 17 |
| commit-claude | 17 | end-session | **20** *(via slash)* |
| prompt-creator | 5 | karpathy-guidelines | 3 |
| code-workflow-feature | 2 | clean-skill | 2 |
| claude-memory | 2 | add-todo-list | 2 |
| batch-effect | 1 | meta-skills-creator | 1 |
| test-bam2beta | 1 | | |

**19 skills à 0 invocation** : audit-trail, check-consistency, compare-batches, correlation, debug-nf, git-commit, git-create-pr, git-fix-pr-comments, git-merge, python-refactor, qc-report, sample, standby-todo-list, subagent-creator, utils-fix-grammar, utils-oneshot, veille, workflow-apex, pull-claude (1 only).

Slash commands invoqués (top 10) :
```
23 /save-code   22 /maj-todo-list   20 /end-session   19 /commit-claude
18 /prompt-creator 12 /karpathy-guidelines  9 /code-workflow-feature
 8 /seqera       3 /plugin           3 /compact
```

## 6. Subagents (4 définis)

| Subagent | Invocations |
|---|---|
| agent-explore (deep) | **75** |
| agent-websearch | 19 |
| agent-explore-quick | 1 |
| **agent-docs** | **0** |

Plus le subagent built-in `Explore` ×16 et `general-purpose` ×21.

## 7. Distribution projets (turns par cwd)

```
15113 Aima-Tower         5056 SampleSheetChecker   5008 Aima-Survey
 3865 Bam2Beta           3699 trace-prod           1497 exploratory-CGFL-HCL
  893 Feature             823 home                  468 .claude
  460 Pod2Bam
```

Top 3 → **Aima-Tower, SampleSheetChecker, Aima-Survey**.

## 8. MCP

```
1 mcp__ide__getDiagnostics  ←  SEUL appel MCP en 30 jours
```

Servers configurés mais **0 invocation** : pubmed, memory, seqera, context7, browser-tools, gmail, calendar, drive, aim_memory.

## 9. Frictions

| Pattern | Count |
|---|---|
| Tool errors totaux (`is_error:true`) | **263** |
| `File has not been read yet` | 26 |
| `File has been modified since read` | 11 |
| `String to replace not found` | 6 |
| `user doesn't want to proceed` (refus Esc) | **27** |
| `Cancelled: parallel tool call` | 14 |
| Traceback Python | 21 |
| `Exit code N` | 130 |
| Sessions avec ≥8 Bash consécutifs | **135** |
| Plus longue chaîne Bash consécutive | **50** |

ScheduleWakeup avec `delaySeconds=300` : **4×** — anti-pattern explicite (system prompt : *"Don't pick 300s. It's the worst-of-both"*).

## 10. Corrections utilisateur (échantillons verbatim)

- `non laisse tomber` (trace-prod 2d864d82)
- `non c'est pas ouf, créer 2 figure...` (Aima-Tower 4515443f)
- `non check encore` (SampleSheetChecker 2debb934)
- `non mais demande moi chaque item un par un` (Bam2Beta 957bf81d)
- `non je veux que toute la suite soit lancé dans un tmux` (Bam2Beta 1cb84555)
- `non ne parallèlise pas` (Aima-Tower)
- `non débrouille toi pour fetch ce papier` (veille)
- `non supprime tout les papier de biorxiv et medrxiv y'a rien qui va`

## 11. Patterns répétés (≥10×) — candidats skill

```
11× "explore le projet en profondeur en background"   ← déjà dans CLAUDE.md global
10× "docker compose down && docker compose build && docker compose up -d && docker compose logs -f"
```

## 12. Hooks configurés (3)

| Event | Matcher | Action |
|---|---|---|
| PreToolUse | Bash | Bloque `aws s3 rm/rb/sync --delete` |
| Notification | * | `notify-send` (desktop) |
| Stop | * | `~/.claude/scripts/auto-push-on-stop.sh` |

**Non configurés** : UserPromptSubmit, SessionStart, SessionEnd, PostToolUse, SubagentStop, PreCompact.

## 13. Permissions

73 allow globaux + 54 local = **127 règles**, **0 deny**, **0 ask**.

## 14. Plugins installés

frontend-design, feature-dev, code-review, code-simplifier (tous claude-plugins-official).

## 15. Background / async

```
117 Bash  run_in_background=true
115 Agent run_in_background=true
```

Boris est très à l'aise avec l'async. `Monitor` utilisé 14× pour `while pgrep ... do sleep N; done` (usage canonique).

## 16. Worktree / sandbox

```
0 EnterWorktree     0 ExitWorktree     0 isolation:worktree
5 EnterPlanMode    13 ExitPlanMode
```

Plan mode utilisé asymétriquement (sortie sans entrée → Esc pendant exécution).

---

*Régénération mensuelle :* relancer toutes les commandes ci-dessus avec `find ... -mtime -30`. Comparer les compteurs entre signal-packs successifs.
