---
name: Inventaire Claude Code AIMA
description: Inventaire complet de tous les outils Claude Code disponibles — skills, agents, MCP, rules, hooks, plugins. Mis à jour le 2026-04-13 après rétrospective complète.
type: reference
originSessionId: 129fb3f7-7613-4550-adf0-9392306d8a85
---
# Inventaire Claude Code — Boris Blipinski (2026-04-13)

## Skills (24 total)

### Bioinfo / AIMA (6)
| Skill | Scope | Usage |
|---|---|---|
| `/batch-effect` | Global | Analyse sources batch effect CGFL vs HCL, tracking variables confondantes |
| `/check-consistency` | Global | Validation croisée trace-prod vs S3 vs outputs Bam2Beta |
| `/sample <id>` | Global | Statut cross-projet d'un sample (scores, QC, S3, metadata) |
| `/debug-nf` | Global | Diagnostic run Nextflow échoué (logs, processus, fix) |
| `/veille` | Global | Analyse rapports PubMed de veille scientifique |
| `/export-gsheet` | trace-prod | Export données vers Google Sheets (3 exports) |

### Pipeline Bam2Beta (3)
| Skill | Usage |
|---|---|
| `/test-bam2beta` | Test non-régression avec Healthy_826 |
| `/qualif-bam2beta` | Qualification version pour production |
| `/maj-bam2beta` | Montée en version (tag, release, changelog) |

### Développement (8)
| Skill | Usage |
|---|---|
| `/code-workflow-feature` | Workflow 4 étapes pour ajouter une feature |
| `/workflow-apex` | Méthodologie APEX (Analyze-Plan-Execute-eXamine) |
| `/utils-oneshot` | Implémentation rapide Explore→Code→Test |
| `/git-commit` | Commit rapide avec message clean |
| `/git-create-pr` | Créer PR avec titre/description auto |
| `/git-fix-pr-comments` | Implémenter les commentaires de review PR |
| `/git-merge` | Merge de branches avec résolution conflits |
| `/python-refactor` | Refactoring Python |

### Claude Code management (5)
| Skill | Usage |
|---|---|
| `/save-code` | Workflow fin de session (README, CLAUDE.md, mémoire, commit, push) |
| `/commit-claude` | Git commit+push ~/.claude/ |
| `/pull-claude` | Git pull ~/.claude/ |
| `/claude-memory` | Init/update système mémoire Claude |
| `/utils-fix-grammar` | Fix grammaire/orthographe dans fichiers |

### Meta-outils (2)
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

## MCP Servers (3)

| MCP | Type | Fonction |
|---|---|---|
| `seqera` | HTTP | API Seqera Tower (monitoring workflows NF) |
| `pubmed` | stdio | Recherche PubMed (search, fetch_summary, get_fulltext) |
| `memory` | stdio | Knowledge graph inter-projets (store, search, link facts) |

## Rules (11 — 6 globales, 5 path-scoped)

### Toujours chargées
| Rule | Contenu |
|---|---|
| `s3-safety.md` | 5 golden rules S3 (jamais supprimer, jamais écraser, profil scw, retry sync) |
| `duckdb.md` | CREATE TABLE AS SELECT ne préserve pas les PK |
| `nextflow.md` | Jamais lancer NF depuis le pipeline dir, jamais hardcoder |
| `secrets.md` | Jamais afficher/copier/committer des credentials |
| `aliases.md` | Commandes fréquentes et chemins (tp, Pipeline, Run, scratch) |
| `troubleshooting.md` | Problèmes récurrents DuckDB, S3, Nextflow, Docker, Pod2Bam |

### Chargées selon le contexte (path-scoped)
| Rule | Quand | Contenu |
|---|---|---|
| `bioinfo-tools.md` | Fichiers .nf, projets pipeline | Conventions modkit, dorado, samtools, raima, génomes |
| `dorado-reference.md` | Pod2Bam, basecall | Images Docker, modèles, trimming, config Docker run |
| `bedmethyl-format.md` | Bam2Beta, IA | 18 colonnes bedMethyl avec relations |
| `stats-guide.md` | exploratory-analysis, IA, .R | Guide stats débutant (Wilcoxon, ROC, Spearman, ComBat-met) |
| `template-claude-md.md` | CLAUDE.md, .claude/ | Template pour nouveaux projets |

## Hooks (2)

| Hook | Event | Fonction |
|---|---|---|
| Protection S3 | PreToolUse (Bash) | Bloque `aws s3 rm`, `aws s3 rb`, `aws s3 sync --delete` |
| Notification | Notification (*) | `notify-send` quand Claude attend une action |

## Plugins (3)

| Plugin | Source |
|---|---|
| feature-dev | claude-plugins-official |
| code-review | claude-plugins-official |
| context7 | claude-plugins-official |

## Automatisations

| Automatisation | Fréquence | Détail |
|---|---|---|
| Veille PubMed | Daily 8h00 | `~/Pipeline/veille-scientifique/veille.py` (6 requêtes) |
| Veille résumé hebdo | Lundi 8h05 | Résumé des 7 derniers jours |
| Exploration auto | Chaque session | `agent-explore` lancé en background au 1er message |
