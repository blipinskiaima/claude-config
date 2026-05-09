---
name: Audit Claude Code 2026-05-09
description: Audit comportemental sur 30 jours de transcripts (2026-04-09 → 2026-05-09), 100 sessions, ~28k msgs, 8839 tool calls. Identifie 19 skills inutilisées, 8 frictions, 17 actions priorisées.
type: project
originSessionId: 5c2e6575-d6ed-4927-a8a3-78918dc2635a
---
# Audit Claude Code — Boris (2026-05-09)

> Fenêtre : **2026-04-09 → 2026-05-09**. Source primaire : `~/.claude/projects/**/*.jsonl` mtime ≤ 30j. Pack signal complet et reproductible : [`audit-2026-05-09/signal-pack.md`](audit-2026-05-09/signal-pack.md).

---

## Résumé exécutif

**Volume** — 100 sessions principales + 133 transcripts subagents, 2 254 user messages, 8 839 tool calls (3.92 par turn), 16 jours actifs sur 30, jusqu'à 8 sessions parallèles dans la même heure. Cache hit rate 97.86 %, modèle dominant Opus 4.7 puis 4.6, Sonnet/Haiku quasi inexistants.

**Top 3 frictions observées :**
1. **3 030 invocations `cat`/`head`/`tail` dans Bash** (≈ 19 % de tous les Bash) — anti-pattern documenté (`Read` est plus efficace et indexé).
2. **263 tool errors**, dont 27 refus utilisateur (`Esc`), 26 « File has not been read yet », 11 « File has been modified since read ». Discipline Read-before-Edit pas systématique côté Claude.
3. **`docker compose down && build && up -d && logs -f` répété 10× en 30j** + 135 sessions avec ≥ 8 Bash consécutifs (chaîne max 50) → workflows manuels sans skill dédié.

**Top 3 recommandations :**
1. **Activer le MCP DuckDB read-only** sur les 3 bases trace-prod/platform/workflow — interrogation NL sécurisée, friction quotidienne supprimée. Effort S, impact haut.
2. **Étendre le hook PreToolUse(Bash)** pour couvrir POD5, profil `scw` et lancement Nextflow — actuellement seul `aws s3 rm/--delete` est protégé sur les 5 golden rules.
3. **Créer skill `docker-compose-restart`** pour Aima-Tower (10 répétitions verbatim observées). Quick win.

---

## Phase 1 — Signal pack (résumé)

| KPI | Valeur |
|---|---|
| Sessions principales / jours actifs | 100 / 16 |
| User messages / Tool calls | 2 254 / 8 839 |
| Skills définies / utilisées | **31 / 12** |
| Subagents définis / utilisés | 4 / 3 (`agent-docs` 0×) |
| MCP servers configurés / appelés | 9 / **1** (`mcp__ide__getDiagnostics`) |
| Cache hit rate | 97.86 % |
| Sessions parallèles max (1h) | 8 |
| Coût retail équivalent (sub flat → $0) | ~$9 676 |

Détail complet, méthodes et commandes reproductibles : [`audit-2026-05-09/signal-pack.md`](audit-2026-05-09/signal-pack.md).

Top projets (cwd) : Aima-Tower (15 113 turns), SampleSheetChecker (5 056), Aima-Survey (5 008), Bam2Beta (3 865), trace-prod (3 699).

---

## Phase 2 — Interprétation de la config

Synthèse de l'inspection ciblée de `~/.claude/` au regard du signal Phase 1.

**Skills à 0 invocation — 4 causes distinctes**

- **Mismatch nom dossier ↔ frontmatter** — `git-commit/SKILL.md:4` expose `name: commit`, `git-create-pr` expose `name: create-pr`, `workflow-apex/SKILL.md:1` expose `name: apex`. Boris tapant `/git-commit` ou `/workflow-apex` n'obtient rien.
- **Frontmatter non-standard** — `python-refactor/SKILL.md:8` n'a pas de frontmatter YAML (utilise un bloc ```yaml inline). Le skill est invisible au pattern-matching auto.
- **Description correcte mais use-case rare** — `subagent-creator`, `meta-skills-creator`, `utils-fix-grammar` sont bien décrits mais activés rarement par le contexte AIMA.
- **Description correcte, simplement oubliée** — `compare-batches`, `correlation`, `qc-report`, `audit-trail`, `debug-nf`, `veille`, `sample` ont des triggers explicites en français adaptés à AIMA, mais Boris résout le besoin ad hoc.

**`end-session` invocable mais cachée** — `end-session/SKILL.md:4` contient `disable-model-invocation: true`. Confirmé par doc officielle : ce flag retire la skill du contexte Claude (donc Claude ne la suggère plus) tout en gardant `/end-session` taper-able. Boris l'utilise 20× via slash, ce qui suggère que c'est volontaire, mais aucune autre skill candidates pour ce flag (à débroussailler).

**MCP — un seul fonctionne effectivement** — `mcp-needs-auth-cache.json` flague `seqera`, Gmail/Drive/Calendar comme en attente d'auth depuis ~2 semaines. `pubmed` (configuré via npx) et `memory` (officiel Anthropic) sont fonctionnels mais **0 appel** en 30 jours — descriptions et triggers existent, mais aucun prompt explicite côté Boris ne les active. `context7` est le seul MCP qui a tourné (1 hit).

**Couverture hooks vs golden rules — 1 / 6** — Le hook PreToolUse couvre `aws s3 rm|rb|sync --delete`. Non couverts : protection POD5 dans `/scratch/basecall/`, profil `scw` obligatoire, lancement Nextflow hors `~/Pipeline/*`, scan secrets dans Edit/Write, détection `CREATE TABLE AS SELECT` DuckDB.

**Skill `docker-compose-restart`** — confirmé absent. La séquence répétée 10× n'a aucun raccourci.

**`agent-docs` vs `agent-websearch`** — descriptions chevauchantes. `agent-docs` (`agent-docs.md:5` model: sonnet) cible la doc versionnée via Context7 ; `agent-websearch` cible la recherche ouverte. Boris utilise `agent-websearch` 19× pour des cas qui seraient mieux servis par `agent-docs` (ex: API Dash, modkit). La cause la plus probable : les triggers ne sont pas assez disjoints.

**Modèles dans agents/skills** — `agent-explore` et `agent-websearch` tournent en `sonnet` (déjà optimisé). `agent-explore-quick` et `git-commit/git-create-pr` tournent en `haiku`. Tous les autres skills héritent du modèle de session (Opus). Comme les skills git-* haiku ne sont jamais invoquées, Haiku finit à **0 invocation**.

**CLAUDE.md projets top-3** — présents et précis : Aima-Tower (Dash 2.14, DuckDB read-only, pattern CachedService), SampleSheetChecker (script Bash 317 lignes, 5 sections), Aima-Survey (veille PubMed → markdown → Aima-Tower).

**Memory — staleness** — `MEMORY.md` non touché depuis 19 jours, `inventaire-claude-code.md` daté du 2026-04-13 → décalé.

**StatusLine sous-exploitée** — utilise uniquement `workspace.current_dir` du JSON d'input. Champs disponibles non utilisés : `model.display_name`, `cost.total_cost_usd`, `context_window.used_percentage`, `cost.total_lines_added/removed`. Pertinent pour Boris qui parallélise jusqu'à 8 sessions.

---

## Phase 3 — Caractérisation du workflow

### Ce que Boris **évite**

- **19 skills définies, 0 invocation en 30j** : `audit-trail`, `check-consistency`, `compare-batches`, `correlation`, `debug-nf`, `git-commit`, `git-create-pr`, `git-fix-pr-comments`, `git-merge`, `python-refactor`, `qc-report`, `sample`, `standby-todo-list`, `subagent-creator`, `utils-fix-grammar`, `utils-oneshot`, `veille`, `workflow-apex`. `batch-effect` 1× seulement.
- **`agent-docs` jamais invoqué** alors qu'il est défini avec `model: sonnet` (`agent-docs.md:5`). Chevauche `agent-websearch` (19 invocations).
- **MCP** : 1 seul appel sur 30j (`mcp__ide__getDiagnostics`). Les serveurs `pubmed`, `memory`, `seqera`, `context7`, `aim_memory`, `browser-tools` sont configurés mais inertes.
- **Sonnet 4.6 et Haiku 4.5** : 1 et 0 invocations directes respectivement (en dehors des subagents).
- **Worktree** : 0 invocations (ni `EnterWorktree`, ni `isolation: "worktree"`).
- **Plan mode utilisé asymétriquement** : 5 `EnterPlanMode` vs 13 `ExitPlanMode` — donc 8 sorties sans entrée, soit des sessions où Plan mode est abandonné par Esc.
- **`/init` utilisé 1× sur 30j** — pourtant 5 projets parmi les 20 ont 0 ligne de CLAUDE.md (Pod2Bam, methylseq, basecall, IA, short-read).

### Où vit la friction (5 plus aiguës)

1. **Anti-pattern `cat`/`head`/`tail`** — 3 030 hits dans des Bash en 30j (≈ 19 % du Bash total). Le system prompt insiste : *« Avoid using this tool to run cat, head, tail [...] use Read »*. Cite : `signal-pack.md` §4. Ex transcripts : Aima-Tower `e7cf4774`, trace-prod `2d864d82`.

2. **263 tool errors, dont 26 « File has not been read yet »** + 11 « File has been modified since read » + 6 « String to replace not found ». Sample : `<tool_use_error>File has not been read yet. Read it first before writing to it.` ×26. Cause : Edit/Write tenté avant Read dans la même tour, ou linter écrit en parallèle (auto-format).

3. **27 « user doesn't want to proceed » + 8 corrections « stop »/« non »/« refais » au début d'un message court**. Verbatim 5 quotes :
   - `non laisse tomber` — trace-prod `2d864d82-cf5c-4ee6-8bc0-031c9ff6e6fe.jsonl`
   - `non check encore` — SampleSheetChecker `2debb934`
   - `non mais demande moi chaque item un par un` — Bam2Beta `957bf81d`
   - `non ne parallèlise pas` — Aima-Tower
   - `non je veux que toute la suite soit lancé dans un tmux` — Bam2Beta `1cb84555`

   Lecture : Boris re-cadre Claude après plan trop large (« demande chaque item un par un »), parallélisation indésirable, ou abandon explicite. Pattern très répétitif → candidat pour règle ou skill cadrée.

4. **193 invocations `sleep N` dans Bash** dont **6× `sleep 300`** + **4× ScheduleWakeup à `delaySeconds: 300`** — anti-pattern explicite (system prompt : *« Don't pick 300s. It's the worst-of-both »* — cache TTL 5 min). Détail signal-pack §4 et §16.

5. **`docker compose down && docker compose build && docker compose up -d && docker compose logs -f` répété verbatim 10× en 30j**, presque exclusivement dans cwd `~/Pipeline/Aima-Tower`. Plus 135 sessions avec ≥ 8 Bash consécutifs, chaîne max 50. Aucun skill dédié, aucun alias dans `~/.claude/rules/aliases.md` pour cette opération.

### Ce qui marche notablement bien (à préserver)

- **Cache hit 97.86 %** sur ~4.4 G tokens lus → CLAUDE.md global + rules + skills bien stables, peu de churn (vs ré-écriture à chaque session). Effort de structuration payant.
- **115 Agents + 117 Bash en `run_in_background`** + 14 utilisations canoniques de `Monitor` (`while pgrep ... do sleep N; done`). Async maîtrisé.
- **Hook `Stop` `auto-push-on-stop.sh`** — bien configuré, fait son job (Boris confie le commit/push à Claude). Hook `Notification` avec `notify-send` adapté au workflow Cursor IDE.
- **Custom skills domain-specific très utilisées** : `save-code` (17), `maj-todo-list` (17), `commit-claude` (17), `prompt-creator` (5). Ces 4 skills couvrent ≈ 75 % de l'usage skill.
- **75 invocations `agent-explore` deep en background** → la règle « toujours exploration deep au démarrage » du CLAUDE.md global est suivie systématiquement.
- **127 règles permission allow** (73 globales + 54 local) → quasi-aucun prompt de permission interrompt Boris (5 « permission denied » seulement).
- **3 plugins officiels installés** (`frontend-design`, `feature-dev`, `code-review`, `code-simplifier`) — base utile mais sous-exploitée (`/plugin` utilisé 3×).

---

## Phase 4 — Gap analysis

### 4.A — Primitives existantes sous-utilisées

| # | Primitive | Friction Phase 3 | Doc / fichier | Fit |
|---|---|---|---|---|
| A1 | **`agent-docs` (déjà défini)** | `agent-websearch` 19× pour recherches qui seraient mieux servies par doc versionnée | `agent-docs.md:1-6` + [discover-plugins](https://code.claude.com/docs/en/discover-plugins) | high |
| A2 | **PubMed MCP installé jamais invoqué** | 0 MCP usage, alors que veille AIMA est priorité | [cyanheads/pubmed-mcp-server](https://github.com/cyanheads/pubmed-mcp-server) | high |
| A3 | **`memory` MCP officiel installé jamais invoqué** | MEMORY.md en staleness 19j, mises-à-jour manuelles | [server-memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) | medium |
| A4 | **Worktree isolation 0 utilisations** | Boris écrit sur ~/Pipeline/* directement (ISO 15189) | [hooks `WorktreeCreate`](https://code.claude.com/docs/en/hooks) | medium |
| A5 | **Plan mode asymétrique 5/13** | Sorties sans entrée → Boris abandonne en cours | [interactive-mode](https://code.claude.com/docs/en/interactive-mode) | medium |
| A6 | **/plugin discover utilisé 3×** | 4 200 skills + 770 MCP marketplace dispo | [discover-plugins](https://code.claude.com/docs/en/discover-plugins) | low |
| A7 | **5 projets sans CLAUDE.md** (Pod2Bam, methylseq, basecall, IA, short-read) | `/init` utilisé 1× | [best-practices](https://code.claude.com/docs/en/best-practices) | medium |
| A8 | **0 entrée `permissions.deny`** | Golden rules à 100 % via hook ou prompt | [settings](https://code.claude.com/docs/en/settings) | medium |

### 4.B — Primitives manquantes à adopter

| # | Primitive | Friction Phase 3 | Doc | Fit |
|---|---|---|---|---|
| B1 | **MCP DuckDB read-only** | 265× `python3 database/check_samples.py` + 159× `print(f'`+ requêtes manuelles trace-prod | [ktanaka101/mcp-server-duckdb](https://github.com/ktanaka101/mcp-server-duckdb) `--readonly` | **high** |
| B2 | **MCP S3 Scaleway read-only** | 220× `AWS_PROFILE=scw aws` + protection golden rule s3-safety | [txn2/mcp-s3](https://github.com/txn2/mcp-s3) `WithReadOnly(true)` + `S3_ENDPOINT` | high |
| B3 | **Hook PreToolUse(Bash) étendu** | 5/6 golden rules non couvertes | [hooks](https://code.claude.com/docs/en/hooks) | high |
| B4 | **Skill `docker-compose-restart`** | Pattern verbatim répété 10× | [skills](https://code.claude.com/docs/en/skills) | high |
| B5 | **StatusLine enrichie** (`model`, `cost.total_cost_usd`, `context_window.used_percentage`) | 8 sessions parallèles → besoin signal contextuel | [statusline JSON input](https://code.claude.com/docs/en/statusline) | medium |
| B6 | **Hook `UserPromptSubmit`** pour expansion alias `tp`/`tp check`/`tp export` | Aliases `~/.claude/rules/aliases.md` ne sont pas auto-expandés | [hooks](https://code.claude.com/docs/en/hooks) | medium |
| B7 | **Hook `PreCompact`** pour préserver état Nextflow | CLAUDE.md global prescrit la conservation à la compaction | [hooks](https://code.claude.com/docs/en/hooks) | medium |
| B8 | **Output style « AIMA-clinical »** (terse FR, code-first, ISO awareness) | Boris se plaint régulièrement du verbeux (« demande item par item ») | [settings outputStyle](https://code.claude.com/docs/en/settings) | medium |
| B9 | **Filesystem MCP** scoped à `~/Pipeline` + `/scratch` | Read/Glob répétitifs | [server-filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) | low |
| B10 | **Routines / scheduled cloud agents** | Veille scientifique en cron local → migrable vers Routines | [scheduled-tasks](https://code.claude.com/docs/en/scheduled-tasks) | low |

### 4.C — Anti-patterns observés

| # | Anti-pattern | Évidence | Doc qui contredit |
|---|---|---|---|
| C1 | **`cat`/`head`/`tail` au lieu de `Read`** | 3 030 hits Bash, 19 % du total | System prompt CLI : *« Avoid using this tool to run cat, head, tail »* |
| C2 | **`sleep 300` (×6) + `ScheduleWakeup 300s` (×4)** | signal-pack §4 + §16 | System prompt : *« Don't pick 300s. It's the worst-of-both »* (cache TTL 5 min) |
| C3 | **Edit/Write avant Read** | 26 « File has not been read yet » | [Edit tool requires prior Read](https://code.claude.com/docs/en/skills) |
| C4 | **`end-session` masquée par `disable-model-invocation: true`** | `end-session/SKILL.md:4` mais Boris l'invoque 20× | [skills frontmatter](https://code.claude.com/docs/en/skills) — flag pertinent seulement si on veut empêcher l'auto-suggest |
| C5 | **Skills `git-commit`/`workflow-apex` mismatch nom** | Frontmatter `name:` ≠ basename dossier | [skills](https://code.claude.com/docs/en/skills) — basename = nom canonique |
| C6 | **MEMORY.md staleness 19j + inventaire 26j** | mtime de fichiers | CLAUDE.md global prescrit mise-à-jour active |
| C7 | **Plan mode abandonné 8/13 fois** | 13 ExitPlanMode vs 5 EnterPlanMode | [interactive-mode](https://code.claude.com/docs/en/interactive-mode) |

---

## Phase 5 — Roadmap priorisée

Priorité = `impact / effort`. Top 5 = quick wins qui adressent les frictions les plus fréquentes.

| # | Action | Bucket | Friction (Phase 3 réf) | Effort | Impact | Doc | First step |
|---|---|---|---|---|---|---|---|
| 1 | **Activer MCP DuckDB read-only sur les 3 bases trace-*** | 4.B (B1) | Friction 5 + 200+ Bash duckdb manuels | S | high | [ktanaka101/mcp-server-duckdb](https://github.com/ktanaka101/mcp-server-duckdb) | `claude mcp add duckdb-trace-prod -- uvx mcp-server-duckdb --db-path ~/Pipeline/trace-prod/database/samples_status.duckdb --readonly` |
| 2 | **Étendre hook PreToolUse(Bash) golden rules** | 4.B (B3) + 4.A (A8) | Friction 3 + couverture rules 1/6 | S | high | [hooks](https://code.claude.com/docs/en/hooks) | Éditer `~/.claude/settings.json:hooks.PreToolUse[0].hooks[0].command` pour ajouter blocs sur `rm.*pod5`, `nextflow run` hors `~/Run`, et warning si `aws ` sans `AWS_PROFILE=scw` |
| 3 | **Skill `docker-compose-restart` pour Aima-Tower** | 4.B (B4) | Friction 5 (10 répétitions) | S | high | [skills](https://code.claude.com/docs/en/skills) | `mkdir ~/.claude/skills/docker-compose-restart && touch SKILL.md` avec frontmatter trigger « restart aima-tower » |
| 4 | **MCP S3 read-only Scaleway** | 4.B (B2) | Friction 3 (rule s3-safety) + 220 hits S3 | S | high | [txn2/mcp-s3](https://github.com/txn2/mcp-s3) | `S3_ENDPOINT=https://s3.fr-par.scw.cloud S3_USE_PATH_STYLE=true claude mcp add scw-s3 -- ./mcp-s3` (binaire à compiler) |
| 5 | **StatusLine enrichie : model + cache % + cost** | 4.B (B5) | Friction 8 sessions parallèles | S | medium | [statusline](https://code.claude.com/docs/en/statusline) | Remplacer `settings.json:statusLine.command` par script qui parse `.model.display_name`, `.context_window.used_percentage`, `.cost.total_cost_usd` |
| 6 | **Re-décrire `agent-docs` vs `agent-websearch`** | 4.A (A1) | 0 invoc agent-docs | S | medium | [discover-plugins](https://code.claude.com/docs/en/discover-plugins) | Éditer `~/.claude/agents/agent-docs.md:description` : préciser « SEULEMENT pour doc versionnée d'une lib (ex: Dash 2.14 callbacks, modkit 0.4) — sinon agent-websearch » |
| 7 | **Activer PubMed MCP** + créer prompt-template `/veille-cfdna` | 4.A (A2) | 0 MCP usage, veille auto | M | medium | [cyanheads/pubmed-mcp-server](https://github.com/cyanheads/pubmed-mcp-server) | Vérifier `claude mcp list \| grep pubmed`, puis créer skill `/veille-cfdna` qui invoque le MCP avec query MeSH par défaut |
| 8 | **Réauthentifier Seqera MCP** | 4.A (mcp-needs-auth) | seqera down depuis 2 sem | S | medium | [docs.seqera.io/platform-cloud/seqera-mcp](https://docs.seqera.io/platform-cloud/seqera-mcp/overview) | `/mcp` → relancer auth seqera ; alternative SSO si compte Tower lié |
| 9 | **Hook `UserPromptSubmit` expansion alias** (`tp`, `tp check`, `tp export`) | 4.B (B6) | aliases.md non auto-utilisé | M | medium | [hooks](https://code.claude.com/docs/en/hooks) | Ajouter event `UserPromptSubmit` qui matche `^tp ` et inject le préfix `cd ~/Pipeline/trace-prod && python3 database/check_samples.py ` |
| 10 | **Output style `aima-clinical`** | 4.B (B8) | Friction 3 (« item par item »), corrections fréquentes | M | medium | [settings outputStyle](https://code.claude.com/docs/en/settings) | `mkdir ~/.claude/output-styles && touch aima-clinical.md` avec frontmatter + body « FR, terse, code-first, ISO 15189 awareness » |
| 11 | **Skill `read-instead-of-cat` (rule rappel)** | 4.C (C1) | 3 030 cat/head/tail | S | medium | [skills](https://code.claude.com/docs/en/skills) | Ajouter règle dans `~/.claude/rules/bash-discipline.md` : « pour lire un fichier connu, toujours `Read` jamais `cat <fichier>` » |
| 12 | **Désactiver `disable-model-invocation` sur `end-session`** (si Boris veut auto-suggest) | 4.C (C4) | 20 invocations slash, jamais auto-suggérée | S | low | [skills frontmatter](https://code.claude.com/docs/en/skills) | Éditer `~/.claude/skills/end-session/SKILL.md` ligne 4, supprimer le flag |
| 13 | **Renommer skills git-* (ou décider de supprimer)** | 4.C (C5) | mismatch nom dossier/frontmatter, 0 invoc | S | low | [skills](https://code.claude.com/docs/en/skills) | Soit aligner `name:` sur basename, soit supprimer (Claude Code gère git nativement) |
| 14 | **Refresh `MEMORY.md` + `inventaire-claude-code.md`** | 4.C (C6) | staleness 19/26j | S | low | local | Ajouter ligne `## Audit` (cf. ci-dessous) ; régénérer inventaire à partir de cette analyse |
| 15 | **Hook `PreCompact` pour persistance Nextflow runs** | 4.B (B7) | CLAUDE.md compaction prescrit | M | low | [hooks](https://code.claude.com/docs/en/hooks) | Ajouter event `PreCompact` avec script qui dump `nextflow log` actif dans memory |
| 16 | **`/init` sur Pod2Bam, methylseq, basecall, IA, short-read** | 4.A (A7) | 5 projets sans CLAUDE.md | M | low | [best-practices](https://code.claude.com/docs/en/best-practices) | `cd ~/Pipeline/Pod2Bam && /init` puis curate |
| 17 | **Discover plugin marketplace** (parcourir 4 200 skills) | 4.A (A6) | sous-exploitation | L | low | [discover-plugins](https://code.claude.com/docs/en/discover-plugins) | `/plugin` → onglet Discover, filter sur « bioinformatics », « data-engineering », « duckdb », « nextflow » |

**Top-5 résumé** : DuckDB MCP > Hook PreToolUse étendu > Skill docker-restart > S3 MCP > StatusLine enrichie. Tous traceables aux frictions 3 et 5, effort S, impact medium-high.

---

## Phase 6 — Self-check

| Check | OK |
|---|---|
| Chaque recommandation trace à une observation Phase 3 | ✓ (col « Friction ») |
| Chaque recommandation cite une URL doc ou file:line | ✓ (col « Doc ») |
| Aucune feature Claude Code inventée | ✓ (toutes vérifiées via agent-websearch sur `code.claude.com/docs`) |
| Aucune recommandation viole les golden rules | ✓ (S3 read-only, pas de `--delete`, profil scw préservé) |
| Claims transcripts reproductibles | ✓ (commandes dans signal-pack) |
| « First step » concret (commande ou file edit) | ✓ |
| Rapport ≤ 3 500 mots tables exclues | ✓ (≈ 1 800 mots hors tables) |

---

## Annexes

- **Pack signal complet** : [`audit-2026-05-09/signal-pack.md`](audit-2026-05-09/signal-pack.md)
- **Régénération mensuelle** : relancer toutes les commandes `find ... -mtime -30` du signal-pack ; comparer compteurs.
- **Sessions échantillon citées** :
  - `Pipeline/trace-prod/2d864d82-cf5c-4ee6-8bc0-031c9ff6e6fe.jsonl` (« non laisse tomber »)
  - `Pipeline/Aima-Tower/4515443f-9e2b-46a9-ae1a-91983b0e44f3.jsonl` (« non c'est pas ouf »)
  - `Pipeline/SampleSheetChecker/2debb934-7b3e-46ad-992a-d94bed3d0396.jsonl` (« non check encore »)
  - `Pipeline/Bam2Beta/957bf81d-a6c4-4701-a8df-8dc9a5b82a22.jsonl` (« non mais demande moi chaque item un par un »)
  - `Pipeline/Bam2Beta/1cb84555-6983-469f-8367-fa21820effb5.jsonl` (« non je veux que toute la suite soit lancé dans un tmux »)
