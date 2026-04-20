---
name: Inventaire Claude Code AIMA
description: Inventaire complet des outils Claude Code disponibles — skills, agents, MCP, rules, hooks, plugins. Mis à jour le 2026-04-20 après exploration profonde de .claude/.
type: reference
originSessionId: 129fb3f7-7613-4550-adf0-9392306d8a85
---
# Inventaire Claude Code — Boris Blipinski (2026-04-20)

## Skills (29 globaux dans ~/.claude/skills/)

### Bioinfo / AIMA — Global (10)
| Skill | Usage |
|---|---|
| `/sample <id>` | Statut cross-projet d'un sample (scores, QC, S3, metadata) |
| `/batch-effect` | Analyse sources batch effect CGFL vs HCL |
| `/compare-batches` | Compare métriques pipeline entre batchs (Wilcoxon, Fisher) |
| `/check-consistency` | Validation croisée trace-prod / S3 / outputs Bam2Beta |
| `/correlation` | Spearman/Pearson sur 2 métriques de samples |
| `/qc-report` | Rapport QC standardisé markdown |
| `/debug-nf` | Diagnostic run Nextflow échoué |
| `/audit-trail` | Traçabilité ISO 15189 pour versions de pipeline |
| `/veille` | Analyse rapports PubMed de veille scientifique |
| `/seqera` | CLI Seqera AI en sous-agent (Nextflow, Platform, workflows) |

### Pipeline Bam2Beta — Scope projet (3)
*Situés dans `~/Pipeline/Bam2Beta/.claude/skills/`, pas dans ~/.claude/skills/*
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

### Git workflow — Global (5)
| Skill | Usage |
|---|---|
| `/git-commit` | Commit rapide avec message clean |
| `/git-create-pr` | Créer PR avec titre/description auto |
| `/git-fix-pr-comments` | Implémenter les commentaires de review PR |
| `/git-merge` | Merge de branches avec résolution conflits |
| `/save-code` | Workflow fin de session (README, CLAUDE.md, mémoire, commit, push) |

### Claude Code management — Global (3)
| Skill | Usage |
|---|---|
| `/claude-memory` | Init/update système mémoire Claude |
| `/commit-claude` | Git commit+push ~/.claude/ |
| `/pull-claude` | Git pull ~/.claude/ |

### Développement généraliste — Global (5)
| Skill | Usage |
|---|---|
| `/code-workflow-feature` | Workflow 4 étapes pour ajouter une feature |
| `/workflow-apex` | Méthodologie APEX (Analyze-Plan-Execute-eXamine) |
| `/utils-oneshot` | Implémentation rapide Explore→Code→Test |
| `/python-refactor` | Refactoring Python |
| `/utils-fix-grammar` | Fix grammaire/orthographe dans fichiers |

### Meta-outils — Global (3)
| Skill | Usage |
|---|---|
| `/meta-skills-creator` | Créer des skills professionnels (processus 6 étapes) |
| `/subagent-creator` | Créer/configurer des sous-agents |
| `/prompt-creator` | Ingénierie de prompts multi-LLM |

## Agents (4)

| Agent | Modèle | Usage |
|---|---|---|
| `agent-explore` | Sonnet | Exploration profonde + détection bioinfo (lancé auto au Session Start) |
| `agent-explore-quick` | Haiku | Chargement rapide contexte (sessions suivantes) |
| `agent-docs` | Sonnet | Recherche documentation via Context7 MCP |
| `agent-websearch` | Sonnet | Recherche web structurée |

## MCP Servers (6 actifs + 3 auth pending)

### Actifs
| MCP | Type | Fonction |
|---|---|---|
| `seqera` | HTTP | API Seqera Tower (monitoring workflows NF) — le plus utilisé |
| `pubmed` | stdio | Recherche PubMed (search, fetch_summary, get_fulltext) |
| `memory` | stdio | Knowledge graph inter-projets (store, search, link facts) |
| `context7` | stdio + plugin | Documentation librairies à jour |
| `browser-tools` | stdio | Console/network/a11y audit web |
| `playwright` | stdio | Automatisation navigateur |

### Déclarés mais auth non validée
| MCP | Statut |
|---|---|
| `claude_ai_Gmail` | Auth pending |
| `claude_ai_Google_Calendar` | Auth pending |
| `claude_ai_Google_Drive` | Auth pending |

## Rules (11 — 6 globales, 5 path-scoped)

### Toujours chargées
| Rule | Contenu |
|---|---|
| `s3-safety.md` | 5 golden rules S3 (jamais supprimer/écraser, profil scw, retry sync) |
| `duckdb.md` | CREATE TABLE AS SELECT ne préserve pas les PK |
| `nextflow.md` | Jamais lancer NF depuis le pipeline dir, jamais hardcoder |
| `secrets.md` | Jamais afficher/copier/committer des credentials |
| `aliases.md` | Commandes fréquentes et chemins (tp, Pipeline, Run, scratch) |
| `troubleshooting.md` | Problèmes récurrents DuckDB, S3, Nextflow, Docker, Pod2Bam |

### Chargées selon le contexte (path-scoped)
| Rule | Quand | Contenu |
|---|---|---|
| `bioinfo-tools.md` | Fichiers .nf, projets pipeline | Conventions modkit, dorado, samtools, raima |
| `dorado-reference.md` | Pod2Bam, basecall | Images Docker, modèles, trimming |
| `bedmethyl-format.md` | Bam2Beta, IA | 18 colonnes bedMethyl avec relations |
| `stats-guide.md` | exploratory-analysis, IA, .R | Guide stats (Wilcoxon, ROC, Spearman, ComBat-met) |
| `template-claude-md.md` | CLAUDE.md, .claude/ | Template pour nouveaux projets |

## Hooks (3)

| Hook | Event | Fonction |
|---|---|---|
| Protection S3 | PreToolUse (Bash) | Bloque `aws s3 rm`, `aws s3 rb`, `aws s3 sync --delete` |
| Notification | Notification (*) | `notify-send` quand Claude attend une action (timeout 5s) |
| Auto-push session end | Stop | `~/.claude/scripts/auto-push-on-stop.sh` — commit+push whitelist memory/rules/scripts/CLAUDE.md (timeout 15s) |

Scripts annexes : `archive-todo.sh`, `archive-todo-monthly.sh` (rotation todo-list).

## Plugins (6 installés, 3 activés)

### Activés dans settings.json
| Plugin | Source |
|---|---|
| feature-dev | claude-plugins-official |
| code-review | claude-plugins-official |
| context7 | claude-plugins-official |

### Installés mais non activés
| Plugin | Source |
|---|---|
| frontend-design | claude-plugins-official |
| code-simplifier | claude-plugins-official |
| example-skills | marketplace Anthropic |

## Permissions notables (settings.json)

- **Allow globales** : Read/Edit/Write/Glob/Grep + ~50 Bash whitelistés (git, docker, nextflow, aws, samtools, tmux, python3, nvidia-smi)
- **Variables d'env inline autorisées** : `BAM=`, `UBAM=`, `S3=`, `WORKDIR=`, `DEMUX_DIR=` — révèle des workflows bash manuels de debug NF
- **Flag expérimental actif** : `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- **Aucun deny explicite** → sécurité S3 repose sur le hook PreToolUse

## Automatisations

| Automatisation | Fréquence | Détail |
|---|---|---|
| Veille PubMed (Aima-Survey) | Daily 8h00 | Rapports markdown + scoring Claude Haiku 4.5 + email |
| Veille résumé hebdo | Lundi 8h05 | Résumé des 7 derniers jours |
| Exploration auto | Chaque session | `agent-explore` deep lancé en background au 1er message |
| Auto-push `.claude/` | Chaque fin de session | Hook Stop → push whitelist |
