---
name: Inventaire Claude Code AIMA
description: Inventaire complet des outils Claude Code disponibles — skills, agents, MCP, rules, hooks, plugins. Mis à jour le 2026-05-22 (audit qualitatif : sécurisation wildcards, cleanup settings.local, path-scope rules).
type: reference
originSessionId: prompt-creator-audit-2026-05-20
---

# Inventaire Claude Code — Boris Blipinski (2026-05-22)

## Skills (37 sur disque après tri itératif 2026-05-20 : 27 trackés dans claude-config + 10 fournis par plugins design/officiels ; 4 supplémentaires scopés projets Pipeline)

> **Audit 2026-05-20 machine -home-boris (3 actions)** :
> 1. Suppression ecosystem gstack — 46 wrappers symlinks + binaire 1.5 GB. Décision : ratio observé 119× MCP chrome / 2× `/browse` montrait que la stack gstack n'était pas le workflow naturel. Réinstaller : `gstack install`.
> 2. Tri skill par skill (37/42 retenus). Suppressions plugins design : `frontend-ui-engineering` (doublon frontend-design), `imagegen-frontend-web`, `industrial-brutalist-ui` (pas le style AIMA), `minimalist-ui` (doublon impeccable), `stitch-design-taste` (Google Stitch spécifique).
> 3. 27 skills trackés gardés intégralement (Bioinfo AIMA, Todo perso, Workflow session, Claude management, Dev/Meta, Docker, Frontend).

### Bioinfo / AIMA — Global (3)
| Skill | Usage |
|---|---|
| `/sample <id>` | Statut cross-projet d'un sample (scores, QC, S3, metadata) |
| `/debug-nf` | Diagnostic run Nextflow échoué |
| `/veille` | Analyse rapports PubMed de veille scientifique |
| `/seqera` | CLI Seqera AI en sous-agent (Nextflow, Platform, workflows) |
| `/seqera-status` | **NEW** — Vérifie état MCP seqera + liste workflows Tower |

### Pipeline Bam2Beta — Scope projet (3)
*Situés dans `~/Pipeline/Bam2Beta/.claude/skills/`*
| Skill | Usage |
|---|---|
| `/test-bam2beta` | Test non-régression avec Healthy_826 |
| `/qualif-bam2beta` | Qualification version pour production |
| `/maj-bam2beta` | Montée en version (tag, release, changelog) |

### trace-prod — Scope projet (1)
*Situé dans `~/Pipeline/trace-prod/.claude/skills/`*
| Skill | Usage |
|---|---|
| `/export-gsheet` | Export données trace-prod vers Google Sheets |

### Todo list personnelle — Global (3)
| Skill | Usage |
|---|---|
| `/add-todo-list` | Ajoute une tâche à `todo-optimisation.md` |
| `/maj-todo-list` | Déplace une tâche vers "Complété" (section du jour) |
| `/standby-todo-list` | Déplace vers/depuis "Stand-by" (avec raison de blocage) |

### Workflow session — Global (4)
| Skill | Usage |
|---|---|
| `/commit-claude` | Git commit+push ~/.claude/ |
| `/pull-claude` | Git pull ~/.claude/ |
| `/save-code` | Workflow fin de session projet (README, CLAUDE.md, mémoire, commit, push) |
| `/end-session` | Orchestrateur : save-code + commit-claude + maj-todo-list |

### Claude Code management — Global (3)
| Skill | Usage |
|---|---|
| `/claude-memory` | Init/update système mémoire (CLAUDE.md, auto memory, rules, @import) |
| `/audit-config` | **NEW** — Audit complet ~/.claude/ + plan cleanup 3 commits |
| `/subagent-creator` | Créer/configurer des sous-agents |

### Docker / Infra — Global (1)
| Skill | Usage |
|---|---|
| `/docker-restart` | **NEW** — Pattern docker compose down/build/up/logs Aima-Tower |

### Développement généraliste — Global (3)
| Skill | Usage |
|---|---|
| `/code-workflow-feature` | Workflow 5 étapes pour ajouter une feature |
| `/workflow-apex` | APEX (Analyze-Plan-Execute-eXamine, fix `name: apex` → `workflow-apex`) |
| `/clean-skill` | Refactoring projet Pipeline avec checkpoint git auto |

### Meta-outils — Global (2)
| Skill | Usage |
|---|---|
| `/meta-skills-creator` | Créer des skills professionnels (processus 6 étapes) |
| `/prompt-creator` | Ingénierie de prompts multi-LLM |

### Frontend / UI Design — Global (6)
| Skill | Usage |
|---|---|
| `frontend-design` | Anthropic — direction esthétique distinctive (utilisé 2× sur 11j) |
| `ui-ux-pro-max` | 161 palettes, 57 font pairings, 99 directives UX |
| `design-review` | Revue visuelle d'un site/page avec screenshots |
| `web-design-guidelines` | Vercel — audit accessibilité + bonnes pratiques web |
| `react-best-practices` | Vercel — perf React/Next.js (desc précisée Tower V3) |
| `composition-patterns` | Vercel — compound components React |
| `tailwind-v4-shadcn` | Tailwind v4 + shadcn/ui + Vite/React (directement Tower V3) |

## Agents (4)

| Agent | Modèle | Usage |
|---|---|---|
| `agent-explore` | Sonnet | Exploration profonde (lancé auto au Session Start, 20× /11j). **memory: user** depuis 2026-05-22 |
| `agent-explore-quick` | Haiku | Chargement rapide (gardé override Boris malgré "jamais quick" CLAUDE.md) |
| `agent-websearch` | Sonnet | Recherche web structurée (6× /11j) |
| `agent-pipeline-cartographer` | Sonnet | **NEW 2026-05-22** — cartographie cross-projets + knowledge curator single-projet ~/Pipeline/ (répondre à des questions sans ouvrir une session dans le projet), memory: user |

> **Audit 2026-05-22** : `agent-docs` supprimé (1 invoc/30j, Context7 appelé direct par main thread). `memory: user` ajouté à `agent-explore` (reco pendante 2026-05-09 #18). `agent-pipeline-cartographer` créé pour répondre aux questions cross-projets (S3, Docker images, dépendances entre projets ~/Pipeline/) sans polluer le contexte main.

## MCP Servers (7 actifs)

### Connectés
| MCP | Type | Usage 11j | Fonction |
|---|---|---|---|
| `Claude_in_Chrome` | via plugin | **13×** | Browser automation (le plus utilisé) |
| `context7` | via plugin | 1× | Documentation librairies à jour |
| `pubmed` | stdio | 0 | Recherche PubMed (pour `/veille`) |

### Déclarés (auth pending ou faible usage)
| MCP | Statut | Action |
|---|---|---|
| `seqera` | ! auth pending depuis ~2 sem | À réauthentifier via `/seqera-status` |
| `claude_ai_Gmail` | ! auth | Pour Aima-Survey futur |
| `claude_ai_Google_Calendar` | ! auth | idem |
| `claude_ai_Google_Drive` | ! auth | idem |

### Supprimés (audit 2026-05-20)
- ~~`memory`~~ — redondant avec auto memory officielle

## Rules (12 — 4 globales golden, 8 path-scoped)

### Toujours chargées (golden rules non négociables — 26 lignes total)
| Rule | Contenu |
|---|---|
| `s3-safety.md` | 5 golden rules S3 |
| `duckdb.md` | CREATE TABLE AS SELECT ne préserve pas les PK |
| `nextflow.md` | Jamais lancer NF depuis le pipeline dir |
| `secrets.md` | Jamais afficher/copier/committer des credentials |

### Path-scoped (chargees selon contexte — 602 lignes total)
| Rule | Paths |
|---|---|
| `bioinfo-tools.md` | Fichiers .nf, projets pipeline |
| `dorado-reference.md` | Pod2Bam, basecall |
| `bedmethyl-format.md` | Bam2Beta, IA |
| `stats-guide.md` | exploratory-analysis, IA, .R |
| `template-claude-md.md` | CLAUDE.md, .claude/ |
| `aima-brand.md` | .tex/.typ/rapport*/report*/Aima-Tower |
| `aliases.md` | **NEW 2026-05-22** : Pipeline/Run/Run2/scratch (commandes tp + chemins) |
| `troubleshooting.md` | **NEW 2026-05-22** : Pipeline/Run/Run2/scratch (DuckDB, S3, NF, Docker) |

## Hooks (3)

| Hook | Event | Fonction |
|---|---|---|
| `pretool-bash-guard.sh` | PreToolUse (Bash) | **10 règles** : S3 destructive, cd+rm, Python destructif, find -delete, dd, xargs rm, redirect .pod5, shred/mkfs, nextflow run hors ~/Run, **injection patterns curl\|bash/eval $(curl)/source <(curl) (NEW 2026-05-22)** |
| Notification | Notification (*) | `notify-send` quand Claude attend une action |
| `auto-push-on-stop.sh` | Stop | Commit+push whitelist ~/.claude/ (timeout 20s) |

## Plugins (5 activés)

| Plugin | Source | Apporte |
|---|---|---|
| feature-dev | claude-plugins-official | Skill /feature-dev |
| code-review | claude-plugins-official | Skill /code-review |
| context7 | claude-plugins-official | MCP context7 |
| superpowers | claude-plugins-official | brainstorming, TDD, debugging, verification, plans... |
| frontend-design | claude-plugins-official | Skill /frontend-design + MCP Claude_in_Chrome |

## Permissions notables

- **Allow globales** : 82 entries — Bash whitelistés (git, docker, nextflow, aws, samtools, tmux, python3) + wildcards `cd ~/Pipeline/**` et autres paths AIMA (sécurisés 2026-05-22, plus de `cd * && *` ni `git * && *`)
- **Allow local** : **43 entries** (cleanup 2026-05-22 : -68 one-shots morts depuis 111)
- **Deny** : **20 deny rules** (S3, rm POD5, rm -rf paths critiques, dd, shred, mkfs)
- **Flag actif** : `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

## Automatisations

| Automatisation | Fréquence | Détail |
|---|---|---|
| Veille PubMed (Aima-Survey) | Daily 8h00 | Rapports markdown + scoring Claude Haiku + email |
| Veille résumé hebdo | Lundi 8h05 | Résumé des 7 derniers jours |
| Exploration auto | Chaque session | `agent-explore` deep en background |
| Auto-push `.claude/` | Chaque fin de session | Hook Stop |

## Historique des audits

| Date | Type | Résultat |
|---|---|---|
| 2026-05-09 | Audit comportemental 30j | 100 sessions, 19 skills à 0 invoc, 25 actions priorisées |
| 2026-05-20 | Cleanup itératif avec Boris | -14 skills, -1 MCP, +3 skills, hook étendu, 1 rule path-scopée |
| 2026-05-22 | Audit qualitatif (best practices) | Sécurisation wildcards (cd/git * && *), hook règle 10 anti-injection, settings.local 111→43 entries, +2 rules path-scopées (aliases, troubleshooting). Items 🟡 restants : MCP auth pending, archive audit 2026-05-09, 12 skills non-trackés, déplacer aima-value-analysis. |
