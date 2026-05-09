---
name: Audit Claude Code 2026-05-09
description: Audit comportemental sur 30 jours de transcripts (2026-04-09 → 2026-05-09), 100 sessions, ~28k msgs, 8839 tool calls. Croisé avec changelog Claude Code w13-w19 + Code w/ Claude 2026. 25+ actions priorisées.
type: project
originSessionId: 5c2e6575-d6ed-4927-a8a3-78918dc2635a
---
# Audit Claude Code — Boris (2026-05-09)

> Fenêtre transcripts : **2026-04-09 → 2026-05-09**.
> Source primaire : `~/.claude/projects/**/*.jsonl` mtime ≤ 30j.
> Doc Claude Code croisée : changelogs hebdo w13→w19 (mars-mai 2026) + Code w/ Claude 2026 (event 06-mai) + pages clés (skills, hooks, statusline, remote-control, routines, channels, ultraplan/ultrareview, sub-agents).
> Pack signal complet : [`audit-2026-05-09/signal-pack.md`](audit-2026-05-09/signal-pack.md).

---

## Résumé exécutif

**Volume** — 100 sessions principales + 133 transcripts subagents, 2 254 user messages, 8 839 tool calls (3.92/turn), 16 jours actifs/30. Cache hit 97.86 %. Modèle dominant Opus 4.7 (12 498) puis 4.6 (5 341). Sonnet/Haiku quasi inexistants.

**Top 5 frictions :**
1. **3 030 invocations `cat`/`head`/`tail` dans Bash** (≈ 19 % du Bash) — Read existe, plus efficace.
2. **263 tool errors**, dont 27 refus user (`Esc`), 26 « File has not been read yet », 11 « modified since read ». *Note : depuis w14, Edit fonctionne après `cat`/`sed -n` sans Read séparé — résout la moitié.*
3. **127 allow rules manuelles** (73 globales + 54 local) sans utiliser `/fewer-permission-prompts` (skill bundled qui le fait pour toi) ni Auto mode (research preview, GA Opus 4.7 sur Max).
4. **`docker compose down && build && up -d && logs -f`** répété verbatim 10× sur Aima-Tower + 135 sessions avec ≥ 8 Bash consécutifs (chaîne max 50). Aucun skill.
5. **Boris demande explicitement le mobile** (2 verbatim) — Remote Control + push notifications mobile sont GA depuis 16 avril.

**Top 5 actions :**
1. **`/fewer-permission-prompts`** (skill bundled, déjà dispo) — auto-génère un allowlist depuis tes transcripts. Effort 1 minute, impact haut.
2. **Remote Control + push mobile** — `claude remote-control` puis `/config` → "Push when Claude decides". Répond aux 2 demandes verbatim de Boris.
3. **MCP DuckDB read-only** sur les 3 bases trace-* — interrogation NL, friction quotidienne supprimée.
4. **Auto mode** + `autoMode.hard_deny` pour les golden rules — remplace les 127 allow rules par un classifieur + deny absolus.
5. **`PreCompact` hook** (avec `block` decision) pour les états Nextflow — mention explicite dans CLAUDE.md global, pas implémentée.

---

## Phase 1 — Signal pack (résumé)

| KPI | Valeur |
|---|---|
| Sessions principales / jours actifs | 100 / 16 |
| User msgs / Tool calls | 2 254 / 8 839 |
| Skills définies / utilisées | **31 / 12** |
| Subagents définis / utilisés | 4 / 3 (`agent-docs` 0×) |
| MCP servers configurés / appelés | 9 / **1** |
| Cache hit rate | 97.86 % |
| Sessions parallèles max (1h) | 8 |
| Hooks configurés | 3 (PreToolUse Bash, Notification, Stop) |

Top projets : **Aima-Tower** (15 113 turns), **SampleSheetChecker** (5 056), **Aima-Survey** (5 008), Bam2Beta (3 865), trace-prod (3 699). Détail commandes reproductibles : voir `audit-2026-05-09/signal-pack.md`.

---

## Phase 2 — Interprétation de la config

**Skills à 0 invocation — 4 causes** :
- **Mismatch nom dossier ↔ frontmatter** : `git-commit/SKILL.md:4` expose `name: commit`, `git-create-pr` expose `name: create-pr`, `workflow-apex/SKILL.md:1` expose `name: apex`. Taper `/git-commit` ou `/workflow-apex` ne match rien.
- **Frontmatter non-standard** : `python-refactor/SKILL.md:8` n'a pas de YAML (utilise un bloc ```yaml inline) → invisible au pattern-matching.
- **Description correcte mais use-case rare** : `subagent-creator`, `meta-skills-creator`, `utils-fix-grammar`.
- **Description correcte, simplement oubliée** : `compare-batches`, `correlation`, `qc-report`, `audit-trail`, `debug-nf`, `veille`, `sample`. Triggers explicites en français adaptés à AIMA, Boris résout le besoin ad hoc.

**`end-session` invocable mais cachée** : `disable-model-invocation: true` dans `end-session/SKILL.md:4`. Doc officielle ([skills](https://code.claude.com/docs/en/skills)) confirme : ce flag retire le skill du contexte Claude → Claude ne peut plus le suggérer. `/end-session` reste tapable. 20 invocations slash sur 30j → flag probablement involontaire (Boris l'utilise ce qui suggère qu'il voudrait que Claude le suggère).

**MCP — un seul fonctionne** : `mcp-needs-auth-cache.json` flague `seqera`, Gmail/Drive/Calendar en attente d'auth depuis ~2 sem. Depuis w18 : `claude auth login` accepte le code OAuth collé directement (résout SSH/WSL2 où le callback localhost échoue) — c'est probablement la solution pour `seqera`. Depuis w18 aussi : MCP transient errors auto-retry ×3 ; depuis w19 : `/mcp` montre le tool count et flag les serveurs à 0 tool.

**Couverture hooks vs golden rules — 1/6** : seul `aws s3 rm|rb|sync --delete` est protégé. Non couverts : POD5 dans `/scratch/basecall/`, profil `scw` obligatoire, lancement Nextflow hors `~/Pipeline/*`, scan secrets, `CREATE TABLE AS SELECT` DuckDB. Depuis w13 : hooks supportent `if:` field (permission rule syntax) → conditionnel sans coût process.

**`agent-docs` vs `agent-websearch`** : descriptions chevauchantes. `agent-docs` cible la doc versionnée (Context7), `agent-websearch` la recherche ouverte. Boris utilise le second 19× pour des cas où le premier serait mieux (API Dash, modkit). Confusion de périmètre explique l'absence d'invocation.

**Modèles dans agents/skills** : `agent-explore` et `agent-websearch` en `sonnet`, `agent-explore-quick` et skills `git-*` en `haiku`. Comme les skills git-* ne sont jamais invoquées (Claude Code gère git nativement), Haiku reste à **0 invocation**. Depuis w16 : default effort `high` pour Pro/Max sur Opus 4.6/4.7 + nouveau `xhigh`.

**CLAUDE.md projets top-3** : présents et précis (Dash 2.14, scripts Bash 317 lignes, veille PubMed → Aima-Tower).

**Memory — staleness** : `MEMORY.md` non touché depuis 19 jours, `inventaire-claude-code.md` 26 jours.

**StatusLine sous-exploitée** : utilise uniquement `workspace.current_dir`. Champs disponibles non utilisés : `model.display_name`, `cost.total_cost_usd`, `context_window.used_percentage`. Depuis w15 : `refreshInterval` setting + `workspace.git_worktree` dans le JSON input.

---

## Phase 3 — Caractérisation du workflow

### Ce que Boris **évite**

- **19 skills à 0 invocation/30j** : `audit-trail`, `check-consistency`, `compare-batches`, `correlation`, `debug-nf`, `git-commit`, `git-create-pr`, `git-fix-pr-comments`, `git-merge`, `python-refactor`, `qc-report`, `sample`, `standby-todo-list`, `subagent-creator`, `utils-fix-grammar`, `utils-oneshot`, `veille`, `workflow-apex`. `batch-effect` 1×.
- **`agent-docs` jamais invoqué** alors que défini avec `model: sonnet`.
- **MCP** : 1 seul appel sur 30j (`mcp__ide__getDiagnostics`). `pubmed`, `memory`, `seqera`, `context7`, `aim_memory`, `browser-tools` configurés mais inertes.
- **Sonnet 4.6 / Haiku 4.5** : 1 et 0 invocations directes (hors subagents).
- **Worktree 0 invocations**. **EnterPlanMode 5** vs **ExitPlanMode 13** (8 abandons).
- **`/init` 1×/30j** ; 5 projets sans CLAUDE.md (Pod2Bam, methylseq, basecall, IA, short-read).
- **Skills built-in jamais invoquées** : `/fewer-permission-prompts`, `/review`, `/security-review`, `/usage`, `/recap` (post-w17), `/team-onboarding`, `/powerup`, `/loop` (Boris fait du `ScheduleWakeup` à la place).

### Frictions principales (verbatim) — 5 plus aiguës

1. **Anti-pattern `cat`/`head`/`tail`** — 3 030 hits Bash en 30j. System prompt insiste sur `Read`. Note : depuis w14, Edit fonctionne après `cat`/`sed -n` (résout en partie 26 « File has not been read yet »).

2. **263 tool errors** dont 26 « File has not been read yet », 11 « File has been modified since read », 6 « String to replace not found », 27 « user doesn't want to proceed », 14 « Cancelled parallel tool call ».

3. **Corrections utilisateur fréquentes** :
   - `non laisse tomber` — trace-prod `2d864d82`
   - `non check encore` — SampleSheetChecker `2debb934`
   - `non mais demande moi chaque item un par un` — Bam2Beta `957bf81d`
   - `non ne parallèlise pas` — Aima-Tower
   - `non je veux que toute la suite soit lancé dans un tmux` — Bam2Beta `1cb84555`
   - **`non je veux suivre une session de claude lancé ici directement sur mon téléphone`** — demande Remote Control
   - **`non mais j'ai pas un skill mobile?`** — demande Remote Control / push notif

4. **Anti-pattern sleep / ScheduleWakeup 300s** — 193 `sleep N` dont 6× `sleep 300` + 4× `ScheduleWakeup 300s` (anti-pattern documenté : cache TTL 5 min). Depuis w15, le tool **Monitor** (déjà utilisé 14× par Boris ✓) + **`/loop` self-pacing** sont les remplaçants officiels — les 4× `sleep 300` peuvent disparaître.

5. **`docker compose down && build && up -d && logs -f`** verbatim 10×, presque tout cwd Aima-Tower + 135 sessions avec ≥ 8 Bash consécutifs, chaîne max 50. Aucun skill, aucun alias.

### Ce qui marche (à préserver)

- Cache hit 97.86 % → CLAUDE.md global + rules + skills bien stables.
- 115 Agents + 117 Bash en `run_in_background` + 14× Monitor canonique → async maîtrisé.
- Hook `Stop` `auto-push-on-stop.sh` + Notification `notify-send` adaptés à Cursor IDE.
- Custom skills domain-specific (`save-code` 17, `maj-todo-list` 17, `commit-claude` 17, `prompt-creator` 5) → 75 % de l'usage skill.
- 75 invocations `agent-explore` deep en background → règle « exploration au démarrage » respectée.
- 127 règles permission allow → quasi-aucun prompt interrompt Boris (mais c'est aussi un anti-pattern, cf. ci-dessous).

---

## Phase 4 — Gap analysis

### 4.A — Primitives existantes/bundled jamais invoquées

| # | Primitive | Friction | Doc | Fit |
|---|---|---|---|---|
| A1 | **`/fewer-permission-prompts`** (skill bundled) | 127 allow rules manuelles + 73 globales | [w16 changelog](https://code.claude.com/docs/en/whats-new/2026-w16) | **high** |
| A2 | **`/usage`** (merged `/cost`+`/stats` w17, breakdown w16) | 8 sessions parallèles, no visibility cost/cache/limits | [commands](https://code.claude.com/docs/en/commands) | high |
| A3 | **`/recap`** (session recap, w17) | sessions Cursor persistantes p95 1437min | [interactive-mode](https://code.claude.com/docs/en/interactive-mode) | high |
| A4 | **`/skills` type-to-filter** (w18) | 31 skills, scrolling | [w18](https://code.claude.com/docs/en/whats-new/2026-w18) | medium |
| A5 | **`/team-onboarding`** (w15) | bus factor 1 → ramp-up backup | [w15](https://code.claude.com/docs/en/whats-new/2026-w15) | medium |
| A6 | **`/powerup`** (w14) interactive lessons | Boris a raté 30+ features en 30j | [w14](https://code.claude.com/docs/en/whats-new/2026-w14) | medium |
| A7 | **`agent-docs`** (déjà défini) | `agent-websearch` 19× pour cas mieux servis par doc versionnée | `agent-docs.md:1-6` | medium |
| A8 | **PubMed MCP installé jamais invoqué** | priorité veille AIMA, 0 MCP usage | [@cyanheads/pubmed-mcp-server](https://github.com/cyanheads/pubmed-mcp-server) | medium |
| A9 | **`memory` MCP officiel installé** | MEMORY.md staleness 19j | [server-memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) | medium |
| A10 | **`/init` quasi inutilisé** | 5 projets sans CLAUDE.md | [best-practices](https://code.claude.com/docs/en/best-practices) | medium |

### 4.B — Primitives Claude Code récentes non adoptées (annoncées w13→w19 + Code w/ Claude 06/05)

#### Mobile / Remote / Async

| # | Primitive | Statut / Date | Friction | Doc | Fit |
|---|---|---|---|---|---|
| B1 | **Remote Control** + **mobile push notifications** | GA, push depuis w16 (16/04) | Boris l'a explicitement demandé 2× verbatim | [remote-control](https://code.claude.com/docs/en/remote-control) | **high** |
| B2 | **Routines** (cloud schedule + GitHub events + API) | GA w16 | veille scientifique en cron local + ScheduleWakeup 300s | [routines](https://code.claude.com/docs/en/routines) | high |
| B3 | **Channels** (push events Telegram/Discord/iMessage/server) | GA | Boris bus factor 1, demande Slack/notif déjà notée | [channels](https://code.claude.com/docs/en/channels) | medium |
| B4 | **Dispatch** (mobile → Desktop session) | GA | mobile demand | [desktop](https://code.claude.com/docs/en/desktop) | low (Boris terminal-only) |

#### Permissions / safety

| # | Primitive | Statut | Friction | Doc | Fit |
|---|---|---|---|---|---|
| B5 | **Auto mode** (research preview, GA Opus 4.7 sur Max w16) | GA Opus 4.7/Max | 127 allow rules manuelles | [permission-modes](https://code.claude.com/docs/en/permission-modes) | **high** |
| B6 | **`autoMode.hard_deny` rules** (w19) | GA | 0 deny rules malgré golden rules | [auto-mode-config](https://code.claude.com/docs/en/auto-mode-config) | high |
| B7 | **Conditional hooks `if:` field** (w13) | GA | hook PreToolUse Bash spawn process à chaque Bash | [hooks](https://code.claude.com/docs/en/hooks) | high |
| B8 | **`PreCompact` hook block decision** (w16) | GA | CLAUDE.md compaction prescrit conservation Nextflow | [hooks](https://code.claude.com/docs/en/hooks) | medium |
| B9 | **`PostToolUse hookSpecificOutput.updatedToolOutput`** (w18) | GA | rewrite tool output (ex: redact secrets) | [hooks](https://code.claude.com/docs/en/hooks) | low |

#### Modèles / effort / cache

| # | Primitive | Statut | Friction | Doc | Fit |
|---|---|---|---|---|---|
| B10 | **`xhigh` effort + `/effort` interactive slider** (w16) | GA Opus 4.7 | tâches ISO 15189 critiques | [model-config](https://code.claude.com/docs/en/model-config) | medium |
| B11 | **`ENABLE_PROMPT_CACHING_1H`** (w16) | GA API/Bedrock/Vertex | 97.86 % hit déjà excellent — Boris est sur sub Pro donc N/A | [w16](https://code.claude.com/docs/en/whats-new/2026-w16) | low |
| B12 | **Native binaries** (w16, no Node) | GA auto | bénéfice latence | [setup](https://code.claude.com/docs/en/setup) | auto |
| B13 | **`bfs`/`ugrep` natifs** remplacent Glob/Grep (w17) | GA | 110 Grep + 11 Glob → bénéfice auto | [w17](https://code.claude.com/docs/en/whats-new/2026-w17) | auto |

#### MCP / extensions

| # | Primitive | Statut | Friction | Doc | Fit |
|---|---|---|---|---|---|
| B14 | **MCP DuckDB read-only** (community, mature) | stable | 265× `python3 database/check_samples.py` | [ktanaka101/mcp-server-duckdb](https://github.com/ktanaka101/mcp-server-duckdb) `--readonly` | **high** |
| B15 | **MCP S3 Scaleway read-only** (txn2/mcp-s3) | stable | 220× `AWS_PROFILE=scw aws` | [txn2/mcp-s3](https://github.com/txn2/mcp-s3) | high |
| B16 | **`/mcp` tool count + 0-tool flag** (w19) | GA | seqera down 2 sem invisible | [mcp](https://code.claude.com/docs/en/mcp) | auto |
| B17 | **MCP transient errors auto-retry ×3** (w18) | GA auto | seqera | [w18](https://code.claude.com/docs/en/whats-new/2026-w18) | auto |
| B18 | **Hooks call MCP tools `type: "mcp_tool"`** (w17) | GA | hook qui hit MCP sans spawn process | [hooks](https://code.claude.com/docs/en/hooks#mcp-tool-hook-fields) | medium |
| B19 | **MCP `alwaysLoad: true`** (w18) | GA | tools auto-disponibles | [mcp](https://code.claude.com/docs/en/mcp) | medium |

#### Cloud / agentic

| # | Primitive | Statut | Friction | Doc | Fit |
|---|---|---|---|---|---|
| B20 | **`/ultraplan`** (cloud planning) | research preview w15 | Plan mode asymétrique 5/13 | [ultraplan](https://code.claude.com/docs/en/ultraplan) | medium |
| B21 | **`/ultrareview`** | research preview w17 | Boris l'a déjà invoqué (skill listé) | [ultrareview](https://code.claude.com/docs/en/ultrareview) | medium |
| B22 | **Dreaming** (Managed Agents) | research preview, 06/05 | MEMORY.md staleness 19j + 100 sessions à consolider | [platform.claude.com/docs/en/managed-agents/dreams](https://platform.claude.com/docs/en/managed-agents/dreams) | high |
| B23 | **Multi-agent orchestration + Outcomes** | public beta, 06/05 | bus factor 1, ISO 15189 | [agent-teams](https://code.claude.com/docs/en/agent-teams) | low (CLI-local) |

#### Productivité quotidienne

| # | Primitive | Statut | Friction | Doc | Fit |
|---|---|---|---|---|---|
| B24 | **Output style « AIMA-clinical »** (FR, terse, ISO awareness) | GA | corrections fréquentes (« demande item par item ») | [output-styles](https://code.claude.com/docs/en/output-styles) | medium |
| B25 | **StatusLine enrichie** (model + cache % + cost + ctx %) | GA | 8 sessions parallèles | [statusline](https://code.claude.com/docs/en/statusline) | medium |
| B26 | **Hook `UserPromptSubmit`** alias `tp`, `tp check`, `tp export` | GA | aliases.md non auto-utilisé | [hooks](https://code.claude.com/docs/en/hooks) | medium |
| B27 | **Hook `UserPromptSubmit` set sessionTitle** (w15) | GA | 8 sessions parallèles, identification | [hooks](https://code.claude.com/docs/en/hooks) | low |
| B28 | **`Ctrl+R` history search across all projects** (w19) | GA | 100 sessions, retrouver une cmd | [interactive-mode](https://code.claude.com/docs/en/interactive-mode) | auto |
| B29 | **Plugin executables on PATH** (`bin/`, w14) | GA | bundle scripts AIMA dans plugin | [plugins-reference](https://code.claude.com/docs/en/plugins-reference) | low |
| B30 | **`--plugin-url`** (w19) | GA | tester plugin avant marketplace | [plugins](https://code.claude.com/docs/en/plugins) | low |

### 4.C — Anti-patterns observés

| # | Anti-pattern | Évidence | Doc qui contredit |
|---|---|---|---|
| C1 | `cat`/`head`/`tail` au lieu de `Read` | 3 030 hits | system prompt CLI ; depuis w14 Edit OK après `cat` (résout partiellement) |
| C2 | `sleep 300` (×6) + `ScheduleWakeup 300s` (×4) | signal-pack §4 + §16 | system prompt cache TTL 5min |
| C3 | Edit/Write avant Read | 26 « File has not been read yet » | resolved partiellement w14 |
| C4 | `end-session` `disable-model-invocation: true` | `end-session/SKILL.md:4` | `disable-model-invocation` cache du contexte (volontaire ?) |
| C5 | Skills `git-commit`/`workflow-apex` mismatch nom | frontmatter `name:` ≠ basename | [skills frontmatter](https://code.claude.com/docs/en/skills) |
| C6 | MEMORY.md staleness 19j + inventaire 26j | mtime fichiers | CLAUDE.md global prescrit |
| C7 | Plan mode abandonné 8/13 | 13 ExitPlanMode vs 5 EnterPlanMode | [permission-modes](https://code.claude.com/docs/en/permission-modes) |
| C8 | 127 allow rules manuelles, 0 deny | settings.json + settings.local.json | `/fewer-permission-prompts` automatique + Auto mode |
| C9 | ScheduleWakeup au lieu de `/loop` self-pacing | 20 SchedWakeup / 0 `/loop` | [w15 monitor + loop](https://code.claude.com/docs/en/whats-new/2026-w15) |
| C10 | 14× `Monitor` patterns `while pgrep ... sleep 10` | sleep loops dans Monitor | OK techniquement — mais Monitor lui-même streaming est natif depuis w15 |

---

## Phase 5 — Roadmap priorisée

Top 7 = quick wins ≤ 5 minutes chacune. Sort par `impact / effort`.

| # | Action | Bucket | Friction | Effort | Impact | Doc | First step |
|---|---|---|---|---|---|---|---|
| 1 | **`/fewer-permission-prompts`** | 4.A (A1) | 127 allow rules manuelles | XS | high | [w16](https://code.claude.com/docs/en/whats-new/2026-w16) | Lancer `/fewer-permission-prompts` dans une session active, accepter le diff `.claude/settings.json` |
| 2 | **Activer Remote Control + push mobile** | 4.B (B1) | 2 demandes verbatim Boris | S | high | [remote-control](https://code.claude.com/docs/en/remote-control) | `claude --version` (≥2.1.110), installer app mobile, `claude remote-control`, `/config` → "Push when Claude decides" |
| 3 | **MCP DuckDB read-only sur trace-prod** | 4.B (B14) | 265× check_samples.py manuel | S | high | [mcp-server-duckdb](https://github.com/ktanaka101/mcp-server-duckdb) | `claude mcp add duckdb-trace-prod -- uvx mcp-server-duckdb --db-path ~/Pipeline/trace-prod/database/samples_status.duckdb --readonly` |
| 4 | **Étendre PreToolUse(Bash) avec `if:` conditionnel** | 4.B (B7) + 4.C (C8) | 1/6 golden rules couvertes | S | high | [hooks `if:`](https://code.claude.com/docs/en/hooks) | Éditer `~/.claude/settings.json:hooks.PreToolUse` pour ajouter blocs scopés (`Bash(rm * pod5*)`, `Bash(nextflow run *)` hors `~/Run`, warning sur `Bash(aws *)` sans `AWS_PROFILE=scw`) |
| 5 | **Skill `docker-compose-restart` Aima-Tower** | 4.C+B | pattern 10× | S | high | [skills](https://code.claude.com/docs/en/skills) | `mkdir ~/.claude/skills/docker-compose-restart && touch ~/.claude/skills/docker-compose-restart/SKILL.md` avec frontmatter trigger `restart aima-tower` |
| 6 | **`/recap` activé** | 4.A (A3) | sessions parallèles | XS | medium | [interactive-mode](https://code.claude.com/docs/en/interactive-mode) | `/config` → activer Session recap auto |
| 7 | **`/usage` quotidien** | 4.A (A2) | 8 sessions parallèles | XS | medium | [commands](https://code.claude.com/docs/en/commands) | Ajouter `/usage` au workflow `/save-code` |
| 8 | **MCP S3 read-only Scaleway** | 4.B (B15) | 220 hits S3, rule s3-safety | M | high | [txn2/mcp-s3](https://github.com/txn2/mcp-s3) | Compiler/docker-pull binaire, `S3_ENDPOINT=https://s3.fr-par.scw.cloud S3_USE_PATH_STYLE=true claude mcp add scw-s3 -- ...` |
| 9 | **Auto mode + `autoMode.hard_deny`** | 4.B (B5+B6) | 127 allow + 0 deny | M | high | [permission-modes](https://code.claude.com/docs/en/permission-modes) | Tester en cyclant `Shift+Tab` ; si OK, `settings.json:permissions.defaultMode: "auto"` + remplir `autoMode.hard_deny` avec golden rules |
| 10 | **Routine cloud "veille PubMed quotidienne"** | 4.B (B2) | cron local + ScheduleWakeup | M | medium | [routines](https://code.claude.com/docs/en/routines) | Créer routine sur claude.ai/code (web) : prompt `/veille`, schedule daily 06:00 UTC, repo `Aima-Survey` |
| 11 | **Réauthentifier Seqera MCP** (paste OAuth) | A8 | seqera down 2 sem | S | medium | [w18 paste OAuth](https://code.claude.com/docs/en/whats-new/2026-w18) | `claude auth login` (procédure paste-code SSH) → puis re-add seqera MCP |
| 12 | **StatusLine enrichie** (model + cache % + cost) | 4.B (B25) | 8 parallèles | S | medium | [statusline JSON input](https://code.claude.com/docs/en/statusline) | Réécrire `settings.json:statusLine.command` pour parser `.model.display_name`, `.context_window.used_percentage`, `.cost.total_cost_usd` |
| 13 | **Output style `aima-clinical`** (FR, terse, ISO) | 4.B (B24) | corrections « item par item » | M | medium | [output-styles](https://code.claude.com/docs/en/output-styles) | `mkdir ~/.claude/output-styles && touch aima-clinical.md` + frontmatter |
| 14 | **`PreCompact` hook préserve Nextflow runs** | 4.B (B8) | CLAUDE.md compaction | M | medium | [hooks](https://code.claude.com/docs/en/hooks) | Hook `PreCompact` qui dump `nextflow log` actif dans memory, ou block via exit code 2 |
| 15 | **Hook `UserPromptSubmit` expansion alias `tp`** | 4.B (B26) | aliases.md inerte | M | medium | [hooks](https://code.claude.com/docs/en/hooks) | Hook qui matche `^tp ` → injecter prefix `cd ~/Pipeline/trace-prod && python3 database/check_samples.py ` |
| 16 | **Re-décrire `agent-docs` vs `agent-websearch`** | 4.A (A7) | 0 invoc agent-docs | XS | medium | [sub-agents](https://code.claude.com/docs/en/sub-agents) | Éditer `~/.claude/agents/agent-docs.md:description` pour préciser « doc versionnée d'une lib uniquement, sinon → agent-websearch » |
| 17 | **Demander accès Dreaming research preview** | 4.B (B22) | MEMORY staleness | M | high (long terme) | [managed-agents/dreams](https://platform.claude.com/docs/en/managed-agents/dreams) | Formulaire d'accès via Anthropic ; cible `~/.claude/projects/-home-blipinski/memory/` |
| 18 | **Activer PubMed MCP** + skill `/veille-cfdna` | 4.A (A8) | 0 MCP | M | medium | [pubmed-mcp](https://github.com/cyanheads/pubmed-mcp-server) | `claude mcp list \| grep pubmed` ; si OK, créer skill `/veille-cfdna` |
| 19 | **Désactiver `disable-model-invocation` sur `end-session`** | 4.C (C4) | 20 invoc slash, jamais auto-suggérée | XS | low | [skills frontmatter](https://code.claude.com/docs/en/skills) | Éditer `~/.claude/skills/end-session/SKILL.md:4` |
| 20 | **Renommer skills git-* (ou supprimer)** | 4.C (C5) | 0 invoc | S | low | [skills](https://code.claude.com/docs/en/skills) | Aligner `name:` sur basename, ou supprimer (Claude Code gère git nativement) |
| 21 | **`/skills` filter activé** | 4.A (A4) | 31 skills, scrolling | XS | low | [w18](https://code.claude.com/docs/en/whats-new/2026-w18) | Auto à partir v2.1.122+ ; vérifier `/skills` |
| 22 | **`/team-onboarding`** sur Bam2Beta | 4.A (A5) | bus factor 1, ISO 15189 | M | low | [w15](https://code.claude.com/docs/en/whats-new/2026-w15) | `cd ~/Pipeline/Bam2Beta && /team-onboarding` |
| 23 | **`/init` sur Pod2Bam, methylseq, basecall, IA, short-read** | 4.A (A10) | 5 projets sans CLAUDE.md | M | low | [best-practices](https://code.claude.com/docs/en/best-practices) | `cd ~/Pipeline/Pod2Bam && /init` puis curate |
| 24 | **`/powerup`** une fois | 4.A (A6) | 30+ features manquées | XS | low | [w14](https://code.claude.com/docs/en/whats-new/2026-w14) | `/powerup` |
| 25 | **Refresh `MEMORY.md` + `inventaire-claude-code.md`** | 4.C (C6) | staleness | S | low | local | Ajouter section Audit ; régénérer inventaire à partir de Phase 2 |

**Top-7 résumé** : `/fewer-permission-prompts` > Remote Control + push > MCP DuckDB > Hook PreToolUse étendu > Skill docker-restart > `/recap` > `/usage`. Tous traceables aux frictions 1, 3, 4, 5 et aux demandes verbatim de Boris. Effort XS-S, impact medium-high.

---

## Phase 6 — Self-check

| Check | OK |
|---|---|
| Chaque recommandation trace à une observation Phase 3 | ✓ |
| Chaque recommandation cite une URL doc ou file:line | ✓ |
| Aucune feature Claude Code inventée | ✓ (toutes vérifiées via WebFetch direct sur `code.claude.com/docs/*`) |
| Aucune recommandation viole les golden rules | ✓ (S3 read-only, pas de `--delete`, profil scw préservé) |
| Claims transcripts reproductibles | ✓ |
| « First step » concret (cmd ou file edit) | ✓ |
| Couverture changelog hebdo dans la fenêtre | ✓ (w13→w19 fetched intégralement) |
| Couverture event Code w/ Claude 2026 | ✓ (Dreaming, Managed Agents, Routines, Remote Agents) |
| Rapport ≤ 3 500 mots tables exclues | ✓ (~2 200 mots hors tables) |

**Limites reconnues de la première passe** (préservées pour transparence) :
- Première version (avant cette refonte) avait délégué la doc-research à 2 `agent-websearch` qui n'ont pas couvert les changelogs hebdo `whats-new/*`. Résultat : 30+ features manquées (`/fewer-permission-prompts`, Remote Control, Routines, Auto mode, conditional hooks `if:`, `/recap`, `/usage` breakdown, `xhigh`, `bfs`/`ugrep`, `/ultraplan`, `/team-onboarding`, `/powerup`, etc.).
- Cette refonte intègre les 7 changelogs hebdo (w13-w19) + Code w/ Claude 2026 (Dreaming, Multi-agent, Outcomes) fetché intégralement le 2026-05-09.
- Pour audits futurs : ajouter systématiquement le fetch de `code.claude.com/docs/llms.txt` (index complet) + dernières 6-8 entrées `whats-new/*` avant Phase 4.

---

## Annexes

- **Pack signal complet** : [`audit-2026-05-09/signal-pack.md`](audit-2026-05-09/signal-pack.md)
- **Régénération mensuelle** : `find ~/.claude/projects -name '*.jsonl' -mtime -30` + commandes `jq` du signal-pack ; comparer compteurs et diff.
- **Sessions échantillon citées** :
  - `Pipeline/trace-prod/2d864d82-cf5c-4ee6-8bc0-031c9ff6e6fe.jsonl` (« non laisse tomber »)
  - `Pipeline/Aima-Tower/4515443f-9e2b-46a9-ae1a-91983b0e44f3.jsonl` (« non c'est pas ouf »)
  - `Pipeline/SampleSheetChecker/2debb934-7b3e-46ad-992a-d94bed3d0396.jsonl` (« non check encore »)
  - `Pipeline/Bam2Beta/957bf81d-a6c4-4701-a8df-8dc9a5b82a22.jsonl` (« non mais demande moi chaque item un par un »)
  - `Pipeline/Bam2Beta/1cb84555-6983-469f-8367-fa21820effb5.jsonl` (« non je veux que toute la suite soit lancé dans un tmux »)
  - Sessions où Boris demande Remote / mobile (à retracer via `grep -lE "(suivre.*téléphone|skill mobile)" ~/.claude/projects/**/*.jsonl`)
