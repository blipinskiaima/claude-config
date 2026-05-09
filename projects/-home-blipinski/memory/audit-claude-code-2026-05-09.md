---
name: Audit Claude Code 2026-05-09
description: Audit comportemental sur 30 jours de transcripts (2026-04-09 → 2026-05-09), 100 sessions, ~28k msgs, 8839 tool calls. Croisé avec doc Claude Code intégrale (skills, hooks, statusline, mcp, sub-agents, output-styles, routines, channels, remote-control, scheduled-tasks, ultraplan, ultrareview, memory, permissions, permission-modes, auto-mode-config, settings, best-practices) + 7 changelogs hebdo (w13-w19) + Code w/ Claude 06/05.
type: project
originSessionId: 5c2e6575-d6ed-4927-a8a3-78918dc2635a
---
# Audit Claude Code — Boris (2026-05-09)

> Fenêtre transcripts : **2026-04-09 → 2026-05-09**.
> Source primaire : `~/.claude/projects/**/*.jsonl` mtime ≤ 30j.
> Doc Claude Code croisée : **18 pages doc fetchées intégralement** + 7 changelogs hebdo + event Code w/ Claude (06/05).
> Pack signal complet : [`audit-2026-05-09/signal-pack.md`](audit-2026-05-09/signal-pack.md).

---

## Résumé exécutif

**Volume** — 100 sessions principales + 133 transcripts subagents, 2 254 user messages, 8 839 tool calls (3.92/turn), 16 jours actifs/30. Cache hit 97.86 %. Modèle dominant Opus 4.7 (12 498) puis 4.6 (5 341). Sonnet/Haiku quasi inexistants en main session.

**Top 5 frictions :**
1. **3 030 invocations `cat`/`head`/`tail` dans Bash** (≈ 19 % du Bash). N'entraîne pas de prompts permission (read-only built-in), mais inefficient vs `Read` (indexation, cache, troncation propre). System prompt CLI le préconise.
2. **263 tool errors** : 27 refus user (`Esc`), 26 « File has not been read yet » (résolu en partie depuis w14 : Edit fonctionne après `cat`/`sed -n`), 11 « modified since read », 14 « Cancelled parallel tool call ».
3. **Boris demande explicitement le mobile** (verbatim 2× dans transcripts) — Remote Control + push notifications mobile sont GA depuis le 16/04, jamais activés.
4. **127 allow rules manuelles** (73 globales + 54 local) sans utiliser `/fewer-permission-prompts` (skill bundled w16 qui le fait pour toi). Aucune `permissions.deny`, alors que les règles d'arguments fragiles (ex: `Bash(rm:*pod5*)` sont contournées par l'env-var prefixing) recommandent un hook PreToolUse pour les golden rules.
5. **`docker compose down && build && up -d && logs -f`** verbatim 10× sur Aima-Tower + 135 sessions ≥ 8 Bash consécutifs (chaîne max 50). Aucun skill.

**Top 5 actions (ordre impact / effort) :**
1. **`/fewer-permission-prompts`** — auto-génère un allowlist depuis tes transcripts. Effort < 1 minute.
2. **Remote Control + push mobile** — `claude --version` (≥ 2.1.110), `claude remote-control`, `/config` → "Push when Claude decides".
3. **MCP DuckDB read-only** sur les 3 bases trace-* — friction quotidienne supprimée.
4. **`PreCompact` hook + `if:` PreToolUse** scopés aux golden rules POD5 / Nextflow / scw — couvre 5/6 rules non protégées.
5. **`/recap` + `/usage`** activés — 8 sessions parallèles → besoin de visibilité.

**⚠ Limites de plan importantes** : Auto mode et `autoMode.*` ne sont **pas disponibles sur Pro** (Max / Team / Enterprise / API uniquement). Boris est sur Pro → pas de levier auto-mode tant qu'il ne change pas de plan. Ultrareview : 3 free runs Pro **expirées le 2026-05-05**, donc payant à $5-20/run.

---

## Phase 1 — Signal pack (résumé)

| KPI | Valeur |
|---|---|
| Sessions principales / jours actifs | 100 / 16 |
| User msgs / Tool calls | 2 254 / 8 839 |
| Skills définies / utilisées | **31 / 12** |
| Subagents définis / utilisés | 4 / 3 (`agent-docs` 0×) |
| MCP servers configurés / appelés | 9 / **1** (`mcp__ide__getDiagnostics`) |
| Cache hit rate | 97.86 % |
| Sessions parallèles max (1h) | 8 |
| Hooks configurés | 3 (PreToolUse Bash, Notification, Stop) |

Top projets : **Aima-Tower** (15 113 turns), **SampleSheetChecker** (5 056), **Aima-Survey** (5 008), Bam2Beta (3 865), trace-prod (3 699). Détail commandes reproductibles : voir signal-pack.md.

---

## Phase 2 — Interprétation de la config

**Skills à 0 invocation — 4 causes** :
- **Mismatch nom dossier ↔ frontmatter** : `git-commit/SKILL.md:4` expose `name: commit`, `git-create-pr` expose `name: create-pr`, `workflow-apex/SKILL.md:1` expose `name: apex`. La doc skills confirme : `name` champ détermine le nom canonique. Taper `/git-commit` ou `/workflow-apex` ne match rien.
- **Frontmatter non-standard** : `python-refactor/SKILL.md:8` n'a pas de YAML (utilise un bloc ```yaml inline) → invisible.
- **Description correcte mais use-case rare** : `subagent-creator`, `meta-skills-creator`, `utils-fix-grammar`.
- **Description correcte, simplement oubliée** : `compare-batches`, `correlation`, `qc-report`, `audit-trail`, `debug-nf`, `veille`, `sample`. Triggers AIMA explicites mais pas activés en pratique.

**`end-session` `disable-model-invocation: true`** : doc skills.md confirme — *« Only you can invoke the skill. Use this for workflows with side effects or that you want to control timing »*. Sortir du contexte est volontaire pour éviter auto-suggest. Boris l'utilise 20× via slash → flag probablement intentionnel.

**MCP — un seul fonctionne** : `mcp-needs-auth-cache.json` flague seqera + Gmail/Drive/Calendar en attente d'auth ~2 sem. **Depuis w18** : `claude auth login` accepte l'OAuth code collé directement (résout SSH où le callback localhost échoue). **Depuis w19** : `/mcp` montre tool count + flag les serveurs à 0 tool. **Depuis w18 aussi** : MCP transient errors auto-retry ×3.

**Couverture hooks vs golden rules — 1/6** : seul `aws s3 rm|rb|sync --delete` est protégé. Non couverts : POD5, profil scw obligatoire, lancement Nextflow hors `~/Pipeline/*`, scan secrets, `CREATE TABLE AS SELECT` DuckDB. **Important** : la doc permissions.md est explicite — *« Bash permission patterns that try to constrain command arguments are fragile »* (env-var prefixing, redirects, variables peuvent contourner). Pour les rules robustes, **hooks PreToolUse + `if:` field** (w13) ou **sandboxing** sont les seules options fiables.

**`agent-docs` vs `agent-websearch`** : descriptions chevauchantes. `agent-docs` cible la doc versionnée (Context7), `agent-websearch` la recherche ouverte. Boris utilise le second 19× pour des cas où le premier serait mieux. Confusion explique non-usage.

**Modèles dans agents/skills** : `agent-explore` et `agent-websearch` en `sonnet`, `agent-explore-quick` et skills `git-*` en `haiku`. Comme git-* jamais invoquées, Haiku reste à **0 invocation**. Note : depuis w16, default effort `high` Pro/Max sur Opus 4.6/4.7 + nouveau `xhigh`.

**`.claude/rules/` est officiellement supporté** par Claude Code (mémoire / path-specific rules). Boris l'utilise déjà avec 6 fichiers (s3-safety, secrets, nextflow, duckdb, aliases, troubleshooting, aima-brand, template-claude-md). La doc memory.md précise : *« Rules without `paths` field are loaded unconditionally »* — toutes les rules de Boris sont globales, ce qui est OK pour des golden rules mais sous-optimal pour aima-brand/template (peuvent être scopés `paths: ["**/*.tex", "**/*.typ"]`).

**Auto memory officielle** : Boris utilise déjà `~/.claude/projects/-home-blipinski/memory/MEMORY.md` (système intégré, lecture des 200 premières lignes / 25KB par session). C'est le mécanisme officiel ; le **MCP `memory`** community est redondant.

**StatusLine sous-exploitée** : utilise uniquement `workspace.current_dir`. Disponibles dans le JSON input : `model.display_name`, `cost.total_cost_usd`, `context_window.used_percentage`, `cost.total_lines_added/removed`, `workspace.git_worktree`. Depuis w15, `refreshInterval` setting permet le re-run périodique.

**CLAUDE.md projets top-3** présents et précis (Dash, scripts Bash 317 lignes, veille PubMed → Aima-Tower).

**Memory staleness** : MEMORY.md non touché depuis 19j (warning système au démarrage), `inventaire-claude-code.md` 26j.

---

## Phase 3 — Caractérisation du workflow

### Ce que Boris **évite**

- **19 skills à 0 invocation/30j** : audit-trail, check-consistency, compare-batches, correlation, debug-nf, git-commit, git-create-pr, git-fix-pr-comments, git-merge, python-refactor, qc-report, sample, standby-todo-list, subagent-creator, utils-fix-grammar, utils-oneshot, veille, workflow-apex. batch-effect 1×.
- **`agent-docs` jamais invoqué** alors que défini avec `model: sonnet`.
- **MCP** : 1 appel /30j. pubmed/memory/seqera/context7/aim_memory/browser-tools configurés mais inertes.
- **Sonnet 4.6 / Haiku 4.5** : 1 et 0 invocations directes (hors subagents).
- **Worktree 0 invocations**. **EnterPlanMode 5** vs **ExitPlanMode 13** (8 abandons).
- **`/init` 1×/30j** ; 5 projets sans CLAUDE.md (Pod2Bam, methylseq, basecall, IA, short-read).
- **Skills built-in jamais invoquées** : `/fewer-permission-prompts`, `/review`, `/security-review`, `/usage`, `/recap` (w17), `/team-onboarding` (w15), `/powerup` (w14), `/loop` (Boris fait `ScheduleWakeup` à la place).

### Frictions principales — 5 plus aiguës (verbatim)

1. **Anti-pattern `cat`/`head`/`tail` Bash** — 3 030 hits. `ls`/`cat`/`head`/`tail` sont read-only built-in (auto-allowed sans prompt) → **pas une friction permission**, mais **friction d'efficacité** : `Read` est indexé, paginated, et le résultat est inclus dans le cache de manière propre. Boris perd ~19 % de son budget Bash. Ex: trace-prod `2d864d82`, Aima-Tower `e7cf4774`.

2. **263 tool errors** dont 26 « File has not been read yet », 11 « File has been modified since read », 6 « String to replace not found », 27 « user doesn't want to proceed », 14 « Cancelled parallel tool call ».

3. **Corrections utilisateur fréquentes** :
   - `non laisse tomber` — trace-prod `2d864d82`
   - `non check encore` — SampleSheetChecker `2debb934`
   - `non mais demande moi chaque item un par un` — Bam2Beta `957bf81d`
   - `non ne parallèlise pas` — Aima-Tower
   - `non je veux que toute la suite soit lancé dans un tmux` — Bam2Beta `1cb84555`
   - **`non je veux suivre une session de claude lancé ici directement sur mon téléphone`** → demande Remote Control
   - **`non mais j'ai pas un skill mobile?`** → demande Remote Control / push notif

4. **Anti-pattern sleep / ScheduleWakeup 300s** — 193 `sleep N` dont 6× `sleep 300` + 4× `ScheduleWakeup` à `delaySeconds: 300` (anti-pattern documenté : cache TTL 5 min). **Depuis w15**, `/loop` self-pacing (1 min – 1 h) + tool **Monitor** sont les remplaçants officiels — Monitor déjà utilisé 14× par Boris ✓.

5. **`docker compose down && build && up -d && logs -f`** verbatim 10×, presque tout cwd Aima-Tower + 135 sessions avec ≥ 8 Bash consécutifs, chaîne max 50. Aucun skill, aucun alias.

### Ce qui marche (à préserver)

- Cache hit 97.86 % → CLAUDE.md global + rules + skills bien stables.
- 115 Agents + 117 Bash en `run_in_background` + 14× Monitor canonique → async maîtrisé.
- Hook `Stop` `auto-push-on-stop.sh` + Notification `notify-send` adaptés à Cursor IDE.
- Custom skills domain-specific (`save-code` 17, `maj-todo-list` 17, `commit-claude` 17, `prompt-creator` 5) → 75 % de l'usage skill.
- 75 invocations `agent-explore` deep en background → règle « exploration au démarrage » respectée.
- `~/.claude/rules/` correctement organisé avec 8 fichiers golden rules → bon usage du système officiel `.claude/rules/`.
- Auto memory active (`~/.claude/projects/-home-blipinski/memory/`) → mécanisme officiel utilisé.

---

## Phase 4 — Gap analysis

### 4.A — Primitives existantes / bundled jamais invoquées

| # | Primitive | Friction | Doc | Fit |
|---|---|---|---|---|
| A1 | **`/fewer-permission-prompts`** (skill bundled w16) | 127 allow rules manuelles | [w16](https://code.claude.com/docs/en/whats-new/2026-w16) | **high** |
| A2 | **`/usage`** (merged `/cost`+`/stats` w17, breakdown w16) | 8 sessions parallèles | [commands](https://code.claude.com/docs/en/commands) | high |
| A3 | **`/recap`** (session recap auto w17) | sessions p95 1437min | [interactive-mode](https://code.claude.com/docs/en/interactive-mode) | high |
| A4 | **`/memory`** view + maintenance | MEMORY.md staleness 19j | [memory](https://code.claude.com/docs/en/memory) | medium |
| A5 | **`/skills` filter** (w18 type-to-search) | 31 skills | [w18](https://code.claude.com/docs/en/whats-new/2026-w18) | medium |
| A6 | **`/team-onboarding`** (w15) | bus factor 1 | [w15](https://code.claude.com/docs/en/whats-new/2026-w15) | medium |
| A7 | **`/powerup`** (w14 interactive lessons) | 30+ features ratées en 30j | [w14](https://code.claude.com/docs/en/whats-new/2026-w14) | low |
| A8 | **`agent-docs`** subagent défini | `agent-websearch` 19× pour cas mieux servis par doc versionnée | `agent-docs.md:1-6` | medium |
| A9 | **PubMed MCP** installé jamais invoqué | priorité veille AIMA | [@cyanheads/pubmed-mcp-server](https://github.com/cyanheads/pubmed-mcp-server) | medium |
| A10 | **Built-in subagent `claude-code-guide`** (Haiku) | Boris a raté 30+ features | [sub-agents](https://code.claude.com/docs/en/sub-agents) | low |
| A11 | **`/init` quasi inutilisé** | 5 projets sans CLAUDE.md | [memory](https://code.claude.com/docs/en/memory) | medium |
| A12 | **`CLAUDE_CODE_NEW_INIT=1`** (multi-phase interactif) | nouveau projet | [memory](https://code.claude.com/docs/en/memory) | low |

### 4.B — Primitives Claude Code récentes non adoptées

#### Mobile / Remote / Async

| # | Primitive | Statut | Friction | Doc | Fit |
|---|---|---|---|---|---|
| B1 | **Remote Control** + **mobile push notifications** | GA (push depuis w16, requires v2.1.110+) | 2 demandes verbatim Boris | [remote-control](https://code.claude.com/docs/en/remote-control) | **high** |
| B2 | **Routines** cloud (Pro/Max/Team/Ent) — schedule min 1h, GitHub events, API webhook | Research preview, GA web depuis w16 | veille scientifique en cron local | [routines](https://code.claude.com/docs/en/routines) | medium |
| B3 | **Channels** plugin MCP (Telegram/Discord/iMessage/fakechat) | Research preview, v2.1.80+ | bus factor 1, demande mobile | [channels](https://code.claude.com/docs/en/channels) | medium |
| B4 | **`/loop` self-pacing + Monitor** | GA depuis w15 | 4× `ScheduleWakeup 300s` anti-pattern | [scheduled-tasks](https://code.claude.com/docs/en/scheduled-tasks) | high |

#### Permissions / safety / hooks

| # | Primitive | Statut | Friction | Doc | Fit |
|---|---|---|---|---|---|
| B5 | **`permissions.deny` rules** (path-based pour Read/Edit, exact pour Bash) | GA | 0 deny malgré 5 golden rules | [permissions](https://code.claude.com/docs/en/permissions) | **high** |
| B6 | **Hook PreToolUse `if:` field** (w13) — scope un hook à une cmd, pas spawn process à chaque Bash | GA | hook actuel spawn à chaque Bash | [hooks](https://code.claude.com/docs/en/hooks) | high |
| B7 | **`PreCompact` hook block decision** (w16) | GA | CLAUDE.md prescrit conservation Nextflow | [hooks](https://code.claude.com/docs/en/hooks) | medium |
| B8 | **Hooks call MCP tools `type: "mcp_tool"`** (w17) | GA | hook qui hit MCP sans process | [hooks](https://code.claude.com/docs/en/hooks#mcp-tool-hook-fields) | low |
| B9 | **`InstructionsLoaded` hook** | GA | debug ce qui est chargé (rules/CLAUDE.md/auto memory) | [hooks](https://code.claude.com/docs/en/hooks) | low |
| B10 | **Hook `UserPromptSubmit` set sessionTitle** (w15) | GA | 8 sessions parallèles | [hooks](https://code.claude.com/docs/en/hooks) | low |
| B11 | **Hook `UserPromptSubmit` expansion alias `tp`** | GA | aliases.md non auto-utilisé | [hooks](https://code.claude.com/docs/en/hooks) | medium |
| B12 | **PostToolUse `hookSpecificOutput.updatedToolOutput`** (w18) | GA | rewrite tool output (ex: redact secrets) | [hooks](https://code.claude.com/docs/en/hooks) | low |
| ~~B5'~~ | ~~Auto mode + `autoMode.hard_deny`~~ | **NON DISPONIBLE SUR PRO** | — | — | **N/A** |

#### MCP / extensions

| # | Primitive | Statut | Friction | Doc | Fit |
|---|---|---|---|---|---|
| B13 | **MCP DuckDB read-only** | stable | 265× check_samples.py | [ktanaka101/mcp-server-duckdb](https://github.com/ktanaka101/mcp-server-duckdb) | **high** |
| B14 | **MCP S3 Scaleway read-only** (txn2/mcp-s3 endpoint custom) | stable | 220× S3 hits, golden rule | [txn2/mcp-s3](https://github.com/txn2/mcp-s3) | high |
| B15 | **Réauthentifier seqera MCP** (paste OAuth w18) | GA | down 2 sem | [w18](https://code.claude.com/docs/en/whats-new/2026-w18) | medium |
| B16 | **MCP `alwaysLoad: true`** (w18, opt out tool-search defer) | GA | tools auto-disponibles | [mcp](https://code.claude.com/docs/en/mcp) | low |

#### Modèles / runtime

| # | Primitive | Statut | Friction | Doc | Fit |
|---|---|---|---|---|---|
| B17 | **`xhigh` effort + `/effort` slider** (w16) | GA Opus 4.7 | tâches ISO 15189 critiques | [model-config](https://code.claude.com/docs/en/model-config) | medium |
| B18 | **Subagent `memory: user|project|local`** (frontmatter) | GA | agent-explore pourrait accumuler obs sur ~/Pipeline | [sub-agents](https://code.claude.com/docs/en/sub-agents) | medium |
| B19 | **Subagent `isolation: worktree`** | GA | exploration risquée hors main worktree | [sub-agents](https://code.claude.com/docs/en/sub-agents) | low |
| B20 | **Subagent `--agents '{...JSON}'` flag CLI** | GA | tests rapides de subagent ad-hoc | [sub-agents](https://code.claude.com/docs/en/sub-agents) | low |
| B21 | **Native binaries (no Node)** + bfs/ugrep | GA auto w16/w17 | 110 Grep + 11 Glob | auto | auto |

#### Cloud / agentic

| # | Primitive | Statut | Friction | Doc | Fit |
|---|---|---|---|---|---|
| B22 | **`/ultraplan`** (cloud planning + comments par section) | Research preview, v2.1.91+, Pro OK | 8 abandons /13 ExitPlanMode | [ultraplan](https://code.claude.com/docs/en/ultraplan) | medium |
| B23 | **`/ultrareview` + `claude ultrareview` non-interactive** | Research preview, v2.1.86+ — **3 free runs Pro expirés 2026-05-05**, $5-20/run après | ISO 15189 Bam2Beta pre-merge | [ultrareview](https://code.claude.com/docs/en/ultrareview) | medium |
| B24 | **Dreaming** (Managed Agents) | Research preview 06/05, **plan inconnu sur Pro** (probablement non) | MEMORY staleness, 100 sessions | [managed-agents/dreams](https://platform.claude.com/docs/en/managed-agents/dreams) | low* |
| B25 | **`--from-pr` resume by PR URL** (w18) | GA | gh CLI 2× /30j → faible levier | [w18](https://code.claude.com/docs/en/whats-new/2026-w18) | low |

#### Productivité quotidienne

| # | Primitive | Statut | Friction | Doc | Fit |
|---|---|---|---|---|---|
| B26 | **Output style « AIMA-clinical »** (FR, terse, ISO awareness) | GA | corrections « item par item » | [output-styles](https://code.claude.com/docs/en/output-styles) | medium |
| B27 | **StatusLine enrichie** (model + cache % + cost + ctx %) | GA | 8 sessions parallèles | [statusline](https://code.claude.com/docs/en/statusline) | medium |
| B28 | **`refreshInterval` statusLine** (w15) | GA | actualisation auto | [statusline](https://code.claude.com/docs/en/statusline) | low |
| B29 | **`@import` syntax dans CLAUDE.md** | GA | factoriser instructions home/projet | [memory](https://code.claude.com/docs/en/memory) | low |
| B30 | **Path-scoped `.claude/rules/`** (`paths:` frontmatter) | GA | aima-brand/template ne sont utiles que pour reports | [memory](https://code.claude.com/docs/en/memory) | low |
| B31 | **`Ctrl+R` history search across all projects** (w19) | GA | 100 sessions, retrouver une cmd | [interactive-mode](https://code.claude.com/docs/en/interactive-mode) | auto |
| B32 | **`CLAUDE.local.md`** (gitignored personal preferences) | GA | aliases tp non versionnés | [memory](https://code.claude.com/docs/en/memory) | low |

### 4.C — Anti-patterns observés

| # | Anti-pattern | Évidence | Doc qui contredit |
|---|---|---|---|
| C1 | **`cat`/`head`/`tail` au lieu de `Read`** — friction d'efficacité, pas permission | 3 030 hits (read-only built-in, mais inefficient) | system prompt CLI + `Read` indexé |
| C2 | **`sleep 300` (×6) + `ScheduleWakeup 300s` (×4)** | signal-pack §4 + §16 | system prompt cache TTL 5min ; alternative `/loop` self-pacing + Monitor |
| C3 | **Edit/Write avant Read** | 26 « File has not been read yet » | Edit fonctionne après `cat`/`sed -n` depuis w14 (résout en partie) |
| C4 | **MEMORY.md staleness 19j + inventaire 26j** | mtime fichiers | CLAUDE.md global prescrit |
| C5 | **Plan mode abandonné 8/13** | 13 ExitPlanMode vs 5 EnterPlanMode | `/ultraplan` (refine via UI dédiée) |
| C6 | **127 allow rules manuelles, 0 deny** | settings.json + settings.local.json | `/fewer-permission-prompts` + `permissions.deny` + hooks |
| C7 | **Skills `git-commit`/`workflow-apex` mismatch nom** | frontmatter `name:` ≠ basename | [skills](https://code.claude.com/docs/en/skills) |
| C8 | **Permission rules d'arguments fragiles** | env-var prefixing contournable | doc permissions explicite : préférer hooks ou sandboxing |
| C9 | **ScheduleWakeup au lieu de `/loop` self-pacing** | 20 SchedWakeup / 0 `/loop` | [w15](https://code.claude.com/docs/en/whats-new/2026-w15) |

---

## Phase 5 — Roadmap priorisée

| # | Action | Bucket | Friction | Effort | Impact | Doc | First step |
|---|---|---|---|---|---|---|---|
| 1 | **`/fewer-permission-prompts`** | 4.A (A1) | 127 allow rules | XS | high | [w16](https://code.claude.com/docs/en/whats-new/2026-w16) | Lancer `/fewer-permission-prompts` dans une session active, accepter le diff `.claude/settings.json` |
| 2 | **Activer Remote Control + push mobile** | 4.B (B1) | 2 demandes verbatim | S | high | [remote-control](https://code.claude.com/docs/en/remote-control) | Vérifier `claude --version` ≥2.1.110, installer app mobile, `claude remote-control`, `/config` → "Push when Claude decides" |
| 3 | **MCP DuckDB read-only sur trace-prod** | 4.B (B13) | 265× check_samples.py | S | high | [mcp-server-duckdb](https://github.com/ktanaka101/mcp-server-duckdb) | `claude mcp add duckdb-trace-prod -- uvx mcp-server-duckdb --db-path ~/Pipeline/trace-prod/database/samples_status.duckdb --readonly` |
| 4 | **Étendre PreToolUse Bash avec `if:` cond + ajouter `permissions.deny`** | 4.B (B5+B6) + 4.C (C6) | 1/6 golden rules couvertes | S | high | [hooks `if:`](https://code.claude.com/docs/en/hooks) + [permissions](https://code.claude.com/docs/en/permissions) | Éditer `~/.claude/settings.json` pour ajouter blocs `if:` scopés (rm POD5, nextflow run hors ~/Run, profil scw) + `permissions.deny: ["Bash(rm * .pod5*)", "Bash(aws s3 rm:*)"]` |
| 5 | **Skill `docker-compose-restart` Aima-Tower** | 4.A+B | pattern verbatim 10× | S | high | [skills](https://code.claude.com/docs/en/skills) | `mkdir ~/.claude/skills/docker-compose-restart && touch SKILL.md` avec frontmatter trigger « restart aima-tower » + body séquence down/build/up/logs |
| 6 | **`/recap` activé + `/usage` quotidien** | 4.A (A2+A3) | 8 sessions parallèles | XS | medium | [interactive-mode](https://code.claude.com/docs/en/interactive-mode) | `/config` → activer Session recap auto ; ajouter `/usage` au workflow `/save-code` |
| 7 | **`/loop` self-pacing remplace `ScheduleWakeup` courts** | 4.B (B4) + 4.C (C2,C9) | 4× `sleep 300` + 20 SchedWakeup | S | medium | [scheduled-tasks](https://code.claude.com/docs/en/scheduled-tasks) | Pour polling : `/loop check CI on my PR` (sans interval = self-pacing 1min-1h) ; pour wait-process : Monitor déjà OK |
| 8 | **MCP S3 read-only Scaleway** | 4.B (B14) | 220 S3 hits + s3-safety | M | high | [txn2/mcp-s3](https://github.com/txn2/mcp-s3) | `S3_ENDPOINT=https://s3.fr-par.scw.cloud S3_USE_PATH_STYLE=true claude mcp add scw-s3 -- ...` (binaire à compiler/docker) |
| 9 | **Réauthentifier Seqera MCP** | 4.A (A8) | seqera down 2 sem | S | medium | [w18 paste OAuth](https://code.claude.com/docs/en/whats-new/2026-w18) | `claude auth login` (procédure paste-code SSH) → `/mcp` re-add |
| 10 | **StatusLine enrichie** (model + cache % + cost) | 4.B (B27) | 8 parallèles | S | medium | [statusline](https://code.claude.com/docs/en/statusline) | Réécrire `settings.json:statusLine.command` pour parser `.model.display_name`, `.context_window.used_percentage`, `.cost.total_cost_usd` |
| 11 | **Routine cloud "veille PubMed quotidienne"** | 4.B (B2) | cron local | M | medium | [routines](https://code.claude.com/docs/en/routines) | Sur web : `claude.ai/code/routines` → New routine, prompt `/veille`, schedule daily 06:00 UTC, repo Aima-Survey |
| 12 | **Output style `aima-clinical`** | 4.B (B26) | corrections « item par item » | M | medium | [output-styles](https://code.claude.com/docs/en/output-styles) | Créer `~/.claude/output-styles/aima-clinical.md` avec frontmatter + body « FR, terse, ISO 15189 awareness » + `outputStyle: "aima-clinical"` dans settings |
| 13 | **`PreCompact` hook préserve Nextflow runs** | 4.B (B7) | CLAUDE.md prescrit | M | medium | [hooks](https://code.claude.com/docs/en/hooks) | Hook `PreCompact` qui dump nextflow log actif dans memory, ou block via exit code 2 |
| 14 | **Hook `UserPromptSubmit` expansion alias `tp`** | 4.B (B11) | aliases.md inerte | M | medium | [hooks](https://code.claude.com/docs/en/hooks) | Hook qui matche `^tp ` → injecter prefix selon aliases.md |
| 15 | **Re-décrire `agent-docs` vs `agent-websearch`** | 4.A (A8) | 0 invoc agent-docs | XS | medium | [sub-agents](https://code.claude.com/docs/en/sub-agents) | Éditer `~/.claude/agents/agent-docs.md:description` : « SEULEMENT pour doc versionnée d'une lib (Dash 2.14, modkit 0.4) — sinon agent-websearch » |
| 16 | **Activer PubMed MCP + skill `/veille-cfdna`** | 4.A (A9) | 0 MCP | M | medium | [pubmed-mcp](https://github.com/cyanheads/pubmed-mcp-server) | Vérifier `claude mcp list \| grep pubmed` ; créer skill `/veille-cfdna` avec query MeSH par défaut |
| 17 | **Channel Telegram bot** (alternative mobile à Remote Control offline) | 4.B (B3) | demande mobile | M | low | [channels](https://code.claude.com/docs/en/channels) | `/plugin install telegram@claude-plugins-official` + `/telegram:configure <token>` + `claude --channels plugin:telegram@...` |
| 18 | **Subagent `agent-explore` avec `memory: user`** | 4.B (B18) | 75 invoc, observations à accumuler | S | medium | [sub-agents](https://code.claude.com/docs/en/sub-agents) | Ajouter `memory: user` dans frontmatter `~/.claude/agents/agent-explore.md` |
| 19 | **Renommer skills git-* (ou supprimer)** | 4.C (C7) | mismatch nom, 0 invoc | S | low | [skills](https://code.claude.com/docs/en/skills) | Aligner `name:` sur basename, ou supprimer (git natif suffit) |
| 20 | **`/skills` filter** (auto à partir v2.1.122+) | 4.A (A5) | 31 skills | XS | low | [w18](https://code.claude.com/docs/en/whats-new/2026-w18) | Vérifier version + tester `/skills` |
| 21 | **`/init` sur 5 projets sans CLAUDE.md** (avec `CLAUDE_CODE_NEW_INIT=1`) | 4.A (A11+A12) | 5 projets nus | M | medium | [memory](https://code.claude.com/docs/en/memory) | `cd ~/Pipeline/Pod2Bam && CLAUDE_CODE_NEW_INIT=1 claude` puis `/init` |
| 22 | **Refresh `MEMORY.md` (auto memory)** | 4.C (C4) | staleness 19j | S | low | [memory](https://code.claude.com/docs/en/memory) | `/memory` pour browser ; éditer manuellement la section Audit |
| 23 | **`/team-onboarding` sur Bam2Beta** | 4.A (A6) | bus factor 1 + ISO 15189 | M | low | [w15](https://code.claude.com/docs/en/whats-new/2026-w15) | `cd ~/Pipeline/Bam2Beta && /team-onboarding` |
| 24 | **`/powerup`** une fois | 4.A (A7) | 30+ features ratées | XS | low | [w14](https://code.claude.com/docs/en/whats-new/2026-w14) | `/powerup` |
| 25 | **`/ultraplan` au lieu de Plan mode local** quand grand projet | 4.B (B22) | 8 abandons /13 | XS | low | [ultraplan](https://code.claude.com/docs/en/ultraplan) | `/ultraplan migrer X` au lieu de Shift+Tab plan |

**Top-7 résumé** : `/fewer-permission-prompts` > Remote Control + push > MCP DuckDB > Hook `if:` + `permissions.deny` > Skill docker-restart > `/recap`+`/usage` > `/loop` self-pacing.

---

## Phase 6 — Self-check

| Check | OK |
|---|---|
| Chaque recommandation trace à une observation Phase 3 | ✓ |
| Chaque recommandation cite une URL doc ou file:line | ✓ |
| Aucune feature Claude Code inventée | ✓ (18 pages doc fetchées + 7 changelogs) |
| Aucune recommandation viole les golden rules | ✓ |
| Claims transcripts reproductibles | ✓ |
| « First step » concret (cmd ou file edit) | ✓ |
| Couverture changelog hebdo | ✓ (w13→w19 fetched intégralement) |
| Couverture event Code w/ Claude 2026 | ✓ |
| Pages doc principales fetchées | ✓ (skills, hooks, statusline, mcp, sub-agents, output-styles, routines, channels, remote-control, scheduled-tasks, ultraplan, ultrareview, memory, permissions, permission-modes, auto-mode-config, settings, best-practices) |
| **Plan-aware (Pro vs Max vs Team)** | ✓ Auto mode marqué N/A pour Pro ; Ultrareview free runs expirés flagué |
| Rapport ≤ 3 500 mots tables exclues | ✓ (~2 600 mots hors tables) |

### Limites reconnues

**Itération 1** (publiée puis corrigée) — agent-websearch avait remonté les bonnes URLs `code.claude.com/docs/en/*` mais sans fetch des pages. Pour audits futurs, **fetch systématique** de :
1. `code.claude.com/docs/llms.txt` (index complet, 115 pages)
2. Dernières 6-8 entrées `whats-new/*` de la fenêtre d'audit
3. Pages clés : `permission-modes`, `auto-mode-config`, `mcp`, `sub-agents`, `memory`, `permissions`, `settings`, `hooks`, `skills`, `statusline`, `best-practices`, `routines`, `channels`, `remote-control`, `output-styles`, `commands`, `interactive-mode`, `model-config`, `ultraplan`, `ultrareview`, `scheduled-tasks`, `sandboxing`.

**Erreurs corrigées** :
- v2 : Auto mode présenté comme adoptable → en réalité **non disponible sur Pro** (Max/Team/Enterprise/API uniquement). Boris Pro → action retirée.
- v2 : `permissions.deny: Bash(rm:*pod5*)` envisagé → en réalité **rules d'arguments fragiles** (env-var prefixing, redirects). Recommandation revue : préférer hooks PreToolUse `if:` + path-based `permissions.deny` (Read/Edit) + sandboxing.
- v1 : Routines présentée comme alternative à `ScheduleWakeup 300s` → cron min **1 h**, donc ne couvre que les besoins quotidiens. `/loop` self-pacing est la vraie alternative aux 90s/120s/300s.
- v2 : MCP `memory` recommandé → en réalité Boris utilise déjà l'**auto memory officielle** (`~/.claude/projects/<project>/memory/`). MCP redondant, retiré.
- v1+v2 : Channels mentionné sans précision → est un **plugin MCP** spécifique avec install + paire bot, pas un mécanisme générique.

---

## Annexes

- **Pack signal complet** : [`audit-2026-05-09/signal-pack.md`](audit-2026-05-09/signal-pack.md)
- **Régénération mensuelle** : `find ~/.claude/projects -name '*.jsonl' -mtime -30` + commandes `jq` du signal-pack ; comparer compteurs et diff.
- **Re-fetcher la doc** : `curl https://code.claude.com/docs/llms.txt` puis itérer sur les changelogs `whats-new/2026-wXX.md` du mois écoulé.
- **Sessions échantillon citées** :
  - `Pipeline/trace-prod/2d864d82` (« non laisse tomber »)
  - `Pipeline/Aima-Tower/4515443f` (« non c'est pas ouf »)
  - `Pipeline/SampleSheetChecker/2debb934` (« non check encore »)
  - `Pipeline/Bam2Beta/957bf81d` (« demande chaque item un par un »)
  - `Pipeline/Bam2Beta/1cb84555` (« lancé dans un tmux »)
  - Sessions où Boris demande Remote / mobile (à retracer via `grep -lE "(suivre.*téléphone|skill mobile)" ~/.claude/projects/**/*.jsonl`)
